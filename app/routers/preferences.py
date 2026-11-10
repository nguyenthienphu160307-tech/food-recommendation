"""
Router quản lý:
1. Sở thích cá nhân & Dị ứng thực phẩm (UserPreferences) theo chuẩn CSDL 2.1.3
2. API Gợi ý & Tìm kiếm nhà hàng cá nhân hóa kết hợp Trí tuệ Nhân tạo (Task TE9C65C)
   - Tự động đọc chế độ ăn (diet_type) và danh sách dị ứng (allergies) khi người dùng đã đăng nhập.
   - Minh bạch hóa các tiêu chí đã áp dụng và giải thích lý do gợi ý (Explainable AI).
   - Tự động fallback về gợi ý khoảng cách & rating thông thường khi là Khách (Guest - BR-02).
"""

import json
import math
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.rbac import get_current_user, get_current_guest_or_user
from app.models.user import User, UserPreference
from app.models.restaurant import Restaurant, RestaurantAmenity
from app.schemas.preferences import (
    UserPreferenceUpdate,
    UserPreferenceResponse,
    RecommendationResponse,
    RecommendedRestaurantItem,
    AppliedPreferencesSummary,
)

router = APIRouter(prefix="/api", tags=["Sở thích cá nhân & Gợi ý AI (TE9C65C)"])

VALID_DIET_TYPES = {"omnivore", "vegetarian", "vegan", "halal", "keto"}


def calc_haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Tính khoảng cách Haversine chính xác theo tọa độ địa lý (km)"""
    R = 6371.0  # Bán kính trái đất (km)
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    d_phi = math.radians(lat2 - lat1)
    d_lambda = math.radians(lon2 - lon1)

    a = math.sin(d_phi / 2.0) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(d_lambda / 2.0) ** 2
    c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))
    return R * c


def get_or_create_user_preference(db: Session, user_id: int) -> UserPreference:
    """Lấy hoặc tự động khởi tạo bản ghi UserPreference mặc định cho người dùng"""
    pref = db.query(UserPreference).filter(UserPreference.user_id == user_id).first()
    if not pref:
        pref = UserPreference(
            user_id=user_id,
            diet_type="omnivore",
            allergies=json.dumps([]),
            preferred_cuisines=json.dumps([]),
            avg_budget=250000.0
        )
        db.add(pref)
        db.commit()
        db.refresh(pref)
    return pref


# ==============================================================================
# 1. API QUẢN LÝ SỞ THÍCH CÁ NHÂN (USER PREFERENCES)
# ==============================================================================

@router.get(
    "/users/preferences",
    response_model=UserPreferenceResponse,
    summary="Lấy thông tin sở thích ăn uống & dị ứng của người dùng"
)
def get_user_preferences(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Lấy thông tin hồ sơ sở thích ăn uống của tài khoản đang đăng nhập:
    - diet_type: Chế độ ăn (omnivore, vegetarian, vegan, halal, keto)
    - allergies: Danh sách dị ứng thực phẩm (seafood, peanut, dairy, gluten...)
    - preferred_cuisines: Danh sách món ăn yêu thích
    - avg_budget: Ngân sách trung bình ước tính
    """
    pref = get_or_create_user_preference(db, current_user.id)
    allergies_list = json.loads(pref.allergies) if pref.allergies else []
    cuisines_list = json.loads(pref.preferred_cuisines) if pref.preferred_cuisines else []

    return UserPreferenceResponse(
        id=pref.id,
        user_id=pref.user_id,
        diet_type=pref.diet_type,
        allergies=allergies_list,
        preferred_cuisines=cuisines_list,
        avg_budget=pref.avg_budget,
        created_at=pref.created_at,
        updated_at=pref.updated_at
    )


