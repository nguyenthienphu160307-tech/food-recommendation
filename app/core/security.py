import os
import random
import string
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional
import bcrypt
import jwt

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "smart_dining_super_secret_jwt_key_2026_food_ai")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")

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
    return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))


def generate_otp(length: int = 6) -> str:
    """
    Sinh ngẫu nhiên mã số xác thực OTP gồm các chữ số (Mặc định 6 số, VD: '392815').
    """
    return "".join(random.choices(string.digits, k=length))

def decode_jwt_token(token: str) -> Dict[str, Any]:
    """
    kiểm tra tính hợp lệ của JWT token.
    jwt.ExpiredSignatureError hoặc jwt.PyJWTError nếu token không hợp lệ hoặc hết hạn.
    """
    return jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])