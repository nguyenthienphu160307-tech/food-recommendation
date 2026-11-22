"""
==============================================================================
QUERY RELAXATION SERVICE (TASK TE9C66F / UC-02 NGOẠI LỆ / STATE 4 HÌNH 8.2 SRS)
==============================================================================
Cơ chế Tự động Nới lỏng Điều kiện khi Truy vấn trả về 0 kết quả:
Khi người dùng tìm kiếm nhưng không có nhà hàng nào thỏa mãn đầy đủ các điều kiện
khắt khe ban đầu (bán kính quá hẹp, ngân sách quá thấp, nhiều tiện ích đồng thời):
1. Giai đoạn 1: Tự động mở rộng bán kính (+3.0 km).
2. Giai đoạn 2: Tự động nới khoảng ngân sách (±25%).
3. Giai đoạn 3: Kết hợp cả mở rộng bán kính (+3km/+6km) và nới khoảng ngân sách (±25%).
4. Giai đoạn 4: Tạm thời nới lỏng các tiện ích phụ (ngoài trời, thú cưng, ăn chay)
   để ưu tiên vị trí và ẩm thực cốt lõi.
5. Giai đoạn 5: Đề xuất các quán thay thế gần đúng nhất (Near-match alternative candidates)
   được xếp hạng theo điểm đánh giá và khoảng cách.
==============================================================================
"""

import logging
from typing import Any, Dict, List, Optional, Tuple
from sqlalchemy import or_
from sqlalchemy.orm import Session, joinedload

from app.models.restaurant import Restaurant, RestaurantAmenity
from app.services.geo_service import calculate_bounding_box, calculate_haversine_distance

logger = logging.getLogger(__name__)