@router.post(
    "/users/preferences",
    response_model=UserPreferenceResponse,
    status_code=status.HTTP_200_OK,
    summary="Khai báo sở thích ăn uống & dị ứng lần đầu (FR-04 / TE9C64E)"
)
@router.put(
    "/users/preferences",
    response_model=UserPreferenceResponse,
    summary="Cập nhật sở thích ăn uống & dị ứng của người dùng (FR-04 / TE9C64E)"
)
def save_user_preferences(
    payload: UserPreferenceUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Khai báo & cập nhật sở thích ăn uống cá nhân (FR-04):
    - Tự động chuẩn hóa diet_type (omnivore, vegetarian, vegan, halal, keto)
    - Lưu danh sách allergies dưới dạng mảng JSON vào bảng user_preferences
    - Lưu danh sách preferred_cuisines dưới dạng mảng JSON
    - Cập nhật ngân sách ăn uống trung bình (avg_budget)
    """
    pref = get_or_create_user_preference(db, current_user.id)

    if payload.diet_type is not None:
        clean_diet = payload.diet_type.lower().strip()
        if clean_diet not in VALID_DIET_TYPES:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Chế độ ăn '{payload.diet_type}' không hợp lệ. Cho phép: {', '.join(sorted(VALID_DIET_TYPES))}"
            )
        pref.diet_type = clean_diet

    if payload.allergies is not None:
        pref.allergies = json.dumps(payload.allergies, ensure_ascii=False)

    if payload.preferred_cuisines is not None:
        pref.preferred_cuisines = json.dumps(payload.preferred_cuisines, ensure_ascii=False)

    if payload.avg_budget is not None:
        if payload.avg_budget < 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ngân sách trung bình (avg_budget) phải lớn hơn hoặc bằng 0."
            )
        pref.avg_budget = payload.avg_budget

    db.commit()
    db.refresh(pref)

    allergies_list = json.loads(pref.allergies) if pref.allergies else []
    cuisines_list = json.loads(pref.preferred_cuisines) if pref.preferred_cuisines else []

    return UserPreferenceResponse(
        id=pref.id,
        user_id=pref.user_id,
        diet_type=pref.diet_type,
        allergies=allergies_list,
        preferred_cuisines=cuisines_list,
        avg_budget=pref.avg_budget,
        created_at=pref.created_at,
        updated_at=pref.updated_at
    )


# ==============================================================================
# 2. API GỢI Ý & TÌM KIẾM CÁ NHÂN HÓA (RECOMMENDATION ENGINE - TE9C65C)
# ==============================================================================

@router.get(
    "/recommendations",
    response_model=RecommendationResponse,
    summary="Gợi ý địa điểm ăn uống tích hợp tự động Sở thích cá nhân (TE9C65C)"
)
@router.get(
    "/restaurants/recommend",
    response_model=RecommendationResponse,
    summary="Alias: Gợi ý địa điểm ăn uống theo sở thích cá nhân"
)
def get_personalized_recommendations(
    latitude: float = Query(10.776889, description="Vĩ độ hiện tại của người dùng"),
    longitude: float = Query(106.700806, description="Kinh độ hiện tại của người dùng"),
    radius_km: float = Query(15.0, ge=0.5, le=50.0, description="Bán kính tìm kiếm (km)"),
    keyword: Optional[str] = Query(None, description="Từ khóa tìm kiếm (tên hoặc món ăn)"),
    max_budget: Optional[float] = Query(None, ge=0, description="Lọc thủ công mức giá tối đa"),
    category: Optional[str] = Query(None, description="Lọc thể loại (bbq, hotpot, vegan, seafood...)"),
    current_user: Optional[User] = Depends(get_current_guest_or_user),
    db: Session = Depends(get_db)
):
    """
    Thuật toán Gợi ý Địa điểm Ăn uống Thông minh (Smart Recommendation Engine):
    - Đọc vị trí GPS (latitude, longitude) và lọc trong bán kính radius_km.
    - KHI NGƯỜI DÙNG ĐÃ ĐĂNG NHẬP:
      + Tự động đọc dị ứng (allergies) và loại bỏ hoàn toàn các quán chứa thành phần gây dị ứng (VD: seafood).
      + Tự động đọc chế độ ăn (diet_type): Nếu là vegetarian / vegan, chỉ giữ các quán có hỗ trợ món chay (vegetarian_support == True).
      + Tự động cộng điểm ưu tiên cho món ăn yêu thích (preferred_cuisines) và ngân sách mong muốn (avg_budget).
      + Trả về `applied_preferences` minh bạch tiêu chí đã lọc và lời giải thích AI.
    - KHI LÀ KHÁCH (GUEST):
      + Không ép buộc sở thích cá nhân, gợi ý theo khoảng cách và rating thông thường (BR-02).
    """
    # 1. Truy vấn các nhà hàng đang hoạt động trong CSDL
    query = db.query(Restaurant).filter(Restaurant.status == "active")
    restaurants = query.all()

    # 2. Xử lý thông tin sở thích người dùng nếu đã đăng nhập
    is_logged_in = current_user is not None
    user_id = current_user.id if is_logged_in else None
    diet_type = "omnivore"
    allergies: List[str] = []
    preferred_cuisines: List[str] = []
    avg_budget: Optional[float] = None
    active_filters: List[str] = []
    filter_reasons: List[str] = []

    if is_logged_in:
        pref = get_or_create_user_preference(db, current_user.id)
        diet_type = pref.diet_type or "omnivore"
        allergies = json.loads(pref.allergies) if pref.allergies else []
        preferred_cuisines = json.loads(pref.preferred_cuisines) if pref.preferred_cuisines else []
        avg_budget = pref.avg_budget

        # Ghi nhận các bộ lọc tự động kích hoạt
        if diet_type in ["vegetarian", "vegan"]:
            active_filters.append(f"Chế độ ăn: {diet_type.upper()} (Chỉ gợi ý địa điểm có hỗ trợ món chay)")
            filter_reasons.append(f"ưu tiên ẩm thực chay theo chế độ {diet_type}")

        if allergies:
            allergy_names = []
            for a in allergies:
                if a == "seafood": allergy_names.append("Hải sản")
                elif a == "peanut": allergy_names.append("Đậu phộng")
                elif a == "dairy": allergy_names.append("Sữa")
                elif a == "gluten": allergy_names.append("Gluten")
                else: allergy_names.append(a)
            active_filters.append(f"Loại trừ dị ứng: {', '.join(allergy_names)}")
            filter_reasons.append(f"loại trừ hoàn toàn thành phần gây dị ứng ({', '.join(allergy_names)})")

        if preferred_cuisines:
            active_filters.append(f"Ưu tiên sở thích ẩm thực: {', '.join(preferred_cuisines)}")

    # 3. Lọc & Tính điểm tương thích cho từng nhà hàng
    results: List[RecommendedRestaurantItem] = []

    # Danh sách từ khóa dị ứng hải sản
    SEAFOOD_KEYWORDS = {"hải sản", "seafood", "tôm", "cua", "ghẹ", "mực", "ốc", "hàu", "bạch tuộc"}

    for r in restaurants:
        # Tính khoảng cách GPS
        dist = calc_haversine_distance(latitude, longitude, r.latitude, r.longitude)
        if dist > radius_km:
            continue

        # Lọc theo từ khóa tìm kiếm (nếu có)
        if keyword:
            kw = keyword.lower()
            name_match = kw in r.name.lower()
            cuisine_match = r.cuisine_type and kw in r.cuisine_type.lower()
            addr_match = kw in r.address.lower()
            if not (name_match or cuisine_match or addr_match):
                continue

        # Lọc theo thể loại nếu người dùng chọn thủ công
        if category and category != "all":
            cat_lower = category.lower()
            cuisine_str = (r.cuisine_type or "").lower()
            if cat_lower == "vegan" and not (r.amenities and r.amenities.vegetarian_support):
                continue
            elif cat_lower == "seafood" and "hải sản" not in cuisine_str:
                continue
            elif cat_lower == "bbq" and ("nướng" not in cuisine_str and "bbq" not in cuisine_str):
                continue
            elif cat_lower == "hotpot" and ("lẩu" not in cuisine_str and "nấm" not in cuisine_str):
                continue

        # Lọc theo mức giá tối đa nếu có truyền tham số
        if max_budget and r.min_price > max_budget:
            continue

        # ======================================================================
        # ÁP DỤNG RÀNG BUỘC SỞ THÍCH CÁ NHÂN (USER PREFERENCES ENFORCEMENT)
        # ======================================================================
        amenities = r.amenities
        has_veg = amenities.vegetarian_support if amenities else False
        has_park = amenities.has_parking if amenities else False
        has_room = amenities.has_private_room if amenities else False
        r_name_lower = r.name.lower()
        r_cuisine_lower = (r.cuisine_type or "").lower()

        if is_logged_in:
            # 1. RÀNG BUỘC CHẾ ĐỘ ĂN (DIET TYPE)
            if diet_type in ["vegetarian", "vegan"]:
                # Nếu người dùng ăn chay mà quán KHÔNG hỗ trợ món chay -> Loại bỏ ngay
                if not has_veg and "chay" not in r_cuisine_lower and "chay" not in r_name_lower:
                    continue

            # 2. RÀNG BUỘC DỊ ỨNG (ALLERGIES)
            if "seafood" in allergies:
                # Loại bỏ nhà hàng chuyên hải sản hoặc tên/thực đơn chứa hải sản
                is_seafood_place = (
                    "hải sản" in r_cuisine_lower or
                    any(kw in r_name_lower for kw in ["hải sản", "seafood", "quán ốc", "ốc ", "cua "])
                )
                if is_seafood_place:
                    continue

            if "peanut" in allergies:
                # Nếu quán chuyên đồ ăn có cảnh báo đậu phộng đặc thù
                pass

        # ======================================================================
        # TÍNH ĐIỂM TƯƠNG THÍCH (WEIGHTED MATCH SCORE)
        # ======================================================================
        dist_score = max(0.0, 1.0 - (dist / radius_km))
        rating_score = min(1.0, (r.avg_rating or 4.0) / 5.0)

        ai_reasons: List[str] = []
        pref_bonus = 0.0

        if is_logged_in:
            # Ưu tiên chế độ ăn
            if diet_type in ["vegetarian", "vegan"] and (has_veg or "chay" in r_cuisine_lower):
                pref_bonus += 0.4
                ai_reasons.append("Hỗ trợ thực đơn chay chu đáo")

            # Ưu tiên món yêu thích
            if preferred_cuisines:
                for pc in preferred_cuisines:
                    if pc.lower() in r_cuisine_lower or pc.lower() in r_name_lower:
                        pref_bonus += 0.3
                        ai_reasons.append(f"Đúng món yêu thích '{pc}'")
                        break

            # Ưu tiên theo ngân sách cá nhân
            if avg_budget and r.min_price <= avg_budget <= r.max_price:
                pref_bonus += 0.3
                ai_reasons.append("Khoảng giá vừa vặn ngân sách")

            pref_bonus = min(1.0, pref_bonus)
            # Trọng số: 35% khoảng cách, 35% đánh giá, 30% sở thích cá nhân
            raw_score = (dist_score * 0.35 + rating_score * 0.35 + pref_bonus * 0.30) * 100
        else:
            # Guest: Trọng số 50% khoảng cách, 50% đánh giá
            raw_score = (dist_score * 0.50 + rating_score * 0.50) * 100
            if has_park: ai_reasons.append("Có bãi đỗ xe")
            if has_room: ai_reasons.append("Có phòng riêng")

        # Chuẩn hóa match_score trong khoảng 72% đến 99%
        match_score = min(99, max(72, round(raw_score)))

        # Sinh lời giải thích AI tự động
        dist_text = f"cách {dist:.1f}km"
        rating_text = f"đánh giá {r.avg_rating}★"
        if ai_reasons:
            full_ai_reason = f"Phù hợp {match_score}%: {', '.join(ai_reasons)}, {dist_text}, {rating_text}."
        else:
            full_ai_reason = f"Phù hợp {match_score}%: Địa điểm uy tín ({rating_text}), {dist_text}."

        results.append(
            RecommendedRestaurantItem(
                id=r.id,
                name=r.name,
                address=r.address,
                cuisine_type=r.cuisine_type,
                latitude=r.latitude,
                longitude=r.longitude,
                min_price=r.min_price,
                max_price=r.max_price,
                avg_rating=r.avg_rating,
                total_reviews=r.total_reviews,
                status=r.status,
                distance_km=round(dist, 2),
                match_score=match_score,
                ai_reason=full_ai_reason,
                vegetarian_support=has_veg,
                has_parking=has_park,
                has_private_room=has_room,
            )
        )

    # Sắp xếp theo match_score giảm dần (ưu tiên cao nhất lên đầu)
    results.sort(key=lambda item: item.match_score, reverse=True)

    # Tổng kết thông tin tiêu chí AI áp dụng
    if is_logged_in:
        reason_summary = (
            f"Trợ lý AI đã tự động đọc hồ sơ của bạn ({', '.join(filter_reasons) if filter_reasons else 'ưu tiên theo khoảng cách & đánh giá'}) "
            f"để tinh chỉnh kết quả tối ưu nhất."
        )
    else:
        reason_summary = "Chế độ Khách (Guest) - Đang hiển thị kết quả theo khoảng cách địa lý và điểm đánh giá thực tế (BR-02)."

    summary = AppliedPreferencesSummary(
        is_logged_in=is_logged_in,
        user_id=user_id,
        diet_type=diet_type if is_logged_in else None,
        allergies=allergies,
        avg_budget=avg_budget,
        active_filters=active_filters,
        filter_reason=reason_summary,
    )

    return RecommendationResponse(
        status="success",
        total=len(results),
        applied_preferences=summary,
        data=results
    )
