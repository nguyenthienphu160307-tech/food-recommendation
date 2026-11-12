import sys
import os

# Thêm thư mục gốc dự án vào sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Đảm bảo console Windows in tiếng Việt UTF-8 không bị lỗi charmap
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from fastapi.testclient import TestClient
from app.main import app
from app.core.database import SessionLocal
from app.models.restaurant import Restaurant, RestaurantAmenity, RestaurantImage

client = TestClient(app)


def seed_sample_restaurants():
    """Tạo dữ liệu mẫu phục vụ kiểm thử API danh sách nhà hàng"""
    db = SessionLocal()
    # Kiểm tra nếu chưa có nhà hàng thì tạo mẫu 3 quán
    if db.query(Restaurant).count() == 0:
        r1 = Restaurant(
            name="Nhà hàng Cơm Niêu Sài Gòn",
            description="Đặc sản cơm niêu truyền thống Việt Nam",
            address="27 Tú Xương, Phường Võ Thị Sáu, Quận 3, TP.HCM",
            phone_number="02839326342",
            cuisine_type="Món Việt",
            latitude=10.7783,
            longitude=106.6872,
            min_price=100000.0,
            max_price=300000.0,
            open_hours="10:00 - 22:00",
            avg_rating=4.5,
            total_reviews=120,
            status="active"
        )
        db.add(r1)
        db.flush()

        # Thêm tiện ích cho quán 1
        a1 = RestaurantAmenity(
            restaurant_id=r1.id,
            has_parking=True,
            has_private_room=True,
            has_outdoor=False,
            pet_friendly=False,
            vegetarian_support=True
        )
        db.add(a1)

        # Thêm ảnh cho quán 1 (1 ảnh bìa, 1 ảnh thường)
        img1 = RestaurantImage(
            restaurant_id=r1.id,
            image_url="https://images.unsplash.com/photo-1555396273-367ea4eb4db5",
            caption="Không gian ấm cúng",
            is_cover=True,
            display_order=1
        )
        img2 = RestaurantImage(
            restaurant_id=r1.id,
            image_url="https://images.unsplash.com/photo-1517248135467-4c7edcad34c4",
            caption="Bàn ăn gia đình",
            is_cover=False,
            display_order=2
        )
        db.add_all([img1, img2])

        # Quán 2
        r2 = Restaurant(
            name="Lẩu Nướng Hàn Quốc Gogi",
            description="Thịt nướng sốt đậm đà chuẩn vị Seoul",
            address="189 Nguyễn Tri Phương, Quận 5, TP.HCM",
            phone_number="02838338338",
            cuisine_type="Lẩu Nướng",
            latitude=10.7554,
            longitude=106.6678,
            min_price=250000.0,
            max_price=500000.0,
            open_hours="11:00 - 23:00",
            avg_rating=4.8,
            total_reviews=250,
            status="active"
        )
        db.add(r2)
        db.flush()

        a2 = RestaurantAmenity(
            restaurant_id=r2.id,
            has_parking=True,
            has_private_room=False,
            has_outdoor=True,
            pet_friendly=True,
            vegetarian_support=False
        )
        db.add(a2)

        img3 = RestaurantImage(
            restaurant_id=r2.id,
            image_url="https://images.unsplash.com/photo-1544025162-d76694265947",
            caption="Thịt nướng xèo xèo",
            is_cover=True,
            display_order=1
        )
        db.add(img3)

        # Quán 3
        r3 = Restaurant(
            name="Quán Chay Thanh Tịnh",
            description="Món chay thanh đạm từ rau củ hữu cơ",
            address="45 Đinh Tiên Hoàng, Quận 1, TP.HCM",
            phone_number="02838229988",
            cuisine_type="Món Chay",
            latitude=10.7891,
            longitude=106.6995,
            min_price=50000.0,
            max_price=150000.0,
            open_hours="07:00 - 21:00",
            avg_rating=4.2,
            total_reviews=85,
            status="active"
        )
        db.add(r3)
        db.flush()

        a3 = RestaurantAmenity(
            restaurant_id=r3.id,
            has_parking=False,
            has_private_room=False,
            has_outdoor=False,
            pet_friendly=False,
            vegetarian_support=True
        )
        db.add(a3)

        img4 = RestaurantImage(
            restaurant_id=r3.id,
            image_url="https://images.unsplash.com/photo-1540420773420-3366772f4999",
            caption="Không gian thanh tịnh",
            is_cover=True,
            display_order=1
        )
        db.add(img4)

        db.commit()
    # Đảm bảo quán 3 cũng có ảnh nếu đã seed từ trước
    r3 = db.query(Restaurant).filter(Restaurant.name == "Quán Chay Thanh Tịnh").first()
    if r3 and not db.query(RestaurantImage).filter(RestaurantImage.restaurant_id == r3.id).first():
        img_r3 = RestaurantImage(
            restaurant_id=r3.id,
            image_url="https://images.unsplash.com/photo-1540420773420-3366772f4999",
            caption="Không gian thanh tịnh",
            is_cover=True,
            display_order=1
        )
        db.add(img_r3)
        db.commit()

    db.close()


