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
    """Payload đầu vào cho API kiểm thử trích xuất tiêu chí từ câu hỏi tự nhiên"""
    prompt: str = Field(
        ...,
        min_length=2,
        description="Câu hỏi tự nhiên của người dùng",
        examples=["Nhóm 4 người muốn ăn đồ nướng ở Quận 1 có chỗ đậu ô tô dưới 300k/người, có phòng riêng"]
    )
    current_context: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Ngữ cảnh tiêu chí của lượt hội thoại trước (hỗ trợ Multi-turn)"
    )


class ExtractCriteriaResponse(BaseModel):
    """Phản hồi trả về gồm JSON tiêu chí đã bóc tách, lời giải thích AI và JSON Schema chuẩn"""
    prompt: str
    extracted_criteria: DiningCriteriaSchema
    ai_explanation: str
    extraction_engine: str = Field(description="Nguồn xử lý: 'llm_api' hoặc 'rule_based_nlp'")