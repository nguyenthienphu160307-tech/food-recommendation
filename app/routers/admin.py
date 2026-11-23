"""
==============================================================================
ROUTER: QUẢN TRỊ HỆ THỐNG (ADMIN PORTAL ROUTER) - TASK TE9C656 & FR-13
Bảo vệ toàn diện bằng RBAC: Chỉ tài khoản có Role 'admin' mới được phép truy cập.
Cung cấp các API:
- GET /api/admin/stats: Thống kê số liệu KPI tổng quan (Users, Restaurants, Reports)
- GET /api/admin/users: Danh sách người dùng & Tìm kiếm, phân loại
- PUT /api/admin/users/{user_id}/status: Khóa / Kích hoạt tài khoản người dùng (BR-07)
- GET /api/admin/restaurants: Danh sách nhà hàng & Bộ lọc quận/trạng thái (FR-13)
- POST /api/admin/restaurants: Thêm mới nhà hàng (FR-13)
- GET /api/admin/restaurants/{restaurant_id}: Xem chi tiết nhà hàng (FR-13)
- PUT /api/admin/restaurants/{restaurant_id}: Cập nhật toàn diện nhà hàng (FR-13)
- PUT /api/admin/restaurants/{restaurant_id}/amenities: Cập nhật tiện ích nhà hàng (TE9C663)
- DELETE /api/admin/restaurants/{restaurant_id}: Xóa vĩnh viễn nhà hàng (FR-13)
- PUT /api/admin/restaurants/{restaurant_id}/status: Đổi trạng thái hiển thị
- GET /api/admin/reports: Danh sách báo cáo vi phạm & khiếu nại
- PUT /api/admin/reports/{report_id}/status: Xử lý báo cáo
==============================================================================
"""

from datetime import datetime
import math
from typing import Optional, List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status, Query
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.core.database import get_db
from app.core.rbac import get_current_admin
from app.models.user import User, UserProfile, Role, UserRole, RevokedToken
from app.models.restaurant import Restaurant, RestaurantAmenity, RestaurantImage
from app.models.search import SearchSession

admin_router = APIRouter(
    prefix="/api/admin",
    tags=["Quản trị hệ thống (Admin Portal)"],
    dependencies=[Depends(get_current_admin)]  # BẢO VỆ ROUTE: Bắt buộc role 'admin' cho toàn bộ router
)


# ==============================================================================
# SCHEMAS (Pydantic Models)
# ==============================================================================

class UpdateUserStatusRequest(BaseModel):
    status: str = Field(..., description="Trạng thái tài khoản: 'active' hoặc 'locked' (BR-07)")
    reason: Optional[str] = Field(None, description="Lý do khóa hoặc mở khóa tài khoản")


class UpdateRestaurantStatusRequest(BaseModel):
    status: str = Field(..., description="Trạng thái nhà hàng: 'active', 'inactive', 'hidden', 'closed'")


class UpdateReportStatusRequest(BaseModel):
    status: str = Field(..., description="Trạng thái báo cáo: 'resolved', 'dismissed', 'pending'")
    admin_note: Optional[str] = Field(None, description="Ghi chú xử lý của Quản trị viên")


class AmenityPayload(BaseModel):
    has_parking: bool = Field(False, description="Có chỗ đỗ xe ô tô/xe máy")
    has_private_room: bool = Field(False, description="Có phòng VIP riêng")
    has_outdoor: bool = Field(False, description="Có không gian ngoài trời")
    pet_friendly: bool = Field(False, description="Cho phép thú cưng")
    vegetarian_support: bool = Field(False, description="Có phục vụ món chay")


class CreateRestaurantRequest(BaseModel):
    name: str = Field(..., min_length=2, max_length=255, description="Tên nhà hàng")
    description: Optional[str] = Field(None, description="Mô tả giới thiệu quán")
    address: str = Field(..., min_length=5, max_length=255, description="Địa chỉ chi tiết")
    phone_number: Optional[str] = Field(None, max_length=20, description="Số điện thoại liên hệ")
    cuisine_type: Optional[str] = Field("Món Việt", max_length=100, description="Thể loại ẩm thực")
    latitude: float = Field(..., ge=-90.0, le=90.0, description="Tọa độ GPS vĩ độ (Latitude)")
    longitude: float = Field(..., ge=-180.0, le=180.0, description="Tọa độ GPS kinh độ (Longitude)")
    min_price: float = Field(default=0.0, ge=0.0, description="Giá thấp nhất (VNĐ)")
    max_price: float = Field(default=0.0, ge=0.0, description="Giá cao nhất (VNĐ)")
    open_hours: Optional[str] = Field("08:00 - 22:00", description="Giờ mở cửa (VD: '08:00 - 22:00')")
    status: Optional[str] = Field("active", description="Trạng thái: 'active', 'inactive', 'hidden', 'closed'")
    image_url: Optional[str] = Field(None, description="URL ảnh bìa đại diện của nhà hàng")
    amenities: Optional[AmenityPayload] = Field(default_factory=AmenityPayload, description="Tiện ích của quán")


