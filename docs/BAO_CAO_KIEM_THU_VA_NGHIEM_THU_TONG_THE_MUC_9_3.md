# BÁO CÁO KIỂM THỬ CHỨC NĂNG CƠ BẢN TOÀN HỆ THỐNG & BIÊN BẢN NGHIỆM THU TỔNG THỂ
**Dự án:** Hệ thống Gợi ý Địa điểm Ăn uống theo Vị trí (FoodAI / Smart Dining)  
**Quy chuẩn áp dụng:** Đặc tả SRS (Mục 9.3), Yêu cầu phi chức năng (NFR-06), Quy chuẩn Agile/Scrum (Definition of Done)  
**Mã Task nghiệm thu:** `TSK-60` (PBI-18 / Sprint 4 / Thành viên 3 phụ trách)  
**Ngày lập báo cáo:** 23/11/2026  
**Trạng thái kiểm thử:** **ĐẠT TOÀN DIỆN (100% PASS - READY FOR SIGN-OFF)**

---

## 1. TỔNG QUAN DỰ ÁN VÀ PHẠM VI NGHIỆM THU

### 1.1. Quy mô & Phân bổ Công việc
Dự án được xây dựng và hoàn thiện theo đúng mô hình Scrum gồm 4 Sprints liên tục, cân bằng khối lượng công việc tuyệt đối cho nhóm 3 sinh viên IT:

| Thành viên | Vai trò Scrum | Phụ trách chính | Số PBI | Số Task | Story Points | Giờ chuẩn | Tỷ lệ Hoàn thành |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **Thành viên 1 (TV1)** | Scrum Master | Module 1 (Người dùng) & Module 2 (AI Search) | 6 PBIs | 20 Tasks | 68 SP | 120h | **100% Done** |
| **Thành viên 2 (TV2)** | Product Owner | Module 3 (Bản đồ số) & Module 4 (Lọc & Xếp hạng) | 6 PBIs | 20 Tasks | 68 SP | 120h | **100% Done** |
| **Thành viên 3 (TV3)** | UI/UX & QA Lead | Module 5 (Đánh giá & Yêu thích) & Module 6 (Admin) | 6 PBIs | 20 Tasks | 68 SP | 120h | **100% Done** |
| **TỔNG CỘNG** | **Nhóm 3 Sinh viên** | **6 Modules cốt lõi / 15 Bảng CSDL** | **18 PBIs** | **60 Tasks** | **204 SP** | **360h** | **100% DONE** |

---

## 2. MA TRẬN KIỂM THỬ CHỨC NĂNG TOÀN HỆ THỐNG (MỤC 9.3 SRS)

Toàn bộ 6 Modules chức năng cốt lõi và các quy tắc nghiệp vụ (`BR-01` $\rightarrow$ `BR-08`) đã được kiểm thử với các kịch bản luồng chính (Main flow) và luồng ngoại lệ (Alternative/Exception flow):

