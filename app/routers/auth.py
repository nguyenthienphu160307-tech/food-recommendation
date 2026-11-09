from datetime import datetime, timedelta
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from sqlalchemy import or_
import jwt

from app.core.database import get_db
from app.models.user import User, UserProfile, Role, UserRole, OTPStorage
from app.schemas.auth import (
    SendOTPRequest,
    RegisterRequest,
    RegisterResponse,
    UserDataResponse,
    StandardResponse,
    LoginRequest,
    LoginResponse,
    UserInfoResponse,
    TokenResponse,
    RefreshTokenRequest,
    RefreshTokenResponse,
    LogoutRequest,
)
from app.core.security import (
    hash_password,
    verify_password,
    generate_otp,
    create_access_token,
    create_refresh_token,
    decode_jwt_token,
    ACCESS_TOKEN_EXPIRE_MINUTES,
)
from app.core.email import send_otp_email
from app.core.rbac import (
    RoleName,
    get_current_guest_or_user,
    get_current_user,
    get_current_admin,
    require_roles,
    oauth2_scheme,
    revoke_token,
    is_token_revoked,
)

router = APIRouter(prefix="/api/auth", tags=["Xác thực & Tài khoản (Auth)"])


# =====================================================================
# 1. API GỬI MÃ OTP ĐĂNG KÝ
# =====================================================================
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


# =====================================================================
# 2. API HOÀN TẤT ĐĂNG KÝ TÀI KHOẢN
# =====================================================================
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


# =====================================================================
# 3. API ĐĂNG NHẬP & CẤP TOKEN (BR-07)
# =====================================================================
@router.post(
    "/login",
    response_model=LoginResponse,
    status_code=status.HTTP_200_OK,
    summary="Đăng nhập tài khoản & Cấp cặp Access/Refresh Token (Kiểm tra BR-07)"
)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    """
    API Đăng nhập tài khoản (PBI-01 / TSK-03):
    1. Nhận tài khoản (Email hoặc Số điện thoại) và mật khẩu người dùng.
    2. Tìm kiếm người dùng trong bảng `Users`.
    3. So khớp mật khẩu bằng `verify_password` (Bcrypt).
    4. Kiểm tra quy tắc nghiệp vụ BR-07:
       - Nếu status != 'active' (ví dụ: 'locked'), chặn đăng nhập và trả về HTTP 403 Forbidden.
    5. Trích xuất danh sách vai trò (Roles: 'user', 'admin') từ bảng liên kết `UserRoles`.
    6. Cấp cặp Access Token (ngắn hạn) và Refresh Token (dài hạn).
    7. Trả về HTTP 200 kèm thông tin cá nhân và cặp token xác thực.
    """
    target = payload.account or payload.email or payload.phone_number

    # 1. Tìm tài khoản người dùng theo Email hoặc Số điện thoại
    user = (
        db.query(User)
        .filter(
            or_(
                User.email == target,
                User.phone_number == target
            )
        )
        .first()
    )

    # 2. Kiểm tra tài khoản tồn tại và so khớp mật khẩu băm
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email/Số điện thoại hoặc mật khẩu không chính xác.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 3. Kiểm tra quy tắc nghiệp vụ BR-07: Tài khoản phải ở trạng thái active
    if user.status != "active":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Tài khoản của bạn đã bị khóa theo chính sách hệ thống (BR-07). Vui lòng liên hệ Quản trị viên để được hỗ trợ.",
        )

    # 4. Lấy danh sách vai trò (roles) của người dùng
    roles = [ur.role.name for ur in user.user_roles if ur.role]
    if not roles:
        roles = ["user"]

    # 5. Cấp cặp token Access & Refresh
    claims = {
        "email": user.email,
        "phone_number": user.phone_number,
        "roles": roles,
        "status": user.status,
    }
    access_token = create_access_token(subject=user.id, claims=claims)
    refresh_token = create_refresh_token(subject=user.id)
    expires_in = ACCESS_TOKEN_EXPIRE_MINUTES * 60

    # 6. Lấy họ và tên từ hồ sơ cá nhân
    full_name = user.profile.full_name if user.profile else "Người dùng"

    return LoginResponse(
        message="Đăng nhập thành công!",
        user=UserInfoResponse(
            id=user.id,
            email=user.email,
            phone_number=user.phone_number,
            full_name=full_name,
            status=user.status,
            roles=roles,
            created_at=user.created_at,
        ),
        tokens=TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
            expires_in=expires_in,
        )
    )


# =====================================================================
# 4. API LÀM MỚI ACCESS TOKEN (REFRESH TOKEN)
# =====================================================================
@router.post(
    "/refresh-token",
    response_model=RefreshTokenResponse,
    status_code=status.HTTP_200_OK,
    summary="Cấp mới Access Token bằng Refresh Token"
)
def refresh_access_token(payload: RefreshTokenRequest, db: Session = Depends(get_db)):
    """
    API gia hạn phiên đăng nhập (Refresh Token):
    1. Kiểm tra tính hợp lệ và thời hạn của Refresh Token.
    2. Đảm bảo token chưa bị thu hồi (Blacklisted).
    3. Kiểm tra user_id trong token và kiểm tra tài khoản status='active' (BR-07).
    4. Cấp Access Token mới.
    """
    try:
        token_data = decode_jwt_token(payload.refresh_token)
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh Token đã hết hạn. Vui lòng đăng nhập lại.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh Token không hợp lệ.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 1. Kiểm tra loại token phải là 'refresh'
    if token_data.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token cung cấp không phải là Refresh Token.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 2. Kiểm tra danh sách thu hồi (Revoked Tokens)
    if is_token_revoked(db, payload.refresh_token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh Token đã bị thu hồi (đã đăng xuất). Vui lòng đăng nhập lại.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_id = token_data.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Dữ liệu token không hợp lệ.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = db.query(User).filter(User.id == int(user_id)).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Tài khoản không tồn tại trên hệ thống.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 3. Quy tắc nghiệp vụ BR-07: Trạng thái tài khoản phải là 'active'
    if user.status != "active":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Tài khoản của bạn đã bị khóa theo chính sách hệ thống (BR-07). Vui lòng liên hệ Quản trị viên để được hỗ trợ.",
        )

    roles = [ur.role.name for ur in user.user_roles if ur.role]
    if not roles:
        roles = ["user"]

    claims = {
        "email": user.email,
        "phone_number": user.phone_number,
        "roles": roles,
        "status": user.status,
    }
    new_access_token = create_access_token(subject=user.id, claims=claims)
    expires_in = ACCESS_TOKEN_EXPIRE_MINUTES * 60

    return RefreshTokenResponse(
        message="Cấp mới Access Token thành công!",
        access_token=new_access_token,
        token_type="bearer",
        expires_in=expires_in,
    )


