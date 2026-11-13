import os
import uuid
import shutil
from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status, UploadFile

from app.models.restaurant import Restaurant, RestaurantImage
from app.schemas.image import (
    RestaurantImageCreate,
    RestaurantImageUpdate,
)

# Thư mục lưu trữ tệp ảnh tĩnh tải lên
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
UPLOAD_DIR = os.path.join(BASE_DIR, "frontend", "uploads", "restaurants")

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".gif"}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB


class ImageService:
    """
    Tầng Service / Repository xử lý toàn bộ nghiệp vụ Quản lý Hình ảnh Nhà hàng (TSK-28 / PBI-16):
    - Thêm ảnh bằng URL hoặc tải lên nhiều tệp (Multiple Uploads).
    - Quản lý cơ chế Ảnh bìa duy nhất (is_cover): Tự động tắt ảnh bìa cũ khi đặt ảnh bìa mới.
    - Sắp xếp thứ tự hiển thị (display_order).
    - Xóa ảnh kèm dọn dẹp file tĩnh và tự động chỉ định ảnh bìa kế tiếp.
    """

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
    def get_images_by_restaurant(
        db: Session,
        restaurant_id: int
    ) -> List[RestaurantImage]:
        """
        Lấy danh sách toàn bộ hình ảnh của nhà hàng:
        - Sắp xếp ưu tiên: Ảnh bìa chính lên đầu (is_cover DESC), sau đó theo display_order ASC, id ASC.
        """
        ImageService.get_restaurant_or_404(db, restaurant_id)
        return (
            db.query(RestaurantImage)
            .filter(RestaurantImage.restaurant_id == restaurant_id)
            .order_by(
                RestaurantImage.is_cover.desc(),
                RestaurantImage.display_order.asc(),
                RestaurantImage.id.asc()
            )
            .all()
        )

    @staticmethod
    def add_image_url(
        db: Session,
        restaurant_id: int,
        payload: RestaurantImageCreate
    ) -> RestaurantImage:
        """
        Thêm một ảnh mới cho nhà hàng bằng URL:
        - Nếu đánh dấu is_cover = True: Tự động chuyển toàn bộ ảnh cũ về is_cover = False.
        - Nếu nhà hàng chưa có ảnh nào: Tự động gán ảnh đầu tiên này làm is_cover = True.
        """
        ImageService.get_restaurant_or_404(db, restaurant_id)

        # Đếm số lượng ảnh hiện có của quán
        existing_count = (
            db.query(RestaurantImage)
            .filter(RestaurantImage.restaurant_id == restaurant_id)
            .count()
        )

        should_be_cover = payload.is_cover or (existing_count == 0)

        if should_be_cover:
            # Tắt cờ is_cover của toàn bộ ảnh hiện tại
            db.query(RestaurantImage).filter(
                RestaurantImage.restaurant_id == restaurant_id
            ).update({"is_cover": False})

        new_image = RestaurantImage(
            restaurant_id=restaurant_id,
            image_url=payload.image_url.strip(),
            caption=payload.caption.strip() if payload.caption else None,
            is_cover=should_be_cover,
            display_order=payload.display_order if payload.display_order > 0 else (existing_count + 1)
        )
        db.add(new_image)
        db.commit()
        db.refresh(new_image)
        return new_image

    @staticmethod
    def add_batch_images(
        db: Session,
        restaurant_id: int,
        images_payload: List[RestaurantImageCreate]
    ) -> List[RestaurantImage]:
        """Thêm nhiều ảnh cùng lúc bằng danh sách URLs."""
        ImageService.get_restaurant_or_404(db, restaurant_id)
        created_images = []
        for p in images_payload:
            img = ImageService.add_image_url(db, restaurant_id, p)
            created_images.append(img)
        return created_images

    @staticmethod
    async def upload_multiple_files(
        db: Session,
        restaurant_id: int,
        files: List[UploadFile],
        captions: Optional[List[str]] = None,
        set_first_as_cover: bool = False
    ) -> List[RestaurantImage]:
        """
        Tải lên nhiều tệp ảnh thực tế từ thiết bị của Admin:
        - Kiểm tra định dạng hợp lệ (.jpg, .jpeg, .png, .webp, .gif).
        - Lưu vào thư mục static trên máy chủ: `frontend/uploads/restaurants/{id}/`.
        - Ghi nhận thông tin vào bảng RestaurantImages.
        """
        ImageService.get_restaurant_or_404(db, restaurant_id)

        if not files or len(files) == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Vui lòng chọn ít nhất một tệp ảnh để tải lên."
            )

        # Tạo thư mục lưu trữ nếu chưa có
        rest_upload_dir = os.path.join(UPLOAD_DIR, f"restaurant_{restaurant_id}")
        os.makedirs(rest_upload_dir, exist_ok=True)

        existing_count = (
            db.query(RestaurantImage)
            .filter(RestaurantImage.restaurant_id == restaurant_id)
            .count()
        )

        saved_records = []
        for idx, file in enumerate(files):
            # Kiểm tra đuôi mở rộng file
            ext = os.path.splitext(file.filename)[1].lower() if file.filename else ""
            if ext not in ALLOWED_EXTENSIONS:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Định dạng tệp '{file.filename}' không được hỗ trợ. Chỉ chấp nhận các định dạng: {', '.join(ALLOWED_EXTENSIONS)}."
                )

            # Đặt tên tệp ngẫu nhiên chống trùng lặp
            unique_filename = f"{uuid.uuid4().hex[:12]}_{int(uuid.uuid1().time)}{ext}"
            file_path = os.path.join(rest_upload_dir, unique_filename)

            # Lưu file vào đĩa
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)

            # Đường dẫn tĩnh phục vụ qua web
            web_url = f"/static/uploads/restaurants/restaurant_{restaurant_id}/{unique_filename}"

            # Xác định cờ is_cover
            is_cover = False
            if (existing_count == 0 and idx == 0) or (set_first_as_cover and idx == 0):
                # Tắt cover cũ
                db.query(RestaurantImage).filter(
                    RestaurantImage.restaurant_id == restaurant_id
                ).update({"is_cover": False})
                is_cover = True

            caption = None
            if captions and idx < len(captions) and captions[idx]:
                caption = captions[idx].strip()
            elif file.filename:
                caption = os.path.splitext(file.filename)[0].replace("-", " ").replace("_", " ")

            new_img = RestaurantImage(
                restaurant_id=restaurant_id,
                image_url=web_url,
                caption=caption,
                is_cover=is_cover,
                display_order=existing_count + idx + 1
            )
            db.add(new_img)
            saved_records.append(new_img)

        db.commit()
        for r in saved_records:
            db.refresh(r)
        return saved_records

    @staticmethod
    def get_image_by_id(db: Session, image_id: int) -> RestaurantImage:
        """Lấy chi tiết một ảnh theo ID. Nếu không có -> 404."""
        img = db.query(RestaurantImage).filter(RestaurantImage.id == image_id).first()
        if not img:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Không tìm thấy hình ảnh với ID={image_id}."
            )
        return img

    @staticmethod
    def update_image(
        db: Session,
        image_id: int,
        payload: RestaurantImageUpdate
    ) -> RestaurantImage:
        """Cập nhật chú thích và thứ tự hiển thị của ảnh."""
        img = ImageService.get_image_by_id(db, image_id)

        if payload.caption is not None:
            img.caption = payload.caption.strip() if payload.caption else None
        if payload.display_order is not None:
            img.display_order = payload.display_order

        db.commit()
        db.refresh(img)
        return img

    @staticmethod
    def set_cover_image(db: Session, image_id: int) -> RestaurantImage:
        """
        Chỉ định một ảnh làm ảnh bìa chính (is_cover = True):
        - Tự động chuyển toàn bộ các ảnh khác của nhà hàng đó về is_cover = False.
        """
        img = ImageService.get_image_by_id(db, image_id)

        # 1. Tắt ảnh bìa cũ của nhà hàng này
        db.query(RestaurantImage).filter(
            RestaurantImage.restaurant_id == img.restaurant_id,
            RestaurantImage.id != image_id
        ).update({"is_cover": False})

        # 2. Bật ảnh bìa cho ảnh này
        img.is_cover = True
        db.commit()
        db.refresh(img)
        return img

    @staticmethod
    def delete_image(db: Session, image_id: int) -> bool:
        """
        Xóa một hình ảnh khỏi CSDL và xóa file vật lý nếu là file upload nội bộ:
        - Nếu ảnh bị xóa đang là ảnh bìa: Tự động chỉ định ảnh đầu tiên còn lại làm ảnh bìa mới.
        """
        img = ImageService.get_image_by_id(db, image_id)
        restaurant_id = img.restaurant_id
        was_cover = img.is_cover

        # Nếu là file upload nội bộ -> thử xóa file trên đĩa
        if img.image_url and img.image_url.startswith("/static/uploads/"):
            relative_path = img.image_url.replace("/static/", "")
            full_disk_path = os.path.join(BASE_DIR, "frontend", relative_path)
            if os.path.exists(full_disk_path):
                try:
                    os.remove(full_disk_path)
                except OSError:
                    pass

        db.delete(img)
        db.commit()

        # Nếu ảnh vừa xóa là ảnh bìa, tìm ảnh còn lại để nâng cấp làm ảnh bìa mới
        if was_cover:
            next_img = (
                db.query(RestaurantImage)
                .filter(RestaurantImage.restaurant_id == restaurant_id)
                .order_by(RestaurantImage.display_order.asc(), RestaurantImage.id.asc())
                .first()
            )
            if next_img:
                next_img.is_cover = True
                db.commit()

        return True