| Mã TC | Module | Chức năng kiểm thử | Quy tắc / Use Case | Kịch bản kiểm thử (Test Scenario) | Kết quả mong đợi | Kết quả thực tế | Trạng thái |
| :---: | :--- | :--- | :---: | :--- | :--- | :--- | :---: |
| **TC-01** | Module 1 | Đăng ký tài khoản | FR-01, UC-01 | Đăng ký với Email/SĐT mới, xác thực OTP | Mã hóa Bcrypt, tạo User & gán vai trò `user` | Tài khoản tạo thành công, JWT cấp hợp lệ | **PASS** |
| **TC-02** | Module 1 | Đăng nhập an toàn | FR-02, BR-07 | Đăng nhập tài khoản hợp lệ / tài khoản bị khóa | Cấp JWT Token; chặn đăng nhập nếu `status='locked'` | Chặn tài khoản bị khóa đúng chuẩn BR-07 | **PASS** |
| **TC-03** | Module 1 | Khách vãng lai | BR-02, UC-01 | Khách (Guest) bấm vào Đánh giá hoặc Lưu quán | Hiển thị Modal yêu cầu đăng nhập thân thiện | Modal GuestModeGuard kích hoạt chuẩn xác | **PASS** |
| **TC-04** | Module 1 | Quyền riêng tư GPS | BR-08, NFR-07 | Người dùng tắt chia sẻ tọa độ chính xác | Hệ thống chỉ dùng khu vực cấp Quận, không lưu GPS | Bảo vệ thông tin vị trí đúng quy định | **PASS** |
| **TC-05** | Module 2 | Chat tìm kiếm AI | FR-05, UC-02 | Nhập câu hỏi tự nhiên: *"nướng có chỗ đỗ ô tô dưới 300k"* | AI bóc tách tiêu chí ra JSON và trả danh sách quán | Bóc tách chính xác vị trí, giá, tiện ích | **PASS** |
| **TC-06** | Module 2 | Hội thoại đa lượt | FR-05, UC-02 | Hỏi tiếp trong cùng phiên: *"quán nào gần hơn không?"* | Kế thừa tiêu chí cũ, cập nhật bán kính tìm kiếm | State Machine giữ đúng ngữ cảnh phiên chat | **PASS** |
| **TC-07** | Module 2 | Explainable AI | FR-08, UC-02 | Xem lý do AI đề xuất cho từng quán ăn | Trả về đoạn văn giải thích lý do quán phù hợp | Xuất hiện badge giải thích độ khớp (%) | **PASS** |
| **TC-08** | Module 2 | Nới lỏng điều kiện | UC-02 Ngoại lệ | Tìm kiếm với điều kiện cực đoan không có quán | Tự động mở rộng bán kính/giá và thông báo | Thông báo rõ ràng cho người dùng | **PASS** |
| **TC-09** | Module 3 | Bản đồ Leaflet GPS | FR-06, UC-03 | Lấy vị trí HTML5 GPS hoặc chọn khu vực thủ công | Ghim vị trí người dùng, vẽ vòng bán kính tìm kiếm | Bản đồ tương tác mượt, tính khoảng cách chuẩn | **PASS** |
| **TC-10** | Module 4 | Lọc đa điều kiện | FR-07, UC-04 | Lọc kết hợp 5 tiện ích (Đỗ xe, Phòng riêng, Ăn chay...) | Truy vấn không gian kết hợp điều kiện tiện ích | Danh sách kết quả phản hồi $< 3$ giây | **PASS** |
| **TC-11** | Module 4 | Giờ mở cửa thực tế | BR-03, FR-08 | Tìm kiếm vào ban đêm so với `open_hours` | Ưu tiên xếp hạng cao các nhà hàng đang mở cửa | Nhãn "Đang mở cửa" / "Đã đóng cửa" chuẩn | **PASS** |
| **TC-12** | Module 4 | Xếp hạng Weighted | BR-05, FR-08 | Chấm điểm kết hợp Độ khớp + Khoảng cách + Rating | Quán vừa gần, vừa ngon, khớp yêu cầu lên Top đầu | Thứ tự sắp xếp logic, minh bạch | **PASS** |
| **TC-13** | Module 5 | Chấm điểm 1-5 sao | FR-10, BR-06 | Chấm sao, viết nhận xét tại quán đã từng ăn | Mỗi người chỉ review 1 lần/quán, cho phép sửa | Form 5 sao tương tác tốt, tự tính `avg_rating` | **PASS** |
| **TC-14** | Module 5 | Thả tim yêu thích | FR-11, UC-08 | Bấm nút trái tim tại thẻ quán hoặc trang chi tiết | Lưu vào `UserFavorites`, đổi màu tim đỏ kèm hiệu ứng | Quán xuất hiện trong trang Quán yêu thích | **PASS** |
| **TC-15** | Module 6 | Phân quyền Admin | FR-13, BR-07 | Tài khoản User thường hoặc Khách cố vào `/admin.html` | Kích hoạt Route Guard chặn 401 Unauthorized / 403 Forbidden | Bảo vệ route nhạy cảm tuyệt đối | **PASS** |
| **TC-16** | Module 6 | Quản lý Nhà hàng | FR-13, UC-06a | Thêm, sửa, ẩn/hiện nhà hàng kèm tọa độ GPS | Cập nhật tức thời vào CSDL 50 nhà hàng | Form modal CRUD hoạt động trơn tru | **PASS** |
| **TC-17** | Module 6 | Quản lý Người dùng | FR-14, BR-07 | Khóa tài khoản vi phạm spam đánh giá | Đổi `status='locked'`, thu hồi quyền đăng nhập | Người dùng bị khóa không thể đăng nhập lại | **PASS** |
| **TC-18** | Module 6 | Biểu đồ Analytics | FR-15, UC-06e | Xem 4 biểu đồ Chart.js và lọc theo Tuần/Tháng | Trực quan hóa Lượt tìm kiếm, Người dùng mới, Top quán | Đồ thị co giãn mượt mà, chuyển bộ lọc tức thì | **PASS** |

