from datetime import datetime
from typing import Optional
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


class StandardResponse(BaseModel):
    """Phản hồi thông báo chung chuẩn tiếng Việt"""
    message: str
    detail: Optional[str] = None