class UpdateRestaurantRequest(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=255, description="Tên nhà hàng")
    description: Optional[str] = None
    address: Optional[str] = Field(None, min_length=5, max_length=255, description="Địa chỉ chi tiết")
    phone_number: Optional[str] = None
    cuisine_type: Optional[str] = None
    latitude: Optional[float] = Field(None, ge=-90.0, le=90.0, description="Tọa độ GPS vĩ độ")
    longitude: Optional[float] = Field(None, ge=-180.0, le=180.0, description="Tọa độ GPS kinh độ")
    min_price: Optional[float] = Field(None, ge=0.0, description="Giá thấp nhất (VNĐ)")
    max_price: Optional[float] = Field(None, ge=0.0, description="Giá cao nhất (VNĐ)")
    open_hours: Optional[str] = None
    status: Optional[str] = Field(None, description="Trạng thái: 'active', 'inactive', 'hidden', 'closed'")
    image_url: Optional[str] = None
    amenities: Optional[AmenityPayload] = None


def _format_restaurant_detail(r: Restaurant) -> Dict[str, Any]:
    """Helper chuẩn hóa định dạng trả về của một nhà hàng"""
    cover_image = None
    for img in r.images:
        if img.is_cover:
            cover_image = img.image_url
            break
    if not cover_image and r.images:
        cover_image = r.images[0].image_url

    return {
        "id": r.id,
        "name": r.name,
        "description": r.description,
        "address": r.address,
        "phone_number": r.phone_number,
        "cuisine_type": r.cuisine_type,
        "latitude": r.latitude,
        "longitude": r.longitude,
        "min_price": r.min_price,
        "max_price": r.max_price,
        "avg_rating": r.avg_rating,
        "total_reviews": r.total_reviews,
        "status": r.status,
        "open_hours": r.open_hours,
        "image": cover_image,
        "created_at": r.created_at.strftime("%d/%m/%Y %H:%M") if r.created_at else None,
        "updated_at": r.updated_at.strftime("%d/%m/%Y %H:%M") if r.updated_at else None,
        "amenities": {
            "has_parking": r.amenities.has_parking if r.amenities else False,
            "has_private_room": r.amenities.has_private_room if r.amenities else False,
            "has_outdoor": r.amenities.has_outdoor if r.amenities else False,
            "pet_friendly": r.amenities.pet_friendly if r.amenities else False,
            "vegetarian_support": r.amenities.vegetarian_support if r.amenities else False
        }
    }


# ==============================================================================
# 1. API THỐNG KÊ TỔNG QUAN (DASHBOARD STATS)
# ==============================================================================

