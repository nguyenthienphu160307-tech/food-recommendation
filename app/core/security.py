import os
import random
import string
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional
import bcrypt
import jwt

# ==========================================
# CẤU HÌNH JWT BẢO MẬT & THỜI HẠN HIỆU LỰC
# ==========================================
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "smart_dining_super_secret_jwt_key_2026_food_ai")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))


def hash_password(password: str) -> str:
    """
    Băm mật khẩu người dùng bằng thuật toán Bcrypt:
    - Tự động sinh Salt ngẫu nhiên chống tấn công Rainbow Table.
    - Lưu vào cột `hashed_password` của bảng `Users`.
    """
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed.decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    So khớp mật khẩu do người dùng nhập với mật khẩu băm trong CSDL.
    """
    try:
        return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))
    except Exception:
        return False


def generate_otp(length: int = 6) -> str:
    """
    Sinh ngẫu nhiên mã số xác thực OTP gồm các chữ số (Mặc định 6 số, VD: '392815').
    """
    return "".join(random.choices(string.digits, k=length))


def create_access_token(
    subject: str | int,
    claims: Optional[Dict[str, Any]] = None,
    expires_delta: Optional[timedelta] = None
) -> str:
    """
    Tạo Access Token JWT (Thời hạn ngắn, mặc định 60 phút):
    - `sub`: ID người dùng (user_id).
    - `type`: "access".
    - `claims`: Thông tin mở rộng như email, roles, status...
    """
    now = datetime.now(timezone.utc)
    if expires_delta:
        expire = now + expires_delta
    else:
        expire = now + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    payload = {
        "sub": str(subject),
        "type": "access",
        "iat": int(now.timestamp()),
        "exp": int(expire.timestamp()),
    }
    if claims:
        payload.update(claims)

    return jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)


def create_refresh_token(
    subject: str | int,
    claims: Optional[Dict[str, Any]] = None,
    expires_delta: Optional[timedelta] = None
) -> str:
    """
    Tạo Refresh Token JWT (Thời hạn dài, mặc định 7 ngày):
    - `sub`: ID người dùng (user_id).
    - `type`: "refresh".
    """
    now = datetime.now(timezone.utc)
    if expires_delta:
        expire = now + expires_delta
    else:
        expire = now + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)

    payload = {
        "sub": str(subject),
        "type": "refresh",
        "iat": int(now.timestamp()),
        "exp": int(expire.timestamp()),
    }
    if claims:
        payload.update(claims)

    return jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)


def decode_jwt_token(token: str) -> Dict[str, Any]:
    """
    Giải mã và kiểm tra tính hợp lệ của JWT token.
    Bắn jwt.ExpiredSignatureError hoặc jwt.PyJWTError nếu token không hợp lệ hoặc hết hạn.
    """
    return jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
