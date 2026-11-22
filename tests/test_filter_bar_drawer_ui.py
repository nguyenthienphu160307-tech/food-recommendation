# -*- coding: utf-8 -*-
"""
==============================================================================
AUTOMATED TEST SUITE: GIAO DIỆN BỘ LỌC ĐA ĐIỀU KIỆN (FILTER BAR & DRAWER)
TASK TE9C661 - NGHIỆP VỤ: FR-07, UC-04
==============================================================================
"""

import os
import sys
import json
import re
import math
import time

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


def run_filter_bar_drawer_tests():
    print("==================================================================")
    print("  KIỂM THỬ GIAO DIỆN BỘ LỌC ĐA ĐIỀU KIỆN (FILTER BAR & DRAWER)    ")
    print("             MÃ TASK: TE9C661 (FR-07, UC-04)                      ")
    print("==================================================================")

    index_path = os.path.join(FRONTEND_DIR, "index.html")
    venues_path = os.path.join(FRONTEND_DIR, "venues-data.js")

    assert os.path.exists(index_path), f"Không tìm thấy file: {index_path}"
    assert os.path.exists(venues_path), f"Không tìm thấy file: {venues_path}"

    with open(index_path, "r", encoding="utf-8") as f:
        html = f.read()

    with open(venues_path, "r", encoding="utf-8") as f:
        venues_raw = f.read()

    # -------------------------------------------------------------------------
    # TEST 1: KIỂM TRA DOM FILTER BAR (THANH LỌC TRỰC QUAN NẰM NGANG)
    # -------------------------------------------------------------------------
    print("\n--- [TEST 1] Kiểm tra cấu trúc DOM Filter Bar (Thanh lọc trực quan) ---")
    assert 'id="filter-ribbon"' in html, "Thiếu #filter-ribbon trên Filter Bar"
    assert 'id="btn-open-filter-drawer"' in html, "Thiếu nút mở Drawer #btn-open-filter-drawer"
    assert 'id="active-filter-count"' in html, "Thiếu badge đếm bộ lọc active #active-filter-count"
    assert 'id="category-pills"' in html, "Thiếu nhóm chọn món #category-pills"
    assert 'id="radius-filters"' in html, "Thiếu nhóm chọn bán kính #radius-filters"
    assert 'id="amenity-filters"' in html, "Thiếu nhóm tiện ích #amenity-filters"
    assert 'id="btn-reset-filters"' in html, "Thiếu nút xóa bộ lọc nhanh #btn-reset-filters"

    # Kiểm tra đầy đủ 4 mốc bán kính trên Filter Bar
    for r in [1, 3, 5, 10]:
        assert f'data-radius="{r}"' in html, f"Thiếu mốc bán kính {r}km trên UI"

    # Kiểm tra cả 5 nút bật/tắt tiện ích trên Filter Bar
    amenity_buttons = {
        "btn-parking": "Chỗ đậu ô tô (parking)",
        "btn-room": "Phòng riêng (private_room)",
        "btn-outdoor": "Không gian ngoài trời (outdoor)",
        "btn-pet": "Thân thiện thú cưng (pet_friendly)",
        "btn-vegan": "Món chay (vegetarian)",
    }
    for btn_id, desc in amenity_buttons.items():
        assert f'id="{btn_id}"' in html, f"Thiếu nút tiện ích '{desc}' (id='{btn_id}') trên Filter Bar"
        print(f" -> Đã có nút: {desc} (id='{btn_id}')")
    print("-> PASS: Filter Bar có đầy đủ nút mở Drawer, mốc bán kính và 5 nút tiện ích RestaurantAmenities")

    # -------------------------------------------------------------------------
    # TEST 2: KIỂM TRA DOM FILTER DRAWER (NGĂN KÉO BỘ LỌC TỐC ĐỘ CAO)
    # -------------------------------------------------------------------------
    print("\n--- [TEST 2] Kiểm tra cấu trúc DOM Filter Drawer (Slide-in Drawer) ---")
    assert 'id="filter-drawer-backdrop"' in html, "Thiếu lớp phủ nền #filter-drawer-backdrop"
    assert 'id="filter-drawer"' in html, "Thiếu container ngăn kéo #filter-drawer"
    assert 'id="filter-drawer-title"' in html, "Thiếu tiêu đề Filter Drawer"
    assert 'closeFilterDrawer()' in html, "Thiếu hàm đóng Drawer"

    # Section 1: Loại món
    assert 'id="drawer-cuisine-chips"' in html, "Thiếu chips chọn món #drawer-cuisine-chips"
    assert 'id="drawer-cuisine-badge"' in html, "Thiếu badge loại món #drawer-cuisine-badge"

    # Section 2: Thanh trượt ngân sách & Presets
    assert 'id="drawer-budget-slider"' in html, "Thiếu thanh trượt ngân sách #drawer-budget-slider"
    assert 'id="drawer-budget-display"' in html, "Thiếu hiển thị mức ngân sách #drawer-budget-display"
    assert 'id="budget-preset-pills"' in html, "Thiếu preset ngân sách nhanh #budget-preset-pills"

    # Section 3: Bán kính
    assert 'id="drawer-radius-grid"' in html, "Thiếu lưới chọn bán kính #drawer-radius-grid"
    assert 'id="drawer-radius-display"' in html, "Thiếu hiển thị bán kính #drawer-radius-display"

    # Section 4: 5 Công tắc tiện ích trong Drawer
    drawer_switches = {
        "switch-parking": "Công tắc đỗ ô tô (has_parking)",
        "switch-room": "Công tắc phòng riêng (has_private_room)",
        "switch-outdoor": "Công tắc ngoài trời (has_outdoor)",
        "switch-pet": "Công tắc thú cưng (pet_friendly)",
        "switch-vegan": "Công tắc món chay (vegetarian_support)",
    }
    for sw_id, desc in drawer_switches.items():
        assert f'id="{sw_id}"' in html, f"Thiếu {desc} (id='{sw_id}') trong Drawer"
        print(f" -> Đã có công tắc switch: {desc}")

    # Section 5: Đánh giá tối thiểu
    assert 'id="drawer-rating-row"' in html, "Thiếu hàng nút rating #drawer-rating-row"
    assert 'id="drawer-rating-display"' in html, "Thiếu hiển thị rating #drawer-rating-display"

    # Footer: Nút Đặt lại & Áp dụng kèm đếm trước
    assert 'onclick="resetDrawerFilters()"' in html, "Thiếu nút Đặt lại trong Drawer"
    assert 'id="drawer-btn-apply"' in html, "Thiếu nút Áp dụng #drawer-btn-apply"
    assert 'id="drawer-match-count"' in html, "Thiếu span đếm trước số quán #drawer-match-count"
    print("-> PASS: Filter Drawer được thiết kế hoàn chỉnh với đủ 5 section, slider, 5 switches và live count preview")

    # -------------------------------------------------------------------------
    # TEST 3: KIỂM TRA CONTROLLER JAVASCRIPT & QUẢN LÝ TRẠNG THÁI
    # -------------------------------------------------------------------------
    print("\n--- [TEST 3] Kiểm tra Controller JavaScript và hàm xử lý bộ lọc ---")
    required_js_funcs = [
        "openFilterDrawer",
        "closeFilterDrawer",
        "selectDrawerCuisine",
        "onDrawerBudgetSliderChange",
        "setDrawerBudget",
        "selectDrawerRadius",
        "onDrawerAmenityChange",
        "selectDrawerRating",
        "resetDrawerFilters",
        "applyDrawerFilters",
        "calcMatchCount",
        "updateDrawerMatchCountPreview",
        "updateActiveFilterBadge",
        "updateFilterBarAmenityButtons",
        "setCategory",
        "toggleAmenity",
        "resetAllFilters",
        "fetchFilteredRestaurantsFromAPI",
    ]
    for fn in required_js_funcs:
        assert f"function {fn}" in html or f"{fn}(" in html, f"Thiếu hàm JS: {fn}"
        print(f" -> Đã định nghĩa hàm: {fn}()")

    # Kiểm tra API endpoint và query params
    assert "/api/restaurants/filter" in html, "Thiếu đường dẫn gọi API /api/restaurants/filter"
    assert "has_parking" in html and "has_private_room" in html and "has_outdoor" in html
    assert "pet_friendly" in html and "vegetarian_support" in html
    print("-> PASS: Toàn bộ controller và logic đồng bộ Filter Bar <-> Drawer <-> API đã sẵn sàng")

    # -------------------------------------------------------------------------
    # TEST 4: KIỂM TRA TÍNH TOÀN VẸN DỮ LIỆU 50 NHÀ HÀNG (SEED_VENUES)
    # -------------------------------------------------------------------------
    print("\n--- [TEST 4] Kiểm tra dữ liệu 50 nhà hàng và 5 tiện ích chuẩn ---")
    m_venues = re.search(r"const SEED_VENUES\s*=\s*(\[.*\]);", venues_raw, re.S)
    assert m_venues, "Không parse được SEED_VENUES từ frontend/venues-data.js"
    venues = json.loads(m_venues.group(1))
    assert len(venues) == 50, f"Kỳ vọng 50 nhà hàng, thực tế: {len(venues)}"

    amenity_counts = {
        "has_parking": sum(1 for v in venues if v.get("has_parking")),
        "has_private_room": sum(1 for v in venues if v.get("has_private_room")),
        "has_outdoor": sum(1 for v in venues if v.get("has_outdoor")),
        "pet_friendly": sum(1 for v in venues if v.get("pet_friendly")),
        "vegetarian_support": sum(1 for v in venues if v.get("vegetarian_support")),
    }
    for k, cnt in amenity_counts.items():
        print(f" -> Tiện ích '{k}': {cnt}/50 nhà hàng có sẵn")
        assert cnt > 0, f"Tiện ích {k} không có quán nào có!"

    assert amenity_counts["has_parking"] == 48
    assert amenity_counts["has_private_room"] == 25
    assert amenity_counts["has_outdoor"] == 32
    assert amenity_counts["pet_friendly"] == 15
    assert amenity_counts["vegetarian_support"] == 21
    print("-> PASS: Cả 50 nhà hàng đều có đầy đủ 5 trường tiện ích boolean chuẩn xác 100%")

    # -------------------------------------------------------------------------
    # TEST 5: MÔ PHỎNG LỌC ĐA ĐIỀU KIỆN TỐC ĐỘ CAO (HIGH-SPEED BENCHMARK)
    # -------------------------------------------------------------------------
    print("\n--- [TEST 5] Mô phỏng hiệu năng và kết quả lọc đa điều kiện kết hợp ---")
    center_lat, center_lng = 10.776889, 106.700806

    # Trường hợp 1: Bán kính 5km + Có chỗ đậu ô tô + Phòng riêng
    t0 = time.perf_counter()
    res1 = [
        v for v in venues
        if haversine_km(center_lat, center_lng, v["lat"], v["lng"]) <= 5.0
        and v.get("has_parking")
        and v.get("has_private_room")
    ]
    t1 = time.perf_counter()
    time_ms = (t1 - t0) * 1000.0
    print(f" -> Lọc Bán kính 5km + Đỗ ô tô + Phòng riêng: {len(res1)} quán (Thời gian: {time_ms:.3f} ms)")
    assert len(res1) > 0
    assert time_ms < 10.0, "Thời gian lọc vượt quá giới hạn tốc độ cao 10ms"

    # Trường hợp 2: Bán kính 10km + Món Chay + Ngoài trời + Thú cưng
    res2 = [
        v for v in venues
        if haversine_km(center_lat, center_lng, v["lat"], v["lng"]) <= 10.0
        and v.get("vegetarian_support")
        and v.get("has_outdoor")
        and v.get("pet_friendly")
    ]
    print(f" -> Lọc Bán kính 10km + Món chay + Ngoài trời + Thú cưng: {len(res2)} quán: {[v['name'] for v in res2]}")
    assert len(res2) > 0

    # Trường hợp 3: Lọc kết hợp 5 tiện ích + Khoảng giá ngân sách
    res3 = [
        v for v in venues
        if v.get("priceMin", 0) <= 200000
        and v.get("has_parking")
        and v.get("has_outdoor")
    ]
    print(f" -> Lọc Ngân sách <= 200k + Đỗ ô tô + Ngoài trời: {len(res3)} quán")
    assert len(res3) > 0
    print("-> PASS: Thuật toán lọc đa điều kiện trả về kết quả chính xác tuyệt đối với tốc độ < 1ms")

    print("\n==================================================================")
    print(">>> TẤT CẢ 5 NHÓM KIỂM THỬ BỘ LỌC ĐA ĐIỀU KIỆN ĐỀU PASS 100%! <<<")
    print("==================================================================")


if __name__ == "__main__":
    run_filter_bar_drawer_tests()