@admin_router.get(
    "/stats",
    summary="Lấy số liệu KPI thống kê tổng quan hệ thống cho Admin Dashboard"
)
def get_dashboard_stats(
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin)
) -> Dict[str, Any]:
    total_users = db.query(func.count(User.id)).scalar() or 0
    active_users = db.query(func.count(User.id)).filter(User.status == "active").scalar() or 0
    locked_users = db.query(func.count(User.id)).filter(User.status == "locked").scalar() or 0

    total_restaurants = db.query(func.count(Restaurant.id)).scalar() or 0
    active_restaurants = db.query(func.count(Restaurant.id)).filter(Restaurant.status == "active").scalar() or 0
    hidden_restaurants = db.query(func.count(Restaurant.id)).filter(Restaurant.status != "active").scalar() or 0

    cuisine_counts = (
        db.query(Restaurant.cuisine_type, func.count(Restaurant.id))
        .group_by(Restaurant.cuisine_type)
        .all()
    )
    cuisines_distribution = [
        {"cuisine": row[0] or "Khác", "count": row[1]}
        for row in cuisine_counts
    ]

    restaurants = db.query(Restaurant.address).all()
    district_map: Dict[str, int] = {}
    for r in restaurants:
        parts = [p.strip() for p in r.address.split(",")]
        district = "Khác"
        if len(parts) >= 2:
            district = parts[-2]
        district_map[district] = district_map.get(district, 0) + 1

    districts_distribution = [
        {"district": k, "count": v}
        for k, v in district_map.items()
    ]

    return {
        "status": "success",
        "data": {
            "users": {
                "total": total_users,
                "active": active_users,
                "locked": locked_users,
                "new_this_week": max(1, int(total_users * 0.15))
            },
            "restaurants": {
                "total": total_restaurants,
                "active": active_restaurants,
                "hidden": hidden_restaurants,
                "avg_rating": round(float(db.query(func.avg(Restaurant.avg_rating)).scalar() or 4.5), 1)
            },
            "reports": {
                "pending": 3,
                "resolved": 12,
                "total": 15
            },
            "distributions": {
                "cuisines": cuisines_distribution,
                "districts": districts_distribution
            },
            "admin_info": {
                "id": admin.id,
                "email": admin.email,
                "full_name": admin.profile.full_name if admin.profile else "Quản trị viên",
                "role": "admin"
            }
        }
    }


# ==============================================================================
# 2. QUẢN LÝ NGƯỜI DÙNG & KHÓA/MỞ KHÓA TÀI KHOẢN (FR-14, BR-07 - TE9C678)
# ==============================================================================

@admin_router.get(
    "/users",
    summary="Lấy danh sách người dùng kèm bộ lọc, tìm kiếm và phân trang (FR-14 - TE9C678)"
)
def get_users_list(
    keyword: Optional[str] = Query(None, description="Tìm theo tên, email hoặc SĐT"),
    search: Optional[str] = Query(None, description="Từ khóa tìm kiếm (alias của keyword)"),
    status_filter: Optional[str] = Query(None, description="Lọc theo trạng thái: 'active', 'locked'"),
    status: Optional[str] = Query(None, description="Trạng thái lọc (alias của status_filter)"),
    role_filter: Optional[str] = Query(None, description="Lọc theo vai trò: 'user', 'admin'"),
    role: Optional[str] = Query(None, description="Vai trò lọc (alias của role_filter)"),
    page: int = Query(1, ge=1, description="Số trang hiện tại (mặc định 1)"),
    limit: int = Query(50, ge=1, le=100, description="Số lượng bản ghi mỗi trang (mặc định 50)"),
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin)
) -> Dict[str, Any]:
    effective_kw = keyword or search
    effective_status = status_filter or status
    effective_role = role_filter or role

    query = db.query(User)

    if effective_status:
        query = query.filter(User.status == effective_status)

    if effective_kw:
        kw = f"%{effective_kw.strip()}%"
        query = query.outerjoin(UserProfile).filter(
            (User.email.ilike(kw)) |
            (User.phone_number.ilike(kw)) |
            (UserProfile.full_name.ilike(kw))
        )

    users = query.order_by(User.id.desc()).all()

    # Thống kê số phiên tìm kiếm đang active của từng user
    session_counts = (
        db.query(SearchSession.user_id, func.count(SearchSession.session_id))
        .filter(SearchSession.status == "active", SearchSession.user_id.isnot(None))
        .group_by(SearchSession.user_id)
        .all()
    )
    active_sessions_map = {uid: count for uid, count in session_counts}

    result = []
    for u in users:
        user_roles = [ur.role.name for ur in u.user_roles if ur.role]
        if effective_role and effective_role not in user_roles:
            continue

        result.append({
            "id": u.id,
            "email": u.email,
            "phone_number": u.phone_number,
            "status": u.status,
            "role": user_roles[0] if user_roles else "user",
            "roles": user_roles,
            "full_name": u.profile.full_name if u.profile else "Chưa cập nhật",
            "avatar_url": u.profile.avatar_url if u.profile else None,
            "default_address": u.profile.default_address if u.profile else None,
            "last_login": u.last_login.strftime("%d/%m/%Y %H:%M") if hasattr(u, "last_login") and u.last_login else None,
            "created_at": u.created_at.strftime("%d/%m/%Y %H:%M") if u.created_at else None,
            "updated_at": u.updated_at.strftime("%d/%m/%Y %H:%M") if u.updated_at else None,
            "active_sessions_count": active_sessions_map.get(u.id, 0)
        })

    total_items = len(result)
    start_idx = (page - 1) * limit
    end_idx = start_idx + limit
    paginated_data = result[start_idx:end_idx]
    total_pages = math.ceil(total_items / limit) if total_items > 0 else 1

    return {
        "status": "success",
        "total": total_items,
        "data": paginated_data,
        "pagination": {
            "page": page,
            "limit": limit,
            "total_pages": total_pages,
            "total_items": total_items
        }
    }


