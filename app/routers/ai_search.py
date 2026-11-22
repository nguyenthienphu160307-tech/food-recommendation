from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
import logging
from app.core.database import get_db
from app.core.guest_guard import enforce_guest_chat_limit
from app.schemas.ai_search import (
    ExtractCriteriaRequest,
    ExtractCriteriaResponse,
    AISearchRecommendRequest,
    AISearchRecommendResponse,
)
from app.core.prompt_template import (
    SYSTEM_PROMPT_TEMPLATE,
    get_dining_criteria_json_schema,
    build_extraction_prompt,
    extract_criteria_from_prompt_async,
    build_ai_explanation,
)
from app.services.chat_session_service import ChatSessionService
from app.services.ai_recommendation_pipeline import AIRecommendationPipeline

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/search", tags=["AI Prompt & Trích xuất Tiêu chí"])

# ==============================================================================
# BỘ NHỚ ĐỆM (CACHE) CHO CÁC CÂU HỎI PHỔ BIẾN - TASK TE9C66B
# Giúp trả kết quả tức thì (< 0.1s) cho các câu hỏi trùng lặp mà không cần gọi LLM
# ==============================================================================
PROMPT_CACHE = {}


@router.get(
    "/prompt-schema",
    summary="Xem thiết kế Prompt Template & JSON Schema trích xuất tiêu chí ăn uống"
)
def get_prompt_and_schema():
    sample_query = "Nhóm 4 người muốn ăn đồ nướng ở Quận 1 có chỗ đậu ô tô dưới 300k/người, có phòng riêng"
    return {
        "task_code": "TE9C66B",
        "json_schema": get_dining_criteria_json_schema(),
        "system_prompt_template": SYSTEM_PROMPT_TEMPLATE,
        "rendered_prompt_example": build_extraction_prompt(sample_query),
        "configured_providers": LLMService.get_configured_providers(),
    }


@router.post(
    "/extract-criteria",
    response_model=ExtractCriteriaResponse,
    summary="Trích xuất tiêu chí (Hỗ trợ Async & Cache) đảm bảo phản hồi < 5s (NFR-01)"
)
async def extract_dining_criteria(
    payload: ExtractCriteriaRequest,
    db: Session = Depends(get_db)
):
    """
    Task TE9C66B:
    - Bật async/await để không block thread server.
    - Áp dụng bộ nhớ đệm (Cache) cho các câu hỏi trùng nhau.
    - Tự động nhảy sang Rule-based Fallback Parser nếu LLM phản hồi chậm hơn 4.5s.
    """
    prompt_key = payload.prompt.strip().lower()

    # 1. KIỂM TRA BỘ NHỚ ĐỆM (CACHE HIT)
    if not payload.current_context and prompt_key in PROMPT_CACHE:
        criteria = PROMPT_CACHE[prompt_key]
        engine_used = "memory_cache"
    else:
        # 2. XỬ LÝ BẤT ĐỒNG BỘ (ASYNC)
        criteria, engine_used = await extract_criteria_from_prompt_async(
            user_prompt=payload.prompt,
            current_context=payload.current_context,
        )

        # Lưu vào Cache nếu đây là câu hỏi mới
        if not payload.current_context:
            PROMPT_CACHE[prompt_key] = criteria

    # 3. Sinh lời giải thích AI
    explanation = build_ai_explanation(criteria)

    # 4. Lưu lịch sử tin nhắn vào CSDL
    if getattr(payload, "session_id", None):
        try:
            ChatSessionService.save_message(db, payload.session_id, "user", payload.prompt)
            ChatSessionService.save_message(db, payload.session_id, "ai", explanation)

            other_cond = criteria.other_conditions.model_dump(exclude_none=True)
            other_cond_str = str(other_cond) if other_cond else None

            ChatSessionService.save_criteria(
                db=db,
                session_id=payload.session_id,
                location_text=criteria.location_text,
                cuisine=criteria.cuisine,
                budget=criteria.budget,
                has_parking=criteria.has_parking if criteria.has_parking is not None else False,
                other_conditions=other_cond_str,
            )
        except Exception as e:
            logger.error(f"Lỗi khi lưu tin nhắn: {e}")

    return ExtractCriteriaResponse(
        prompt=payload.prompt,
        extracted_criteria=criteria,
        ai_explanation=explanation,
        extraction_engine=engine_used,
    )


@router.post(
    "/ai-recommend",
    response_model=AISearchRecommendResponse,
    summary="Tích hợp AI Search (Module 2) -> Spatial Filter & Ranking Top N (Module 4) - TE9C670 & TE9C675"
)
async def ai_search_and_recommend(
    request: Request,
    payload: AISearchRecommendRequest,
    db: Session = Depends(get_db),
):
    """
    Task TE9C670 & TE9C675:
    - Kiểm tra giới hạn 3 lượt chat miễn phí nếu là Guest chưa đăng nhập (BR-02).
    - Trích xuất SearchCriteria từ câu hỏi tự nhiên (Async + Cache + Fallback).
    - Chuyển đổi sang tham số Spatial & Filter -> Xếp hạng bằng RankingEngine -> Trả về Top N.
    """
    # 1. Kiểm tra giới hạn lượt chat cho Guest (BR-02 - Task TE9C675)
    enforce_guest_chat_limit(request)

    prompt_key = payload.prompt.strip().lower()

    # 2. Trích xuất tiêu chí tìm kiếm (Module 2)
    if not payload.current_context and prompt_key in PROMPT_CACHE:
        criteria = PROMPT_CACHE[prompt_key]
        engine_used = "memory_cache"
    else:
        criteria, engine_used = await extract_criteria_from_prompt_async(
            user_prompt=payload.prompt,
            current_context=payload.current_context,
        )
        if not payload.current_context:
            PROMPT_CACHE[prompt_key] = criteria

    # 3. Chuyển đổi SearchCriteria -> Spatial & Filter -> Ranking Top N (Module 4)
    pipeline_output = AIRecommendationPipeline.query_and_rank(
        db=db,
        criteria=criteria,
        user_lat=payload.user_lat,
        user_lng=payload.user_lng,
        radius_km=payload.radius_km,
        top_n=payload.top_n,
    )

    # 4. Sinh lời giải thích (Explainable AI) & lưu lịch sử chat nếu có session_id
    explanation = build_ai_explanation(criteria)
    if getattr(payload, "session_id", None):
        try:
            ChatSessionService.save_message(db, payload.session_id, "user", payload.prompt)
            ChatSessionService.save_message(db, payload.session_id, "ai", explanation)
        except Exception as e:
            logger.error(f"Lỗi khi lưu tin nhắn phiên chat AI Recommend: {e}")

    return AISearchRecommendResponse(
        prompt=payload.prompt,
        extracted_criteria=criteria,
        resolved_location=pipeline_output["resolved_location"],
        ai_explanation=explanation,
        extraction_engine=engine_used,
        total_candidates=pipeline_output["total_candidates"],
        top_n=payload.top_n,
        recommendations=pipeline_output["recommendations"],
    )