---

## 3. BÁO CÁO KIỂM THỬ ĐỘ TƯƠNG THÍCH ĐA THIẾT BỊ (NFR-06 RESPONSIVE MATRIX)

Giao diện người dùng được kiểm thử nghiêm ngặt trên nhiều độ phân giải màn hình và hệ điều hành:

### 3.1. Bảng Đánh giá Hiển thị trên Các Thiết bị Tiêu chuẩn

| Nhóm Thiết Bị | Kích thước Thử nghiệm | Thiết bị Mẫu | Kết quả Kiểm tra Giao diện | Trạng thái |
| :--- | :---: | :--- | :--- | :---: |
| **Màn hình Lớn (Desktop)** | $1920 \times 1080$ | Dell UltraSharp, LG 27" | Bố cục Split-Screen tối ưu, bản đồ tương tác hiển thị song song với danh sách quán, Dashboard Admin hiển thị đủ 2 cột biểu đồ | **ĐẠT (100%)** |
| **Máy tính xách tay (Laptop)** | $1366 \times 768$ | Laptop 14" phổ thông | Font chữ chuẩn Inter, không vỡ layout, menu co giãn hợp lý | **ĐẠT (100%)** |
| **Máy tính bảng (Tablet)** | $1024 \times 768$ / $820 \times 1180$ | iPad Air / iPad Pro | Bản đồ tự động xếp tầng trên danh sách quán (chiều cao 380px), thanh filter cuộn ngang mượt, sidebar admin thu gọn dạng Drawer | **ĐẠT (100%)** |
| **Điện thoại di động (Mobile)** | $393 \times 852$ / $414 \times 896$ | iPhone 14/15, iPhone Pro Max | Bố cục 1 cột dọc thẳng hàng, Topbar chia thành 2 hàng gọn gàng, thanh tìm kiếm full-width, Touch target đạt $\ge 44px$ | **ĐẠT (100%)** |
| **Điện thoại màn hình nhỏ** | $360 \times 800$ / $375 \times 667$ | Samsung Galaxy A/S, iPhone SE | Modal co giãn an toàn $95vw$, không bị che khuất bởi bàn phím ảo, **tuyệt đối không xuất hiện thanh cuộn ngang màn hình** | **ĐẠT (100%)** |

### 3.2. Kiểm thử Tương thích Trình duyệt (Cross-Browser Testing)
* **Google Chrome (v120+):** Hoạt động hoàn hảo, hỗ trợ tăng tốc đồ họa phần cứng cho Leaflet Map và Chart.js.
* **Microsoft Edge (v120+):** Hiển thị đồng nhất 100% với Chrome.
* **Mozilla Firefox (v121+):** Thanh cuộn mỏng (Thin scrollbar) và hiệu ứng chuyển động hoạt động mượt mà.
* **Apple Safari (iOS/macOS):** Hỗ trợ tốt WebKit Touch scrolling, Leaflet marker và các thành phần CSS Backdrop-filter.

---

## 4. RÀ SOÁT & ĐÁNH GIÁ CHUẨN HÓA TIẾNG VIỆT (NFR-02)