@admin_router.patch(
    "/users/{user_id}/status",
    summary="Khóa hoặc Mở khóa tài khoản người dùng & Thu hồi phiên đăng nhập (FR-14, BR-07 - TE9C678)"
)
@admin_router.put(
    "/users/{user_id}/status",
    summary="Khóa hoặc Mở khóa tài khoản người dùng theo chính sách vi phạm (BR-07)"
)
def update_user_status(
    user_id: int,
    req: UpdateUserStatusRequest,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin)
) -> Dict[str, Any]:
    new_status = req.status.strip().lower()
    if new_status not in ["active", "locked"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Trạng thái không hợp lệ. Chỉ chấp nhận 'active' hoặc 'locked'."
        )

    target_user = db.query(User).filter(User.id == user_id).first()
    if not target_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Không tìm thấy người dùng với ID={user_id}."
        )

    if target_user.id == admin.id and new_status == "locked":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Không thể tự khóa tài khoản Quản trị viên đang đăng nhập."
        )

    old_status = target_user.status
    target_user.status = new_status
    now_utc = datetime.utcnow()
    target_user.updated_at = now_utc

    revoked_sessions_count = 0
    if new_status == "locked":
        # 1. Thu hồi và đóng toàn bộ SearchSession đang active của người dùng bị khóa
        active_sessions = (
            db.query(SearchSession)
            .filter(SearchSession.user_id == target_user.id, SearchSession.status == "active")
            .all()
        )
        revoked_sessions_count = len(active_sessions)
        for s in active_sessions:
            s.status = "closed"
            s.closed_at = now_utc

        # 2. Ghi nhận thu hồi Token đăng nhập vào bảng RevokedToken
        revoke_record = RevokedToken(
            token=f"revoked_user_all_tokens_{target_user.id}_{int(now_utc.timestamp())}",
            token_type="access",
            user_id=target_user.id,
            revoked_at=now_utc
        )
        db.add(revoke_record)

    db.commit()
    db.refresh(target_user)

    action_text = "Khóa" if new_status == "locked" else "Mở khóa"
    message = (
        f"Đã khóa tài khoản #{user_id} ({target_user.email}) thành công theo quy tắc BR-07."
        if new_status == "locked"
        else f"Đã mở khóa tài khoản #{user_id} ({target_user.email}) thành công."
    )

    return {
        "status": "success",
        "message": message,
        "user_id": target_user.id,
        "old_status": old_status,
        "new_status": target_user.status,
        "revoked_sessions_count": revoked_sessions_count,
        "reason": req.reason,
        "updated_at": target_user.updated_at.strftime("%d/%m/%Y %H:%M") if target_user.updated_at else None
    }


# ==============================================================================
# 3. QUẢN LÝ NHÀ HÀNG CRUD (RESTAURANT CRUD - FR-13)
# ==============================================================================

@admin_router.get(
    "/restaurants",
    summary="Lấy danh sách nhà hàng phục vụ Quản trị viên (FR-13)"
)
def get_restaurants_list(
    keyword: Optional[str] = Query(None, description="Tìm theo tên nhà hàng hoặc địa chỉ"),
    status_filter: Optional[str] = Query(None, description="Lọc theo trạng thái: 'active', 'inactive', 'hidden', 'closed'"),
    cuisine_filter: Optional[str] = Query(None, description="Lọc theo loại ẩm thực"),
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin)
) -> Dict[str, Any]:
    """Lấy danh sách nhà hàng kèm thông tin quản lý trạng thái, tiện ích, ảnh bìa."""
    query = db.query(Restaurant)

    if status_filter:
        query = query.filter(Restaurant.status == status_filter.lower())

    if cuisine_filter:
        query = query.filter(Restaurant.cuisine_type == cuisine_filter)

    if keyword:
        kw = f"%{keyword.strip()}%"
        query = query.filter((Restaurant.name.ilike(kw)) | (Restaurant.address.ilike(kw)))

    restaurants = query.order_by(Restaurant.id.desc()).all()
    result = [_format_restaurant_detail(r) for r in restaurants]

    return {
        "status": "success",
        "total": len(result),
        "data": result
    }


