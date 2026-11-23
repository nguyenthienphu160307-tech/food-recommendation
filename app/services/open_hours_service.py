"""
Module Dịch vụ Phân tích & Kiểm tra Giờ mở cửa hoạt động thực tế (Task TSK-37 / BR-03).
Thuộc PBI-11: Hệ thống xếp hạng nhà hàng theo mức độ khớp tiêu chí, ưu tiên quán đang mở cửa.

Các tính năng chính:
1. Chuẩn hóa & phân tích các định dạng giờ mở cửa (chuẩn, ca gãy, qua đêm, 24/7).
2. Kiểm tra trạng thái mở/đóng cửa theo thời gian thực (Múi giờ Việt Nam Asia/Ho_Chi_Minh GMT+7).
3. Tính toán nhãn hiển thị và thời gian thay đổi trạng thái kế tiếp (mở lại lúc / đóng lúc).
4. Tính điểm thưởng xếp hạng (BR-03 & BR-05 Ranking Bonus) cho các quán đang mở cửa.
"""
import re
from datetime import datetime, time, timedelta, timezone
from typing import Any, Dict, List, Optional, Tuple

# Múi giờ chuẩn Việt Nam (UTC+7 / GMT+7)
VIETNAM_TZ = timezone(timedelta(hours=7))
DEFAULT_OPEN_BONUS_WEIGHT = 2.0  # Điểm trọng số cộng thưởng cho quán đang mở cửa (BR-03)


def get_vietnam_now() -> datetime:
    """Lấy thời điểm hiện tại theo múi giờ Việt Nam (UTC+7)"""
    return datetime.now(VIETNAM_TZ)


def normalize_time_str(t_str: str) -> Optional[time]:
    """
    Chuẩn hóa chuỗi thời gian thành đối tượng datetime.time.
    Hỗ trợ:
      - '08:00', '8:00', '8:30'
      - '8h', '8h30', '8h00'
      - '8:00 AM', '10:00 PM', '8:30pm'
      - '8', '22'
    """
    if not t_str:
        return None
    s = t_str.strip().lower()

    # Dạng tiếng Việt: '8h', '8h30', '8h00'
    m_vn = re.match(r"^(\d{1,2})h(?:(\d{1,2}))?$", s)
    if m_vn:
        h = int(m_vn.group(1))
        mn = int(m_vn.group(2)) if m_vn.group(2) else 0
        if 0 <= h <= 23 and 0 <= mn <= 59:
            return time(h, mn)
        if h == 24 and mn == 0:
            return time(23, 59, 59)

    # Dạng AM / PM: '8:30 am', '10:00 pm', '8pm'
    m_ampm = re.match(r"^(\d{1,2})(?::(\d{1,2}))?\s*(am|pm)$", s)
    if m_ampm:
        h = int(m_ampm.group(1))
        mn = int(m_ampm.group(2)) if m_ampm.group(2) else 0
        period = m_ampm.group(3)
        if period == "pm" and h < 12:
            h += 12
        elif period == "am" and h == 12:
            h = 0
        if 0 <= h <= 23 and 0 <= mn <= 59:
            return time(h, mn)

    # Dạng chuẩn: '08:00', '8:30'
    m_std = re.match(r"^(\d{1,2}):(\d{1,2})$", s)
    if m_std:
        h = int(m_std.group(1))
        mn = int(m_std.group(2))
        if 0 <= h <= 23 and 0 <= mn <= 59:
            return time(h, mn)
        if h == 24 and mn == 0:
            return time(23, 59, 59)

    # Dạng chỉ số giờ: '8', '22'
    if s.isdigit():
        h = int(s)
        if 0 <= h <= 23:
            return time(h, 0)
        if h == 24:
            return time(23, 59, 59)

    return None


def parse_open_hours_intervals(open_hours_str: Optional[str]) -> List[Tuple[time, time, bool, bool]]:
    """
    Phân tích chuỗi open_hours thành danh sách các khoảng thời gian hoạt động.
    Trả về danh sách tuple: (start_time, end_time, is_overnight, is_all_day)
    """
    if not open_hours_str or not open_hours_str.strip():
        return []

    s = open_hours_str.strip().lower()

    # Nhận diện quán mở cửa 24/7 hoặc mở cả ngày
    if any(k in s for k in ["24/7", "24/24", "mở cả ngày", "cả ngày", "suốt ngày", "24h", "cả tuần 24/7"]):
        return [(time(0, 0), time(23, 59, 59), False, True)]

    # Tách các ca hoạt động (phân tách bởi dấu phẩy, chấm phẩy, gạch chéo, hoặc 'và' / '&')
    parts = re.split(r"[,;|\n]|(?:\bvà\b)|&", s)
    intervals = []

    for part in parts:
        part = part.strip()
        if not part:
            continue
        # Bắt dải thời gian: vd "08:00 - 22:00", "8h30 đến 23h", "10:00 – 14:00"
        m = re.search(
            r"([0-9]{1,2}(?:[:h][0-9]{1,2})?(?:\s*[ap]m)?)\s*(?:-|đến|–|to)\s*([0-9]{1,2}(?:[:h][0-9]{1,2})?(?:\s*[ap]m)?)",
            part,
            re.IGNORECASE,
        )
        if m:
            t1 = normalize_time_str(m.group(1))
            t2 = normalize_time_str(m.group(2))
            if t1 and t2:
                is_overnight = t1 > t2
                intervals.append((t1, t2, is_overnight, False))

    return intervals