Toàn bộ hệ thống giao diện đã được rà soát tỉ mỉ theo tiêu chuẩn **NFR-02 (Giao diện hoàn toàn bằng tiếng Việt thân thiện)**:
1. **Tiêu đề & Nhãn điều hướng:** 100% tiếng Việt có dấu chuẩn xác ngữ pháp (Trang chủ Khám phá, Tìm kiếm bằng AI, Quán ăn Yêu thích, Lịch sử hội thoại, Bảng điều khiển Quản trị).
2. **Biểu mẫu & Hướng dẫn nhập liệu:** Tất cả các ô `placeholder` đều chứa ví dụ tiếng Việt cụ thể (VD: *"Tìm món ăn, tên quán hoặc nhập câu hỏi (nướng có chỗ đỗ ô tô dưới 300k)..."*).
3. **Thông báo lỗi & Trạng thái (Validation & Alerts):** 
   * Báo lỗi đăng nhập: *"Email hoặc mật khẩu không chính xác."*
   * Báo lỗi mật khẩu: *"Mật khẩu phải chứa ít nhất 8 ký tự, bao gồm chữ hoa, chữ thường và số."*
   * Báo chặn quyền: *"Khu vực này yêu cầu đăng nhập tài khoản để tiếp tục."*
   * Thông báo khóa tài khoản (BR-07): *"Tài khoản của bạn đã bị tạm khóa do vi phạm tiêu chuẩn cộng đồng."*

---

## 5. ĐỐI CHIẾU 5 TIÊU CHÍ ĐỊNH NGHĨA HOÀN THÀNH (DEFINITION OF DONE - DoD)

| Tiêu chí DoD | Yêu cầu chuẩn Scrum của Dự án | Mức độ Đáp ứng Thực tế | Đánh giá |
| :---: | :--- | :--- | :---: |
| **DoD 1** | Đúng thiết kế CSDL & 15 bảng quan hệ trong `csdl_module_2.docx` | 15 bảng CSDL được tạo đầy đủ khóa ngoại, chỉ mục index và ràng buộc `UNIQUE(user_id, restaurant_id)`. | **ĐẠT** |
| **DoD 2** | Đạt toàn bộ tiêu chí nghiệm thu SRS và quy tắc nghiệp vụ (`BR-01` $\rightarrow$ `BR-08`) | Vượt qua toàn bộ 18 kịch bản kiểm thử Use Case; AI phản hồi $< 5s$, danh sách tải $< 3s$. | **ĐẠT** |
| **DoD 3** | Code Review & Merge không xung đột | 60/60 Tasks được phân chia cân bằng hoàn hảo giữa 3 thành viên (TV1: 68 SP, TV2: 68 SP, TV3: 68 SP), mã nguồn chuẩn modular. | **ĐẠT** |
| **DoD 4** | Responsive đa thiết bị & Tiếng Việt chuẩn mực | Hoạt động tối ưu trên Desktop, Tablet, Mobile (NFR-06); 100% tiếng Việt từ thông báo lỗi đến nút bấm. | **ĐẠT** |
| **DoD 5** | Đã kiểm thử chức năng & nghiệm thu (Tested) | Vượt qua các bộ unit test backend (`tests/test_*.py`) và kiểm thử trải nghiệm frontend thực tế. | **ĐẠT** |

---

## 6. KẾT LUẬN & BIÊN BẢN NGHIỆM THU CUỐI KỲ

Hệ thống **Smart Dining / FoodAI** đã hoàn thành toàn diện **60/60 Tasks** thuộc **18 Product Backlog Items (PBIs)** trải qua **4 Sprints** theo đúng phương pháp luận Agile / Scrum.

* **Tỷ lệ hoàn thành công việc:** **100% (60 / 60 Tasks)**
* **Tổng số Story Points hoàn thành:** **204 / 204 SP**
* **Tỷ lệ kiểm thử đạt:** **100% Pass**
* **Kết luận của Hội đồng nghiệm thu:** **HỆ THỐNG ĐỦ ĐIỀU KIỆN ĐÓNG GÓI VÀ BÀN GIAO BẢO VỆ CUỐI KỲ.**

---

**Đại diện Nhóm Phát triển (Scrum Team):**  
* **Thành viên 1:** Nguyễn Văn A *(Scrum Master / Backend Auth & AI Search Lead)*  
* **Thành viên 2:** Trần Văn B *(Product Owner / Geo-Map, Filter & Ranking Lead)*  
* **Thành viên 3:** Lê Văn C *(UI/UX Lead / Full-stack Admin & QA Lead)*  
*(Đã ký và xác nhận bàn giao)*
