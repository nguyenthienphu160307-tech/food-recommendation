from typing import List, Optional
from fastapi import APIRouter, Depends, status, UploadFile, File, Form
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.image_service import ImageService
from app.schemas.image import (
    RestaurantImageCreate,
    RestaurantImageBatchCreate,
    RestaurantImageUpdate,
    RestaurantImageResponse,
    SetCoverResponse,
)

router = APIRouter(tags=["Quản lý Hình ảnh Nhà hàng (RestaurantImages - TSK-28)"])


# =====================================================================
# 1. API TRUY VẤN VÀ THÊM HÌNH ẢNH (RestaurantImages)
# =====================================================================

@router.get(
    "/api/restaurants/{restaurant_id}/images",
    response_model=List[RestaurantImageResponse],
    status_code=status.HTTP_200_OK,
    summary="Lấy toàn bộ thư viện hình ảnh của nhà hàng"
)
def get_restaurant_images(
    restaurant_id: int,
    db: Session = Depends(get_db)
):
    """
    Truy vấn thư viện ảnh của một nhà hàng:
    - Sắp xếp ưu tiên: Ảnh bìa chính lên đầu (`is_cover=True`), sau đó theo thứ tự hiển thị `display_order`.
    """
    return ImageService.get_images_by_restaurant(db, restaurant_id)


@router.post(
    "/api/restaurants/{restaurant_id}/images",
    response_model=RestaurantImageResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Thêm ảnh mới bằng đường link URL (Admin - UC-06b)"
)
def add_restaurant_image(
    restaurant_id: int,
    payload: RestaurantImageCreate,
    db: Session = Depends(get_db)
):
    """
    Thêm một ảnh mới bằng link URL:
    - Nếu `is_cover: true`: Tự động tắt ảnh bìa cũ của quán.
    - Nếu quán chưa có ảnh nào: Tự động gán ảnh đầu tiên này làm ảnh bìa.
    """
    return ImageService.add_image_url(db, restaurant_id, payload)


@router.post(
    "/api/restaurants/{restaurant_id}/images/batch",
    response_model=List[RestaurantImageResponse],
    status_code=status.HTTP_201_CREATED,
    summary="Thêm nhiều ảnh cùng lúc bằng danh sách URLs (Admin - UC-06b)"
)
def add_restaurant_images_batch(
    restaurant_id: int,
    payload: RestaurantImageBatchCreate,
    db: Session = Depends(get_db)
):
    """Thêm hàng loạt ảnh bằng danh sách đường dẫn URL."""
    return ImageService.add_batch_images(db, restaurant_id, payload.images)


@router.post(
    "/api/restaurants/{restaurant_id}/images/upload",
    response_model=List[RestaurantImageResponse],
    status_code=status.HTTP_201_CREATED,
    summary="Tải lên một hoặc nhiều tệp ảnh thực tế (Multiple Uploads - TSK-28)"
)
async def upload_restaurant_images(
    restaurant_id: int,
    files: List[UploadFile] = File(..., description="Danh sách các file ảnh (.jpg, .jpeg, .png, .webp)"),
    set_first_as_cover: bool = Form(False, description="Đặt ảnh đầu tiên trong đợt tải lên làm ảnh bìa"),
    db: Session = Depends(get_db)
):
    """
    API hỗ trợ tải lên nhiều tệp ảnh cùng lúc cho nhà hàng (Multipart/Form-Data):
    1. Kiểm tra định dạng đuôi file hợp lệ (.jpg, .png, .webp).
    2. Lưu trữ tệp vật lý vào thư mục `/static/uploads/restaurants/restaurant_{id}/`.
    3. Ghi thông tin vào CSDL MySQL.
    """
    return await ImageService.upload_multiple_files(
        db=db,
        restaurant_id=restaurant_id,
        files=files,
        set_first_as_cover=set_first_as_cover
    )


# =====================================================================
# 2. API QUẢN TRỊ ẢNH CHI TIẾT (Chi tiết, Cập nhật, Đặt ảnh bìa, Xóa)
# =====================================================================

@router.get(
    "/api/restaurant-images/{image_id}",
    response_model=RestaurantImageResponse,
    status_code=status.HTTP_200_OK,
    summary="Lấy thông tin chi tiết một bức ảnh"
)
def get_image_detail(
    image_id: int,
    db: Session = Depends(get_db)
):
    """Truy vấn thông tin chi tiết một bức ảnh cụ thể."""
    return ImageService.get_image_by_id(db, image_id)


@router.put(
    "/api/restaurant-images/{image_id}",
    response_model=RestaurantImageResponse,
    status_code=status.HTTP_200_OK,
    summary="Cập nhật chú thích và thứ tự hiển thị của ảnh (Admin - UC-06b)"
)
def update_image_info(
    image_id: int,
    payload: RestaurantImageUpdate,
    db: Session = Depends(get_db)
):
    """Chỉnh sửa chú thích (`caption`) và thứ tự hiển thị (`display_order`)."""
    return ImageService.update_image(db, image_id, payload)


@router.patch(
    "/api/restaurant-images/{image_id}/set-cover",
    response_model=SetCoverResponse,
    status_code=status.HTTP_200_OK,
    summary="Đặt một ảnh làm ảnh bìa chính của nhà hàng (Admin - UC-06b)"
)
def set_cover_image(
    image_id: int,
    db: Session = Depends(get_db)
):
    """
    Chỉ định ảnh đại diện chính cho nhà hàng:
    - Ảnh được chọn sẽ có `is_cover = true`.
    - Toàn bộ ảnh khác của nhà hàng đó sẽ tự động chuyển về `is_cover = false`.
    """
    updated_img = ImageService.set_cover_image(db, image_id)
    return SetCoverResponse(
        image_id=updated_img.id,
        restaurant_id=updated_img.restaurant_id,
        is_cover=True,
        message=f"Đã đặt hình ảnh #{image_id} làm ảnh bìa chính của nhà hàng thành công!"
    )


@router.delete(
    "/api/restaurant-images/{image_id}",
    status_code=status.HTTP_200_OK,
    summary="Xóa một bức ảnh khỏi thư viện (Admin - UC-06b)"
)
def delete_restaurant_image(
    image_id: int,
    db: Session = Depends(get_db)
):
    """
    Xóa một hình ảnh khỏi thư viện:
    - Xóa bản ghi trong CSDL và dọn dẹp file tĩnh trên đĩa (nếu có).
    - Nếu ảnh bị xóa là ảnh bìa, tự động chọn ảnh còn lại làm ảnh bìa mới.
    """
    ImageService.delete_image(db, image_id)
    return {
        "status": "success",
        "message": f"Đã xóa hình ảnh #{image_id} khỏi thư viện thành công."
    }