def check_restaurant_open_status(
    open_hours: Optional[str],
    check_dt: Optional[datetime] = None,
    bonus_weight: float = DEFAULT_OPEN_BONUS_WEIGHT,
) -> Dict[str, Any]:
    """
    Kiểm tra trạng thái mở cửa của nhà hàng tại thời điểm `check_dt` (Quy tắc BR-03).
    
    Tham số:
      - open_hours: Chuỗi giờ mở cửa lưu trong CSDL (VD: '08:00 - 22:00')
      - check_dt: Thời điểm kiểm tra (Mặc định: Giờ hiện tại tại Việt Nam UTC+7)
      - bonus_weight: Trọng số điểm thưởng cộng vào xếp hạng khi đang mở cửa (BR-03)
      
    Trả về dict:
      - is_open: bool (True nếu đang trong giờ mở cửa, False nếu đang đóng)
      - status_code: 'OPEN' | 'OPEN_24_7' | 'CLOSED' | 'UNKNOWN'
      - status_label: 'Đang mở cửa' | 'Đã đóng cửa' | 'Chưa cập nhật'
      - detail_text: Chi tiết hiển thị (VD: 'Mở cửa đến 22:00', 'Mở lại lúc 17:00')
      - badge_color: 'green' | 'red' | 'gray'
      - bonus_score: float (Điểm ưu tiên cộng vào xếp hạng)
    """
    if check_dt is None:
        check_dt = get_vietnam_now()
    elif check_dt.tzinfo is None:
        check_dt = check_dt.replace(tzinfo=VIETNAM_TZ)

    cur_time = check_dt.time()
    intervals = parse_open_hours_intervals(open_hours)

    # 1. Trường hợp không có dữ liệu giờ mở cửa
    if not intervals:
        return {
            "is_open": False,
            "status_code": "UNKNOWN",
            "status_label": "Chưa cập nhật",
            "detail_text": "Chưa rõ giờ mở cửa",
            "badge_color": "gray",
            "bonus_score": 0.0,
            "open_hours_raw": open_hours or "",
        }

    # 2. Kiểm tra xem thời điểm hiện tại có nằm trong ca mở cửa nào không
    for t1, t2, is_overnight, is_all_day in intervals:
        # Ca 24/7 cả ngày
        if is_all_day:
            return {
                "is_open": True,
                "status_code": "OPEN_24_7",
                "status_label": "Đang mở cửa",
                "detail_text": "Mở cửa cả ngày (24/7)",
                "badge_color": "green",
                "bonus_score": bonus_weight,
                "open_hours_raw": open_hours or "",
            }

        # Ca mở xuyên đêm (VD: 18:00 - 02:00 sáng hôm sau)
        if is_overnight:
            if cur_time >= t1 or cur_time <= t2:
                close_label = t2.strftime("%H:%M")
                detail = f"Mở cửa đến {close_label} (sáng hôm sau)" if cur_time >= t1 else f"Mở cửa đến {close_label}"
                return {
                    "is_open": True,
                    "status_code": "OPEN",
                    "status_label": "Đang mở cửa",
                    "detail_text": detail,
                    "badge_color": "green",
                    "bonus_score": bonus_weight,
                    "open_hours_raw": open_hours or "",
                }
        else:
            # Ca tiêu chuẩn trong ngày (VD: 08:00 - 22:00)
            if t1 <= cur_time <= t2:
                return {
                    "is_open": True,
                    "status_code": "OPEN",
                    "status_label": "Đang mở cửa",
                    "detail_text": f"Mở cửa đến {t2.strftime('%H:%M')}",
                    "badge_color": "green",
                    "bonus_score": bonus_weight,
                    "open_hours_raw": open_hours or "",
                }

    # 3. Nếu không nằm trong ca nào -> Đã đóng cửa, tính thời điểm mở lại kế tiếp
    # Sắp xếp các ca theo thời gian bắt đầu
    sorted_intervals = sorted(intervals, key=lambda x: x[0])
    next_open_time = None

    for t1, t2, is_overnight, is_all_day in sorted_intervals:
        if cur_time < t1:
            next_open_time = t1
            break

    if next_open_time:
        detail_msg = f"Mở lại lúc {next_open_time.strftime('%H:%M')}"
    else:
        # Nếu đã qua hết các ca trong ngày, mở lại ca đầu tiên vào sáng ngày mai
        first_shift_start = sorted_intervals[0][0].strftime("%H:%M")
        detail_msg = f"Mở lại lúc {first_shift_start} ngày mai"

    return {
        "is_open": False,
        "status_code": "CLOSED",
        "status_label": "Đã đóng cửa",
        "detail_text": detail_msg,
        "badge_color": "red",
        "bonus_score": 0.0,
        "open_hours_raw": open_hours or "",
    }


def calculate_open_hours_bonus(
    open_hours: Optional[str],
    check_dt: Optional[datetime] = None,
    bonus_weight: float = DEFAULT_OPEN_BONUS_WEIGHT,
) -> float:
    """
    Tính điểm thưởng ưu tiên xếp hạng cho nhà hàng dựa trên quy tắc BR-03:
    Nếu quán đang mở cửa -> cộng `bonus_weight` điểm.
    Nếu quán đang đóng cửa hoặc không rõ -> 0.0 điểm.
    """
    res = check_restaurant_open_status(open_hours=open_hours, check_dt=check_dt, bonus_weight=bonus_weight)
    return res["bonus_score"]
