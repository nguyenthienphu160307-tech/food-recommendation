import json
import os
import re
from typing import Any, Dict, Optional, Tuple
import httpx

from app.schemas.ai_search import DiningCriteriaSchema, OtherConditionsSchema

# ==============================================================================
# 1. JSON SCHEMA CHUẨN ĐỂ TRUYỀN VÀO LLM STRUCTURED OUTPUT / FUNCTION CALLING
# ==============================================================================
def get_dining_criteria_json_schema() -> Dict[str, Any]:
    """Trả về JSON Schema chuẩn của DiningCriteriaSchema phục vụ LLM."""
    return DiningCriteriaSchema.model_json_schema()


# ==============================================================================
# 2. PROMPT TEMPLATE CHUẨN (SYSTEM INSTRUCTION + FEW-SHOT EXAMPLES)
# ==============================================================================
SYSTEM_PROMPT_TEMPLATE = """Bạn là AI NLP Engine của hệ thống gợi ý nhà hàng Smart Dining.
Nhiệm vụ của bạn là phân tích câu truy vấn tiếng Việt của người dùng và trích xuất chính xác các tiêu chí ăn uống sang định dạng JSON.

### QUY TẮC TRÍCH XUẤT BẮT BUỘC:
1. Chỉ trả về duy nhất một chuỗi JSON hợp lệ tuân thủ chặt chẽ JSON Schema bên dưới. Không giải thích, không bọc ngoài bằng văn bản thừa.
2. Chuẩn hóa các trường dữ liệu:
   - `location_text`: Trích xuất địa danh, tên đường, phường, quận/huyện (VD: "Quận 1", "Bình Thạnh", "Gò Vấp", "Thủ Đức"). Nếu không đề cập, để `null`.
   - `cuisine`: Chuẩn hóa về một trong các danh mục trên hệ thống nếu khớp ý nghĩa:
     + "nướng", "thịt nướng", "bbq", "hàn quốc" -> "BBQ Hàn Quốc"
     + "chay", "thuần chay", "thanh đạm", "vegan" -> "Món Chay"
     + "cơm tấm", "sườn bì chả" -> "Cơm tấm"
     + "phở", "bún", "lẩu nấm", "món việt", "cơm việt" -> "Món Việt"
     + Nếu là món khác, giữ nguyên tên ngắn gọn. Nếu không đề cập, để `null`.
   - `budget`: Quy đổi mọi mức tiền tệ tiếng Việt về số nguyên VNĐ (Integer):
     + "300k", "300 nghìn", "300 ngàn", "3 trăm" -> 300000
     + "1.5 triệu", "1tr5" -> 1500000
     + Nếu không đề cập ngân sách, để `null`.
   - `has_parking`: Đặt `true` nếu người dùng yêu cầu "chỗ đậu ô tô", "bãi đỗ xe hơi", "đậu xe", "gửi ô tô". Đặt `false` nếu nói "không cần chỗ đậu xe". Ngược lại để `null`.
   - `other_conditions`:
     + `has_private_room`: `true` nếu cần "phòng riêng", "phòng VIP", "yên tĩnh", "tiếp khách".
     + `pet_friendly`: `true` nếu nhắc tới "thú cưng", "mang chó mèo", "pet".
     + `vegetarian_support`: `true` nếu nhắc tới "ăn chay", "có món chay", "hỗ trợ đồ chay".
     + `has_outdoor`: `true` nếu nhắc tới "ngoài trời", "sân vườn", "thoáng mát", "rooftop".
     + `group_size`: Số nguyên chỉ số lượng người ăn (VD: "nhóm 4 người" -> 4, "cặp đôi" -> 2).

### JSON SCHEMA ĐẦU RA:
{json_schema}

### VÍ DỤ MẪU (FEW-SHOT EXAMPLES):
Input: "Nhóm 4 người muốn ăn đồ nướng ở Quận 1 có chỗ đậu ô tô dưới 300k/người, cần phòng riêng yên tĩnh"
Output:
{{
  "location_text": "Quận 1",
  "cuisine": "BBQ Hàn Quốc",
  "budget": 300000,
  "has_parking": true,
  "other_conditions": {{
    "has_private_room": true,
    "pet_friendly": null,
    "vegetarian_support": null,
    "has_outdoor": null,
    "group_size": 4
  }}
}}
"""

def build_extraction_prompt(user_prompt: str, current_context: Optional[Dict[str, Any]] = None) -> str:
    """Ghép nối System Prompt, JSON Schema, Ngữ cảnh cũ và câu hỏi hiện tại."""
    schema_str = json.dumps(get_dining_criteria_json_schema(), ensure_ascii=False, indent=2)
    base_prompt = SYSTEM_PROMPT_TEMPLATE.format(json_schema=schema_str)

    context_block = ""
    if current_context:
        context_block = (
            f"\n### NGỮ CẢNH HỘI THOẠI TRƯỚC ĐÓ (Kế thừa và cập nhật thêm tiêu chí mới):\n"
            f"{json.dumps(current_context, ensure_ascii=False)}\n"
        )

    return f"{base_prompt}{context_block}\n### TRUY VẤN CỦA NGƯỜI DÙNG:\nInput: \"{user_prompt}\"\nOutput:\n"


