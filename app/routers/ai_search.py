from typing import Optional
from fastapi import APIRouter, Depends, Request, status
from sqlalchemy.orm import Session
import logging
from app.core.database import get_db
from app.core.guest_guard import enforce_guest_chat_limit
from app.schemas.ai_search import (
    ExtractCriteriaRequest,
    ExtractCriteriaResponse,
    AISearchRecommendRequest,
    AISearchRecommendResponse,
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
    extract_criteria_from_prompt_async,
    build_ai_explanation,
)
from app.services.chat_session_service import ChatSessionService
from app.services.ai_recommendation_pipeline import AIRecommendationPipeline
from app.services.llm_service import LLMService
from app.services.query_relaxation_service import QueryRelaxationService
from app.services.multi_turn_state_machine import SearchSessionState, VALID_STATE_TRANSITIONS

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
    if getattr(payload, "provider", None) == "rule_based":
        from app.core.prompt_template import _rule_based_extract
        criteria = _rule_based_extract(payload.prompt, payload.current_context)
        engine_used = "rule_based_nlp"
    elif not payload.current_context and prompt_key in PROMPT_CACHE:
        criteria = PROMPT_CACHE[prompt_key]
        engine_used = "memory_cache"
    else:
        # 2. XỬ LÝ BẤT ĐỒNG BỘ (ASYNC)
        criteria, engine_used = await extract_criteria_from_prompt_async(
            user_prompt=payload.prompt,
            current_context=payload.current_context,
        )
        if engine_used == "rule_based_nlp_fallback" and getattr(payload, "provider", None) == "rule_based":
            engine_used = "rule_based_nlp"

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
    "/llm-parse-and-save",
    response_model=LLMParseAndSaveResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Phân tích câu chat bằng LLM và tự động tạo phiên mới nếu chưa có (TE9C668) - AI Search prefix"
)
def parse_and_save_ai_search(
    payload: LLMParseAndSaveRequest,
    session_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    from app.services.llm_service import LLMService
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


@router.get(
    "/state-diagram",
    summary="Lấy siêu dữ liệu 8 trạng thái State Machine (Hình 8.2 - TE9C669)"
)
def get_state_diagram_metadata():
    return {
        "task_code": "TE9C669",
        "diagram_name": "State Diagram Vòng đời tìm kiếm (Hình 8.2 SRS)",
        "states": [{"state": s.value, "name": s.name} for s in SearchSessionState],
        "valid_transitions": {
            k.value: [v.value for v in vals] for k, vals in VALID_STATE_TRANSITIONS.items()
        },
    }


@router.post(
    "/relax",
    response_model=QueryRelaxationResponse,
    summary="Tìm kiếm kèm cơ chế tự động nới lỏng điều kiện (TE9C66F)"
)
def relax_search_endpoint(
    payload: QueryRelaxationRequest,
    db: Session = Depends(get_db),
):
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
    items = [
        MultiTurnRestaurantItem(
            id=r.id,
            name=r.name,
            address=r.address,
            cuisine_type=r.cuisine_type,
            avg_rating=r.avg_rating,
            min_price=r.min_price,
            max_price=r.max_price,
            distance_km=dist,
            cover_image_url=r.images[0].image_url if r.images else None,
            has_parking=r.amenities.has_parking if r.amenities else False,
            has_private_room=r.amenities.has_private_room if r.amenities else False,
        )
        for r, dist in results
    ]
    return QueryRelaxationResponse(
        results_count=len(items),
        is_relaxed=bool(meta.get("relaxation_applied")),
        relaxation_info=QueryRelaxationInfo(**meta),
        results=items,
    )