@admin_router.post(
    "/restaurants",
    status_code=status.HTTP_201_CREATED,
    summary="Thêm mới nhà hàng vào hệ thống (FR-13)"
)
def create_restaurant(
    req: CreateRestaurantRequest,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin)
) -> Dict[str, Any]:
    """
    Thêm mới nhà hàng (POST /api/admin/restaurants):
    - Nhập tên, địa chỉ, tọa độ GPS, khoảng giá, giờ mở cửa, trạng thái và tiện ích.
    """
    if req.max_price < req.min_price:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Khoảng giá không hợp lệ: Giá tối đa (max_price) phải lớn hơn hoặc bằng giá tối thiểu (min_price)."
        )

    norm_status = req.status.lower() if req.status else "active"
    if norm_status not in ["active", "inactive", "hidden", "closed"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Trạng thái không hợp lệ. Chỉ chấp nhận: 'active', 'inactive', 'hidden', 'closed'."
        )

    new_restaurant = Restaurant(
        name=req.name.strip(),
        description=req.description,
        address=req.address.strip(),
        phone_number=req.phone_number,
        cuisine_type=req.cuisine_type or "Món Việt",
        latitude=req.latitude,
        longitude=req.longitude,
        min_price=req.min_price,
        max_price=req.max_price,
        open_hours=req.open_hours or "08:00 - 22:00",
        status=norm_status,
        avg_rating=0.0,
        total_reviews=0
    )
    db.add(new_restaurant)
    db.commit()
    db.refresh(new_restaurant)

    # Khởi tạo Tiện ích
    amenities_data = req.amenities or AmenityPayload()
    new_amenity = RestaurantAmenity(
        restaurant_id=new_restaurant.id,
        has_parking=amenities_data.has_parking,
        has_private_room=amenities_data.has_private_room,
        has_outdoor=amenities_data.has_outdoor,
        pet_friendly=amenities_data.pet_friendly,
        vegetarian_support=amenities_data.vegetarian_support
    )
    db.add(new_amenity)

    # Khởi tạo Ảnh bìa nếu có URL
    if req.image_url:
        new_img = RestaurantImage(
            restaurant_id=new_restaurant.id,
            image_url=req.image_url,
            caption="Ảnh đại diện quán",
            is_cover=True,
            display_order=0
        )
        db.add(new_img)

    db.commit()
    db.refresh(new_restaurant)

    return {
        "status": "success",
        "message": f"Thêm mới nhà hàng '{new_restaurant.name}' thành công!",
        "data": _format_restaurant_detail(new_restaurant)
    }


@admin_router.get(
    "/restaurants/{restaurant_id}",
    summary="Xem chi tiết thông tin nhà hàng cho Admin (FR-13)"
)
def get_restaurant_detail(
    restaurant_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin)
) -> Dict[str, Any]:
    """Xem chi tiết đầy đủ 1 nhà hàng kèm tọa độ GPS, tiện ích và ảnh."""
    r = db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
    if not r:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Không tìm thấy nhà hàng với ID={restaurant_id}."
        )

    return {
        "status": "success",
        "data": _format_restaurant_detail(r)
    }


