# BÁO CÁO KIỂM THỬ NGHIỆM THU (QA REPORT) — TASK TE9C680
**Dự án:** Smart Dining — Hệ thống Gợi ý Địa điểm Ăn uống theo Vị trí & Chat AI  
**Phạm vi kiểm thử:** UC-03 (Định vị GPS & Bản đồ), UC-04 (Lọc đa điều kiện), UC-09 (Xem chi tiết nhà hàng & Bản đồ)
**Môi trường:** FastAPI + Uvicorn (`http://127.0.0.1:8000`), SQLite/MySQL, Leaflet.js 1.9.4, Trình duyệt Edge/Chrome  

---

## 1. Tổng hợp kết quả kiểm thử (Test Summary)

| Nhóm chức năng | Mã Use Case | Tổng số TC | Passed | Failed | Tỷ lệ đạt |
| :--- | :--- | :---: | :---: | :---: | :---: |
| Định vị GPS & Chọn vị trí thủ công | UC-03 | 4 | 4 | 0 | **100%** |
| Lọc nhà hàng đa điều kiện & Bán kính | UC-04 | 5 | 5 | 0 | **100%** |
| Xem chi tiết nhà hàng, Thực đơn & Bản đồ | UC-09 | 4 | 4 | 0 | **100%** |
| **Tổng cộng** | **3 Use Cases** | **13** | **13** | **0** | **100%** |

---

## 2. Chi tiết các Ca kiểm thử (Test Cases Execution)

### 2.1. UC-03: Tìm kiếm theo vị trí GPS & Chọn vị trí thủ công
| Mã TC | Tên kịch bản kiểm thử | Dữ liệu đầu vào | Kết quả kỳ vọng | Kết quả thực tế | Trạng thái |
| :--- | :--- | :--- | :--- | :--- | :---: |
| **TC-03-01** | Định vị GPS trình duyệt thành công | Cho phép quyền Geolocation tại Q1 (`10.7769, 106.7009`) | Bản đồ `flyTo` tới vị trí GPS, vẽ vòng tròn bán kính đỏ, cập nhật nhãn địa chỉ | Hoạt động đúng, khoảng cách Haversine hiển thị chính xác | **PASS** |
| **TC-03-02** | Từ chối quyền GPS (Fallback) | Bấm "Block" quyền vị trí | Tự động bật Modal chọn Quận/Huyện TP.HCM (18 khu vực) | Modal bật ngay khi bị từ chối, chọn Quận 3 cập nhật tâm bản đồ | **PASS** |
| **TC-03-03** | Kéo thả ghim / Click chọn điểm trên bản đồ | Kéo ghim đỏ sang Bình Thạnh (`10.8035, 106.7145`) | Cập nhật tọa độ mới, tính lại khoảng cách và danh sách quán | Danh sách & ghim cập nhật tức thì (< 200ms) | **PASS** |
| **TC-03-04** | Đổi lớp bản đồ nền (Streets / Satellite) | Chuyển giữa Google Streets, Vệ tinh, OSM | Bản đồ đổi tile mượt, không mất ghim nhà hàng | Đổi lớp nền mượt, giữ nguyên marker và vòng tròn bán kính | **PASS** |

### 2.2. UC-04: Lọc nhà hàng đa điều kiện (Filter Bar & Drawer)
| Mã TC | Tên kịch bản kiểm thử | Dữ liệu đầu vào | Kết quả kỳ vọng | Kết quả thực tế | Trạng thái |
| :--- | :--- | :--- | :--- | :--- | :---: |
| **TC-04-01** | Lọc theo mốc bán kính | Chọn lần lượt `1km`, `3km`, `5km`, `10km` từ Q1 | Số lượng quán tăng dần (13 → 26 → 37 → 45 quán), vòng tròn co giãn đúng | Khớp 100% số lượng và bán kính hiển thị | **PASS** |
| **TC-04-02** | Lọc theo loại hình ẩm thực | Chọn `Món Chay` / `Lẩu & BBQ` | Chỉ hiển thị các quán thuộc danh mục đã chọn | Trả về đúng danh sách quán khớp loại món | **PASS** |
| **TC-04-03** | Lọc kết hợp 5 tiện ích (`RestaurantAmenities`) | Bật đồng thời `has_parking=true` & `has_private_room=true` | API `GET /api/restaurants/filter` trả về quán có đủ cả 2 tiện ích | Kết quả chính xác 100%, không lẫn quán thiếu tiện ích | **PASS** |
| **TC-04-04** | Lọc theo thanh trượt ngân sách & Đánh giá sao | `price_max=300000`, `min_rating=4.5` | Chỉ giữ quán có `min_price <= 300k` và `avg_rating >= 4.5` | Lọc đúng, bộ đếm preview trong Drawer khớp thực tế | **PASS** |
| **TC-04-05** | Validation tham số lỗi | `price_min=500000, price_max=100000` hoặc thiếu `lng` | Trả về HTTP `400 Bad Request` kèm thông báo tiếng Việt | Chặn lỗi chuẩn xác, không gây sập server | **PASS** |

### 2.3. UC-09: Xem chi tiết nhà hàng, Thực đơn & Bản đồ
| Mã TC | Tên kịch bản kiểm thử | Dữ liệu đầu vào | Kết quả kỳ vọng | Kết quả thực tế | Trạng thái |
| :--- | :--- | :--- | :--- | :--- | :---: |
| **TC-09-01** | Mở trang chi tiết nhà hàng | `GET /restaurant-detail?id=1` | Hiển thị đủ tên quán, địa chỉ, giờ mở cửa, khoảng giá, rating | Hiển thị đầy đủ, tốc độ tải < 1 giây | **PASS** |
| **TC-09-02** | Thư viện ảnh Slider & 5 Tiện ích | Chuyển ảnh Next/Prev, kiểm tra 5 badge tiện ích | Ảnh chuyển mượt, hiển thị đúng trạng thái Có/Không hỗ trợ | Slider và 5 tiện ích khớp dữ liệu CSDL | **PASS** |
| **TC-09-03** | Thực đơn phân nhóm & Tìm kiếm món | Lọc theo tab nhóm món & gõ từ khóa tên món | Lọc đúng món ăn, hiển thị giá VNĐ và trạng thái Còn/Hết món | Hoạt động chính xác | **PASS** |
| **TC-09-04** | Bản đồ Mini Map & Chỉ đường Google Maps | Bấm nút "Mở chỉ đường Google Maps" | Mở tab Google Maps điền sẵn tọa độ xuất phát → đích | Đường dẫn `origin` & `destination` chính xác | **PASS** |

---

## 3. Kết quả chạy kiểm thử tự động (Pytest)
- `tests/test_te9c65e_uc03_filter.py`: **PASSED**
- `tests/test_map_markers_radius_popup.py`: **PASSED (5/5)**
- `tests/test_restaurant_multi_filter.py`: **PASSED (8/8)**
- `tests/test_restaurant_detail_api_ui.py`: **PASSED**
- `tests/test_performance_te9c67f.py`: **PASSED (Avg < 50ms << 3000ms, Error Rate = 0%)**

## 4. Kết luận nghiệm thu
Toàn bộ các chức năng thuộc **UC-03, UC-04, UC-09** đã đáp ứng đầy đủ yêu cầu chức năng (FR-06, FR-07, FR-09) và phi chức năng (NFR-01 < 3s, NFR-04 lỗi < 1%). Hệ thống đạt điều kiện nghiệm thu Sprint 4.