from datetime import datetime
from sqlalchemy import (
    Column, Integer, String, Float, Boolean, DateTime, Text, ForeignKey, Index
)
from sqlalchemy.orm import relationship
from app.core.database import Base


class Restaurant(Base):
    """
    1. Bảng lưu trữ thông tin cốt lõi của Nhà hàng (Restaurants)
    - Quản lý địa chỉ, thông tin liên hệ, khoảng giá và tọa độ địa lý (GPS)
    - Tích hợp Composite Index trên tọa độ (latitude, longitude) và khoảng giá (min_price, max_price)
    """
    __tablename__ = "restaurants"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    address = Column(String(255), nullable=False)
    phone_number = Column(String(20), nullable=True)
    cuisine_type = Column(String(100), nullable=True, index=True)  # VD: "Món Việt", "Lẩu Nướng", "Món Nhật"
    
    # Tọa độ GPS phục vụ tính khoảng cách và hiển thị bản đồ
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)

    # Khoảng giá phục vụ bộ lọc ngân sách
    min_price = Column(Float, default=0.0, nullable=False, index=True)
    max_price = Column(Float, default=0.0, nullable=False, index=True)

    open_hours = Column(String(100), nullable=True)               # VD: "08:00 - 22:00"
    avg_rating = Column(Float, default=0.0, nullable=False, index=True)  # Điểm đánh giá trung bình (1.0 -> 5.0)
    total_reviews = Column(Integer, default=0, nullable=False)     # Tổng số lượt đánh giá
    status = Column(String(20), default="active", nullable=False) # 'active', 'closed', 'hidden'
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Khai báo các Chỉ mục tối ưu hóa truy vấn không gian & bộ lọc (TSK-06)
    __table_args__ = (
        Index("idx_restaurant_coords", "latitude", "longitude"),        # Tăng tốc độ tính khoảng cách & Bounding Box
        Index("idx_restaurant_price_range", "min_price", "max_price"), # Tăng tốc bộ lọc theo khoảng giá
    )

    # Các mối quan hệ liên kết (Relationships)
    amenities = relationship("RestaurantAmenity", back_populates="restaurant", uselist=False, cascade="all, delete-orphan")
    menus = relationship("RestaurantMenu", back_populates="restaurant", cascade="all, delete-orphan")
    images = relationship("RestaurantImage", back_populates="restaurant", cascade="all, delete-orphan")


class RestaurantAmenity(Base):
    """
    2. Bảng lưu trữ 5 tiện ích đặc trưng của Nhà hàng (RestaurantAmenities)
    - Mỗi cờ tiện ích đều được đánh Index để phục vụ lọc đa điều kiện cực nhanh
    """
    __tablename__ = "restaurant_amenities"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    restaurant_id = Column(Integer, ForeignKey("restaurants.id", ondelete="CASCADE"), nullable=False, unique=True)
    
    has_parking = Column(Boolean, default=False, nullable=False, index=True)         # Có chỗ đậu ô tô / xe máy
    has_private_room = Column(Boolean, default=False, nullable=False, index=True)    # Có phòng riêng VIP
    has_outdoor = Column(Boolean, default=False, nullable=False, index=True)         # Có không gian ngoài trời / sân vườn
    pet_friendly = Column(Boolean, default=False, nullable=False, index=True)        # Thân thiện với thú cưng
    vegetarian_support = Column(Boolean, default=False, nullable=False, index=True)  # Có món chay phục vụ
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    restaurant = relationship("Restaurant", back_populates="amenities")


class RestaurantMenu(Base):
    """
    3. Bảng danh mục thực đơn của Nhà hàng (RestaurantMenus)
    - Phân chia nhóm món (VD: Khai vị, Món chính, Đồ uống, Tráng miệng)
    """
    __tablename__ = "restaurant_menus"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    restaurant_id = Column(Integer, ForeignKey("restaurants.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(100), nullable=False)                    # Tên danh mục (VD: 'Món Nướng', 'Đồ Uống')
    description = Column(String(255), nullable=True)
    display_order = Column(Integer, default=0, nullable=False)    # Thứ tự hiển thị
    created_at = Column(DateTime, default=datetime.utcnow)

    restaurant = relationship("Restaurant", back_populates="menus")
    items = relationship("MenuItem", back_populates="menu", cascade="all, delete-orphan")


class MenuItem(Base):
    """
    4. Bảng chi tiết từng món ăn trong thực đơn (MenuItems)
    - Lưu tên món, giá tiền, ảnh minh họa và trạng thái phục vụ
    """
    __tablename__ = "menu_items"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    menu_id = Column(Integer, ForeignKey("restaurant_menus.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(150), nullable=False, index=True)
    description = Column(Text, nullable=True)
    price = Column(Float, nullable=False, default=0.0)
    image_url = Column(String(500), nullable=True)
    is_available = Column(Boolean, default=True, nullable=False)   # Còn món hay hết món
    created_at = Column(DateTime, default=datetime.utcnow)

    menu = relationship("RestaurantMenu", back_populates="items")


class RestaurantImage(Base):
    """
    5. Bảng thư viện hình ảnh của Nhà hàng (RestaurantImages)
    - Quản lý ảnh không gian quán, chọn ảnh bìa (is_cover) và thứ tự hiển thị
    """
    __tablename__ = "restaurant_images"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    restaurant_id = Column(Integer, ForeignKey("restaurants.id", ondelete="CASCADE"), nullable=False, index=True)
    image_url = Column(String(500), nullable=False)
    caption = Column(String(255), nullable=True)                  # Chú thích ảnh (VD: "Không gian ngoài trời")
    is_cover = Column(Boolean, default=False, nullable=False, index=True)  # Cờ đánh dấu ảnh đại diện / ảnh bìa
    display_order = Column(Integer, default=0, nullable=False)    # Thứ tự sắp xếp ảnh
    created_at = Column(DateTime, default=datetime.utcnow)

    restaurant = relationship("Restaurant", back_populates="images")
