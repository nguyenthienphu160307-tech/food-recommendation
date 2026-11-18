from typing import Optional
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.ai_search import (
    ExtractCriteriaRequest,
    ExtractCriteriaResponse,
    LLMParseAndSaveRequest,
    LLMParseAndSaveResponse,
    QueryRelaxationRequest,
    QueryRelaxationResponse,
    QueryRelaxationInfo,
    MultiTurnRestaurantItem,
)
from app.core.prompt_template import (
    SYSTEM_PROMPT_TEMPLATE,
    get_dining_criteria_json_schema,
    build_extraction_prompt,
)
from app.services.llm_service import LLMService
from app.services.chat_session_service import ChatSessionService

router = APIRouter(prefix="/api/search", tags=["AI LLM & Trích xuất Tiêu chí (TE9C65A & TE9C668)"])


@router.get(
    "/prompt-schema",
    summary="Xem thiết kế Prompt Template & JSON Schema trích xuất tiêu chí ăn uống (TE9C65A)"
)
def get_prompt_and_schema():
    """
    Trả về toàn bộ JSON Schema chuẩn và System Prompt Template dành cho LLM
    để bóc tách location_text, cuisine, budget, has_parking và other_conditions.
    """
    sample_query = "Nhóm 4 người muốn ăn đồ nướng ở Quận 1 có chỗ đậu ô tô dưới 300k/người, có phòng riêng"
    return {
        "task_code": "TE9C65A",
        "json_schema": get_dining_criteria_json_schema(),
        "system_prompt_template": SYSTEM_PROMPT_TEMPLATE,
        "rendered_prompt_example": build_extraction_prompt(sample_query),
        "configured_providers": LLMService.get_configured_providers(),
    }


@router.post(
    "/extract-criteria",
    response_model=ExtractCriteriaResponse,
    summary="Trích xuất tiêu chí ăn uống từ câu hỏi tự nhiên (NER / Structured JSON / LLM)"
)
def extract_dining_criteria(payload: ExtractCriteriaRequest):
    """
    Nhận câu truy vấn tiếng Việt tự nhiên của người dùng và bóc tách thành JSON Schema chuẩn:
    - Hỗ trợ LLM Provider: 'auto', 'gemini', 'openai', 'rule_based'.
    - `location_text`: Địa điểm / Khu vực
    - `cuisine`: Loại hình ẩm thực
    - `budget`: Ngân sách tối đa (VNĐ)
    - `has_parking`: Chỗ đỗ xe ô tô
    - `other_conditions`: Phòng riêng (`has_private_room`), Thú cưng (`pet_friendly`), Ăn chay (`vegetarian_support`), Ngoài trời (`has_outdoor`), Số người (`group_size`)
    """
    provider = getattr(payload, "provider", "auto") or "auto"
    criteria, explanation, engine_used = LLMService.extract_criteria(
        prompt=payload.prompt,
        current_context=payload.current_context,
        provider=provider,
    )

    return ExtractCriteriaResponse(
        prompt=payload.prompt,
        extracted_criteria=criteria,
        ai_explanation=explanation,
        extraction_engine=engine_used,
    )


@router.post(
    "/llm-parse-and-save",
    response_model=LLMParseAndSaveResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Phân tích câu chat qua LLM và tự động lưu vào bảng SearchCriteria (TE9C668)"
)
def llm_parse_and_save_criteria(
    payload: LLMParseAndSaveRequest,
    session_id: Optional[int] = Query(None, description="ID phiên chat liên kết; nếu để trống sẽ tự động khởi tạo phiên mới"),
    db: Session = Depends(get_db),
):
    """
    API Tích hợp LLM/NLP phân tích câu chat tự nhiên sang SearchCriteria (TE9C668):
    1. Kết nối dịch vụ LLM (Gemini API hoặc OpenAI API).
    2. Phân tích câu hỏi tự nhiên thành tiêu chí ẩm thực có cấu trúc.
    3. Tự động Geocode tọa độ GPS từ địa danh bóc tách được.
    4. Áp dụng bảo vệ quyền riêng tư vị trí GPS (BR-08 / TSK-20).
    5. Lưu tiêu chí vào bảng `SearchCriteria` và lưu tin nhắn vào bảng `SearchMessages`.
    """
    # Nếu chưa có session_id, tự tạo phiên chat mới
    if session_id is None:
        new_sess = ChatSessionService.create_session(db, user_id=payload.user_id)
        session_id = new_sess.session_id

    result = LLMService.parse_and_save_to_criteria(
        db=db,
        session_id=session_id,
        user_message=payload.message,
        provider=payload.provider or "auto",
        user_id=payload.user_id,
    )

    return LLMParseAndSaveResponse(**result)


