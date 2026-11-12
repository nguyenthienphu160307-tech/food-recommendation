from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.core.database import get_db
from app.models.user import User, UserProfile, Role, UserRole, OTPStorage
from app.schemas.auth import (
    SendOTPRequest,
    RegisterRequest,
    RegisterResponse,
    UserDataResponse,
    StandardResponse,
)
from app.core.security import hash_password, generate_otp
from app.core.email import send_otp_email

router = APIRouter(prefix="/api/auth", tags=["Xác thực & Tài khoản (Auth)"])


@router.post(
    "/send-otp",
    response_model=StandardResponse,
    status_code=status.HTTP_200_OK,
    summary="Gửi mã OTP đăng ký tài khoản"
)
def send_otp(
    payload: SendOTPRequest, 
    db: Session = Depends(get_db)
):
    """
    API gửi mã OTP xác thực:
    1. Yêu cầu nhập Email để nhận mã OTP.
    2. Kiểm tra Email hoặc Số điện thoại đã được đăng ký trong bảng Users hay chưa.
    3. Nếu đã tồn tại -> Trả về lỗi 409 Conflict.
    4. Nếu chưa -> Sinh ngẫu nhiên mã OTP 6 chữ số, hạn 5 phút.
    5. Gửi mã OTP trực tiếp vào hòm thư Email cá nhân của người dùng qua SMTP (Không in console).
    6. Lưu vào bảng `OTPStorage` khi gửi thành công.
    """
    if not payload.email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Hệ thống gửi mã OTP qua Email. Vui lòng cung cấp địa chỉ Email của bạn."
        )

    contact = payload.email

    # 1. Kiểm tra tài khoản đã tồn tại trong CSDL hay chưa
    filters = [User.email == payload.email]
    if payload.phone_number:
        filters.append(User.phone_number == payload.phone_number)

    existing_user = db.query(User).filter(or_(*filters)).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email hoặc số điện thoại này đã được đăng ký tài khoản."
        )

    # 2. Sinh mã OTP 6 số và tính thời điểm hết hạn (cộng thêm 5 phút)
    otp_code = generate_otp(6)
    expired_at = datetime.utcnow() + timedelta(minutes=5)

    # 3. Gửi mã OTP trực tiếp vào hòm thư cá nhân thực tế của người dùng
    email_sent = send_otp_email(to_email=payload.email, otp_code=otp_code)
    if not email_sent:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Không thể gửi email chứa mã OTP. Vui lòng kiểm tra lại địa chỉ email hoặc kết nối mạng."
        )

    # 4. Lưu bản ghi OTP vào CSDL
    new_otp = OTPStorage(
        contact=contact,
        otp_code=otp_code,
        expired_at=expired_at,
        is_used=False
    )
    db.add(new_otp)
    db.commit()

    return StandardResponse(
        message=f"Mã OTP đã được gửi trực tiếp tới hòm thư {payload.email}. Vui lòng kiểm tra Email của bạn!",
        detail=f"Mã có hiệu lực trong 5 phút đến {expired_at.strftime('%H:%M:%S')}"
    )


@router.post(
    "/register",
    response_model=RegisterResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Đăng ký tài khoản mới kèm xác thực OTP"
)
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    """
    API hoàn tất đăng ký tài khoản (PBI-01 / TSK-02):
    1. Kiểm tra mã OTP: Có tồn tại, khớp mã, chưa sử dụng và còn hạn trong 5 phút hay không.
    2. Băm mật khẩu bằng Bcrypt.
    3. Thêm bản ghi vào 3 bảng liên kết:
       - `Users`: Lưu thông tin đăng nhập, mật khẩu băm, status='active'.
       - `UserProfiles`: Lưu hồ sơ người dùng (họ và tên).
       - `UserRoles`: Gán quyền mặc định là 'user'.
    4. Đánh dấu mã OTP đã được sử dụng (`is_used = True`).
    5. Trả về HTTP 201 Created kèm dữ liệu người dùng.
    """
    contact = payload.email if payload.email else payload.phone_number

    # 1. Tìm mã OTP mới nhất của người dùng này mà chưa bị sử dụng
    otp_record = (
        db.query(OTPStorage)
        .filter(
            OTPStorage.contact == contact,
            OTPStorage.is_used == False
        )
        .order_by(OTPStorage.id.desc())
        .first()
    )

    if not otp_record or otp_record.otp_code != payload.otp_code:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Mã xác thực OTP không chính xác hoặc không tồn tại."
        )

    # 2. Kiểm tra thời hạn hiệu lực của OTP (5 phút)
    if datetime.utcnow() > otp_record.expired_at:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Mã OTP đã hết hạn hiệu lực. Vui lòng yêu cầu cấp mã mới."
        )

    # 3. Kiểm tra trùng lặp tài khoản (phòng trường hợp người dùng thao tác song song)
    filters = []
    if payload.email:
        filters.append(User.email == payload.email)
    if payload.phone_number:
        filters.append(User.phone_number == payload.phone_number)

    if db.query(User).filter(or_(*filters)).first():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email hoặc số điện thoại này đã được đăng ký tài khoản."
        )

    # 4. Băm mật khẩu bằng thuật toán Bcrypt
    hashed_pwd = hash_password(payload.password)

    # 5. Lưu vào bảng `Users`
    new_user = User(
        email=payload.email,
        phone_number=payload.phone_number,
        hashed_password=hashed_pwd,
        status="active"
    )
    db.add(new_user)
    db.flush()  # Lấy new_user.id tự sinh để gắn vào các bảng liên kết

    # 6. Lưu vào bảng `UserProfiles`
    new_profile = UserProfile(
        user_id=new_user.id,
        full_name=payload.full_name
    )
    db.add(new_profile)

    # 7. Lấy Role 'user' (nếu chưa có trong CSDL thì tự động khởi tạo)
    default_role = db.query(Role).filter(Role.name == "user").first()
    if not default_role:
        default_role = Role(name="user", description="Người dùng hệ thống thông thường")
        db.add(default_role)
        db.flush()

    # 8. Lưu vào bảng liên kết `UserRoles`
    user_role_link = UserRole(
        user_id=new_user.id,
        role_id=default_role.id
    )
    db.add(user_role_link)

    # 9. Đánh dấu OTP đã được sử dụng để tránh tấn công phát lại (Replay Attack)
    otp_record.is_used = True

    # 10. Commit toàn bộ giao dịch vào CSDL
    db.commit()
    db.refresh(new_user)

    # 11. Trả về phản hồi thành công HTTP 201
    return RegisterResponse(
        message="Đăng ký tài khoản thành công!",
        data=UserDataResponse(
            id=new_user.id,
            email=new_user.email,
            phone_number=new_user.phone_number,
            full_name=payload.full_name,
            status=new_user.status,
            role=default_role.name,
            created_at=new_user.created_at
        )
    )