class QueryRelaxationService:
    """Service chuyên trách thực thi thuật toán nới lỏng điều kiện tìm kiếm (TE9C66F)."""

    # Hằng số nới lỏng theo đúng yêu cầu đề bài
    RADIUS_STEP_KM: float = 3.0          # Bước mở rộng bán kính (+3km)
    MAX_RADIUS_KM: float = 15.0         # Trần bán kính mở rộng tối đa
    BUDGET_RELAX_RATIO: float = 0.25     # Tỷ lệ nới khoảng ngân sách (±25%)
    DEFAULT_INITIAL_RADIUS: float = 3.0 # Bán kính mặc định ban đầu nếu chưa xác định

    @classmethod
    def execute_query(
        cls,
        db: Session,
        lat: Optional[float] = None,
        lng: Optional[float] = None,
        radius_km: Optional[float] = None,
        cuisine: Optional[str] = None,
        budget: Optional[int] = None,
        price_min: Optional[float] = None,
        price_max: Optional[float] = None,
        min_rating: Optional[float] = None,
        has_parking: Optional[bool] = None,
        has_private_room: Optional[bool] = None,
        has_outdoor: Optional[bool] = None,
        pet_friendly: Optional[bool] = None,
        vegetarian_support: Optional[bool] = None,
        limit: int = 10,
    ) -> List[Tuple[Restaurant, float]]:
        """
        Truy vấn không gian và lọc điều kiện kết hợp với Bounding Box SQL và khoảng cách Haversine.
        Trả về danh sách tuple (Restaurant, distance_km) sắp xếp theo (-avg_rating, distance_km).
        """
        query = db.query(Restaurant).options(
            joinedload(Restaurant.amenities),
            joinedload(Restaurant.images),
        ).filter(Restaurant.status == "active")

        # 1. Lọc theo loại hình ẩm thực (hỗ trợ các biến thể hoa/thường tiếng Việt trong CSDL)
        if cuisine and cuisine.strip():
            raw_c = cuisine.strip()
            variants = list({raw_c, raw_c.lower(), raw_c.title(), raw_c.capitalize()})
            c_conditions = []
            for v in variants:
                c_conditions.extend([
                    Restaurant.cuisine_type.ilike(f"%{v}%"),
                    Restaurant.name.ilike(f"%{v}%"),
                    Restaurant.description.ilike(f"%{v}%"),
                ])
            query = query.filter(or_(*c_conditions))

        # 2. Lọc theo ngân sách tối đa (budget)
        if budget is not None and budget > 0:
            query = query.filter(Restaurant.min_price <= float(budget))

        # 3. Lọc theo khoảng giá giao nhau (price_min, price_max)
        if price_min is not None:
            query = query.filter(Restaurant.max_price >= float(price_min))
        if price_max is not None:
            query = query.filter(Restaurant.min_price <= float(price_max))

        # 4. Lọc theo điểm đánh giá tối thiểu
        if min_rating is not None and min_rating > 0:
            query = query.filter(Restaurant.avg_rating >= float(min_rating))

        # 5. Lọc theo các cờ tiện ích trong RestaurantAmenities
        amenity_filters: Dict[str, Optional[bool]] = {
            "has_parking": has_parking,
            "has_private_room": has_private_room,
            "has_outdoor": has_outdoor,
            "pet_friendly": pet_friendly,
            "vegetarian_support": vegetarian_support,
        }
        active_amenities = [(k, v) for k, v in amenity_filters.items() if v is True]
        if active_amenities:
            query = query.join(RestaurantAmenity, Restaurant.id == RestaurantAmenity.restaurant_id)
            for col_name, _ in active_amenities:
                query = query.filter(getattr(RestaurantAmenity, col_name).is_(True))

        # 6. Sơ lọc Bounding Box theo tọa độ GPS nếu có bán kính
        has_coords = (lat is not None and lng is not None)
        center_lat = lat or 10.7769
        center_lng = lng or 106.7009

        if has_coords and radius_km is not None and radius_km > 0:
            bbox = calculate_bounding_box(center_lat, center_lng, radius_km)
            query = query.filter(
                Restaurant.latitude.between(bbox.min_lat, bbox.max_lat),
                Restaurant.longitude.between(bbox.min_lng, bbox.max_lng),
            )

        candidates = query.all()

        # 7. Tính khoảng cách Haversine chính xác và kiểm tra ngưỡng bán kính
        matched: List[Tuple[Restaurant, float]] = []
        for r in candidates:
            dist = calculate_haversine_distance(center_lat, center_lng, r.latitude, r.longitude, unit="km")
            if radius_km is not None and dist > radius_km:
                continue
            matched.append((r, round(dist, 2)))

        # Sắp xếp ưu tiên: Điểm đánh giá cao nhất, khoảng cách gần nhất
        matched.sort(key=lambda item: (-item[0].avg_rating, item[1]))
        return matched[:limit]

    @classmethod
    def relax_and_search(
        cls,
        db: Session,
        lat: Optional[float] = None,
        lng: Optional[float] = None,
        radius_km: Optional[float] = None,
        cuisine: Optional[str] = None,
        budget: Optional[int] = None,
        price_min: Optional[float] = None,
        price_max: Optional[float] = None,
        min_rating: Optional[float] = None,
        has_parking: Optional[bool] = None,
        has_private_room: Optional[bool] = None,
        has_outdoor: Optional[bool] = None,
        pet_friendly: Optional[bool] = None,
        vegetarian_support: Optional[bool] = None,
        limit: int = 10,
    ) -> Tuple[List[Tuple[Restaurant, float]], Dict[str, Any]]:
        """
        Thực hiện tìm kiếm với cơ chế Tự động Nới lỏng Điều kiện (UC-02 Ngoại lệ):
        - Nếu truy vấn gốc có kết quả: trả về ngay, relaxation_applied = False.
        - Nếu truy vấn gốc có 0 kết quả: tuần tự áp dụng 4 cấp độ nới lỏng:
          + Cấp 1: Mở rộng bán kính +3km
          + Cấp 2: Nới khoảng ngân sách ±25%
          + Cấp 3: Kết hợp mở rộng bán kính (+3km/+6km) VÀ nới ngân sách ±25%
          + Cấp 4: Tạm thời nới lỏng các tiện ích phụ (ngoài trời, thú cưng, ăn chay)
        """
        init_radius = radius_km if (radius_km is not None and radius_km > 0) else cls.DEFAULT_INITIAL_RADIUS
        has_coords = (lat is not None and lng is not None)

        relaxation_metadata: Dict[str, Any] = {
            "relaxation_applied": False,
            "strategy": "none",
            "stage": 0,
            "original_radius_km": init_radius if has_coords else None,
            "relaxed_radius_km": init_radius if has_coords else None,
            "radius_delta_km": 0.0,
            "original_budget": budget,
            "relaxed_budget": budget,
            "budget_delta_percent": 0.0,
            "original_price_min": price_min,
            "relaxed_price_min": price_min,
            "original_price_max": price_max,
            "relaxed_price_max": price_max,
            "relaxed_amenities": [],
            "explanation_message": None,
        }

        # =========================================================================
        # BƯỚC 0: TRUY VẤN GỐC (STRICT QUERY)
        # =========================================================================
        strict_results = cls.execute_query(
            db=db,
            lat=lat,
            lng=lng,
            radius_km=init_radius if has_coords else None,
            cuisine=cuisine,
            budget=budget,
            price_min=price_min,
            price_max=price_max,
            min_rating=min_rating,
            has_parking=has_parking,
            has_private_room=has_private_room,
            has_outdoor=has_outdoor,
            pet_friendly=pet_friendly,
            vegetarian_support=vegetarian_support,
            limit=limit,
        )

        if len(strict_results) > 0:
            return strict_results, relaxation_metadata

        # =========================================================================
        # BƯỚC 1: MỞ RỘNG BÁN KÍNH (+3.0 KM) - TE9C66F
        # =========================================================================
        if has_coords:
            step1_radius = round(init_radius + cls.RADIUS_STEP_KM, 2)
            step1_results = cls.execute_query(
                db=db,
                lat=lat,
                lng=lng,
                radius_km=step1_radius,
                cuisine=cuisine,
                budget=budget,
                price_min=price_min,
                price_max=price_max,
                min_rating=min_rating,
                has_parking=has_parking,
                has_private_room=has_private_room,
                has_outdoor=has_outdoor,
                pet_friendly=pet_friendly,
                vegetarian_support=vegetarian_support,
                limit=limit,
            )

            if len(step1_results) > 0:
                relaxation_metadata.update({
                    "relaxation_applied": True,
                    "strategy": "radius_expansion",
                    "stage": 1,
                    "relaxed_radius_km": step1_radius,
                    "radius_delta_km": cls.RADIUS_STEP_KM,
                    "explanation_message": (
                        f"Không tìm thấy nhà hàng phù hợp trong bán kính {init_radius} km. "
                        f"Hệ thống đã tự động mở rộng bán kính thêm +{cls.RADIUS_STEP_KM} km "
                        f"(lên {step1_radius} km) để tìm thấy {len(step1_results)} quán phù hợp gần bạn nhất."
                    ),
                })
                return step1_results, relaxation_metadata

        # =========================================================================
        # BƯỚC 2: NỚI KHOẢNG NGÂN SÁCH (±25%) - TE9C66F
        # =========================================================================
        has_budget = (budget is not None and budget > 0)
        has_price_range = (price_min is not None or price_max is not None)

        if has_budget or has_price_range:
            relaxed_b = int(budget * (1.0 + cls.BUDGET_RELAX_RATIO)) if has_budget else None
            relaxed_p_min = max(0.0, price_min * (1.0 - cls.BUDGET_RELAX_RATIO)) if price_min is not None else None
            relaxed_p_max = price_max * (1.0 + cls.BUDGET_RELAX_RATIO) if price_max is not None else None

            # Thử nới ngân sách ở bán kính gốc
            step2_results = cls.execute_query(
                db=db,
                lat=lat,
                lng=lng,
                radius_km=init_radius if has_coords else None,
                cuisine=cuisine,
                budget=relaxed_b,
                price_min=relaxed_p_min,
                price_max=relaxed_p_max,
                min_rating=min_rating,
                has_parking=has_parking,
                has_private_room=has_private_room,
                has_outdoor=has_outdoor,
                pet_friendly=pet_friendly,
                vegetarian_support=vegetarian_support,
                limit=limit,
            )

            if len(step2_results) > 0:
                budget_desc = f"{relaxed_b:,}đ".replace(",", ".") if relaxed_b else "linh hoạt"
                relaxation_metadata.update({
                    "relaxation_applied": True,
                    "strategy": "budget_expansion",
                    "stage": 2,
                    "relaxed_budget": relaxed_b,
                    "budget_delta_percent": round(cls.BUDGET_RELAX_RATIO * 100, 1),
                    "relaxed_price_min": relaxed_p_min,
                    "relaxed_price_max": relaxed_p_max,
                    "explanation_message": (
                        f"Không tìm thấy nhà hàng trong mức ngân sách ban đầu. "
                        f"Hệ thống đã tự động nới khoảng ngân sách ±25% (lên mức {budget_desc}) "
                        f"để tìm thấy {len(step2_results)} gợi ý phù hợp chất lượng."
                    ),
                })
                return step2_results, relaxation_metadata

        # =========================================================================
        # BƯỚC 3: KẾT HỢP MỞ RỘNG BÁN KÍNH (+3KM / +6KM) VÀ NỚI NGÂN SÁCH (±25%)
        # =========================================================================
        relaxed_b = int(budget * (1.0 + cls.BUDGET_RELAX_RATIO)) if has_budget else None
        relaxed_p_min = max(0.0, price_min * (1.0 - cls.BUDGET_RELAX_RATIO)) if price_min is not None else None
        relaxed_p_max = price_max * (1.0 + cls.BUDGET_RELAX_RATIO) if price_max is not None else None

        radii_to_try = [
            round(init_radius + cls.RADIUS_STEP_KM, 2),
            round(init_radius + cls.RADIUS_STEP_KM * 2, 2),
            cls.MAX_RADIUS_KM,
        ]

        for test_rad in radii_to_try:
            if has_coords and test_rad > init_radius:
                comb_results = cls.execute_query(
                    db=db,
                    lat=lat,
                    lng=lng,
                    radius_km=test_rad,
                    cuisine=cuisine,
                    budget=relaxed_b,
                    price_min=relaxed_p_min,
                    price_max=relaxed_p_max,
                    min_rating=min_rating,
                    has_parking=has_parking,
                    has_private_room=has_private_room,
                    has_outdoor=has_outdoor,
                    pet_friendly=pet_friendly,
                    vegetarian_support=vegetarian_support,
                    limit=limit,
                )
                if len(comb_results) > 0:
                    relaxation_metadata.update({
                        "relaxation_applied": True,
                        "strategy": "combined_radius_budget",
                        "stage": 3,
                        "relaxed_radius_km": test_rad,
                        "radius_delta_km": round(test_rad - init_radius, 1),
                        "relaxed_budget": relaxed_b,
                        "budget_delta_percent": round(cls.BUDGET_RELAX_RATIO * 100, 1),
                        "relaxed_price_min": relaxed_p_min,
                        "relaxed_price_max": relaxed_p_max,
                        "explanation_message": (
                            f"Hệ thống đã tự động kết hợp mở rộng bán kính lên {test_rad} km (+{round(test_rad - init_radius, 1)} km) "
                            f"và nới khoảng ngân sách ±25% để tìm thấy {len(comb_results)} địa điểm chất lượng gần bạn."
                        ),
                    })
                    return comb_results, relaxation_metadata

        # =========================================================================
        # BƯỚC 4: NỚI LỎNG TIỆN ÍCH PHỤ (SECONDARY AMENITIES RELAXATION)
        # =========================================================================
        relaxed_amenities_list = []
        if has_outdoor:
            relaxed_amenities_list.append("has_outdoor")
        if pet_friendly:
            relaxed_amenities_list.append("pet_friendly")
        if vegetarian_support:
            relaxed_amenities_list.append("vegetarian_support")

        step4_radius = min(cls.MAX_RADIUS_KM, init_radius + cls.RADIUS_STEP_KM * 2) if has_coords else None

        # Nới lỏng tiện ích phụ, giữ tiện ích cốt lõi (chỗ đậu ô tô, phòng riêng nếu có)
        step4_results = cls.execute_query(
            db=db,
            lat=lat,
            lng=lng,
            radius_km=step4_radius,
            cuisine=cuisine,
            budget=relaxed_b,
            price_min=relaxed_p_min,
            price_max=relaxed_p_max,
            min_rating=None,  # Bỏ lọc rating tối thiểu
            has_parking=has_parking,
            has_private_room=has_private_room,
            has_outdoor=None,
            pet_friendly=None,
            vegetarian_support=None,
            limit=limit,
        )

        if len(step4_results) > 0:
            relaxation_metadata.update({
                "relaxation_applied": True,
                "strategy": "amenities_relaxed",
                "stage": 4,
                "relaxed_radius_km": step4_radius,
                "relaxed_budget": relaxed_b,
                "relaxed_amenities": relaxed_amenities_list,
                "explanation_message": (
                    f"Hệ thống đã tự động mở rộng bán kính lên {step4_radius} km, nới ngân sách ±25% "
                    f"và tạm thời nới lỏng các tiêu chí tiện ích phụ để ưu tiên tìm quán đúng loại ẩm thực."
                ),
            })
            return step4_results, relaxation_metadata

        # =========================================================================
        # BƯỚC 5: TÌM ỨNG VIÊN THAY THẾ GẦN ĐÚNG NHẤT (NEAR-MATCH ALTERNATIVE CANDIDATES)
        # =========================================================================
        # Chỉ giữ vị trí và bán kính tối đa 15km, lấy các quán có đánh giá cao nhất
        step5_results = cls.execute_query(
            db=db,
            lat=lat,
            lng=lng,
            radius_km=cls.MAX_RADIUS_KM if has_coords else None,
            cuisine=None,
            budget=None,
            price_min=None,
            price_max=None,
            min_rating=None,
            has_parking=None,
            has_private_room=None,
            has_outdoor=None,
            pet_friendly=None,
            vegetarian_support=None,
            limit=limit,
        )

        relaxation_metadata.update({
            "relaxation_applied": True,
            "strategy": "near_match_fallback",
            "stage": 5,
            "relaxed_radius_km": cls.MAX_RADIUS_KM if has_coords else None,
            "relaxed_budget": None,
            "relaxed_amenities": ["has_parking", "has_private_room", "has_outdoor", "pet_friendly", "vegetarian_support"],
            "explanation_message": (
                f"Không có nhà hàng nào thỏa mãn đầy đủ các tiêu chí khắt khe đã chọn. "
                f"Hệ thống đề xuất {len(step5_results)} địa điểm ăn uống nổi bật nhất trong khu vực mở rộng "
                f"(bán kính {cls.MAX_RADIUS_KM} km) để bạn tham khảo."
            ),
        })
        return step5_results, relaxation_metadata
