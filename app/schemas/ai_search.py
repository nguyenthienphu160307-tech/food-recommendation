from datetime import datetime
from typing import Any, Dict, List, Optional
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
    provider: Optional[str] = Field(
        default="auto",
        description="Nhà cung cấp LLM: 'auto', 'gemini', 'openai', 'rule_based'"
    )


class ExtractCriteriaResponse(BaseModel):
    """Phản hồi trả về gồm JSON tiêu chí đã bóc tách, lời giải thích AI và JSON Schema chuẩn"""
    prompt: str
    extracted_criteria: DiningCriteriaSchema
    ai_explanation: str
    extraction_engine: str = Field(description="Nguồn xử lý: 'gemini_api', 'openai_api', hoặc 'rule_based_nlp'")


class LLMParseAndSaveRequest(BaseModel):
    """Yêu cầu phân tích câu chat tự nhiên qua LLM và lưu vào bảng SearchCriteria (TE9C668)"""
    message: str = Field(..., min_length=1, description="Câu chat tự nhiên tiếng Việt của người dùng")
    provider: Optional[str] = Field("auto", description="Nhà cung cấp LLM: 'auto', 'gemini', 'openai', 'rule_based'")
    user_id: Optional[int] = Field(None, description="ID người dùng nếu có (để áp dụng cài đặt quyền riêng tư vị trí)")


class LLMParseAndSaveResponse(BaseModel):
    """Phản hồi kết quả bóc tách LLM và lưu vào bảng SearchCriteria (TE9C668)"""
    session_id: int = Field(..., description="ID phiên chat liên kết")
    criteria_id: int = Field(..., description="ID bản ghi SearchCriteria mới tạo")
    user_message_id: int = Field(..., description="ID tin nhắn của người dùng trong SearchMessages")
    ai_message_id: int = Field(..., description="ID tin nhắn phản hồi của AI trong SearchMessages")
    user_message: str = Field(..., description="Nội dung câu chat của người dùng")
    ai_explanation: str = Field(..., description="Lời giải thích / phản hồi sinh bởi AI")
    extraction_engine: str = Field(..., description="Engine thực hiện bóc tách ('gemini_api', 'openai_api', 'rule_based_nlp')")
    location_text: Optional[str] = Field(None, description="Tên khu vực địa lý bóc tách được")
    latitude: Optional[float] = Field(None, description="Vĩ độ tâm tìm kiếm sau Geocoding")
    longitude: Optional[float] = Field(None, description="Kinh độ tâm tìm kiếm sau Geocoding")
    cuisine: Optional[str] = Field(None, description="Loại hình ẩm thực chuẩn hóa")
    budget: Optional[int] = Field(None, description="Ngân sách tối đa (VNĐ)")
    has_parking: Optional[bool] = Field(None, description="Yêu cầu chỗ đậu xe ô tô")
    other_conditions: Dict[str, Any] = Field(default_factory=dict, description="Các tiện ích mở rộng (phòng riêng, ngoài trời, thú cưng, món chay, số người)")
    is_obfuscated: bool = Field(False, description="Cờ đánh dấu tọa độ đã được làm mờ theo BR-08")
    created_at: datetime = Field(..., description="Thời gian tạo bản ghi")

    class Config:
        from_attributes = True


# ==============================================================================
# SCHEMAS MULTI-TURN STATE MACHINE & CONTEXT MANAGER (TASK TE9C669 / HÌNH 8.2)
# ==============================================================================

class MultiTurnChatRequest(BaseModel):
    """Payload gửi câu hỏi hội thoại nhiều lượt (VD: 'Quán nào rẻ hơn?', 'Đổi sang Quận 3')"""
    message: str = Field(..., min_length=1, description="Câu hỏi hoặc yêu cầu điều chỉnh tiêu chí của người dùng")
    provider: Optional[str] = Field("auto", description="Nhà cung cấp LLM: 'auto', 'gemini', 'openai', 'rule_based'")
    user_id: Optional[int] = Field(None, description="ID người dùng nếu có (để kiểm tra cài đặt quyền riêng tư GPS)")


class MultiTurnRestaurantItem(BaseModel):
    """Thông tin tóm tắt nhà hàng trả về trong lượt hội thoại"""
    id: int
    name: str
    address: str
    cuisine_type: Optional[str] = None
    avg_rating: float
    min_price: float
    max_price: float
    distance_km: float
    cover_image_url: Optional[str] = None
    has_parking: bool = False
    has_private_room: bool = False


class MultiTurnChatResponse(BaseModel):
    """Phản hồi kết quả xử lý lượt hội thoại theo State Diagram (Hình 8.2)"""
    session_id: int
    current_state: str = Field(..., description="Trạng thái hiện tại trong State Machine (Hình 8.2)")
    status: str = Field(..., description="Trạng thái phiên ('active' hoặc 'closed')")
    criteria_id: Optional[int] = None
    user_message_id: Optional[int] = None
    ai_message_id: Optional[int] = None
    ai_message: str
    extraction_engine: Optional[str] = None
    relaxation_applied: bool = Field(False, description="Đánh dấu có kích hoạt Nới lỏng Điều kiện (State 4) hay không")
    relaxation_info: Dict[str, Any] = Field(default_factory=dict, description="Chi tiết các điều kiện đã được nới lỏng")
    merged_criteria: Optional[Dict[str, Any]] = Field(None, description="Tiêu chí tìm kiếm sau khi hợp nhất thông minh")
    results: List[MultiTurnRestaurantItem] = Field(default_factory=list, description="Danh sách nhà hàng được xếp hạng (State 5 & 6)")


class SessionStateResponse(BaseModel):
    """Phản hồi trạng thái hiện tại và lịch sử tiêu chí của phiên hội thoại"""
    session_id: int
    current_state: str
    status: str
    started_at: datetime
    total_messages: int
    total_criteria_versions: int
    latest_criteria: Optional[Dict[str, Any]] = None
    criteria_history: List[Dict[str, Any]] = Field(default_factory=list)

