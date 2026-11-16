from typing import Any, Dict, Optional
from pydantic import BaseModel, Field


class OtherConditionsSchema(BaseModel):
    """Nhóm tiêu chí tiện ích mở rộng (other_conditions) khớp với bảng RestaurantAmenities"""
    has_private_room: Optional[bool] = Field(
        default=None,
        description="Yêu cầu phòng riêng, không gian yên tĩnh, tiếp khách (True/False/None)"
    )
    pet_friendly: Optional[bool] = Field(
        default=None,
        description="Cho phép mang theo thú cưng chó/mèo (True/False/None)"
    )
    vegetarian_support: Optional[bool] = Field(
        default=None,
        description="Có thực đơn chay hoặc hỗ trợ món chay (True/False/None)"
    )
    has_outdoor: Optional[bool] = Field(
        default=None,
        description="Có không gian ngoài trời, sân vườn, thoáng mát (True/False/None)"
    )
    group_size: Optional[int] = Field(
        default=None,
        ge=1,
        description="Số lượng người ăn nếu được đề cập trong câu hỏi (VD: nhóm 4 người -> 4)"
    )


class DiningCriteriaSchema(BaseModel):
    """
    JSON Schema chuẩn cho LLM bóc tách tiêu chí ăn uống (Task TE9C65A)
    Ánh xạ trực tiếp vào bảng SearchCriteria trong CSDL.
    """
    location_text: Optional[str] = Field(
        default=None,
        description="Tên đường, phường, quận hoặc khu vực địa lý được nhắc tới (VD: 'Quận 1', 'Gò Vấp', 'Đa Kao')"
    )
    cuisine: Optional[str] = Field(
        default=None,
        description="Loại hình ẩm thực chuẩn hóa (VD: 'BBQ Hàn Quốc', 'Món Việt', 'Món Chay', 'Cơm tấm', 'Lẩu')"
    )
    budget: Optional[int] = Field(
        default=None,
        ge=0,
        description="Ngân sách tối đa tính theo VNĐ/người (VD: 'dưới 300k' -> 300000, '150 nghìn' -> 150000)"
    )
    has_parking: Optional[bool] = Field(
        default=None,
        description="Yêu cầu có bãi đỗ xe / chỗ đậu ô tô (True/False/None)"
    )
    other_conditions: OtherConditionsSchema = Field(
        default_factory=OtherConditionsSchema,
        description="Các điều kiện tiện ích phụ trợ: phòng riêng, thú cưng, ăn chay, sân vườn, số người"
    )


class ExtractCriteriaRequest(BaseModel):
    """Schema request cho API trích xuất tiêu chí."""
    prompt: str = Field(..., description="Câu hỏi tự nhiên của người dùng")
    session_id: Optional[int] = Field(None, description="ID của phiên chat hiện tại để lưu lịch sử (TE9C66A)")
    current_context: Optional[Dict[str, Any]] = Field(None, description="Ngữ cảnh hội thoại trước đó")

class ExtractCriteriaResponse(BaseModel):
    """Schema response trả về cho Frontend."""
    prompt: str = Field(..., description="Câu hỏi gốc của người dùng")
    extracted_criteria: Dict[str, Any] = Field(..., description="JSON chứa các tiêu chí đã bóc tách")
    ai_explanation: str = Field(..., description="Lời giải thích tự nhiên từ AI về cách trích xuất tiêu chí")
    extraction_engine: str = Field(..., description="Engine đã sử dụng (vd: Gemini, Rule-based)")