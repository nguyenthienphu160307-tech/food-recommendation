from datetime import datetime
from typing import Optional, List
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
import jwt

from app.core.database import get_db
from app.core.security import decode_jwt_token
from app.models.user import User, RevokedToken

# Chuẩn HTTPBearer của FastAPI hỗ trợ nút Authorize trực quan trên Swagger UI (/docs)
# auto_error=False để cho phép cả người dùng Guest (chưa đăng nhập) gọi API công khai
oauth2_scheme = HTTPBearer(auto_error=False)


class RoleName:
    """Định nghĩa các hằng số vai trò trong hệ thống"""
    GUEST = "guest"
    USER = "user"
    ADMIN = "admin"


def is_token_revoked(db: Session, token: str) -> bool:
    """Kiểm tra token có nằm trong danh sách đã bị thu hồi (đăng xuất) hay chưa"""
    revoked = db.query(RevokedToken).filter(RevokedToken.token == token).first()
    return revoked is not None


def revoke_token(
    db: Session,
    token: str,
    token_type: str = "access",
    user_id: Optional[int] = None,
    expires_at: Optional[datetime] = None
) -> None:
    """Thêm token vào bảng thu hồi khi người dùng thực hiện Đăng xuất (Logout)"""
    if not is_token_revoked(db, token):
        record = RevokedToken(
            token=token,
            token_type=token_type,
            user_id=user_id,
            expires_at=expires_at
        )
        db.add(record)
        db.commit()


def get_current_guest_or_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> Optional[User]:
    """
    Dependency phân quyền mức độ Guest & User:
    - Nếu KHÔNG truyền token (Guest): Trả về `None`.
      Áp dụng cho BR-02: Khách chưa đăng nhập chỉ được xem thông tin cơ bản và tìm kiếm hạn chế.
    - Nếu CÓ truyền token: Giải mã JWT, kiểm tra thu hồi và kiểm tra trạng thái tài khoản BR-07.
      Nếu hợp lệ -> Trả về thực thể User đầy đủ thông tin.
    """
    if not credentials or not credentials.credentials:
        return None

    token = credentials.credentials
    try:
        payload = decode_jwt_token(token)
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Phiên đăng nhập đã hết hạn. Vui lòng đăng nhập lại.",
            headers={"WWW-Authenticate": "Bearer"}
        )
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token xác thực không hợp lệ.",
            headers={"WWW-Authenticate": "Bearer"}
        )

    # 1. Kiểm tra Token Blacklist (đã đăng xuất chưa)
    if is_token_revoked(db, token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Phiên đăng nhập đã bị kết thúc (Token đã đăng xuất). Vui lòng đăng nhập lại.",
            headers={"WWW-Authenticate": "Bearer"}
        )

    # 2. Kiểm tra loại token phải là 'access'
    token_type = payload.get("type")
    if token_type != "access":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Loại token không hợp lệ (yêu cầu Access Token).",
            headers={"WWW-Authenticate": "Bearer"}
        )

    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Dữ liệu xác thực trong token không hợp lệ.",
            headers={"WWW-Authenticate": "Bearer"}
        )

    # 3. Lấy thông tin User từ CSDL
    user = db.query(User).filter(User.id == int(user_id)).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Tài khoản không tồn tại trên hệ thống.",
            headers={"WWW-Authenticate": "Bearer"}
        )

    # 4. Kiểm tra quy tắc nghiệp vụ BR-07: Tài khoản phải ở trạng thái active
    if user.status != "active":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Tài khoản của bạn đã bị khóa theo chính sách hệ thống (BR-07). Vui lòng liên hệ Quản trị viên để được mở lại.",
        )

    return user


def get_current_user(
    current_user: Optional[User] = Depends(get_current_guest_or_user)
) -> User:
    """
    Dependency bắt buộc người dùng đã Đăng nhập (User/Admin):
    - Áp dụng BR-01: Yêu cầu đăng nhập mới được thực hiện các tính năng như đánh giá, bookmark...
    - Từ chối Guest với mã lỗi HTTP 401 Unauthorized.
    """
    if current_user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Vui lòng đăng nhập tài khoản để thực hiện chức năng này.",
            headers={"WWW-Authenticate": "Bearer"}
        )
    return current_user


def get_current_admin(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Dependency phân quyền Quản trị viên (Admin):
    - Bắt buộc tài khoản đã đăng nhập và sở hữu Role 'admin'.
    - Áp dụng BR-07: Chỉ Admin mới có quyền quản trị, khóa tài khoản, duyệt dữ liệu...
    - Trả về lỗi 403 Forbidden nếu là User thông thường.
    """
    roles = [ur.role.name for ur in current_user.user_roles if ur.role]
    if RoleName.ADMIN not in roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Quyền truy cập bị từ chối: Chức năng này chỉ dành cho Quản trị viên (Admin)."
        )
    return current_user


def require_roles(allowed_roles: List[str]):
    """
    Factory Dependency linh hoạt kiểm tra RBAC theo danh sách vai trò cho phép:
    Ví dụ: Depends(require_roles(["admin"])) hoặc Depends(require_roles(["user", "admin"]))
    """
    def role_checker(current_user: User = Depends(get_current_user)) -> User:
        user_roles = [ur.role.name for ur in current_user.user_roles if ur.role]
        if not any(role in user_roles for role in allowed_roles):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Quyền truy cập bị từ chối: Yêu cầu vai trò {', '.join(allowed_roles)}."
            )
        return current_user

    return role_checker
