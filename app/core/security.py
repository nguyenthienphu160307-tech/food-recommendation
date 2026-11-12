import random
import string
import bcrypt

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
