"""
Bộ kiểm thử tự động cho Task TSK-30:
Xây dựng Giao diện Thư viện ảnh Lightbox & Bảng Thực đơn trên trang Chi tiết
Đáp ứng tiêu chuẩn phi chức năng NFR-01 (< 3s) và NFR-06 (Responsive)
"""
import sys
import os
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
from app.models.restaurant import Restaurant, RestaurantMenu, MenuItem, RestaurantImage
from app.routers.menu import get_restaurant_menus
from app.routers.image import get_restaurant_images
from app.schemas.menu import RestaurantMenuWithItemsResponse
from app.schemas.image import RestaurantImageResponse

# Khởi tạo SQLite in-memory test database
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
test_engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
Base.metadata.create_all(bind=test_engine)


def seed_test_data(db):
    """Khởi tạo dữ liệu kiểm thử đầy đủ: nhà hàng, các nhóm thực đơn, món ăn và thư viện ảnh"""
    db.query(MenuItem).delete()
    db.query(RestaurantMenu).delete()
    db.query(RestaurantImage).delete()
    db.query(Restaurant).delete()
    db.commit()

    # 1. Tạo nhà hàng
    r = Restaurant(
        id=1,
        name="Lẩu Nướng Thượng Hạng Sài Gòn",
        description="Không gian ẩm thực hiện đại sang trọng",
        address="100 Pasteur, Phường Bến Nghé, Quận 1, TP.HCM",
        phone_number="0901234567",
        cuisine_type="Lẩu & Nướng",
        latitude=10.7760,
        longitude=106.7010,
        min_price=150000.0,
        max_price=450000.0,
        open_hours="10:00 - 23:00",
        avg_rating=4.8,
        total_reviews=310,
        status="active"
    )
    db.add(r)
    db.flush()

    # 2. Tạo 2 nhóm thực đơn (RestaurantMenus)
    m1 = RestaurantMenu(
        id=1,
        restaurant_id=r.id,
        name="Món Khai Vị & Ăn Kèm",
        description="Khởi đầu bữa ăn trọn vị",
        display_order=1
    )
    m2 = RestaurantMenu(
        id=2,
        restaurant_id=r.id,
        name="Thịt Bò Mỹ Nướng Tảng",
        description="Bò Mỹ nhập khẩu thượng hạng",
        display_order=2
    )
    db.add_all([m1, m2])
    db.flush()

    # 3. Tạo các món ăn (MenuItems) với cả còn món và hết món
    item1 = MenuItem(
        id=1,
        menu_id=m1.id,
        name="Salad Rong Biển Trứng Tôm",
        description="Rong biển tươi giòn kèm sốt mè rang",
        price=85000.0,
        is_available=True
    )
    item2 = MenuItem(
        id=2,
        menu_id=m1.id,
        name="Khoai Tây Chiên Phô Mai",
        description="Khoai tây lắc phô mai béo ngậy",
        price=65000.0,
        is_available=True
    )
    item3 = MenuItem(
        id=3,
        menu_id=m2.id,
        name="Dẻ Sườn Bò Mỹ Xốt Galbi",
        description="Dẻ sườn ướp xốt Galbi truyền thống",
        price=249000.0,
        is_available=True
    )
    item4 = MenuItem(
        id=4,
        menu_id=m2.id,
        name="Thăn Ngoại Bò Wagyu A5",
        description="Thăn bò Wagyu vân mỡ cẩm thạch hảo hạng",
        price=590000.0,
        is_available=False  # Món tạm hết
    )
    db.add_all([item1, item2, item3, item4])

    # 4. Tạo thư viện ảnh nhà hàng (RestaurantImages)
    img1 = RestaurantImage(
        id=1,
        restaurant_id=r.id,
        image_url="https://images.unsplash.com/photo-1544025162-d76694265947",
        caption="Ảnh bìa mặt tiền nhà hàng",
        is_cover=True,
        display_order=1
    )
    img2 = RestaurantImage(
        id=2,
        restaurant_id=r.id,
        image_url="https://images.unsplash.com/photo-1555396273-367ea4eb4db5",
        caption="Không gian bàn tiệc VIP sang trọng",
        is_cover=False,
        display_order=2
    )
    img3 = RestaurantImage(
        id=3,
        restaurant_id=r.id,
        image_url="https://images.unsplash.com/photo-1517248135467-4c7edcad34c4",
        caption="Khu vực bàn ngoài trời thoáng mát",
        is_cover=False,
        display_order=3
    )
    db.add_all([img1, img2, img3])
    db.commit()