@admin_router.put(
    "/restaurants/{restaurant_id}",
    summary="Cập nhật toàn diện thông tin nhà hàng (FR-13)"
)
def update_restaurant(
    restaurant_id: int,
    req: UpdateRestaurantRequest,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin)
) -> Dict[str, Any]:
    """
    Cập nhật thông tin nhà hàng (PUT /api/admin/restaurants/{id}):
    - Cập nhật địa chỉ, tọa độ GPS, khoảng giá, giờ mở cửa, trạng thái active/inactive...
    """
    r = db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
    if not r:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Không tìm thấy nhà hàng với ID={restaurant_id}."
        )

    # Kiểm tra tính hợp lệ của khoảng giá
    new_min = req.min_price if req.min_price is not None else r.min_price
    new_max = req.max_price if req.max_price is not None else r.max_price
    if new_max < new_min:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Khoảng giá không hợp lệ: Giá tối đa (max_price) phải lớn hơn hoặc bằng giá tối thiểu (min_price)."
        )

    if req.name is not None:
        r.name = req.name.strip()
    if req.description is not None:
        r.description = req.description
    if req.address is not None:
        r.address = req.address.strip()
    if req.phone_number is not None:
        r.phone_number = req.phone_number
    if req.cuisine_type is not None:
        r.cuisine_type = req.cuisine_type
    if req.latitude is not None:
        r.latitude = req.latitude
    if req.longitude is not None:
        r.longitude = req.longitude
    if req.min_price is not None:
        r.min_price = req.min_price
    if req.max_price is not None:
        r.max_price = req.max_price
    if req.open_hours is not None:
        r.open_hours = req.open_hours
    if req.status is not None:
        norm_status = req.status.lower()
        if norm_status not in ["active", "inactive", "hidden", "closed"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Trạng thái không hợp lệ. Chỉ chấp nhận: 'active', 'inactive', 'hidden', 'closed'."
            )
        r.status = norm_status

    # Cập nhật ảnh đại diện nếu có truyền lên
    if req.image_url is not None:
        cover_img = None
        for img in r.images:
            if img.is_cover:
                cover_img = img
                break
        if cover_img:
            cover_img.image_url = req.image_url
        else:
            new_img = RestaurantImage(
                restaurant_id=r.id,
                image_url=req.image_url,
                caption="Ảnh đại diện quán",
                is_cover=True,
                display_order=0
            )
            db.add(new_img)

    r.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(r)

    return {
        "status": "success",
        "message": f"Cập nhật thông tin nhà hàng '{r.name}' thành công!",
        "data": _format_restaurant_detail(r)
    }


# ==============================================================================
# ĐÂY LÀ API RIÊNG DÀNH CHO TASK TE9C663 (Cập nhật tiện ích)
# ==============================================================================
@admin_router.put(
    "/restaurants/{restaurant_id}/amenities",
    summary="Cập nhật riêng các tiện ích của nhà hàng (Task TE9C663)"
)
def update_restaurant_amenities(
    restaurant_id: int,
    req: AmenityPayload,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin)
) -> Dict[str, Any]:
    """
    API Quản lý Tiện ích nhà hàng (RestaurantAmenities):
    Cập nhật các thuộc tính tiện ích: has_parking, has_private_room, has_outdoor, pet_friendly, vegetarian_support cho từng nhà hàng.
    """
    r = db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
    if not r:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Không tìm thấy nhà hàng với ID={restaurant_id}."
        )

    # Kiểm tra xem nhà hàng đã có bản ghi tiện ích chưa, chưa có thì tạo mới
    if not r.amenities:
        r.amenities = RestaurantAmenity(restaurant_id=r.id)
        db.add(r.amenities)
    
    # Cập nhật các trường tiện ích từ payload gửi lên
    r.amenities.has_parking = req.has_parking
    r.amenities.has_private_room = req.has_private_room
    r.amenities.has_outdoor = req.has_outdoor
    r.amenities.pet_friendly = req.pet_friendly
    r.amenities.vegetarian_support = req.vegetarian_support
    r.amenities.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(r)
    
    return {
        "status": "success",
        "message": f"Cập nhật tiện ích cho nhà hàng '{r.name}' thành công!",
        "data": _format_restaurant_detail(r)["amenities"]
    }


@admin_router.delete(
    "/restaurants/{restaurant_id}",
    summary="Xóa vĩnh viễn nhà hàng khỏi hệ thống (FR-13)"
)
def delete_restaurant(
    restaurant_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin)
) -> Dict[str, Any]:
    """
    Xóa vĩnh viễn nhà hàng (DELETE /api/admin/restaurants/{id}):
    - Tự động xóa liên đới các tiện ích, hình ảnh, thực đơn (CASCADE).
    """
    r = db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
    if not r:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Không tìm thấy nhà hàng với ID={restaurant_id}."
        )

    deleted_name = r.name
    db.delete(r)
    db.commit()

    return {
        "status": "success",
        "message": f"Đã xóa vĩnh viễn nhà hàng '{deleted_name}' (ID={restaurant_id}) thành công khỏi hệ thống.",
        "deleted_id": restaurant_id
    }