@router.get(
    "/state-diagram",
    summary="Xem cấu trúc và các bước chuyển của State Diagram Vòng đời tìm kiếm (Hình 8.2 SRS - TE9C669)"
)
def get_state_diagram_metadata():
    """
    Trả về định nghĩa 8 trạng thái và sơ đồ chuyển đổi State Diagram (Hình 8.2 SRS).
    """
    from app.services.multi_turn_state_machine import SearchSessionState, VALID_STATE_TRANSITIONS
    return {
        "task_code": "TE9C669",
        "diagram_name": "Hình 8.2. State Diagram – Vòng đời phiên tìm kiếm",
        "states": [
            {"id": 1, "state": SearchSessionState.SESSION_IDLE.value, "title": "Khởi tạo Phiên (Session Idle)", "description": "Chờ câu hỏi hoặc vị trí GPS"},
            {"id": 2, "state": SearchSessionState.PARSING_INTENT.value, "title": "Đang phân tích NLP (Parsing Intent)", "description": "Trích xuất vị trí, món, ngân sách, tiện ích"},
            {"id": 3, "state": SearchSessionState.SPATIAL_FILTERING.value, "title": "Truy vấn Không gian (Spatial Filtering)", "description": "Quét bán kính GPS & lọc tiện ích"},
            {"id": 4, "state": SearchSessionState.QUERY_RELAXATION.value, "title": "Nới lỏng Điều kiện (Query Relaxation)", "description": "Mở rộng bán kính / ngân sách khi 0 kết quả"},
            {"id": 5, "state": SearchSessionState.RANKING_AND_AI.value, "title": "Xếp hạng & Giải thích (Ranking & AI)", "description": "Chấm điểm độ khớp & sinh lý do đề xuất"},
            {"id": 6, "state": SearchSessionState.RESULT_PRESENTED.value, "title": "Hiển thị Kết quả (Result Presented)", "description": "Hiển thị danh sách quán & Bản đồ"},
            {"id": 7, "state": SearchSessionState.CONTEXT_REFINING.value, "title": "Hội thoại Nhiều lượt (Context Refining)", "description": "Cập nhật SearchCriteria trong cùng phiên"},
            {"id": 8, "state": SearchSessionState.SESSION_CLOSED.value, "title": "Đóng Phiên (Session Closed)", "description": "Lưu lịch sử SearchSessions (status=closed)"},
        ],
        "valid_transitions": {
            k.value: [v.value for v in vals] for k, vals in VALID_STATE_TRANSITIONS.items()
        }
    }


@router.post(
    "/relax",
    response_model=QueryRelaxationResponse,
    summary="Tìm kiếm với cơ chế tự động nới lỏng điều kiện khi 0 kết quả (TE9C66F / UC-02 Ngoại lệ)"
)
def search_with_query_relaxation(
    payload: QueryRelaxationRequest,
    db: Session = Depends(get_db)
):
    """
    API Thực thi Cơ chế Tự động Nới lỏng Điều kiện (TE9C66F / UC-02 Ngoại lệ):
    - Khi truy vấn gốc trả về 0 kết quả:
      + Tự động mở rộng bán kính (+3.0 km: từ r lên r + 3km).
      + Hoặc tự động nới khoảng ngân sách (±25%).
      + Tạm thời nới lỏng các tiện ích phụ.
      + Trả về danh sách quán thay thế gần đúng nhất kèm metadata chi tiết bước nới lỏng.
    """
    from app.services.query_relaxation_service import QueryRelaxationService

    results, meta = QueryRelaxationService.relax_and_search(
        db=db,
        lat=payload.lat,
        lng=payload.lng,
        radius_km=payload.radius_km,
        cuisine=payload.cuisine,
        budget=payload.budget,
        price_min=payload.price_min,
        price_max=payload.price_max,
        min_rating=payload.min_rating,
        has_parking=payload.has_parking,
        has_private_room=payload.has_private_room,
        has_outdoor=payload.has_outdoor,
        pet_friendly=payload.pet_friendly,
        vegetarian_support=payload.vegetarian_support,
        limit=payload.limit,
    )

    items = []
    for r, dist in results:
        cover_img = None
        if r.images:
            c_img = next((img for img in r.images if img.is_cover), None)
            cover_img = c_img.image_url if c_img else r.images[0].image_url
        has_park = r.amenities.has_parking if r.amenities else False
        has_priv = r.amenities.has_private_room if r.amenities else False
        items.append(
            MultiTurnRestaurantItem(
                id=r.id,
                name=r.name,
                address=r.address,
                cuisine_type=r.cuisine_type,
                avg_rating=r.avg_rating or 0.0,
                min_price=r.min_price or 0.0,
                max_price=r.max_price or 0.0,
                distance_km=dist,
                cover_image_url=cover_img,
                has_parking=has_park,
                has_private_room=has_priv,
            )
        )

    return QueryRelaxationResponse(
        status="success",
        task_code="TE9C66F",
        results_count=len(items),
        is_relaxed=meta.get("relaxation_applied", False),
        relaxation_info=QueryRelaxationInfo(**meta),
        results=items,
    )