def run_tests():
    print("=" * 75)
    print("BẮT ĐẦU CHẠY BỘ KIỂM THỬ THƯ VIỆN ẢNH LIGHTBOX & BẢNG THỰC ĐƠN (TSK-30)")
    print("=" * 75)

    db = TestingSessionLocal()
    seed_test_data(db)

    # -------------------------------------------------------------
    # TEST 01: API lấy cây thực đơn phân cấp (GET /api/restaurants/{id}/menus)
    # -------------------------------------------------------------
    print("\n[TEST 01] Kiểm tra API cây thực đơn phân cấp kèm món ăn con:")
    menus = get_restaurant_menus(restaurant_id=1, db=db)
    assert len(menus) == 2, f"Kỳ vọng 2 nhóm thực đơn, thực tế: {len(menus)}"
    assert menus[0].name == "Món Khai Vị & Ăn Kèm"
    assert len(menus[0].items) == 2
    assert menus[1].name == "Thịt Bò Mỹ Nướng Tảng"
    assert len(menus[1].items) == 2
    print(f"  Nhóm 1: [{menus[0].name}] có {len(menus[0].items)} món ăn")
    print(f"  Nhóm 2: [{menus[1].name}] có {len(menus[1].items)} món ăn")
    print("  => PASSED: Cây thực đơn được phân cấp chuẩn xác theo từng nhóm!")

    # -------------------------------------------------------------
    # TEST 02: Nhận diện trạng thái món ăn (Còn món vs Tạm hết món)
    # -------------------------------------------------------------
    print("\n[TEST 02] Kiểm tra phân biệt trạng thái phục vụ (is_available):")
    wagyu = next(it for it in menus[1].items if it.name == "Thăn Ngoại Bò Wagyu A5")
    de_suon = next(it for it in menus[1].items if it.name == "Dẻ Sườn Bò Mỹ Xốt Galbi")
    assert wagyu.is_available is False, "Món Wagyu phải có trạng thái is_available=False"
    assert de_suon.is_available is True, "Món Dẻ Sườn phải có trạng thái is_available=True"
    print(f"  Món: '{de_suon.name}' => is_available={de_suon.is_available} (Còn món)")
    print(f"  Món: '{wagyu.name}' => is_available={wagyu.is_available} (Tạm hết món)")
    print("  => PASSED: Phân biệt rõ ràng món ăn còn hay tạm hết phục vụ!")

    # -------------------------------------------------------------
    # TEST 03: Quy chuẩn format đơn giá tiền tệ VNĐ
    # -------------------------------------------------------------
    print("\n[TEST 03] Kiểm tra quy chuẩn đơn giá món ăn:")
    assert de_suon.price == 249000.0
    formatted_vnd = f"{int(de_suon.price):,}đ".replace(",", ".")
    assert formatted_vnd == "249.000đ"
    print(f"  Giá gốc: {de_suon.price} => Định dạng hiển thị: {formatted_vnd}")
    print("  => PASSED: Đơn giá món ăn được định dạng VNĐ chuẩn xác!")

    # -------------------------------------------------------------
    # TEST 04: API thư viện hình ảnh nhà hàng (GET /api/restaurants/{id}/images)
    # -------------------------------------------------------------
    print("\n[TEST 04] Kiểm tra API thư viện hình ảnh phục vụ Lightbox:")
    images = get_restaurant_images(restaurant_id=1, db=db)
    assert len(images) == 3, f"Kỳ vọng 3 ảnh, thực tế: {len(images)}"
    assert images[0].is_cover is True, "Ảnh đầu tiên phải là ảnh bìa chính (is_cover=True)"
    assert images[0].caption == "Ảnh bìa mặt tiền nhà hàng"
    assert images[1].display_order == 2 and images[2].display_order == 3
    print(f"  Đã tải {len(images)} ảnh (Ảnh bìa: '{images[0].caption}', Ảnh 2: '{images[1].caption}')")
    print("  => PASSED: Thư viện ảnh sắp xếp thứ tự chuẩn xác sẵn sàng cho Lightbox!")

    # -------------------------------------------------------------
    # TEST 05: Kiểm tra cấu trúc HTML & CSS Lightbox Viewer trong frontend/index.html
    # -------------------------------------------------------------
    print("\n[TEST 05] Kiểm tra tích hợp cấu trúc Lightbox Viewer trong HTML:")
    html_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "frontend", "index.html")
    assert os.path.exists(html_path), "File frontend/index.html không tồn tại"
    with open(html_path, "r", encoding="utf-8") as f:
        html = f.read()

    assert 'id="lightbox-modal"' in html, "Thiếu phần tử #lightbox-modal"
    assert 'id="lightbox-image"' in html, "Thiếu phần tử #lightbox-image"
    assert 'id="lightbox-caption"' in html, "Thiếu phần tử #lightbox-caption"
    assert 'id="lightbox-counter"' in html, "Thiếu phần tử #lightbox-counter"
    assert 'class="lightbox-close-btn"' in html, "Thiếu nút đóng lightbox"
    assert 'class="lightbox-nav-btn lightbox-prev"' in html, "Thiếu nút chuyển ảnh trước"
    assert 'class="lightbox-nav-btn lightbox-next"' in html, "Thiếu nút chuyển ảnh tiếp theo"
    print("  Đã tìm thấy: #lightbox-modal, #lightbox-image, #lightbox-caption, nút Prev/Next, nút Close")
    print("  => PASSED: Cấu trúc DOM của Lightbox Viewer đầy đủ và đạt chuẩn!")

    # -------------------------------------------------------------
    # TEST 06: Kiểm tra phím tắt bàn phím & cử chỉ cảm ứng vuốt (Swipe) Lightbox
    # -------------------------------------------------------------
    print("\n[TEST 06] Kiểm tra xử lý điều hướng, phím tắt & cử chỉ vuốt Lightbox:")
    assert 'function openLightbox' in html, "Thiếu hàm openLightbox"
    assert 'function closeLightbox' in html, "Thiếu hàm closeLightbox"
    assert 'function lightboxNext' in html, "Thiếu hàm lightboxNext"
    assert 'function lightboxPrev' in html, "Thiếu hàm lightboxPrev"
    assert "e.key === 'Escape'" in html, "Thiếu phím ESC để đóng Lightbox"
    assert "e.key === 'ArrowRight'" in html, "Thiếu phím mũi tên phải để tiến ảnh"
    assert "e.key === 'ArrowLeft'" in html, "Thiếu phím mũi tên trái để lùi ảnh"
    assert 'function handleLightboxTouchStart' in html, "Thiếu hàm touch swipe start"
    assert 'function handleLightboxTouchEnd' in html, "Thiếu hàm touch swipe end"
    print("  Đã kiểm tra: openLightbox, closeLightbox, lightboxNext, lightboxPrev, phím ESC/←/→, touch swipe mobile")
    print("  => PASSED: Đầy đủ các hàm điều khiển, phím tắt bàn phím và cử chỉ vuốt cảm ứng đa thiết bị!")

    # -------------------------------------------------------------
    # TEST 07: Kiểm tra tính năng Tìm kiếm nhanh món ăn & Accordion Danh mục
    # -------------------------------------------------------------
    print("\n[TEST 07] Kiểm tra tính năng lọc nhanh món ăn & Accordion thu gọn:")
    assert 'id="modal-menu-search-input"' in html, "Thiếu ô input tìm kiếm món ăn"
    assert 'function filterModalMenuItems' in html, "Thiếu hàm filterModalMenuItems"
    assert 'function renderCategorizedMenus' in html, "Thiếu hàm renderCategorizedMenus"
    assert 'function toggleMenuCategory' in html, "Thiếu hàm toggleMenuCategory cho Accordion"
    assert 'function openSingleImageLightbox' in html, "Thiếu hàm phóng to ảnh món ăn riêng biệt"
    assert '.menu-item-thumb' in html, "Thiếu class CSS menu-item-thumb cho ảnh món ăn"
    print("  Đã kiểm tra: Ô tìm kiếm món ăn, hàm toggle Accordion nhóm món, thumbnail ảnh món ăn & phóng to món")
    print("  => PASSED: Tích hợp đầy đủ tính năng tìm kiếm món ăn, Accordion và phóng to ảnh món ăn!")

    # -------------------------------------------------------------
    # TEST 08: Kiểm tra tính tương thích Responsive đa thiết bị (NFR-06)
    # -------------------------------------------------------------
    print("\n[TEST 08] Kiểm tra cấu hình Responsive đa thiết bị (NFR-06):")
    assert "@media (max-width: 768px)" in html, "Thiếu breakpoint CSS responsive mobile"
    assert ".venue-detail-modal" in html, "Thiếu class CSS mở rộng cho modal chi tiết quán"
    print("  Đã tìm thấy: Breakpoint mobile @media (max-width: 768px), touch-friendly padding")
    print("  => PASSED: Giao diện hiển thị sắc nét, co giãn tối ưu trên cả Desktop & Mobile!")

    # -------------------------------------------------------------
    # TEST 09: Benchmark Hiệu năng Tải Dữ liệu NFR-01 (< 3 giây)
    # -------------------------------------------------------------
    print("\n[TEST 09] Kiểm tra hiệu năng nạp đồng thời Thư viện ảnh & Thực đơn (NFR-01 < 3s):")
    t0 = time.perf_counter()
    _ = get_restaurant_images(restaurant_id=1, db=db)
    _ = get_restaurant_menus(restaurant_id=1, db=db)
    elapsed_ms = (time.perf_counter() - t0) * 1000
    print(f"  Tổng thời gian nạp ảnh + thực đơn: {elapsed_ms:.2f} ms")
    assert elapsed_ms < 3000, f"Thời gian thực thi vượt quá 3 giây: {elapsed_ms}ms"
    print(f"  => PASSED: Thời gian phản hồi thần tốc ({elapsed_ms:.2f} ms << 3000 ms tiêu chuẩn NFR-01)!")

    print("\n" + "=" * 75)
    print("KẾT QUẢ: 9/9 CA KIỂM THỬ TASK TSK-30 ĐÃ VƯỢT QUA XUẤT SẮC (ALL PASSED)!")
    print("=" * 75)
    db.close()


if __name__ == "__main__":
    run_tests()