# ==============================================================================
# 3. FALLBACK PARSER & ASYNC EXTRACTION ENGINE (TASK TE9C66B)
# ==============================================================================
def _rule_based_extract(user_prompt: str, current_context: Optional[Dict[str, Any]] = None) -> DiningCriteriaSchema:
    """
    Bộ trích xuất NLP Tiếng Việt tốc độ cao (Fallback Parser).
    Được tối ưu Regex để luôn phản hồi dưới 1 giây.
    """
    text = user_prompt.lower()
    ctx = current_context or {}
    other_ctx = ctx.get("other_conditions") or {}

    location_text = ctx.get("location_text")
    loc_match = re.search(r"(quận\s*\d+|q\.\s*\d+|gò vấp|bình thạnh|thủ đức|tân bình|phú nhuận|đa kao)", text)
    if loc_match:
        raw_loc = loc_match.group(1).strip()
        location_text = raw_loc.title() if not raw_loc.startswith("q.") else raw_loc.upper()

    cuisine = ctx.get("cuisine")
    if any(k in text for k in ["nướng", "bbq", "hàn quốc"]):
        cuisine = "BBQ Hàn Quốc"
    elif any(k in text for k in ["chay", "thanh đạm", "vegan"]):
        cuisine = "Món Chay"
    elif "cơm tấm" in text or "sườn bì" in text:
        cuisine = "Cơm tấm"
    elif any(k in text for k in ["phở", "bún", "món việt", "lẩu"]):
        cuisine = "Món Việt"

    budget = ctx.get("budget")
    m_k = re.search(r"(\d+(?:[\.,]\d+)?)\s*(?:k|nghìn|ngàn)\b", text)
    m_tr = re.search(r"(\d+(?:[\.,]\d+)?)\s*(?:triệu|tr|củ)\b", text)
    if m_k:
        budget = int(float(m_k.group(1).replace(",", ".")) * 1000)
    elif m_tr:
        budget = int(float(m_tr.group(1).replace(",", ".")) * 1000000)

    has_parking = ctx.get("has_parking")
    if any(k in text for k in ["đỗ ô tô", "đậu xe", "bãi xe"]):
        has_parking = False if "không cần" in text else True

    return DiningCriteriaSchema(
        location_text=location_text,
        cuisine=cuisine,
        budget=budget,
        has_parking=has_parking,
        other_conditions=OtherConditionsSchema(
            has_private_room=other_ctx.get("has_private_room") or bool(re.search(r"phòng (riêng|vip)|yên tĩnh", text)),
            pet_friendly=other_ctx.get("pet_friendly") or bool(re.search(r"thú cưng|chó|mèo", text)),
            vegetarian_support=other_ctx.get("vegetarian_support") or bool(re.search(r"chay|thuần chay", text)),
            has_outdoor=other_ctx.get("has_outdoor") or bool(re.search(r"ngoài trời|sân vườn|thoáng mát", text)),
            group_size=int(re.search(r"(\d+)\s*(?:người|khách)", text).group(1)) if re.search(r"(\d+)\s*(?:người|khách)", text) else (2 if "cặp đôi" in text else other_ctx.get("group_size")),
        ),
    )


def build_ai_explanation(criteria: DiningCriteriaSchema) -> str:
    """Sinh câu giải thích tự nhiên tiếng Việt dựa trên tiêu chí đã bóc tách."""
    parts = []
    if criteria.cuisine: parts.append(f"ẩm thực **{criteria.cuisine}**")
    if criteria.location_text: parts.append(f"tại khu vực **{criteria.location_text}**")
    if criteria.budget: parts.append(f"ngân sách dưới **{criteria.budget:,}đ/người**".replace(",", "."))
    if criteria.has_parking: parts.append("có **bãi đỗ ô tô**")

    conds = []
    if criteria.other_conditions.has_private_room: conds.append("phòng riêng yên tĩnh")
    if criteria.other_conditions.pet_friendly: conds.append("cho phép mang thú cưng")
    if criteria.other_conditions.vegetarian_support: conds.append("hỗ trợ món chay")
    if criteria.other_conditions.has_outdoor: conds.append("không gian ngoài trời")

    if conds: parts.append("kèm tiện ích: " + ", ".join(conds))

    if not parts:
        return "Hệ thống đã ghi nhận yêu cầu và sẽ gợi ý các địa điểm có đánh giá cao nhất."
    return "Đã bóc tách tiêu chí: Ưu tiên nhà hàng " + ", ".join(parts) + "."


async def extract_criteria_from_prompt_async(
    user_prompt: str,
    current_context: Optional[Dict[str, Any]] = None
) -> Tuple[DiningCriteriaSchema, str]:
    """
    Hàm phân tích từ khóa bất đồng bộ (Async) TE9C66B:
    - Timeout ngắn gọn (max 4.5 giây) để đảm bảo SLA < 5s.
    - Gọi API Gemini Async, nếu lỗi/timeout -> rẽ nhánh ngay sang Fallback Parser.
    """
    gemini_key = os.getenv("GEMINI_API_KEY", "").strip()
    
    if gemini_key and "your_" not in gemini_key:
        try:
            full_prompt = build_extraction_prompt(user_prompt, current_context)
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={gemini_key}"
            payload = {
                "contents": [{"parts": [{"text": full_prompt}]}],
                "generationConfig": {"responseMimeType": "application/json"},
            }
            # Sử dụng AsyncClient với timeout tối đa 4.5s để thỏa mãn NFR-01 (< 5s)
            async with httpx.AsyncClient(timeout=4.5) as client:
                resp = await client.post(url, json=payload)
                if resp.status_code == 200:
                    raw_text = resp.json()["candidates"][0]["content"]["parts"][0]["text"]
                    parsed_dict = json.loads(raw_text)
                    return DiningCriteriaSchema(**parsed_dict), "llm_api_async"
        except Exception as e:
            # Bắt mọi lỗi: Timeout, JSONDecodeError, Mất mạng...
            print(f"[Fallback Triggered] Lỗi gọi LLM: {e}")
            pass

    # Nếu không có API Key, hoặc API chậm quá 4.5s, lập tức dùng Fallback Parser (chạy chưa tới 0.1s)
    return _rule_based_extract(user_prompt, current_context), "rule_based_nlp_fallback"