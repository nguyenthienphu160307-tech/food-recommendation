from typing import List, Optional
from sqlalchemy.orm import Session, joinedload
from fastapi import HTTPException, status

from app.models.restaurant import Restaurant, RestaurantMenu, MenuItem
from app.schemas.menu import (
    RestaurantMenuCreate,
    RestaurantMenuUpdate,
    MenuItemCreate,
    MenuItemUpdate,
)


class MenuService:
    """
    Tầng Service / Repository xử lý toàn bộ nghiệp vụ Quản lý Thực đơn và Món ăn (TSK-27 / PBI-16):
    - Quản lý danh mục thực đơn (RestaurantMenus): Tạo, lấy danh sách, sửa, xóa (cascade).
    - Quản lý từng món ăn (MenuItems): Thêm món, cập nhật giá/thông tin, bật/tắt trạng thái còn món, xóa món.
    """

    # =========================================================================
    # 1. NGHIỆP VỤ NHÓM THỰC ĐƠN (RestaurantMenus)
    # =========================================================================

    @staticmethod
    def get_restaurant_or_404(db: Session, restaurant_id: int) -> Restaurant:
        """Kiểm tra sự tồn tại của nhà hàng. Nếu không thấy -> 404."""
        restaurant = db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
        if not restaurant:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Không tìm thấy nhà hàng với ID={restaurant_id}."
            )
        return restaurant

    @staticmethod
    def create_menu(
        db: Session,
        restaurant_id: int,
        payload: RestaurantMenuCreate
    ) -> RestaurantMenu:
        """
        Tạo nhóm thực đơn mới cho nhà hàng:
        - Kiểm tra nhà hàng tồn tại.
        - Khởi tạo bản ghi RestaurantMenu và lưu vào CSDL.
        """
        MenuService.get_restaurant_or_404(db, restaurant_id)

        new_menu = RestaurantMenu(
            restaurant_id=restaurant_id,
            name=payload.name.strip(),
            description=payload.description.strip() if payload.description else None,
            display_order=payload.display_order
        )
        db.add(new_menu)
        db.commit()
        db.refresh(new_menu)
        return new_menu

    @staticmethod
    def get_menus_by_restaurant(
        db: Session,
        restaurant_id: int
    ) -> List[RestaurantMenu]:
        """
        Lấy toàn bộ cây thực đơn của nhà hàng kèm danh sách các món ăn (Eager Loading):
        - Sắp xếp tăng dần theo display_order, sau đó theo id.
        """
        MenuService.get_restaurant_or_404(db, restaurant_id)

        menus = (
            db.query(RestaurantMenu)
            .filter(RestaurantMenu.restaurant_id == restaurant_id)
            .options(joinedload(RestaurantMenu.items))
            .order_by(RestaurantMenu.display_order.asc(), RestaurantMenu.id.asc())
            .all()
        )
        return menus

    @staticmethod
    def get_menu_by_id(db: Session, menu_id: int) -> RestaurantMenu:
        """Lấy chi tiết một nhóm thực đơn theo ID. Nếu không có -> 404."""
        menu = (
            db.query(RestaurantMenu)
            .filter(RestaurantMenu.id == menu_id)
            .options(joinedload(RestaurantMenu.items))
            .first()
        )
        if not menu:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Không tìm thấy nhóm thực đơn với ID={menu_id}."
            )
        return menu

    @staticmethod
    def update_menu(
        db: Session,
        menu_id: int,
        payload: RestaurantMenuUpdate
    ) -> RestaurantMenu:
        """
        Cập nhật thông tin nhóm thực đơn (tên, mô tả, thứ tự hiển thị).
        """
        menu = MenuService.get_menu_by_id(db, menu_id)

        if payload.name is not None:
            menu.name = payload.name.strip()
        if payload.description is not None:
            menu.description = payload.description.strip() if payload.description else None
        if payload.display_order is not None:
            menu.display_order = payload.display_order

        db.commit()
        db.refresh(menu)
        return menu

    @staticmethod
    def delete_menu(db: Session, menu_id: int) -> bool:
        """
        Xóa nhóm thực đơn khỏi hệ thống:
        - Tự động xóa cascade các món ăn thuộc nhóm theo thiết lập ORM & CSDL.
        """
        menu = MenuService.get_menu_by_id(db, menu_id)
        db.delete(menu)
        db.commit()
        return True

    # =========================================================================
    # 2. NGHIỆP VỤ MÓN ĂN (MenuItems)
    # =========================================================================

    @staticmethod
    def create_menu_item(
        db: Session,
        menu_id: int,
        payload: MenuItemCreate
    ) -> MenuItem:
        """
        Thêm một món ăn mới vào nhóm thực đơn:
        - Kiểm tra nhóm thực đơn tồn tại.
        - Đảm bảo giá tiền không âm (>= 0).
        - Lưu vào bảng menu_items.
        """
        MenuService.get_menu_by_id(db, menu_id)

        if payload.price < 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Giá tiền món ăn không được là số âm."
            )

        new_item = MenuItem(
            menu_id=menu_id,
            name=payload.name.strip(),
            description=payload.description.strip() if payload.description else None,
            price=float(payload.price),
            image_url=payload.image_url.strip() if payload.image_url else None,
            is_available=payload.is_available
        )
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
        return new_item

    @staticmethod
    def get_menu_items_by_menu(
        db: Session,
        menu_id: int
    ) -> List[MenuItem]:
        """Lấy danh sách tất cả các món ăn trong một nhóm thực đơn."""
        MenuService.get_menu_by_id(db, menu_id)
        return (
            db.query(MenuItem)
            .filter(MenuItem.menu_id == menu_id)
            .order_by(MenuItem.id.asc())
            .all()
        )

    @staticmethod
    def get_menu_item_by_id(db: Session, item_id: int) -> MenuItem:
        """Lấy chi tiết một món ăn theo ID. Nếu không tìm thấy -> 404."""
        item = db.query(MenuItem).filter(MenuItem.id == item_id).first()
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Không tìm thấy món ăn với ID={item_id}."
            )
        return item

    @staticmethod
    def update_menu_item(
        db: Session,
        item_id: int,
        payload: MenuItemUpdate
    ) -> MenuItem:
        """
        Chỉnh sửa thông tin món ăn (tên, giá tiền, mô tả, ảnh, trạng thái còn món).
        """
        item = MenuService.get_menu_item_by_id(db, item_id)

        if payload.price is not None:
            if payload.price < 0:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Giá tiền món ăn không được là số âm."
                )
            item.price = float(payload.price)

        if payload.name is not None:
            item.name = payload.name.strip()
        if payload.description is not None:
            item.description = payload.description.strip() if payload.description else None
        if payload.image_url is not None:
            item.image_url = payload.image_url.strip() if payload.image_url else None
        if payload.is_available is not None:
            item.is_available = payload.is_available

        db.commit()
        db.refresh(item)
        return item

    @staticmethod
    def toggle_item_availability(
        db: Session,
        item_id: int,
        is_available: bool
    ) -> MenuItem:
        """
        Bật/tắt nhanh trạng thái phục vụ của món ăn (Còn món / Hết món).
        """
        item = MenuService.get_menu_item_by_id(db, item_id)
        item.is_available = is_available
        db.commit()
        db.refresh(item)
        return item

    @staticmethod
    def delete_menu_item(db: Session, item_id: int) -> bool:
        """Xóa một món ăn khỏi thực đơn."""
        item = MenuService.get_menu_item_by_id(db, item_id)
        db.delete(item)
        db.commit()
        return True
