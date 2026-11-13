from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.menu_service import MenuService
from app.schemas.menu import (
    RestaurantMenuCreate,
    RestaurantMenuUpdate,
    RestaurantMenuResponse,
    RestaurantMenuWithItemsResponse,
    MenuItemCreate,
    MenuItemUpdate,
    MenuItemAvailabilityUpdate,
    MenuItemResponse,
)

router = APIRouter(tags=["Quản lý Thực đơn & Món ăn (Menus & MenuItems - TSK-27)"])


# =====================================================================
# 1. API QUẢN LÝ NHÓM THỰC ĐƠN (RestaurantMenus)
# =====================================================================

@router.get(
    "/api/restaurants/{restaurant_id}/menus",
    response_model=List[RestaurantMenuWithItemsResponse],
    status_code=status.HTTP_200_OK,
    summary="Lấy danh sách nhóm thực đơn kèm món ăn của nhà hàng"
)
def get_restaurant_menus(
    restaurant_id: int,
    db: Session = Depends(get_db)
):
    """
    Truy vấn toàn bộ cây thực đơn của một nhà hàng:
    - Trả về danh sách nhóm thực đơn (RestaurantMenus) đã sắp xếp theo `display_order`.
    - Mỗi nhóm thực đơn kèm đầy đủ danh sách món ăn (MenuItems).
    """
    return MenuService.get_menus_by_restaurant(db, restaurant_id)


@router.post(
    "/api/restaurants/{restaurant_id}/menus",
    response_model=RestaurantMenuResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Tạo nhóm thực đơn mới cho nhà hàng (Admin - UC-06b)"
)
def create_restaurant_menu(
    restaurant_id: int,
    payload: RestaurantMenuCreate,
    db: Session = Depends(get_db)
):
    """
    Thêm một danh mục thực đơn mới cho nhà hàng (Ví dụ: 'Món Khai Vị', 'Món Chính', 'Đồ Uống').
    """
    return MenuService.create_menu(db, restaurant_id, payload)


@router.get(
    "/api/menus/{menu_id}",
    response_model=RestaurantMenuWithItemsResponse,
    status_code=status.HTTP_200_OK,
    summary="Lấy chi tiết một nhóm thực đơn theo ID"
)
def get_menu_detail(
    menu_id: int,
    db: Session = Depends(get_db)
):
    """Lấy thông tin nhóm thực đơn kèm danh sách món ăn con bên trong."""
    return MenuService.get_menu_by_id(db, menu_id)


@router.put(
    "/api/menus/{menu_id}",
    response_model=RestaurantMenuResponse,
    status_code=status.HTTP_200_OK,
    summary="Chỉnh sửa nhóm thực đơn (Admin - UC-06b)"
)
def update_restaurant_menu(
    menu_id: int,
    payload: RestaurantMenuUpdate,
    db: Session = Depends(get_db)
):
    """Cập nhật tên nhóm, mô tả hoặc thứ tự hiển thị của thực đơn."""
    return MenuService.update_menu(db, menu_id, payload)


@router.delete(
    "/api/menus/{menu_id}",
    status_code=status.HTTP_200_OK,
    summary="Xóa nhóm thực đơn (Cascade xóa các món con) (Admin - UC-06b)"
)
def delete_restaurant_menu(
    menu_id: int,
    db: Session = Depends(get_db)
):
    """
    Xóa một nhóm thực đơn:
    - Toàn bộ món ăn thuộc nhóm này sẽ được tự động xóa theo quan hệ cascade.
    """
    MenuService.delete_menu(db, menu_id)
    return {
        "status": "success",
        "message": f"Đã xóa nhóm thực đơn #{menu_id} và các món ăn liên quan thành công."
    }


# =====================================================================
# 2. API QUẢN LÝ MÓN ĂN CHI TIẾT (MenuItems)
# =====================================================================

@router.post(
    "/api/menus/{menu_id}/items",
    response_model=MenuItemResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Thêm món ăn mới vào nhóm thực đơn (Admin - UC-06b)"
)
def create_menu_item(
    menu_id: int,
    payload: MenuItemCreate,
    db: Session = Depends(get_db)
):
    """
    Thêm món ăn mới vào nhóm thực đơn:
    - Bắt buộc: Tên món, đơn vị giá (>= 0).
    - Tùy chọn: Mô tả hương vị, ảnh món ăn (`image_url`), trạng thái phục vụ (`is_available`).
    """
    return MenuService.create_menu_item(db, menu_id, payload)


@router.get(
    "/api/menus/{menu_id}/items",
    response_model=List[MenuItemResponse],
    status_code=status.HTTP_200_OK,
    summary="Lấy danh sách tất cả món ăn trong một nhóm thực đơn"
)
def get_items_by_menu(
    menu_id: int,
    db: Session = Depends(get_db)
):
    """Lấy danh sách các món ăn thuộc nhóm thực đơn `menu_id`."""
    return MenuService.get_menu_items_by_menu(db, menu_id)


@router.get(
    "/api/menu-items/{item_id}",
    response_model=MenuItemResponse,
    status_code=status.HTTP_200_OK,
    summary="Lấy chi tiết một món ăn theo ID"
)
def get_menu_item_detail(
    item_id: int,
    db: Session = Depends(get_db)
):
    """Truy vấn thông tin chi tiết một món ăn cụ thể."""
    return MenuService.get_menu_item_by_id(db, item_id)


@router.put(
    "/api/menu-items/{item_id}",
    response_model=MenuItemResponse,
    status_code=status.HTTP_200_OK,
    summary="Chỉnh sửa thông tin món ăn và giá tiền (Admin - UC-06b)"
)
def update_menu_item(
    item_id: int,
    payload: MenuItemUpdate,
    db: Session = Depends(get_db)
):
    """
    Cập nhật thông tin món ăn:
    - Cho phép cập nhật tên món, mô tả, giá tiền, ảnh minh họa và trạng thái phục vụ.
    """
    return MenuService.update_menu_item(db, item_id, payload)


@router.patch(
    "/api/menu-items/{item_id}/availability",
    response_model=MenuItemResponse,
    status_code=status.HTTP_200_OK,
    summary="Bật/Tắt nhanh trạng thái còn món (Còn món / Hết món) (Admin - UC-06b)"
)
def toggle_item_availability(
    item_id: int,
    payload: MenuItemAvailabilityUpdate,
    db: Session = Depends(get_db)
):
    """
    Cập nhật nhanh trạng thái phục vụ:
    - `is_available: true`  -> Còn món
    - `is_available: false` -> Tạm hết món
    """
    return MenuService.toggle_item_availability(db, item_id, payload.is_available)


@router.delete(
    "/api/menu-items/{item_id}",
    status_code=status.HTTP_200_OK,
    summary="Xóa một món ăn khỏi thực đơn (Admin - UC-06b)"
)
def delete_menu_item(
    item_id: int,
    db: Session = Depends(get_db)
):
    """Xóa một món ăn khỏi thực đơn."""
    MenuService.delete_menu_item(db, item_id)
    return {
        "status": "success",
        "message": f"Đã xóa món ăn #{item_id} thành công."
    }
