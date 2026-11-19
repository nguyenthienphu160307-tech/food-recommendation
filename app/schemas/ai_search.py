from typing import Any, Dict, Optional, List
from pydantic import BaseModel, Field


class OtherConditionsSchema(BaseModel):
    """Lược đồ các tiêu chí phụ bổ sung."""
    has_private_room: Optional[bool] = Field(None, description="Cần phòng riêng VIP / yên tĩnh")
    pet_friendly: Optional[bool] = Field(None, description="Cho phép mang thú cưng (chó, mèo)")
    vegetarian_support: Optional[bool] = Field(None, description="Có phục vụ hoặc hỗ trợ món chay")
    has_outdoor: Optional[bool] = Field(None, description="Có không gian ngoài trời / sân vườn")
    group_size: Optional[int] = Field(None, description="Số lượng người đi ăn")


class DiningCriteriaSchema(BaseModel):
    """Lược đồ JSON trích xuất từ câu hỏi tự nhiên của người dùng."""
    location_text: Optional[str] = Field(None, description="Địa điểm / Khu vực (Ví dụ: 'Quận 1', 'Thủ Đức')")
    cuisine: Optional[str] = Field(None, description="Loại hình ẩm thực (Ví dụ: 'Lẩu', 'Nướng', 'Hải Sản')")
    budget: Optional[int] = Field(None, description="Ngân sách tối đa tính bằng VNĐ (Ví dụ: 300000)")
    has_parking: Optional[bool] = Field(None, description="Yêu cầu có chỗ đỗ xe ô tô/xe máy")
    other_conditions: OtherConditionsSchema = Field(default_factory=OtherConditionsSchema, description="Các yêu cầu phụ")


class ExtractCriteriaRequest(BaseModel):
    """Yêu cầu từ Frontend gửi lên để xử lý ngôn ngữ tự nhiên."""
    prompt: str = Field(..., min_length=2, max_length=500, description="Câu hỏi hoặc lệnh tìm kiếm từ người dùng")
    session_id: Optional[int] = Field(None, description="ID của phiên chat hiện tại để lưu lịch sử (TE9C66A)")
    current_context: Optional[Dict[str, Any]] = Field(None, description="Ngữ cảnh JSON chứa các tiêu chí đã bóc tách từ lượt chat trước")


class ExtractCriteriaResponse(BaseModel):
    """Phản hồi sau khi phân tích NLP (LLM / Rule-based)."""
    prompt: str = Field(..., description="Câu hỏi gốc của người dùng")
    extracted_criteria: DiningCriteriaSchema = Field(..., description="Dữ liệu đã chuẩn hóa cấu trúc")
    ai_explanation: str = Field(..., description="Lời giải thích phản hồi tự nhiên (Explainable AI - TE9C66A)")
    extraction_engine: str = Field(..., description="Chế độ phân tích đang dùng (vd: 'rule_based_nlp', 'llm_api')")
    
    
class AISearchRecommendRequest(BaseModel):
    """Yêu cầu tìm kiếm AI trọn gói (Module 2 -> Module 4)."""
    prompt: str = Field(..., min_length=2, max_length=500, description="Câu hỏi tự nhiên của người dùng")
    user_lat: Optional[float] = Field(None, ge=-90.0, le=90.0, description="Vĩ độ GPS hiện tại của người dùng")
    user_lng: Optional[float] = Field(None, ge=-180.0, le=180.0, description="Kinh độ GPS hiện tại của người dùng")
    radius_km: float = Field(default=5.0, gt=0, le=50.0, description="Bán kính tìm kiếm (km)")
    top_n: int = Field(default=5, ge=1, le=20, description="Số lượng nhà hàng Top N trả về")
    session_id: Optional[int] = Field(None, description="ID phiên chat để lưu lịch sử")
    current_context: Optional[Dict[str, Any]] = Field(None, description="Ngữ cảnh hội thoại lượt trước")


class AISearchRecommendResponse(BaseModel):
    """Kết quả trả về Top N nhà hàng đã qua Spatial Filter & RankingEngine."""
    task_code: str = "TE9C670"
    prompt: str
    extracted_criteria: DiningCriteriaSchema
    resolved_location: Dict[str, Any]
    ai_explanation: str
    extraction_engine: str
    total_candidates: int
    top_n: int
    recommendations: List[Dict[str, Any]]