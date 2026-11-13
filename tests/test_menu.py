"""
test_menu.py — Bộ kiểm thử Tự động Quản lý Thực đơn & Món ăn (TSK-27 / PBI-16 / UC-06b)
========================================================================================
Kiểm thử toàn diện 9 ca kiểm thử:
  - TSK-27: CRUD RestaurantMenus (Nhóm thực đơn) & MenuItems (Món ăn, đơn giá, trạng thái).
  - Validation: Giá tiền không âm (price >= 0), tên không rỗng.
  - Cascade Delete: Xóa nhóm thực đơn tự động xóa toàn bộ món ăn con.
  - Availability Toggle: Bật/tắt nhanh trạng thái còn món.
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
from app.models.restaurant import Restaurant, RestaurantMenu, MenuItem
from app.services.menu_service import MenuService
from app.routers.menu import (
    create_restaurant_menu,
    get_restaurant_menus,
    get_menu_detail,
    update_restaurant_menu,
    delete_restaurant_menu,
    create_menu_item,
    get_items_by_menu,
    get_menu_item_detail,
    update_menu_item,
    toggle_item_availability,
    delete_menu_item,
)
from app.schemas.menu import (
    RestaurantMenuCreate,
    RestaurantMenuUpdate,
    MenuItemCreate,
    MenuItemUpdate,
    MenuItemAvailabilityUpdate,
)

Base.metadata.create_all(bind=test_engine)


def setup_sample_restaurant():
    """Tạo nhà hàng mẫu để gắn thực đơn"""
    db = TestingSessionLocal()
    restaurant = Restaurant(
        name="Nhà hàng Bò Nướng Phố",
        address="123 Nguyễn Thị Minh Khai, Q1",
        latitude=10.7769,
        longitude=106.7009,
        min_price=100000.0,
        max_price=300000.0,
        cuisine_type="Lẩu Nướng"
    )
    db.add(restaurant)
    db.commit()
    db.refresh(restaurant)
    rest_id = restaurant.id
    db.close()
    return rest_id


def test_01_create_restaurant_menu():
    """Kiểm thử tạo mới nhóm thực đơn cho nhà hàng (TSK-27)"""
    print("\n[TEST 01] Kiểm thử tạo nhóm thực đơn mới (POST /api/restaurants/{id}/menus):")
    db = TestingSessionLocal()
    try:
        rest_id = setup_sample_restaurant()
        payload = RestaurantMenuCreate(
            name="Món Khai Vị",
            description="Các món gỏi, súp mở đầu bữa tiệc",
            display_order=1
        )
        menu = create_restaurant_menu(restaurant_id=rest_id, payload=payload, db=db)

        print(f"  Tạo thành công: ID={menu.id}, Name='{menu.name}', DisplayOrder={menu.display_order}")
        assert menu.id is not None
        assert menu.restaurant_id == rest_id
        assert menu.name == "Món Khai Vị"
        assert menu.display_order == 1
        print("  => PASSED: Nhóm thực đơn đã được lưu chuẩn xác vào CSDL!")
    finally:
        db.close()


def test_02_create_menu_invalid_restaurant():
    """Kiểm thử chặn tạo thực đơn cho nhà hàng không tồn tại (Kỳ vọng 404)"""
    print("\n[TEST 02] Kiểm thử tạo thực đơn với restaurant_id không tồn tại (HTTP 404):")
    db = TestingSessionLocal()
    try:
        from fastapi import HTTPException
        payload = RestaurantMenuCreate(name="Đồ Uống")
        try:
            create_restaurant_menu(restaurant_id=99999, payload=payload, db=db)
            assert False, "Kỳ vọng ném ra HTTPException 404 nhưng không xảy ra."
        except HTTPException as e:
            print(f"  Bắt đúng mã lỗi HTTP: {e.status_code} - {e.detail}")
            assert e.status_code == 404
            print("  => PASSED: Đã chặn đúng khi ID nhà hàng không tồn tại!")
    finally:
        db.close()


def test_03_create_menu_item():
    """Kiểm thử thêm món ăn mới vào nhóm thực đơn (POST /api/menus/{id}/items)"""
    print("\n[TEST 03] Kiểm thử thêm món ăn mới vào thực đơn (TSK-27):")
    db = TestingSessionLocal()
    try:
        # Lấy nhóm thực đơn vừa tạo
        menu = db.query(RestaurantMenu).first()
        payload = MenuItemCreate(
            name="Gỏi Củ Hủ Dừa Tôm Thịt",
            description="Củ hủ dừa giòn ngọt, tôm sú tươi ngon và thịt ba chỉ hảo hạng",
            price=125000.0,
            image_url="https://images.unsplash.com/photo-1540420773420-3366772f4999?w=400",
            is_available=True
        )
        item = create_menu_item(menu_id=menu.id, payload=payload, db=db)

        print(f"  Thêm thành công: ID={item.id}, Name='{item.name}', Price={item.price:,.0f}đ, is_available={item.is_available}")
        assert item.id is not None
        assert item.menu_id == menu.id
        assert item.name == "Gỏi Củ Hủ Dừa Tôm Thịt"
        assert item.price == 125000.0
        assert item.is_available is True
        print("  => PASSED: Món ăn được lưu chuẩn xác kèm giá tiền và trạng thái còn món!")
    finally:
        db.close()


def test_04_create_menu_item_invalid_price():
    """Kiểm thử chặn món ăn có giá tiền âm (price < 0)"""
    print("\n[TEST 04] Kiểm thử chặn món ăn có giá tiền âm (Validation Error):")
    from pydantic import ValidationError
    try:
        MenuItemCreate(
            name="Món Ăn Lỗi Giá",
            price=-50000.0
        )
        assert False, "Kỳ vọng ném lỗi ValidationError khi giá âm nhưng không xảy ra."
    except ValidationError as e:
        print(f"  Pydantic bắt đúng lỗi: {e.errors()[0]['msg']}")
        print("  => PASSED: Hệ thống đã chặn thành công giá tiền âm!")


def test_05_get_restaurant_menus_with_items():
    """Kiểm thử lấy danh sách toàn bộ thực đơn kèm món ăn con (Eager Loading)"""
    print("\n[TEST 05] Kiểm thử lấy toàn bộ cây thực đơn của nhà hàng (GET /api/restaurants/{id}/menus):")
    db = TestingSessionLocal()
    try:
        menu = db.query(RestaurantMenu).first()
        rest_id = menu.restaurant_id

        # Thêm món thứ 2 vào menu
        payload2 = MenuItemCreate(
            name="Chả Giò Hải Sản Mayo",
            description="Chả giò chiên vàng giòn rụm chấm xốt mayonnaise",
            price=95000.0,
            is_available=True
        )
        create_menu_item(menu_id=menu.id, payload=payload2, db=db)

        # Gọi endpoint lấy toàn bộ menu của nhà hàng
        menus = get_restaurant_menus(restaurant_id=rest_id, db=db)

        print(f"  Nhà hàng ID={rest_id} có {len(menus)} nhóm thực đơn:")
        for m in menus:
            print(f"    - [{m.name}] ({len(m.items)} món ăn):")
            for it in m.items:
                print(f"        + {it.name} - {it.price:,.0f}đ (Còn món: {it.is_available})")

        assert len(menus) >= 1
        assert len(menus[0].items) >= 2
        print("  => PASSED: Cây thực đơn được tải đầy đủ cùng các món ăn con!")
    finally:
        db.close()


def test_06_update_menu_and_item():
    """Kiểm thử chỉnh sửa nhóm thực đơn và món ăn (PUT /api/menus/{id} & PUT /api/menu-items/{id})"""
    print("\n[TEST 06] Kiểm thử chỉnh sửa nhóm thực đơn và thông tin món ăn:")
    db = TestingSessionLocal()
    try:
        item = db.query(MenuItem).first()

        # Cập nhật giá món ăn từ 125k lên 135k và đổi tên
        update_payload = MenuItemUpdate(
            name="Gỏi Củ Hủ Dừa Tôm Càng",
            price=135000.0,
            description="Nâng cấp tôm càng xanh tươi sống"
        )
        updated_item = update_menu_item(item_id=item.id, payload=update_payload, db=db)

        print(f"  Món ăn sau khi cập nhật: Name='{updated_item.name}', Price={updated_item.price:,.0f}đ")
        assert updated_item.name == "Gỏi Củ Hủ Dừa Tôm Càng"
        assert updated_item.price == 135000.0

        # Cập nhật nhóm thực đơn
        menu_update = RestaurantMenuUpdate(name="Khai Vị Đặc Biệt")
        updated_menu = update_restaurant_menu(menu_id=item.menu_id, payload=menu_update, db=db)
        print(f"  Nhóm thực đơn sau khi cập nhật: Name='{updated_menu.name}'")
        assert updated_menu.name == "Khai Vị Đặc Biệt"
        print("  => PASSED: Cập nhật thông tin thực đơn và món ăn thành công!")
    finally:
        db.close()


def test_07_toggle_item_availability():
    """Kiểm thử bật/tắt trạng thái còn món (PATCH /api/menu-items/{id}/availability)"""
    print("\n[TEST 07] Kiểm thử bật/tắt nhanh trạng thái còn món (Toggle is_available):")
    db = TestingSessionLocal()
    try:
        item = db.query(MenuItem).first()
        initial_status = item.is_available

        # Đổi trạng thái sang Hết món (False)
        payload_off = MenuItemAvailabilityUpdate(is_available=False)
        res_off = toggle_item_availability(item_id=item.id, payload=payload_off, db=db)
        print(f"  Đổi sang: is_available={res_off.is_available} (Hết món)")
        assert res_off.is_available is False

        # Đổi lại sang Còn món (True)
        payload_on = MenuItemAvailabilityUpdate(is_available=True)
        res_on = toggle_item_availability(item_id=item.id, payload=payload_on, db=db)
        print(f"  Đổi lại sang: is_available={res_on.is_available} (Còn món)")
        assert res_on.is_available is True

        print("  => PASSED: Tính năng toggle trạng thái phục vụ hoạt động tức thì!")
    finally:
        db.close()


def test_08_delete_menu_item():
    """Kiểm thử xóa một món ăn (DELETE /api/menu-items/{id})"""
    print("\n[TEST 08] Kiểm thử xóa một món ăn khỏi thực đơn:")
    db = TestingSessionLocal()
    try:
        item = db.query(MenuItem).order_by(MenuItem.id.desc()).first()
        deleted_id = item.id

        res = delete_menu_item(item_id=deleted_id, db=db)
        assert res["status"] == "success"

        # Kiểm tra không còn trong DB
        check_item = db.query(MenuItem).filter(MenuItem.id == deleted_id).first()
        assert check_item is None
        print(f"  Đã xóa sạch món ID={deleted_id} khỏi CSDL.")
        print("  => PASSED: Xóa món ăn thành công!")
    finally:
        db.close()


def test_09_delete_menu_cascade():
    """Kiểm thử xóa nhóm thực đơn và tự động xóa cascade toàn bộ món con (TSK-27)"""
    print("\n[TEST 09] Kiểm thử xóa nhóm thực đơn kèm xóa cascade toàn bộ món con:")
    db = TestingSessionLocal()
    try:
        # Tạo thêm 1 menu phụ kèm 2 món con
        rest = db.query(Restaurant).first()
        menu = create_restaurant_menu(
            restaurant_id=rest.id,
            payload=RestaurantMenuCreate(name="Tráng Miệng Xóa Thử"),
            db=db
        )

        create_menu_item(menu_id=menu.id, payload=MenuItemCreate(name="Chè Khúc Bạch", price=35000.0), db=db)
        create_menu_item(menu_id=menu.id, payload=MenuItemCreate(name="Rau Câu Dừa", price=25000.0), db=db)

        items_before = db.query(MenuItem).filter(MenuItem.menu_id == menu.id).count()
        print(f"  Trước khi xóa: Menu ID={menu.id} có {items_before} món con.")
        assert items_before == 2

        # Thực hiện xóa nhóm thực đơn
        delete_restaurant_menu(menu_id=menu.id, db=db)

        # Kiểm tra menu đã mất
        check_menu = db.query(RestaurantMenu).filter(RestaurantMenu.id == menu.id).first()
        assert check_menu is None

        # Kiểm tra toàn bộ món con cũng tự động mất theo cascade
        items_after = db.query(MenuItem).filter(MenuItem.menu_id == menu.id).count()
        print(f"  Sau khi xóa: Số món con còn lại trong menu={items_after}.")
        assert items_after == 0

        print("  => PASSED: Cascade Delete hoạt động chuẩn xác 100%!")
    finally:
        db.close()


if __name__ == "__main__":
    print("=" * 75)
    print("BẮT ĐẦU CHẠY BỘ KIỂM THỬ QUẢN LÝ THỰC ĐƠN & MÓN ĂN (TSK-27)")
    print("=" * 75)

    test_01_create_restaurant_menu()
    test_02_create_menu_invalid_restaurant()
    test_03_create_menu_item()
    test_04_create_menu_item_invalid_price()
    test_05_get_restaurant_menus_with_items()
    test_06_update_menu_and_item()
    test_07_toggle_item_availability()
    test_08_delete_menu_item()
    test_09_delete_menu_cascade()

    print("\n" + "=" * 75)
    print("KẾT QUẢ: 9/9 CA KIỂM THỬ TASK TSK-27 ĐÃ VƯỢT QUA XUẤT SẮC (ALL PASSED)!")
    print("=" * 75)
