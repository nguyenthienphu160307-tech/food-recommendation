# HƯỚNG DẪN CÀI ĐẶT & TÀI LIỆU BÀN GIAO HỆ THỐNG SMART DINING 

## 1. Tổng quan dự án
**Smart Dining (Food Recommendation)** là hệ thống gợi ý địa điểm ăn uống theo vị trí địa lý (GPS/Haversine) kết hợp Trợ lý AI (NLP/LLM & Fallback Parser), bản đồ tương tác Leaflet và thuật toán xếp hạng đa tiêu chí (Ranking Engine BR-06).

## Cách tải mã nguồn
1. Tải mã nguồn nhánh `main`:
   ```bash
   git clone -b main [https://github.com/nguyenthienphu160307-tech/food-recommendation.git](https://github.com/nguyenthienphu160307-tech/food-recommendation.git)
   cd food-recommendation
### Cấu trúc thư mục chính
- `app/`: Mã nguồn Backend FastAPI (chia theo `core/`, `models/`, `routers/`, `schemas/`, `services/`).
- `frontend/`: Giao diện người dùng & trang quản trị Admin (HTML5, CSS3, Vanilla JS, Leaflet.js).
- `database/`: Script khởi tạo bảng SQL (`init_db.sql`), migration (`migrate_te9c654.py`) và dữ liệu mẫu (`seed_restaurants.py`, `seed_restaurants.sql`).
- `tests/`: Bộ kiểm thử tự động Pytest (bao gồm bộ 50 kịch bản NLP tiếng Việt `test_nlp_50_scenarios.py`).
- `docs/`: Tài liệu SRS, sơ đồ kiến trúc, ERD, Sequence Diagram và tài liệu bàn giao này.

---

## 2. Yêu cầu môi trường
- **Python:** 3.10 trở lên (khuyến nghị Python 3.11).
- **Cơ sở dữ liệu:** SQLite (tích hợp sẵn, chạy ngay) hoặc MySQL 8.0 (qua XAMPP hoặc Docker).
- **Công cụ tùy chọn:** Git, Docker Desktop, XAMPP.

---

## 3. Cấu hình biến môi trường (`.env`)
Sao chép file mẫu `.env.example` thành `.env`:
```bash
copy .env.example .env   # Trên Windows
cp .env.example .env     # Trên Linux/macOS