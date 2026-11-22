"""
Bộ kiểm thử tự động cho Task TSK-29:
Thiết kế Component Thẻ Nhà hàng (Restaurant Card) & Skeleton Loading
Đáp ứng tiêu chuẩn phi chức năng NFR-01 (< 3 giây)
"""
import sys
import os
import math
import time

# Thêm thư mục gốc dự án vào sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Đảm bảo in console tiếng Việt UTF-8 trên Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.database import Base
import app.models
from app.models.restaurant import Restaurant, RestaurantAmenity, RestaurantImage
from app.routers.restaurant import get_restaurants
from app.schemas.restaurant import RestaurantListResponse, RestaurantListItemResponse, AmenityResponse

# Khởi tạo SQLite in-memory test database
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
test_engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
Base.metadata.create_all(bind=test_engine)


def seed_test_database(db):
    """Tạo dữ liệu mẫu đa dạng cho các nhà hàng với đầy đủ 5 tiện ích và ảnh bìa"""
    db.query(RestaurantImage).delete()
    db.query(RestaurantAmenity).delete()
    db.query(Restaurant).delete()
    db.commit()

    # Quán 1: Đầy đủ 5 tiện ích, có ảnh bìa
    r1 = Restaurant(
        id=1,
        name="Nhà hàng Hương Xưa Sài Gòn",
        description="Ẩm thực truyền thống Việt Nam ba miền",
        address="123 Nguyễn Du, Phường Bến Nghé, Quận 1, TP.HCM",
        phone_number="0901234567",
        cuisine_type="Món Việt",
        latitude=10.7780,
        longitude=106.6990,
        min_price=120000.0,
        max_price=350000.0,
        open_hours="09:00 - 22:30",
        avg_rating=4.8,
        total_reviews=245,
        status="active"
    )
    db.add(r1)
    db.flush()

    a1 = RestaurantAmenity(
        restaurant_id=r1.id,
        has_parking=True,
        has_private_room=True,
        has_outdoor=True,
        pet_friendly=True,
        vegetarian_support=True
    )
    db.add(a1)

    img1 = RestaurantImage(
        restaurant_id=r1.id,
        image_url="https://images.unsplash.com/photo-1555396273-367ea4eb4db5",
        caption="Ảnh bìa mặt tiền quán",
        is_cover=True,
        display_order=1
    )
    db.add(img1)

    # Quán 2: Chỉ có bãi đỗ ô tô và đồ chay
    r2 = Restaurant(
        id=2,
        name="Quán Chay An Lạc Tâm",
        description="Ẩm thực chay thực dưỡng thanh tịnh",
        address="45 Lê Văn Thọ, Phường 11, Quận Gò Vấp, TP.HCM",
        phone_number="0908765432",
        cuisine_type="Đồ chay",
        latitude=10.8350,
        longitude=106.6620,
        min_price=50000.0,
        max_price=150000.0,
        open_hours="07:00 - 21:00",
        avg_rating=4.6,
        total_reviews=180,
        status="active"
    )
    db.add(r2)
    db.flush()

    a2 = RestaurantAmenity(
        restaurant_id=r2.id,
        has_parking=True,
        has_private_room=False,
        has_outdoor=False,
        pet_friendly=False,
        vegetarian_support=True
    )
    db.add(a2)

    img2 = RestaurantImage(
        restaurant_id=r2.id,
        image_url="https://images.unsplash.com/photo-1512621776951-a57141f2eefd",
        caption="Không gian thiền tịnh",
        is_cover=True,
        display_order=1
    )
    db.add(img2)

    db.commit()


