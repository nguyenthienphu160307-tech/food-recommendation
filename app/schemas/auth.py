from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, model_validator

class SendOTPRequest(BaseModel):
    """Schema dữ liệu gửi lên khi yêu cầu cấp mã OTP"""
    email: Optional[str] = Field(None, description="Địa chỉ Email đăng ký")
    phone_number: Optional[str] = Field(None, description="Số điện thoại đăng ký")

    @model_validator(mode="after")
    def check_contact(self):
        if not self.email and not self.phone_number:
            raise ValueError("Vui lòng cung cấp ít nhất Email hoặc Số điện thoại.")
        if self.email:
            self.email = self.email.strip().lower()
        if self.phone_number:
            self.phone_number = self.phone_number.strip()
        return self


class RegisterRequest(BaseModel):
    """Schema dữ liệu gửi lên khi hoàn tất đăng ký tài khoản"""
    email: Optional[str] = Field(None, description="Địa chỉ Email đăng ký")
    phone_number: Optional[str] = Field(None, description="Số điện thoại đăng ký")
    password: str = Field(..., min_length=6, description="Mật khẩu tối thiểu 6 ký tự")
    full_name: str = Field(..., min_length=2, max_length=100, description="Họ và tên người dùng")
    otp_code: str = Field(..., min_length=6, max_length=6, description="Mã xác thực OTP gồm 6 chữ số")

    @model_validator(mode="after")
    def check_inputs(self):
        if not self.email and not self.phone_number:
            raise ValueError("Vui lòng cung cấp ít nhất Email hoặc Số điện thoại.")
        if self.email:
            self.email = self.email.strip().lower()
        if self.phone_number:
            self.phone_number = self.phone_number.strip()
        self.full_name = self.full_name.strip()
        self.otp_code = self.otp_code.strip()
        return self


class UserDataResponse(BaseModel):
    """Dữ liệu trả về tóm tắt thông tin người dùng mới đăng ký"""
    id: int
    email: Optional[str] = None
    phone_number: Optional[str] = None
    full_name: str
    status: str
    role: str
    created_at: datetime

    class Config:
        from_attributes = True


class RegisterResponse(BaseModel):
    """Phản hồi HTTP 201 cho API đăng ký thành công"""
    message: str
    data: UserDataResponse


class LoginRequest(BaseModel):
    """
    Schema dữ liệu gửi lên khi Đăng nhập:
    - Hỗ trợ nhập `account` (tự động nhận diện Email hoặc Số điện thoại)
    - Hoặc điền riêng trường `email` hoặc `phone_number`
    """
    account: Optional[str] = Field(None, description="Email hoặc Số điện thoại đăng nhập")
    email: Optional[str] = Field(None, description="Email đăng nhập")
    phone_number: Optional[str] = Field(None, description="Số điện thoại đăng nhập")
    password: str = Field(..., min_length=1, description="Mật khẩu tài khoản")

    @model_validator(mode="after")
    def validate_account(self):
        target = self.account or self.email or self.phone_number
        if not target or not target.strip():
            raise ValueError("Vui lòng cung cấp Email hoặc Số điện thoại để đăng nhập.")
        if self.account:
            self.account = self.account.strip()
        if self.email:
            self.email = self.email.strip().lower()
        if self.phone_number:
            self.phone_number = self.phone_number.strip()
        return self


class TokenResponse(BaseModel):
    """Cặp Access Token và Refresh Token chuẩn JWT"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int = Field(..., description="Thời hạn Access Token tính theo giây (VD: 3600s)")


class UserInfoResponse(BaseModel):
    """Thông tin tài khoản trả về sau khi xác thực thành công"""
    id: int
    email: Optional[str] = None
    phone_number: Optional[str] = None
    full_name: Optional[str] = None
    status: str
    roles: List[str] = []
    created_at: datetime

    class Config:
        from_attributes = True


class LoginResponse(BaseModel):
    """Phản hồi HTTP 200 cho API Đăng nhập thành công"""
    message: str
    user: UserInfoResponse
    tokens: TokenResponse


class RefreshTokenRequest(BaseModel):
    """Yêu cầu cấp mới Access Token qua Refresh Token"""
    refresh_token: str = Field(..., description="Mã Refresh Token hợp lệ")


class RefreshTokenResponse(BaseModel):
    """Phản hồi cấp mới Access Token thành công"""
    message: str
    access_token: str
    refresh_token: Optional[str] = None
    token_type: str = "bearer"
    expires_in: int


class LogoutRequest(BaseModel):
    """Payload tùy chọn khi Đăng xuất để thu hồi cả Refresh Token"""
    refresh_token: Optional[str] = Field(None, description="Refresh Token cần thu hồi đồng thời")


class StandardResponse(BaseModel):
    """Phản hồi thông báo chung chuẩn tiếng Việt"""
    message: str
    detail: Optional[str] = None
