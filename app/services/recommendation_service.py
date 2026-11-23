"""
Module Dịch vụ Sinh lý do Đề xuất & Chấm điểm Độ phù hợp (% Match Score) - Task TSK-40 / PBI-11.
Module 4: Lọc, gợi ý và xếp hạng nhà hàng

Tính năng:
1. Tính khoảng cách địa lý Haversine từ GPS người dùng đến nhà hàng.
2. Tính điểm độ phù hợp % Match Score kết hợp (Khoảng cách, Đánh giá, Tiện ích, Giờ mở cửa BR-03).
3. Tự động sinh các tag lý do đề xuất trực quan (Match Reason Chips).
4. Tạo câu tóm tắt đề xuất ngắn gọn một dòng (Recommendation Summary).
"""
import math
from datetime import datetime
from typing import Any, Dict, List, Optional

from app.services.open_hours_service import (
    check_restaurant_open_status,
    get_vietnam_now,
    VIETNAM_TZ,
)

# Tọa độ mặc định trung tâm Quận 1, TP.HCM
DEFAULT_USER_LAT = 10.7860
DEFAULT_USER_LON = 106.7003


def calculate_distance_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Tính khoảng cách giữa 2 tọa độ GPS theo công thức Haversine (Đơn vị: km)
    """
    R = 6371.0  # Bán kính Trái Đất theo km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(math.radians(lat1))
        * math.cos(math.radians(lat2))
        * math.sin(dlon / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return round(R * c, 2)


def calculate_match_score(
    distance_km: float,
    avg_rating: float,
    amenities: Optional[Any] = None,
    is_open: bool = False,
    max_radius_km: float = 15.0,
) -> int:
    """
    Tính điểm phần trăm độ phù hợp (% Match Score) từ 65% đến 99% theo trọng số (BR-05):
      - Khoảng cách địa lý: 35%
      - Điểm đánh giá sao: 25%
      - Tiện ích đáp ứng: 25%
      - Trạng thái đang mở cửa (BR-03): 15%
    """
    # 1. Điểm khoảng cách (0.0 -> 1.0)
    dist_score = max(0.0, 1.0 - (distance_km / max_radius_km))

    # 2. Điểm đánh giá sao (0.0 -> 1.0)
    rating_score = min(1.0, max(0.0, (avg_rating or 4.0) / 5.0))

    # 3. Điểm tiện ích (mỗi tiện ích có sẵn đóng góp điểm)
    amenity_count = 0
    if amenities:
        if getattr(amenities, "has_parking", False):
            amenity_count += 1
        if getattr(amenities, "has_private_room", False):
            amenity_count += 1
        if getattr(amenities, "has_outdoor", False):
            amenity_count += 1
        if getattr(amenities, "pet_friendly", False):
            amenity_count += 1
        if getattr(amenities, "vegetarian_support", False):
            amenity_count += 1
    amenity_score = min(1.0, amenity_count / 3.0)  # Tối đa khi có từ 3 tiện ích trở lên

    # 4. Điểm mở cửa BR-03 (1.0 nếu mở, 0.0 nếu đóng)
    open_score = 1.0 if is_open else 0.0

    # Tổng hợp theo tỷ trọng BR-05
    raw_score = (
        dist_score * 0.35
        + rating_score * 0.25
        + amenity_score * 0.25
        + open_score * 0.15
    )

    # Quy đổi về thang điểm 65% - 99%
    percent = int(round(65 + raw_score * 34))
    return max(65, min(99, percent))


def generate_match_reasons(
    restaurant: Any,
    user_lat: Optional[float] = None,
    user_lon: Optional[float] = None,
    check_dt: Optional[datetime] = None,
    is_open: Optional[bool] = None,
) -> List[str]:
    """
    Tự động sinh các tag lý do đề xuất trực quan (Match Highlights) cho nhà hàng:
    - Khoảng cách địa lý & thời gian di chuyển
    - Trạng thái giờ mở cửa (BR-03)
    - Mức giá / ngân sách hợp lý
    - Tiện ích nổi bật (ô tô, phòng riêng, ngoài trời, thú cưng, đồ chay)
    - Đánh giá sao & độ uy tín cộng đồng
    """
    reasons: List[str] = []

    # 1. Kiểm tra vị trí & khoảng cách
    u_lat = user_lat if user_lat is not None else DEFAULT_USER_LAT
    u_lon = user_lon if user_lon is not None else DEFAULT_USER_LON
    r_lat = getattr(restaurant, "latitude", None)
    r_lon = getattr(restaurant, "longitude", None)

    if r_lat is not None and r_lon is not None:
        dist = calculate_distance_km(u_lat, u_lon, float(r_lat), float(r_lon))
        if dist < 1.0:
            reasons.append(f"📍 Rất gần bạn ({dist:.1f}km)")
        elif dist <= 3.0:
            est_mins = max(3, round(dist * 3.2))
            reasons.append(f"📍 Cách {dist:.1f}km (~{est_mins}p đi xe)")
        else:
            reasons.append(f"📍 Cách {dist:.1f}km")

    # 2. Kiểm tra giờ mở cửa thực tế (BR-03)
    if is_open is None:
        open_hours_str = getattr(restaurant, "open_hours", None)
        open_info = check_restaurant_open_status(open_hours_str, check_dt=check_dt)
        is_open = open_info["is_open"]

    if is_open:
        reasons.append("🟢 Đang mở cửa đón khách")
    else:
        open_hours_str = getattr(restaurant, "open_hours", "")
        if open_hours_str and "18:00" in open_hours_str and "02:00" in open_hours_str:
            reasons.append("🌙 Mở xuyên đêm đến 02:00")

    # 3. Mức giá & ngân sách
    min_p = getattr(restaurant, "min_price", 0.0) or 0.0
    max_p = getattr(restaurant, "max_price", 0.0) or 0.0
    if max_p > 0:
        if max_p <= 120000:
            reasons.append("💵 Giá hạt dẻ (< 120k)")
        elif max_p <= 300000:
            reasons.append(f"💵 Trong tầm giá {int(max_p/1000)}k")
        elif max_p <= 600000:
            reasons.append("💵 Hợp túi tiền tiệc nhóm")
        else:
            reasons.append("💵 Đẳng cấp thượng hạng")

    # 4. Tiện ích nổi bật (RestaurantAmenities)
    am = getattr(restaurant, "amenities", None)
    if am:
        if getattr(am, "has_parking", False):
            reasons.append("🚗 Có chỗ đỗ ô tô")
        if getattr(am, "has_private_room", False):
            reasons.append("🚪 Có phòng riêng yên tĩnh")
        if getattr(am, "has_outdoor", False):
            reasons.append("🌿 Không gian ngoài trời thoáng mát")
        if getattr(am, "pet_friendly", False):
            reasons.append("🐾 Thân thiện thú cưng")
        if getattr(am, "vegetarian_support", False):
            reasons.append("🥗 Phục vụ món chay")

    # 5. Đánh giá sao & độ uy tín cộng đồng
    avg_r = getattr(restaurant, "avg_rating", 0.0) or 0.0
    tot_rev = getattr(restaurant, "total_reviews", 0) or 0
    if avg_r >= 4.7:
        reasons.append(f"⭐ Đánh giá xuất sắc {avg_r:.1f}★")
    elif avg_r >= 4.5:
        reasons.append(f"⭐ Đánh giá cao {avg_r:.1f}★")
    
    if tot_rev >= 200:
        reasons.append(f"🔥 Rất đông khách ({tot_rev} đánh giá)")

    # 6. Loại ẩm thực đặc trưng
    cuisine = getattr(restaurant, "cuisine_type", None)
    if cuisine and len(reasons) < 5:
        reasons.append(f"🍽️ {cuisine}")

    # Giữ tối đa 5 lý do nổi bật nhất để giao diện gọn gàng, súc tích
    return reasons[:5]


def generate_recommendation_summary(match_score: int, match_reasons: List[str]) -> str:
    """
    Sinh dòng tóm tắt đề xuất một dòng (One-line Recommendation Summary).
    Ví dụ: 'Khớp 95% • Cách 1.2km • Có bãi ô tô • Trong tầm giá 250k'
    """
    cleaned_reasons = []
    for r in match_reasons:
        # Bỏ icon đầu chuỗi để tóm tắt gọn gàng
        text = r.split(" ", 1)[-1] if " " in r else r
        cleaned_reasons.append(text)
    
    parts = [f"Khớp {match_score}%"] + cleaned_reasons[:3]
    return " • ".join(parts)
