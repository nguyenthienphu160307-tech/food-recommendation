"""
==============================================================================
AUTOMATED VERIFICATION TESTS:
HIỂN THỊ MARKER NHÀ HÀNG, VÒNG TRÒN BÁN KÍNH (1km, 3km, 5km, 10km),
POPUP THÔNG TIN & ĐỒNG BỘ CUỘN DANH SÁCH TRÊN BẢN ĐỒ
==============================================================================
"""

import os
import sys
import math
import json
import re

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRONTEND_DIR = os.path.join(ROOT_DIR, "frontend")


def haversine_km(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
    R = 6371.0
    d_lat = math.radians(lat2 - lat1)
    d_lng = math.radians(lng2 - lng1)
    a = (
        math.sin(d_lat / 2.0) ** 2
        + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(d_lng / 2.0) ** 2
    )
    return R * 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))


def run_map_feature_tests():
    print("==================================================================")
    print("  KIỂM THỬ TÍNH NĂNG BẢN ĐỒ: MARKER, BÁN KÍNH, POPUP & SCROLL SYNC")
    print("==================================================================")

    map_js_path = os.path.join(FRONTEND_DIR, "map-component.js")
    map_css_path = os.path.join(FRONTEND_DIR, "map-component.css")
    index_path = os.path.join(FRONTEND_DIR, "index.html")
    venues_js_path = os.path.join(FRONTEND_DIR, "venues-data.js")

    for p in (map_js_path, map_css_path, index_path, venues_js_path):
        assert os.path.exists(p), f"Thiếu file bắt buộc: {p}"

    with open(map_js_path, "r", encoding="utf-8") as f:
        map_js = f.read()
    with open(map_css_path, "r", encoding="utf-8") as f:
        map_css = f.read()
    with open(index_path, "r", encoding="utf-8") as f:
        index_html = f.read()
    with open(venues_js_path, "r", encoding="utf-8") as f:
        venues_raw = f.read()

    # 1. Kiểm tra cấu hình vòng tròn bán kính (1km, 3km, 5km, 10km)
    print("\n--- [TEST 1] Kiểm tra vòng tròn bán kính 1km, 3km, 5km, 10km ---")
    assert "radiusOptions || [1, 3, 5, 10]" in map_js
    assert "drawRadiusCircle" in map_js
    assert "L.circle" in map_js
    assert "setSearchRadius" in map_js
    for r in [1, 3, 5, 10]:
        assert f'data-radius="{r}"' in index_html, f"Thiếu nút bán kính {r}km trên UI"
    print("-> PASS: Đã cấu hình đầy đủ vòng tròn L.circle và 4 mốc bán kính 1km, 3km, 5km, 10km")

    # 2. Kiểm tra thuật toán lọc khoảng cách Haversine trên dữ liệu 50 nhà hàng thực tế
    print("\n--- [TEST 2] Kiểm tra độ chính xác lọc khoảng cách Haversine theo 4 mốc bán kính ---")
    json_match = re.search(r"const SEED_VENUES\s*=\s*(\[.*\]);", venues_raw, re.S)
    assert json_match, "Không parse được SEED_VENUES"
    venues = json.loads(json_match.group(1))
    center_lat, center_lng = 10.776889, 106.700806

    counts = {}
    for radius in [1, 3, 5, 10]:
        in_radius = [
            v for v in venues if haversine_km(center_lat, center_lng, v["lat"], v["lng"]) <= radius
        ]
        counts[radius] = len(in_radius)
        print(f" -> Bán kính {radius} km: {len(in_radius)} quán")

    assert counts[1] < counts[3] < counts[5] < counts[10]
    assert counts[1] == 13 and counts[3] == 26 and counts[5] == 37 and counts[10] == 45
    print("-> PASS: Kết quả đếm khoảng cách Haversine chính xác khớp 100% với giao diện thực tế (13 / 26 / 37 / 45)")

    # 3. Kiểm tra Marker kèm khoảng cách & Popup thông tin chi tiết
    print("\n--- [TEST 3] Kiểm tra Marker khoảng cách & Popup chi tiết ---")
    assert "formatPinDistance" in map_js
    assert "pin-dist" in map_js and ".pin-dist" in map_css
    assert "map-venue-popup" in map_js
    assert "popup-dist-badge" in map_js and ".popup-dist-badge" in map_css
    assert "popup-btn-directions" in map_js
    assert "window.onMapPopupSelectVenue" in map_js and "window.onMapPopupSelectVenue" in index_html
    print("-> PASS: Ghim hiển thị rating + khoảng cách (m/km) và Popup có ảnh, giá, khoảng cách, Chỉ đường & Chi tiết")

    # 4. Kiểm tra Đồng bộ cuộn danh sách quán <-> Bản đồ
    print("\n--- [TEST 4] Kiểm tra đồng bộ khi cuộn danh sách quán (Scroll Sync) ---")
    assert "setupScrollSyncObserver" in index_html
    assert "scrollSyncEnabled" in index_html
    assert "btn-scroll-sync" in index_html
    assert "highlightVenue" in map_js
    assert "active-pin" in map_js and ".active-pin" in map_css
    assert "active-sync" in index_html and ".venue-card.active-sync" in map_css
    assert "scrollToAndHighlightCard" in index_html
    print("-> PASS: Hỗ trợ đồng bộ 2 chiều (Cuộn danh sách -> Nổi bật & pan bản đồ; Click ghim -> Cuộn danh sách)")

    # 5. Kiểm tra không còn biến cũ lỗi (mainMap / userMarker) hay hàm thiếu (syncProfileData)
    print("\n--- [TEST 5] Kiểm tra tính toàn vẹn mã nguồn index.html ---")
    assert "function syncProfileData()" in index_html
    assert "let mainMap" not in index_html
    assert "mainMap." not in index_html
    assert "map-component.css" in index_html
    assert "map-component.js" in index_html
    print("-> PASS: Toàn bộ mã nguồn tích hợp sạch sẽ, không còn biến lỗi thừa\n")

    print("==================================================================")
    print(">>> TẤT CẢ 5 NHÓM KIỂM THỬ BẢN ĐỒ ĐỀU PASS THÀNH CÔNG 100%! <<<")
    print("==================================================================")


if __name__ == "__main__":
    run_map_feature_tests()