def run_tests():
    print("--- [BƯỚC 1] Khởi tạo dữ liệu mẫu nếu bảng nhà hàng đang trống ---")
    seed_sample_restaurants()

    print("\n--- [TEST 1] Gọi API lấy danh sách mặc định (page=1, limit=10) ---")
    res1 = client.get("/api/restaurants")
    print("Response status:", res1.status_code)
    data1 = res1.json()
    assert res1.status_code == 200, f"Expected 200, got {res1.status_code}"
    assert "data" in data1
    assert "pagination" in data1
    print("Số lượng nhà hàng trả về:", len(data1["data"]))
    print("Thông tin phân trang:", data1["pagination"])
    assert data1["pagination"]["page"] == 1
    assert data1["pagination"]["total_items"] >= 3

    print("\n--- [TEST 2] Kiểm tra ảnh bìa (is_cover=True) và cờ tiện ích (amenities) ---")
    first_restaurant = data1["data"][0]
    print(f"Nhà hàng đầu tiên: {first_restaurant['name']}")
    print(f"Ảnh bìa: {first_restaurant['cover_image_url']}")
    print(f"Tiện ích: {first_restaurant['amenities']}")
    assert first_restaurant["cover_image_url"] is not None
    assert first_restaurant["amenities"] is not None
    assert "has_parking" in first_restaurant["amenities"]

    print("\n--- [TEST 3] Kiểm tra phân trang với limit=2 (Trang 1 và Trang 2) ---")
    res_page1 = client.get("/api/restaurants?page=1&limit=2")
    data_page1 = res_page1.json()
    assert res_page1.status_code == 200
    assert len(data_page1["data"]) == 2
    assert data_page1["pagination"]["total_pages"] >= 2
    assert data_page1["pagination"]["limit"] == 2

    res_page2 = client.get("/api/restaurants?page=2&limit=2")
    data_page2 = res_page2.json()
    assert res_page2.status_code == 200
    assert data_page2["pagination"]["page"] == 2
    # ID của trang 2 phải khác trang 1
    id_page1 = [x["id"] for x in data_page1["data"]]
    id_page2 = [x["id"] for x in data_page2["data"]]
    assert set(id_page1).isdisjoint(set(id_page2)), "Các mục ở trang 1 và trang 2 không được trùng nhau"
    print("-> Phân trang hoạt động hoàn hảo, không bị trùng lặp dữ liệu giữa các trang!")

    print("\n--- [TEST 4] Kiểm tra validation khi truyền page không hợp lệ (page=0) ---")
    res_invalid = client.get("/api/restaurants?page=0")
    print("Response status:", res_invalid.status_code)
    assert res_invalid.status_code == 422, f"Expected 422 validation error, got {res_invalid.status_code}"
    print("-> FastAPI Pydantic đã chặn đúng tham số không hợp lệ (HTTP 422)!")

    print("\n>>> TẤT CẢ CÁC CA KIỂM THỬ TASK TSK-09 ĐỀU ĐẠT CHUẨN (ALL TESTS PASSED)! <<<")


if __name__ == "__main__":
    run_tests()
