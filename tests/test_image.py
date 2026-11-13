"""
test_image.py — Bộ kiểm thử Tự động Quản lý Hình ảnh Nhà hàng (TSK-28 / PBI-16 / UC-06b)
==========================================================================================
Kiểm thử toàn diện 9 ca kiểm thử:
  - TSK-28: CRUD RestaurantImages (Thêm ảnh URL, nhiều ảnh, xóa ảnh).
  - Ảnh bìa duy nhất (is_cover): Tự động bật ảnh đầu tiên, đổi ảnh bìa tự động tắt cờ ảnh cũ.
  - Tự động gán ảnh bìa thay thế khi ảnh bìa hiện tại bị xóa.
  - Sắp xếp thứ tự hiển thị (display_order).
  - Cascade Delete: Xóa nhà hàng tự động dọn sạch thư viện ảnh.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# SQLite in-memory engine độc lập cho kiểm thử
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
test_engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

from app.core.database import Base
import app.models
from app.models.restaurant import Restaurant, RestaurantImage
from app.services.image_service import ImageService
from app.routers.image import (
    get_restaurant_images,
    add_restaurant_image,
    add_restaurant_images_batch,
    get_image_detail,
    update_image_info,
    set_cover_image,
    delete_restaurant_image,
)
from app.schemas.image import (
    RestaurantImageCreate,
    RestaurantImageBatchCreate,
    RestaurantImageUpdate,
)

Base.metadata.create_all(bind=test_engine)


def setup_sample_restaurant():
    """Tạo nhà hàng mẫu để gắn thư viện ảnh"""
    db = TestingSessionLocal()
    restaurant = Restaurant(
        name="Lẩu Nướng Phố Đêm",
        address="456 Hai Bà Trưng, Quận 1",
        latitude=10.7850,
        longitude=106.6950,
        min_price=150000.0,
        max_price=350000.0,
        cuisine_type="Lẩu Nướng"
    )
    db.add(restaurant)
    db.commit()
    db.refresh(restaurant)
    rest_id = restaurant.id
    db.close()
    return rest_id


def test_01_add_image_url():
    """Kiểm thử thêm 1 ảnh mới cho nhà hàng bằng URL (POST /api/restaurants/{id}/images)"""
    print("\n[TEST 01] Kiểm thử thêm ảnh bằng URL (TSK-28):")
    db = TestingSessionLocal()
    try:
        rest_id = setup_sample_restaurant()
        payload = RestaurantImageCreate(
            image_url="https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=800",
            caption="Mặt tiền quán về đêm lung linh ánh đèn",
            is_cover=False,
            display_order=1
        )
        img = add_restaurant_image(restaurant_id=rest_id, payload=payload, db=db)

        print(f"  Thêm thành công: ID={img.id}, Cover={img.is_cover}, Caption='{img.caption}'")
        assert img.id is not None
        assert img.restaurant_id == rest_id
        # Vì đây là ảnh đầu tiên của quán, logic tự động set is_cover = True
        assert img.is_cover is True
        print("  => PASSED: Ảnh đầu tiên được lưu và tự động đặt làm ảnh bìa chính!")
    finally:
        db.close()


def test_02_add_image_invalid_restaurant():
    """Kiểm thử chặn thêm ảnh cho nhà hàng không tồn tại (HTTP 404)"""
    print("\n[TEST 02] Kiểm thử thêm ảnh cho nhà hàng không tồn tại (HTTP 404):")
    db = TestingSessionLocal()
    try:
        from fastapi import HTTPException
        payload = RestaurantImageCreate(
            image_url="https://images.unsplash.com/photo-1544025162-d76694265947?w=800"
        )
        try:
            add_restaurant_image(restaurant_id=99999, payload=payload, db=db)
            assert False, "Kỳ vọng ném ra HTTPException 404 nhưng không xảy ra."
        except HTTPException as e:
            print(f"  Bắt đúng mã lỗi: {e.status_code} - {e.detail}")
            assert e.status_code == 404
            print("  => PASSED: Đã chặn đúng khi ID nhà hàng không tồn tại!")
    finally:
        db.close()


def test_03_first_image_auto_cover():
    """Kiểm thử logic ảnh đầu tiên luôn được đảm bảo làm ảnh bìa (is_cover = True)"""
    print("\n[TEST 03] Kiểm thử logic tự động gán ảnh bìa đầu tiên:")
    db = TestingSessionLocal()
    try:
        rest = db.query(Restaurant).first()
        img1 = db.query(RestaurantImage).filter(RestaurantImage.restaurant_id == rest.id).first()
        assert img1.is_cover is True
        print(f"  Ảnh ID={img1.id} của nhà hàng ID={rest.id} có is_cover={img1.is_cover}")
        print("  => PASSED: Nhà hàng luôn có ảnh bìa mặc định!")
    finally:
        db.close()


def test_04_set_cover_image():
    """Kiểm thử đặt ảnh mới làm ảnh bìa và tự động hủy cờ ảnh bìa cũ (PATCH /set-cover)"""
    print("\n[TEST 04] Kiểm thử cơ chế đổi ảnh bìa chính duy nhất (Set Cover):")
    db = TestingSessionLocal()
    try:
        rest = db.query(Restaurant).first()
        # Thêm ảnh thứ 2 với is_cover=False
        payload2 = RestaurantImageCreate(
            image_url="https://images.unsplash.com/photo-1555396273-367ea4eb4db5?w=800",
            caption="Không gian tầng 2 thoáng mát",
            is_cover=False,
            display_order=2
        )
        img2 = add_restaurant_image(restaurant_id=rest.id, payload=payload2, db=db)
        print(f"  Đã thêm ảnh 2: ID={img2.id}, is_cover={img2.is_cover}")
        assert img2.is_cover is False

        # Thực hiện gọi API set ảnh 2 làm ảnh bìa
        cover_res = set_cover_image(image_id=img2.id, db=db)
        print(f"  Kết quả đặt ảnh bìa: {cover_res.message}")
        assert cover_res.is_cover is True

        # Kiểm tra lại trong DB: Ảnh 2 phải là True, ảnh 1 phải tự động chuyển thành False
        img1_db = db.query(RestaurantImage).filter(RestaurantImage.id == 1).first()
        img2_db = db.query(RestaurantImage).filter(RestaurantImage.id == img2.id).first()

        print(f"  Sau khi đổi: Ảnh 1 cover={img1_db.is_cover} | Ảnh 2 cover={img2_db.is_cover}")
        assert img1_db.is_cover is False, "Ảnh cũ phải bị tắt cờ is_cover."
        assert img2_db.is_cover is True, "Ảnh mới phải bật cờ is_cover."
        print("  => PASSED: Đảm bảo tính duy nhất của ảnh bìa chính (Single Cover Invariant)!")
    finally:
        db.close()


def test_05_batch_add_images():
    """Kiểm thử thêm hàng loạt ảnh qua danh sách URLs (POST /images/batch)"""
    print("\n[TEST 05] Kiểm thử thêm nhiều ảnh cùng lúc bằng Batch URLs:")
    db = TestingSessionLocal()
    try:
        rest = db.query(Restaurant).first()
        batch_payload = RestaurantImageBatchCreate(
            images=[
                RestaurantImageCreate(
                    image_url="https://images.unsplash.com/photo-1550966871-3ed3cdb5ed0c?w=800",
                    caption="Quầy bar sang trọng",
                    display_order=3
                ),
                RestaurantImageCreate(
                    image_url="https://images.unsplash.com/photo-1559339352-11d035aa65de?w=800",
                    caption="Bàn ăn gia đình ấm cúng",
                    display_order=4
                )
            ]
        )
        batch_res = add_restaurant_images_batch(restaurant_id=rest.id, payload=batch_payload, db=db)

        print(f"  Đã thêm thành công {len(batch_res)} ảnh qua batch:")
        for b in batch_res:
            print(f"    - ID={b.id}: '{b.caption}' (Order={b.display_order})")

        assert len(batch_res) == 2
        print("  => PASSED: Thêm hàng loạt ảnh qua Batch URLs thành công!")
    finally:
        db.close()


def test_06_update_image_caption_and_order():
    """Kiểm thử cập nhật chú thích và thứ tự hiển thị (PUT /restaurant-images/{id})"""
    print("\n[TEST 06] Kiểm thử chỉnh sửa caption và display_order:")
    db = TestingSessionLocal()
    try:
        img = db.query(RestaurantImage).filter(RestaurantImage.id == 1).first()
        update_payload = RestaurantImageUpdate(
            caption="Mặt tiền quán (Cập nhật góc chụp mới)",
            display_order=99
        )
        updated = update_image_info(image_id=img.id, payload=update_payload, db=db)

        print(f"  Ảnh sau khi sửa: Caption='{updated.caption}', Order={updated.display_order}")
        assert updated.caption == "Mặt tiền quán (Cập nhật góc chụp mới)"
        assert updated.display_order == 99
        print("  => PASSED: Cập nhật thông tin ảnh thành công!")
    finally:
        db.close()


def test_07_delete_image():
    """Kiểm thử xóa ảnh thông thường khỏi thư viện (DELETE /restaurant-images/{id})"""
    print("\n[TEST 07] Kiểm thử xóa ảnh khỏi thư viện:")
    db = TestingSessionLocal()
    try:
        # Lấy ảnh không phải ảnh bìa để xóa
        non_cover = db.query(RestaurantImage).filter(RestaurantImage.is_cover == False).first()
        del_id = non_cover.id

        del_res = delete_restaurant_image(image_id=del_id, db=db)
        assert del_res["status"] == "success"

        # Kiểm tra không còn trong DB
        check_del = db.query(RestaurantImage).filter(RestaurantImage.id == del_id).first()
        assert check_del is None
        print(f"  Đã xóa sạch ảnh ID={del_id} khỏi CSDL.")
        print("  => PASSED: Xóa ảnh thành công!")
    finally:
        db.close()


def test_08_delete_cover_auto_fallback():
    """Kiểm thử tự động chỉ định ảnh bìa thay thế khi xóa ảnh bìa chính (TSK-28)"""
    print("\n[TEST 08] Kiểm thử tự động chọn ảnh bìa thay thế khi ảnh bìa bị xóa:")
    db = TestingSessionLocal()
    try:
        rest = db.query(Restaurant).first()
        cover_img = db.query(RestaurantImage).filter(
            RestaurantImage.restaurant_id == rest.id,
            RestaurantImage.is_cover == True
        ).first()

        print(f"  Ảnh bìa hiện tại trước khi xóa: ID={cover_img.id}")
        del_cover_id = cover_img.id

        # Xóa ảnh bìa chính
        delete_restaurant_image(image_id=del_cover_id, db=db)

        # Kiểm tra xem có ảnh bìa mới được tự động chỉ định hay không
        new_cover = db.query(RestaurantImage).filter(
            RestaurantImage.restaurant_id == rest.id,
            RestaurantImage.is_cover == True
        ).first()

        print(f"  Ảnh bìa mới sau khi tự động chỉ định: ID={new_cover.id if new_cover else None}")
        assert new_cover is not None, "Nhà hàng phải có ảnh bìa mới thay thế khi còn ảnh khác trong thư viện."
        assert new_cover.id != del_cover_id
        print("  => PASSED: Tự động duy trì ảnh bìa khi xóa ảnh bìa cũ!")
    finally:
        db.close()


def test_09_cascade_delete_with_restaurant():
    """Kiểm thử xóa nhà hàng tự động dọn sạch thư viện ảnh (Cascade Delete)"""
    print("\n[TEST 09] Kiểm thử Cascade Delete ảnh khi xóa nhà hàng:")
    db = TestingSessionLocal()
    try:
        rest = db.query(Restaurant).first()
        rest_id = rest.id
        img_count_before = db.query(RestaurantImage).filter(RestaurantImage.restaurant_id == rest_id).count()
        print(f"  Trước khi xóa: Nhà hàng ID={rest_id} có {img_count_before} bức ảnh.")
        assert img_count_before > 0

        # Xóa nhà hàng
        db.delete(rest)
        db.commit()

        # Kiểm tra thư viện ảnh của nhà hàng đã được dọn sạch hoàn toàn
        img_count_after = db.query(RestaurantImage).filter(RestaurantImage.restaurant_id == rest_id).count()
        print(f"  Sau khi xóa: Số ảnh còn lại của nhà hàng={img_count_after}.")
        assert img_count_after == 0
        print("  => PASSED: Cascade Delete hoạt động chuẩn xác 100%!")
    finally:
        db.close()


if __name__ == "__main__":
    print("=" * 75)
    print("BẮT ĐẦU CHẠY BỘ KIỂM THỬ QUẢN LÝ HÌNH ẢNH NHÀ HÀNG (TSK-28)")
    print("=" * 75)

    test_01_add_image_url()
    test_02_add_image_invalid_restaurant()
    test_03_first_image_auto_cover()
    test_04_set_cover_image()
    test_05_batch_add_images()
    test_06_update_image_caption_and_order()
    test_07_delete_image()
    test_08_delete_cover_auto_fallback()
    test_09_cascade_delete_with_restaurant()

    print("\n" + "=" * 75)
    print("KẾT QUẢ: 9/9 CA KIỂM THỬ TASK TSK-28 ĐÃ VƯỢT QUA XUẤT SẮC (ALL PASSED)!")
    print("=" * 75)
