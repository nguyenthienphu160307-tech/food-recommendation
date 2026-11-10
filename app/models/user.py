from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
from app.core.database import Base

class User(Base):
    """Bảng lưu thông tin tài khoản đăng nhập (Users)"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String(255), unique=True, index=True, nullable=True)
    phone_number = Column(String(20), unique=True, index=True, nullable=True)
    hashed_password = Column(String(255), nullable=False)
    status = Column(String(20), default="active", nullable=False)  # 'active', 'locked' (BR-07)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Quan hệ 1 - 1 với bảng UserProfiles
    profile = relationship("UserProfile", back_populates="user", uselist=False, cascade="all, delete-orphan")
    # Quan hệ 1 - 1 với bảng UserPreferences (Sở thích cá nhân & Dị ứng)
    preference = relationship("UserPreference", back_populates="user", uselist=False, cascade="all, delete-orphan")
    # Quan hệ 1 - N với bảng UserRoles
    user_roles = relationship("UserRole", back_populates="user", cascade="all, delete-orphan")

    @property
    def roles(self):
        """Danh sách tên vai trò của người dùng (VD: ['user'], ['admin'])"""
        return [ur.role.name for ur in self.user_roles if ur.role]


class UserProfile(Base):
    """Bảng lưu hồ sơ chi tiết người dùng (UserProfiles)"""
    __tablename__ = "user_profiles"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True)
    full_name = Column(String(100), nullable=False)
    avatar_url = Column(String(500), nullable=True)
    default_address = Column(String(255), nullable=True)
    default_lat = Column(Float, nullable=True)
    default_lng = Column(Float, nullable=True)

    user = relationship("User", back_populates="profile")


class Role(Base):
    """Bảng danh mục quyền hạn hệ thống (Roles: 'user', 'admin')"""
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(50), unique=True, nullable=False)  # 'user', 'admin'
    description = Column(String(255), nullable=True)

    user_roles = relationship("UserRole", back_populates="role")


class UserRole(Base):
    """Bảng liên kết phân quyền nhiều-nhiều giữa User và Role (UserRoles)"""
    __tablename__ = "user_roles"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    role_id = Column(Integer, ForeignKey("roles.id", ondelete="CASCADE"), nullable=False)

    user = relationship("User", back_populates="user_roles")
    role = relationship("Role", back_populates="user_roles")


class OTPStorage(Base):
    """Bảng lưu trữ mã OTP xác thực tạm thời kèm thời hạn hiệu lực"""
    __tablename__ = "otp_storage"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    contact = Column(String(255), index=True, nullable=False)  # Lưu email hoặc SĐT
    otp_code = Column(String(6), nullable=False)
    expired_at = Column(DateTime, nullable=False)              # Thời điểm hết hạn (5 phút)
    is_used = Column(Boolean, default=False, nullable=False)   # Trạng thái đã dùng mã hay chưa
    created_at = Column(DateTime, default=datetime.utcnow)


class RevokedToken(Base):
    """Bảng lưu trữ danh sách Token đã bị thu hồi khi Đăng xuất (Logout)"""
    __tablename__ = "revoked_tokens"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    token = Column(String(500), unique=True, index=True, nullable=False)
    token_type = Column(String(20), default="access", nullable=False)  # 'access', 'refresh'
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=True)
    revoked_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    expires_at = Column(DateTime, nullable=True)


class UserPreference(Base):
    """
    Bảng lưu trữ sở thích ăn uống và thông tin dị ứng của người dùng (UserPreferences)
    - Quản lý chế độ ăn (diet_type): omnivore, vegetarian, vegan, halal, keto
    - Dị ứng thực phẩm (allergies): seafood, peanut, dairy, gluten... (lưu dạng JSON)
    - Nhóm món ăn yêu thích (preferred_cuisines): Món Việt, Lẩu Nướng, Món Nhật... (lưu dạng JSON)
    - Ngân sách trung bình (avg_budget)
    Phục vụ tích hợp tự động vào bộ tiêu chí gợi ý mặc định (Task TE9C65C)
    """
    __tablename__ = "user_preferences"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True, index=True)
    diet_type = Column(String(50), default="omnivore", nullable=False)   # 'omnivore', 'vegetarian', 'vegan', 'halal', 'keto'
    allergies = Column(String(500), default="[]", nullable=False)        # JSON string list: ["seafood", "peanut"]
    preferred_cuisines = Column(String(500), default="[]", nullable=False) # JSON string list: ["Món Việt", "Món Nhật"]
    avg_budget = Column(Float, default=250000.0, nullable=True)          # Ngân sách trung bình (VNĐ)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="preference")

