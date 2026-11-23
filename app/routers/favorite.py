from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.rbac import get_current_user, get_current_guest_or_user
from app.models.user import User
from app.services.favorite_service import FavoriteService
from app.schemas.favorite import (
    FavoriteCreateRequest,
    FavoriteDeleteRequest,
    FavoriteItemResponse,
    FavoriteListResponse,
    FavoriteActionResponse,
    FavoriteCheckResponse,
)

router = APIRouter(prefix="/api/favorites", tags=["Danh sách Yêu thích (Favorites - FR-11, UC-08 / TE9C67D)"])


def _resolve_user_id(
    current_user: Optional[User],
    explicit_user_id: Optional[int] = None
) -> int:
    """Xác định user_id từ JWT Token (BR-01) hoặc fallback tham số trực tiếp trong Unit Test"""
    if current_user is not None and getattr(current_user, "id", None) is not None:
        return current_user.id
    if explicit_user_id is not None and not hasattr(explicit_user_id, "default"):
        return explicit_user_id
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Vui lòng đăng nhập tài khoản để thực hiện chức năng này (BR-01).",
        headers={"WWW-Authenticate": "Bearer"}
    )


@router.post(
    "",
    response_model=FavoriteActionResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Lưu nhà hàng vào danh sách yêu thích (Task TE9C67D / FR-11, UC-08)"
)
def add_favorite(
    payload: FavoriteCreateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    API Lưu Nhà hàng vào Danh sách Yêu thích (Task TE9C67D / FR-11, UC-08):
    - Yêu cầu xác thực tài khoản qua JWT Token (BR-01).
    - Kiểm tra trạng thái tài khoản không bị khóa (BR-07).
    - Kiểm tra tính tồn tại của nhà hàng (Restaurants).
    - Ràng buộc UNIQUE(user_id, restaurant_id): Chặn trùng lặp, trả về HTTP 409 Conflict nếu đã lưu.
    - Trả về HTTP 201 Created khi lưu thành công.
    """
    user_id = _resolve_user_id(current_user, payload.user_id)
    fav = FavoriteService.add_favorite(
        db=db,
        user_id=user_id,
        restaurant_id=payload.restaurant_id,
        note=payload.note
    )

    return FavoriteActionResponse(
        status="success",
        task_code="TE9C67D",
        message="Đã lưu nhà hàng vào danh sách yêu thích thành công.",
        favorite_id=fav.id,
        restaurant_id=fav.restaurant_id,
        is_favorite=True
    )


@router.delete(
    "/{restaurant_id}",
    response_model=FavoriteActionResponse,
    status_code=status.HTTP_200_OK,
    summary="Bỏ lưu nhà hàng khỏi danh sách yêu thích qua Path Param (Task TE9C67D / FR-11, UC-08)"
)
def delete_favorite_by_path(
    restaurant_id: int,
    user_id: Optional[int] = Query(None, description="ID người dùng (tùy chọn khi gọi Unit Test)"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    API Bỏ lưu Nhà hàng khỏi Danh sách Yêu thích (DELETE /api/favorites/{restaurant_id}):
    - Yêu cầu đăng nhập tài khoản (BR-01).
    - Tìm và xóa bản ghi `UserFavorite` của user_id và restaurant_id.
    - Trả về HTTP 404 Not Found nếu nhà hàng chưa từng được lưu trong danh sách.
    """
    uid = _resolve_user_id(current_user, user_id)
    FavoriteService.remove_favorite(
        db=db,
        user_id=uid,
        restaurant_id=restaurant_id
    )

    return FavoriteActionResponse(
        status="success",
        task_code="TE9C67D",
        message=f"Đã bỏ lưu nhà hàng #{restaurant_id} khỏi danh sách yêu thích.",
        restaurant_id=restaurant_id,
        is_favorite=False
    )


@router.delete(
    "",
    response_model=FavoriteActionResponse,
    status_code=status.HTTP_200_OK,
    summary="Bỏ lưu nhà hàng khỏi danh sách yêu thích qua Query/Payload (Task TE9C67D)"
)
def delete_favorite(
    restaurant_id: Optional[int] = Query(None, description="ID nhà hàng cần bỏ lưu"),
    payload: Optional[FavoriteDeleteRequest] = None,
    user_id: Optional[int] = Query(None, description="ID người dùng (tùy chọn khi gọi Unit Test)"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Hỗ trợ bỏ lưu nhà hàng qua Query Parameter hoặc Payload (DELETE /api/favorites)"""
    target_rid = restaurant_id
    explicit_uid = user_id
    if payload:
        if payload.restaurant_id:
            target_rid = payload.restaurant_id
        if payload.user_id:
            explicit_uid = payload.user_id

    if not target_rid or hasattr(target_rid, "default"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Vui lòng cung cấp restaurant_id cần bỏ lưu."
        )

    uid = _resolve_user_id(current_user, explicit_uid)
    FavoriteService.remove_favorite(
        db=db,
        user_id=uid,
        restaurant_id=target_rid
    )

    return FavoriteActionResponse(
        status="success",
        task_code="TE9C67D",
        message=f"Đã bỏ lưu nhà hàng #{target_rid} khỏi danh sách yêu thích.",
        restaurant_id=target_rid,
        is_favorite=False
    )


@router.get(
    "",
    response_model=FavoriteListResponse,
    status_code=status.HTTP_200_OK,
    summary="Xem danh sách nhà hàng yêu thích của tôi (Task TE9C67D / FR-11, UC-08)"
)
def get_my_favorites(
    page: int = Query(1, ge=1, description="Số thứ tự trang (1-based)"),
    limit: int = Query(10, ge=1, le=100, description="Số lượng nhà hàng trên mỗi trang"),
    sort_by: str = Query("newest", description="Tiêu chí sắp xếp: 'newest', 'rating', 'price_asc', 'price_desc', 'distance'"),
    lat: Optional[float] = Query(None, ge=-90.0, le=90.0, description="Vĩ độ người dùng để tính khoảng cách"),
    lng: Optional[float] = Query(None, ge=-180.0, le=180.0, description="Kinh độ người dùng để tính khoảng cách"),
    user_id: Optional[int] = Query(None, description="ID người dùng (tùy chọn khi gọi Unit Test)"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    API Xem Danh sách Nhà hàng Yêu thích (GET /api/favorites):
    - Bắt buộc đăng nhập tài khoản (BR-01).
    - Trả về danh sách quán đã lưu kèm ảnh bìa, tiện ích, điểm đánh giá, trạng thái giờ mở cửa thực tế (BR-03).
    - Hỗ trợ tính khoảng cách GPS khi truyền tọa độ `lat` và `lng`.
    - Phân trang chuẩn RESTful (page, limit, total, total_pages).
    """
    uid = _resolve_user_id(current_user, user_id)
    return FavoriteService.get_user_favorites(
        db=db,
        user_id=uid,
        page=page,
        limit=limit,
        sort_by=sort_by,
        lat=lat,
        lng=lng
    )


@router.get(
    "/check/{restaurant_id}",
    response_model=FavoriteCheckResponse,
    status_code=status.HTTP_200_OK,
    summary="Kiểm tra trạng thái yêu thích của một nhà hàng (Task TE9C67D)"
)
def check_favorite_status(
    restaurant_id: int,
    user_id: Optional[int] = Query(None, description="ID người dùng (tùy chọn khi gọi Unit Test)"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Kiểm tra nhanh xem người dùng hiện tại đã bookmark nhà hàng này chưa (phục vụ biểu tượng Trái tim trên UI)"""
    uid = _resolve_user_id(current_user, user_id)
    return FavoriteService.check_favorite_status(
        db=db,
        user_id=uid,
        restaurant_id=restaurant_id
    )
