from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import logging

from app.core.database import get_db
from app.schemas.ai_search import (
    ExtractCriteriaRequest,
    ExtractCriteriaResponse,
)
from app.core.prompt_template import (
    SYSTEM_PROMPT_TEMPLATE,
    get_dining_criteria_json_schema,
    build_extraction_prompt,
    extract_criteria_from_prompt,
    build_ai_explanation,
)
# Nhúng Service để lưu tin nhắn vào CSDL
from app.services.chat_session_service import ChatSessionService

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/search", tags=["AI Prompt & Trích xuất Tiêu chí (TE9C65A)"])


@router.get(
    "/prompt-schema",
    summary="Xem thiết kế Prompt Template & JSON Schema trích xuất tiêu chí ăn uống (TE9C65A)"
)
def get_prompt_and_schema():
    sample_query = "Nhóm 4 người muốn ăn đồ nướng ở Quận 1 có chỗ đậu ô tô dưới 300k/người, có phòng riêng"
    return {
        "task_code": "TE9C65A",
        "json_schema": get_dining_criteria_json_schema(),
        "system_prompt_template": SYSTEM_PROMPT_TEMPLATE,
        "rendered_prompt_example": build_extraction_prompt(sample_query),
    }


@router.post(
    "/extract-criteria",
    response_model=ExtractCriteriaResponse,
    summary="Trích xuất tiêu chí và sinh lời giải thích (TE9C66A)"
)
def extract_dining_criteria(
    payload: ExtractCriteriaRequest,
    db: Session = Depends(get_db)
):
    # 1. Trích xuất tiêu chí từ câu hỏi của user
    criteria, engine_used = extract_criteria_from_prompt(
        user_prompt=payload.prompt,
        current_context=payload.current_context,
    )
    
    # 2. Module TE9C66A: Sinh lời giải thích đề xuất (Explainable AI Generator)
    explanation = build_ai_explanation(criteria)

    # 3. Lưu lịch sử tin nhắn vào CSDL nếu có truyền session_id
    if payload.session_id:
        try:
            # Lưu câu hỏi của User (sender_type='user')
            ChatSessionService.save_message(
                db=db, 
                session_id=payload.session_id, 
                sender_type="user", 
                content=payload.prompt
            )
            # Lưu câu trả lời / giải thích của AI (sender_type='ai')
            ChatSessionService.save_message(
                db=db, 
                session_id=payload.session_id, 
                sender_type="ai", 
                content=explanation
            )
            
            # (Tùy chọn) Lưu bộ tiêu chí để truy xuất bộ lọc bản đồ
            other_cond_str = str(criteria.get("other_conditions", ""))
            ChatSessionService.save_criteria(
                db=db,
                session_id=payload.session_id,
                location_text=criteria.get("location_text"),
                cuisine=criteria.get("cuisine"),
                budget=criteria.get("budget"),
                has_parking=criteria.get("has_parking", False),
                other_conditions=other_cond_str if other_cond_str != "{}" else None
            )
        except Exception as e:
            logger.error(f"Lỗi khi lưu tin nhắn vào session {payload.session_id}: {e}")

    return ExtractCriteriaResponse(
        prompt=payload.prompt,
        extracted_criteria=criteria,
        ai_explanation=explanation,
        extraction_engine=engine_used,
    )