# =====================================================================
# 5. API ĐĂNG XUẤT TÀI KHOẢN (LOGOUT)
# =====================================================================
@router.post(
    "/logout",
    response_model=StandardResponse,
    status_code=status.HTTP_200_OK,
    summary="Đăng xuất tài khoản & Thu hồi Token"
)
def logout(
    payload: Optional[LogoutRequest] = None,
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(oauth2_scheme),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    API Đăng xuất tài khoản an toàn:
    1. Yêu cầu đăng nhập hợp lệ (Access Token còn hiệu lực).
    2. Thu hồi Access Token hiện tại vào bảng `RevokedToken`.
    3. Nếu client gửi kèm Refresh Token, thu hồi luôn Refresh Token tương ứng.
    4. Trả về thông báo thành công.
    """
    # 1. Thu hồi Access Token đang sử dụng
    if credentials and credentials.credentials:
        revoke_token(
            db=db,
            token=credentials.credentials,
            token_type="access",
            user_id=current_user.id
        )

    # 2. Thu hồi Refresh Token nếu được gửi lên
    if payload and payload.refresh_token:
        revoke_token(
            db=db,
            token=payload.refresh_token,
            token_type="refresh",
            user_id=current_user.id
        )

    return StandardResponse(
        message="Đăng xuất tài khoản thành công! Phiên làm việc đã được hủy bỏ an toàn.",
        detail=f"Tài khoản {current_user.email or current_user.phone_number} đã đăng xuất."
    )


# =====================================================================
# 6. API LẤY THÔNG TIN TÀI KHOẢN HIỆN TẠI (GET /me)
# =====================================================================
@router.get(
    "/me",
    response_model=UserInfoResponse,
    summary="Lấy thông tin tài khoản hiện tại (Yêu cầu đăng nhập)"
)
def get_me(current_user: User = Depends(get_current_user)):
    """Trả về thông tin chi tiết và danh sách vai trò của người dùng hiện tại"""
    roles = [ur.role.name for ur in current_user.user_roles if ur.role]
    full_name = current_user.profile.full_name if current_user.profile else "Người dùng"
    return UserInfoResponse(
        id=current_user.id,
        email=current_user.email,
        phone_number=current_user.phone_number,
        full_name=full_name,
        status=current_user.status,
        roles=roles,
        created_at=current_user.created_at,
    )


# =====================================================================
# 7. CÁC ENDPOINT MINH HỌA MIDDLEWARE PHÂN QUYỀN RBAC (Guest/User/Admin)
# =====================================================================
@router.get(
    "/public-info",
    summary="Phân biệt Guest vs Người dùng đã đăng nhập (BR-02)"
)
def public_info(current_user: Optional[User] = Depends(get_current_guest_or_user)):
    """
    Endpoint phân quyền minh họa:
    - Nếu là Guest (chưa đăng nhập): Chỉ trả về thông tin cơ bản giới hạn (BR-02).
    - Nếu đã đăng nhập (User/Admin): Trả về dữ liệu cá nhân hóa đầy đủ (BR-01).
    """
    if not current_user:
        return {
            "role": RoleName.GUEST,
            "access_level": "limited",
            "message": "Bạn đang duyệt hệ thống với tư cách Khách (Guest) - chỉ hiển thị dữ liệu cơ bản theo quy định BR-02."
        }
    roles = [ur.role.name for ur in current_user.user_roles if ur.role]
    return {
        "role": roles[0] if roles else RoleName.USER,
        "access_level": "full",
        "user_id": current_user.id,
        "message": f"Xin chào {current_user.email or current_user.phone_number}, bạn có toàn quyền tra cứu và tương tác!"
    }


@router.get(
    "/user-only",
    summary="Khu vực dành cho User đã đăng nhập (User & Admin)"
)
def user_only_area(current_user: User = Depends(get_current_user)):
    """Chỉ User hoặc Admin có tài khoản active mới truy cập được"""
    return {
        "message": "Truy cập thành công vào khu vực dành cho thành viên!",
        "user_id": current_user.id,
        "email": current_user.email
    }


@router.get(
    "/admin-only",
    summary="Khu vực dành riêng cho Quản trị viên (Admin)"
)
def admin_only_area(current_user: User = Depends(get_current_admin)):
    """Chỉ Admin có tài khoản active mới truy cập được (BR-07)"""
    return {
        "message": "Truy cập thành công vào khu vực Quản trị viên (Admin)!",
        "admin_id": current_user.id,
        "email": current_user.email
    }
