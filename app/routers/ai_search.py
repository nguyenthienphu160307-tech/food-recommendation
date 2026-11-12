from fastapi import APIRouter
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

router = APIRouter(prefix="/api/search", tags=["AI Prompt & Trích xuất Tiêu chí (TE9C65A)"])


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
    }


@router.post(
    "/extract-criteria",
    response_model=ExtractCriteriaResponse,
    summary="Trích xuất tiêu chí ăn uống từ câu hỏi tự nhiên (NER / Structured JSON)"
)
def extract_dining_criteria(payload: ExtractCriteriaRequest):
    """
    Nhận câu truy vấn tiếng Việt tự nhiên của người dùng và bóc tách thành JSON Schema chuẩn:
    - `location_text`: Địa điểm / Khu vực
    - `cuisine`: Loại hình ẩm thực
    - `budget`: Ngân sách tối đa (VNĐ)
    - `has_parking`: Chỗ đỗ xe ô tô
    - `other_conditions`: Phòng riêng (`has_private_room`), Thú cưng (`pet_friendly`), Ăn chay (`vegetarian_support`), Ngoài trời (`has_outdoor`), Số người (`group_size`)
    """
    criteria, engine_used = extract_criteria_from_prompt(
        user_prompt=payload.prompt,
        current_context=payload.current_context,
    )
    explanation = build_ai_explanation(criteria)

    return ExtractCriteriaResponse(
        prompt=payload.prompt,
        extracted_criteria=criteria,
        ai_explanation=explanation,
        extraction_engine=engine_used,
    )