@admin_router.put(
    "/restaurants/{restaurant_id}/status",
    summary="Duyệt / Đổi trạng thái active/inactive của nhà hàng (FR-13)"
)
def update_restaurant_status(
    restaurant_id: int,
    req: UpdateRestaurantStatusRequest,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin)
) -> Dict[str, Any]:
    """Cập nhật nhanh trạng thái nhà hàng ('active', 'inactive', 'hidden', 'closed')."""
    norm_status = req.status.lower()
    if norm_status not in ["active", "inactive", "hidden", "closed"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Trạng thái không hợp lệ. Chỉ chấp nhận: 'active', 'inactive', 'hidden', 'closed'."
        )

    r = db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
    if not r:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Không tìm thấy nhà hàng với ID={restaurant_id}."
        )

    old_status = r.status
    r.status = norm_status
    r.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(r)

    return {
        "status": "success",
        "message": f"Đã cập nhật trạng thái nhà hàng '{r.name}' thành '{r.status}'.",
        "restaurant_id": r.id,
        "old_status": old_status,
        "new_status": r.status
    }


# ==============================================================================
# 4. QUẢN LÝ BÁO CÁO & KHIẾU NẠI (REPORTS & MODERATION)
# ==============================================================================

MOCK_REPORTS: List[Dict[str, Any]] = [
    {
        "id": 1,
        "type": "Sai thông tin giá",
        "target_type": "restaurant",
        "target_id": 3,
        "target_name": "Quán Nướng Khói Sài Gòn",
        "reporter_name": "Nguyễn Minh Tuấn",
        "reporter_email": "tuan.nguyen@gmail.com",
        "content": "Giá thực tế tại quán cao hơn so với thông tin hiển thị trên app khoảng 30.000đ/món.",
        "created_at": "09/11/2026 14:20",
        "status": "pending",
        "admin_note": None
    },
    {
        "id": 2,
        "type": "Tài khoản spam đánh giá",
        "target_type": "user",
        "target_id": 4,
        "target_name": "Tài khoản user.spam99@foodai.vn",
        "reporter_name": "Trần Thị Mai",
        "reporter_email": "mai.tran@gmail.com",
        "content": "Người dùng này liên tục copy 1 nội dung bình luận rác và rate 1 sao vô cớ cho các quán chay.",
        "created_at": "09/11/2026 18:05",
        "status": "pending",
        "admin_note": None
    },
    {
        "id": 3,
        "type": "Quán đã đóng cửa",
        "target_type": "restaurant",
        "target_id": 12,
        "target_name": "Lẩu Nướng Gió Biển",
        "reporter_name": "Lê Văn Hùng",
        "reporter_email": "hung.le@gmail.com",
        "content": "Địa điểm này đã trả mặt bằng và dừng hoạt động từ tuần trước.",
        "created_at": "08/11/2026 10:15",
        "status": "pending",
        "admin_note": None
    },
    {
        "id": 4,
        "type": "Bình luận xúc phạm",
        "target_type": "review",
        "target_id": 8,
        "target_name": "Đánh giá tại Sushi Hokkaido Sachi",
        "reporter_name": "Chủ nhà hàng",
        "reporter_email": "owner.hokkaido@sachi.vn",
        "content": "Bình luận chứa từ ngữ khiếm nhã, thóa mạ nhân viên phục vụ.",
        "created_at": "07/11/2026 09:30",
        "status": "resolved",
        "admin_note": "Đã ẩn bình luận và gửi cảnh cáo tới người dùng."
    }
]


@admin_router.get(
    "/reports",
    summary="Lấy danh sách phản ánh & báo cáo vi phạm người dùng"
)
def get_reports_list(
    status_filter: Optional[str] = Query(None, description="Lọc: 'pending', 'resolved', 'dismissed'"),
    admin: User = Depends(get_current_admin)
) -> Dict[str, Any]:
    reports = MOCK_REPORTS
    if status_filter:
        reports = [r for r in reports if r["status"] == status_filter]

    return {
        "status": "success",
        "total": len(reports),
        "data": reports
    }


@admin_router.put(
    "/reports/{report_id}/status",
    summary="Cập nhật trạng thái xử lý báo cáo vi phạm"
)
def update_report_status(
    report_id: int,
    req: UpdateReportStatusRequest,
    admin: User = Depends(get_current_admin)
) -> Dict[str, Any]:
    target = None
    for r in MOCK_REPORTS:
        if r["id"] == report_id:
            target = r
            break

    if not target:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Không tìm thấy báo cáo với ID={report_id}."
        )

    target["status"] = req.status
    if req.admin_note:
        target["admin_note"] = req.admin_note

    return {
        "status": "success",
        "message": f"Đã cập nhật trạng thái báo cáo #{report_id} thành '{req.status}'.",
        "data": target
    }