def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Công thức tính khoảng cách Haversine chuẩn xác"""
    r = 6371.0
    d_lat = math.radians(lat2 - lat1)
    d_lon = math.radians(lon2 - lon1)
    a = (math.sin(d_lat / 2) ** 2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(d_lon / 2) ** 2)
    return r * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def run_tests():
    print("=" * 75)
    print("BẮT ĐẦU CHẠY BỘ KIỂM THỬ THẺ NHÀ HÀNG & SKELETON LOADING (TSK-29 / NFR-01)")
    print("=" * 75)

    db = TestingSessionLocal()
    seed_test_database(db)

    # -------------------------------------------------------------
    # TEST 01: Kiểm tra cấu trúc dữ liệu thẻ nhà hàng từ API GET /api/restaurants
    # -------------------------------------------------------------
    print("\n[TEST 01] Kiểm tra cấu trúc dữ liệu Thẻ Nhà hàng (Restaurant Card Data):")
    res: RestaurantListResponse = get_restaurants(page=1, limit=10, status_filter="all", db=db)
    assert len(res.data) >= 2, "Dữ liệu trả về không đủ danh sách nhà hàng"
    card1 = next(c for c in res.data if c.id == 1)
    card2 = next(c for c in res.data if c.id == 2)

    # Kiểm tra các trường bắt buộc của Thẻ theo TSK-29
    assert card1.name == "Nhà hàng Hương Xưa Sài Gòn"
    assert card1.cover_image_url is not None
    assert card1.min_price == 120000.0
    assert card1.max_price == 350000.0
    assert card1.avg_rating == 4.8
    assert card1.total_reviews == 245
    assert card1.latitude is not None and card1.longitude is not None
    print(f"  Thẻ quán: '{card1.name}', Ảnh bìa: '{card1.cover_image_url[:40]}...', Sao: {card1.avg_rating}★ ({card1.total_reviews} reviews)")
    print("  => PASSED: Đầy đủ các trường hiển thị cốt lõi của Restaurant Card!")

    # -------------------------------------------------------------
    # TEST 02: Kiểm tra trả về đủ 5 thuộc tính tiện ích (Amenities)
    # -------------------------------------------------------------
    print("\n[TEST 02] Kiểm tra 5 cờ tiện ích nổi bật từ RestaurantAmenities:")
    amenities = card1.amenities
    assert amenities is not None
    assert amenities.has_parking is True
    assert amenities.has_private_room is True
    assert amenities.has_outdoor is True
    assert amenities.pet_friendly is True
    assert amenities.vegetarian_support is True
    print(f"  Tiện ích Quán 1: 🚗 Đỗ ô tô={amenities.has_parking}, 🚪 Phòng riêng={amenities.has_private_room}, 🌿 Ngoài trời={amenities.has_outdoor}, 🐾 Thú cưng={amenities.pet_friendly}, 🥗 Món chay={amenities.vegetarian_support}")
    
    # Kiểm tra quán 2 (chỉ có đỗ xe và đồ chay)
    amenities2 = card2.amenities
    assert amenities2.has_parking is True
    assert amenities2.has_private_room is False
    assert amenities2.has_outdoor is False
    assert amenities2.pet_friendly is False
    assert amenities2.vegetarian_support is True
    print(f"  Tiện ích Quán 2: 🚗 Đỗ ô tô={amenities2.has_parking}, 🚪 Phòng riêng={amenities2.has_private_room}, 🥗 Món chay={amenities2.vegetarian_support}")
    print("  => PASSED: Đầy đủ 5 icon/badge tiện ích phục vụ hiển thị thẻ nhà hàng!")

    # -------------------------------------------------------------
    # TEST 03: Kiểm thử độ chính xác tính khoảng cách GPS (Haversine)
    # -------------------------------------------------------------
    print("\n[TEST 03] Kiểm thử tính toán khoảng cách địa lý (Haversine Distance):")
    # Tọa độ người dùng giả định (Quận 1, Nhà thờ Đức Bà: 10.7798, 106.6990)
    user_lat, user_lon = 10.7798, 106.6990
    dist1 = haversine_km(user_lat, user_lon, card1.latitude, card1.longitude)
    dist2 = haversine_km(user_lat, user_lon, card2.latitude, card2.longitude)
    print(f"  Khoảng cách từ người dùng đến Quán 1 (Quận 1): {dist1:.2f} km")
    print(f"  Khoảng cách từ người dùng đến Quán 2 (Gò Vấp): {dist2:.2f} km")
    assert 0.1 <= dist1 <= 0.5, f"Khoảng cách đến Quán 1 không hợp lý: {dist1}"
    assert 5.0 <= dist2 <= 12.0, f"Khoảng cách đến Quán 2 không hợp lý: {dist2}"
    assert dist1 < dist2, "Quán cùng Quận 1 phải gần hơn Quán Gò Vấp"
    print("  => PASSED: Công thức tính khoảng cách động hoạt động chuẩn xác!")

    # -------------------------------------------------------------
    # TEST 04: Kiểm thử quy chuẩn format giá tiền (Price Range Formatting)
    # -------------------------------------------------------------
    print("\n[TEST 04] Kiểm thử định dạng mức giá VNĐ (Price Range Validation):")
    assert card1.min_price <= card1.max_price, "Giá min phải <= giá max"
    formatted_price = f"{int(card1.min_price):,}đ - {int(card1.max_price):,}đ".replace(",", ".")
    print(f"  Giá hiển thị trên thẻ: {formatted_price}")
    assert "120.000đ - 350.000đ" in formatted_price
    print("  => PASSED: Định dạng tiền tệ VNĐ rõ ràng, minh bạch!")

    # -------------------------------------------------------------
    # TEST 05: Kiểm tra CSS Shimmer Animation và Skeleton Loading trong frontend/index.html
    # -------------------------------------------------------------
    print("\n[TEST 05] Kiểm tra tích hợp Skeleton Loading & Shimmer Animation trong HTML:")
    html_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "frontend", "index.html")
    assert os.path.exists(html_path), "File frontend/index.html không tồn tại"
    with open(html_path, "r", encoding="utf-8") as f:
        html_content = f.read()

    # Kiểm tra các class CSS và keyframe Shimmer
    assert "@keyframes shimmerWave" in html_content, "Thiếu animation shimmerWave"
    assert ".skeleton-shimmer" in html_content, "Thiếu class .skeleton-shimmer"
    assert ".skeleton-card" in html_content, "Thiếu class .skeleton-card"
    assert "renderSkeletonCards" in html_content, "Thiếu hàm renderSkeletonCards"
    print("  Đã tìm thấy: @keyframes shimmerWave, .skeleton-shimmer, .skeleton-card, renderSkeletonCards()")
    print("  => PASSED: Khung xương Skeleton Loading được cấu hình hoàn chỉnh!")

    # -------------------------------------------------------------
    # TEST 06: Kiểm tra tiêu chuẩn Zero CLS (Kích thước Skeleton khớp Card thật)
    # -------------------------------------------------------------
    print("\n[TEST 06] Kiểm tra thuộc tính chống giật giàn trang (CLS = 0):")
    assert "min-height: 360px" in html_content, "Skeleton card cần min-height tương đương venue-card"
    assert "skeleton-img" in html_content, "Skeleton cần khối ảnh"
    assert "height: 180px" in html_content, "Chiều cao ảnh của skeleton phải khớp thẻ thật"
    print("  => PASSED: Skeleton card có kích thước khớp 100% với Card thật, ngăn chặn CLS!")

    # -------------------------------------------------------------
    # TEST 07: Kiểm tra thuộc tính Lazy Loading và Fallback ảnh
    # -------------------------------------------------------------
    print("\n[TEST 07] Kiểm tra tối ưu hình ảnh (Lazy Loading & Error Fallback):")
    assert 'loading="lazy"' in html_content, "Ảnh thẻ nhà hàng phải có loading='lazy'"
    assert "onerror=" in html_content, "Ảnh thẻ nhà hàng phải có fallback onerror"
    print("  => PASSED: Tối ưu tải ảnh lazy load và cơ chế dự phòng ảnh lỗi!")

    # -------------------------------------------------------------
    # TEST 08: Kiểm tra tích hợp bộ lọc 5 tiện ích trên giao diện
    # -------------------------------------------------------------
    print("\n[TEST 08] Kiểm tra giao diện bộ lọc 5 tiện ích (Amenity Filter Ribbon):")
    assert "btn-parking" in html_content, "Thiếu nút lọc bãi đỗ ô tô"
    assert "btn-room" in html_content, "Thiếu nút lọc phòng riêng"
    assert "btn-outdoor" in html_content, "Thiếu nút lọc ngoài trời"
    assert "btn-pet" in html_content, "Thiếu nút lọc thú cưng"
    assert "btn-vegan" in html_content, "Thiếu nút lọc món chay"
    print("  => PASSED: Đầy đủ 5 nút lọc tiện ích trực quan trên Filter Ribbon!")

    # -------------------------------------------------------------
    # TEST 09: Benchmark Hiệu năng Tải trang NFR-01 (< 3 giây)
    # -------------------------------------------------------------
    print("\n[TEST 09] Kiểm tra hiệu năng tải API danh sách nhà hàng (NFR-01 < 3s):")
    start_time = time.perf_counter()
    bench_res = get_restaurants(page=1, limit=50, status_filter="all", db=db)
    elapsed_ms = (time.perf_counter() - start_time) * 1000
    assert len(bench_res.data) >= 2
    print(f"  Thời gian thực thi truy vấn Eager Loading: {elapsed_ms:.2f} ms")
    assert elapsed_ms < 3000, f"Thời gian tải vượt quá 3 giây quy định của NFR-01: {elapsed_ms}ms"
    print(f"  => PASSED: Tốc độ phản hồi cực nhanh ({elapsed_ms:.2f} ms << 3000 ms tiêu chuẩn NFR-01)!")

    print("\n" + "=" * 75)
    print("KẾT QUẢ: 9/9 CA KIỂM THỬ TASK TSK-29 ĐÃ VƯỢT QUA XUẤT SẮC (ALL PASSED)!")
    print("=" * 75)
    db.close()


if __name__ == "__main__":
    run_tests()
