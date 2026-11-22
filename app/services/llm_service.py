"""
==============================================================================
LLM & NLP SERVICE (TASK TE9C668 / MODULE 2 & 3)
==============================================================================
Dịch vụ tích hợp Mô hình Ngôn ngữ Lớn (LLM / NLP) bóc tách câu hỏi tự nhiên:
1. Kết nối Google Gemini API (gemini-2.5-flash / gemini-1.5-flash) với Structured Output.
2. Kết nối OpenAI API (gpt-4o-mini / gpt-3.5-turbo) với JSON Mode.
3. Hỗ trợ cơ chế Fallback thông minh sang Rule-based NLP Tiếng Việt siêu tốc khi
   chưa cấu hình API Key hoặc khi gặp sự cố mạng/hết hạn ngạch.
4. Tự động Geocoding tọa độ GPS từ địa danh bóc tách được (location_text).
5. Tự động áp dụng cơ chế bảo vệ quyền riêng tư vị trí (BR-08 / NFR-07).
6. Tự động lưu trữ kết quả phân tích vào bảng `SearchCriteria` và lưu tin nhắn vào
   bảng `SearchMessages` phục vụ Multi-turn Chat.
==============================================================================
"""

import json
import logging
import os
import re
from datetime import datetime
from typing import Any, Dict, Optional, Tuple

import httpx
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.prompt_template import (
    SYSTEM_PROMPT_TEMPLATE,
    build_ai_explanation,
    build_extraction_prompt,
    get_dining_criteria_json_schema,
    _rule_based_extract,
)
from app.models.search import SearchCriteria, SearchMessage, SearchSession
from app.schemas.ai_search import DiningCriteriaSchema, OtherConditionsSchema
from app.services.geocoding_service import GeocodingService
from app.services.privacy_service import LocationPrivacyService

logger = logging.getLogger(__name__)


class LLMService:
    """Tầng Service xử lý kết nối LLM (Gemini / OpenAI) và lưu trữ SearchCriteria."""

    # Model defaults
    GEMINI_MODELS = ["gemini-2.5-flash", "gemini-1.5-flash"]
    OPENAI_DEFAULT_MODEL = "gpt-4o-mini"

    @classmethod
    def get_configured_providers(cls) -> Dict[str, bool]:
        """Kiểm tra xem các API Key nào đang được cấu hình."""
        gemini_key = os.getenv("GEMINI_API_KEY", "").strip()
        openai_key = os.getenv("OPENAI_API_KEY", "").strip()
        return {
            "gemini": bool(gemini_key and "your_" not in gemini_key.lower()),
            "openai": bool(openai_key and "your_" not in openai_key.lower()),
        }

    @classmethod
    def call_gemini_api(
        cls,
        prompt: str,
        current_context: Optional[Dict[str, Any]] = None,
        api_key: Optional[str] = None,
        timeout: float = 8.0,
    ) -> DiningCriteriaSchema:
        """
        Gọi Google Gemini API để bóc tách câu truy vấn sang DiningCriteriaSchema.
        """
        gemini_key = api_key or os.getenv("GEMINI_API_KEY", "").strip()
        if not gemini_key or "your_" in gemini_key.lower():
            raise ValueError("GEMINI_API_KEY chưa được cấu hình hoặc không hợp lệ.")

        full_prompt = build_extraction_prompt(prompt, current_context)
        payload = {
            "contents": [{"parts": [{"text": full_prompt}]}],
            "generationConfig": {
                "responseMimeType": "application/json",
                "temperature": 0.1,
            },
        }

        last_error = None
        for model in cls.GEMINI_MODELS:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={gemini_key}"
            try:
                with httpx.Client(timeout=timeout) as client:
                    resp = client.post(url, json=payload)
                    if resp.status_code == 200:
                        data = resp.json()
                        parts = data.get("candidates", [{}])[0].get("content", {}).get("parts", [])
                        if parts:
                            raw_text = parts[0].get("text", "")
                            cleaned = cls._clean_json_string(raw_text)
                            parsed_dict = json.loads(cleaned)
                            return DiningCriteriaSchema(**parsed_dict)
                    else:
                        last_error = f"Gemini API returned {resp.status_code}: {resp.text}"
            except Exception as e:
                last_error = str(e)

        raise RuntimeError(f"Không thể gọi Gemini API: {last_error}")

    @classmethod
    def call_openai_api(
        cls,
        prompt: str,
        current_context: Optional[Dict[str, Any]] = None,
        api_key: Optional[str] = None,
        timeout: float = 8.0,
    ) -> DiningCriteriaSchema:
        """
        Gọi OpenAI Chat Completions API với response_format={"type": "json_object"}.
        """
        openai_key = api_key or os.getenv("OPENAI_API_KEY", "").strip()
        if not openai_key or "your_" in openai_key.lower():
            raise ValueError("OPENAI_API_KEY chưa được cấu hình hoặc không hợp lệ.")

        schema_str = json.dumps(get_dining_criteria_json_schema(), ensure_ascii=False, indent=2)
        system_content = SYSTEM_PROMPT_TEMPLATE.format(json_schema=schema_str)

        user_content = prompt
        if current_context:
            user_content = (
                f"[Ngữ cảnh trước: {json.dumps(current_context, ensure_ascii=False)}]\n"
                f"Câu hỏi hiện tại: {prompt}"
            )

        headers = {
            "Authorization": f"Bearer {openai_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": cls.OPENAI_DEFAULT_MODEL,
            "messages": [
                {"role": "system", "content": system_content},
                {"role": "user", "content": user_content},
            ],
            "response_format": {"type": "json_object"},
            "temperature": 0.1,
        }

        url = "https://api.openai.com/v1/chat/completions"
        with httpx.Client(timeout=timeout) as client:
            resp = client.post(url, json=payload, headers=headers)
            if resp.status_code == 200:
                data = resp.json()
                raw_text = data.get("choices", [{}])[0].get("message", {}).get("content", "")
                cleaned = cls._clean_json_string(raw_text)
                parsed_dict = json.loads(cleaned)
                return DiningCriteriaSchema(**parsed_dict)
            else:
                raise RuntimeError(f"OpenAI API returned {resp.status_code}: {resp.text}")

    @classmethod
    def extract_criteria(
        cls,
        prompt: str,
        current_context: Optional[Dict[str, Any]] = None,
        provider: str = "auto",
    ) -> Tuple[DiningCriteriaSchema, str, str]:
        """
        Hàm trung tâm bóc tách tiêu chí ăn uống:
        - provider: 'auto', 'gemini', 'openai', hoặc 'rule_based'
        - Trả về Tuple: (DiningCriteriaSchema, ai_explanation, engine_used)
        """
        prov = (provider or "auto").lower().strip()
        active_providers = cls.get_configured_providers()

        # 1. Thử gọi Gemini nếu được chỉ định hoặc auto
        if prov in ("gemini", "auto") and active_providers["gemini"]:
            try:
                criteria = cls.call_gemini_api(prompt, current_context)
                explanation = build_ai_explanation(criteria)
                return criteria, explanation, "gemini_api"
            except Exception as e:
                logger.warning(f"[LLMService] Gemini extraction failed: {e}. Trying fallback.")
                if prov == "gemini":
                    # Fallback sang rule-based khi chỉ định gemini nhưng bị lỗi
                    criteria = _rule_based_extract(prompt, current_context)
                    explanation = build_ai_explanation(criteria)
                    return criteria, explanation, "rule_based_nlp"

        # 2. Thử gọi OpenAI nếu được chỉ định hoặc auto
        if prov in ("openai", "auto") and active_providers["openai"]:
            try:
                criteria = cls.call_openai_api(prompt, current_context)
                explanation = build_ai_explanation(criteria)
                return criteria, explanation, "openai_api"
            except Exception as e:
                logger.warning(f"[LLMService] OpenAI extraction failed: {e}. Trying fallback.")
                if prov == "openai":
                    # Fallback sang rule-based khi chỉ định openai nhưng bị lỗi
                    criteria = _rule_based_extract(prompt, current_context)
                    explanation = build_ai_explanation(criteria)
                    return criteria, explanation, "rule_based_nlp"

        # 3. Mặc định / Fallback sang Rule-based NLP Tiếng Việt
        criteria = _rule_based_extract(prompt, current_context)
        explanation = build_ai_explanation(criteria)
        return criteria, explanation, "rule_based_nlp"

    @classmethod
    def parse_and_save_to_criteria(
        cls,
        db: Session,
        session_id: int,
        user_message: str,
        provider: str = "auto",
        user_id: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Quy trình trọn gói bóc tách câu chat tự nhiên và lưu vào bảng SearchCriteria:
        1. Kiểm tra session hợp lệ và đang mở (active).
        2. Lưu tin nhắn người dùng vào SearchMessages.
        3. Lấy tiêu chí trước đó của phiên để làm ngữ cảnh Multi-turn (nếu có).
        4. Gọi LLM/NLP để bóc tách tiêu chí ăn uống.
        5. Tự động Geocode tọa độ GPS từ location_text.
        6. Áp dụng cơ chế làm mờ tọa độ bảo vệ quyền riêng tư (BR-08 / TSK-20).
        7. Lưu tiêu chí đã bóc tách vào bảng SearchCriteria.
        8. Lưu câu trả lời / giải thích của AI vào SearchMessages.
        9. Trả về kết quả hoàn chỉnh.
        """
        # Bước 1: Kiểm tra session
        session_obj = db.query(SearchSession).filter(SearchSession.session_id == session_id).first()
        if not session_obj:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Không tìm thấy phiên chat với ID={session_id}.",
            )

        if session_obj.status != "active":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Phiên chat này đã kết thúc (closed). Không thể gửi thêm tin nhắn mới.",
            )

        clean_message = (user_message or "").strip()
        if not clean_message:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Nội dung câu chat không được để trống.",
            )

        # Bước 2: Lưu tin nhắn người dùng vào SearchMessages
        user_msg = SearchMessage(
            session_id=session_id,
            sender_type="user",
            content=clean_message,
            created_at=datetime.utcnow(),
        )
        db.add(user_msg)
        db.commit()
        db.refresh(user_msg)

        # Bước 3: Lấy tiêu chí trước đó của phiên để hỗ trợ Multi-turn
        latest_crit = (
            db.query(SearchCriteria)
            .filter(SearchCriteria.session_id == session_id)
            .order_by(SearchCriteria.criteria_id.desc())
            .first()
        )

        current_context = None
        if latest_crit:
            other_dict = {}
            if latest_crit.other_conditions:
                try:
                    other_dict = json.loads(latest_crit.other_conditions)
                except Exception:
                    pass
            current_context = {
                "location_text": latest_crit.location_text,
                "cuisine": latest_crit.cuisine,
                "budget": latest_crit.budget,
                "has_parking": latest_crit.has_parking,
                "other_conditions": other_dict,
            }

        # Bước 4: Bóc tách tiêu chí qua LLM/NLP
        criteria_schema, ai_explanation, engine_used = cls.extract_criteria(
            prompt=clean_message,
            current_context=current_context,
            provider=provider,
        )

        # Bước 5: Geocoding vị trí địa lý
        lat = None
        lng = None
        loc_text = criteria_schema.location_text

        if loc_text:
            geo_res = GeocodingService.geocode(loc_text)
            lat = geo_res.get("latitude")
            lng = geo_res.get("longitude")
        elif latest_crit and latest_crit.latitude and latest_crit.longitude:
            # Kế thừa tọa độ từ lượt trước nếu câu hiện tại không đổi địa điểm
            lat = latest_crit.latitude
            lng = latest_crit.longitude
            loc_text = latest_crit.location_text

        # Bước 6: Áp dụng quyền riêng tư GPS (BR-08 / TSK-20)
        effective_user_id = user_id if user_id is not None else session_obj.user_id
        privacy_res = LocationPrivacyService.apply_privacy_to_coordinates(
            lat=lat, lng=lng, user_id=effective_user_id, db=db
        )
        final_lat = privacy_res["latitude"]
        final_lng = privacy_res["longitude"]
        is_obfuscated = privacy_res["is_obfuscated"]

        # Bước 7: Lưu vào bảng SearchCriteria
        other_conds_dict = criteria_schema.other_conditions.model_dump()
        other_conds_json = json.dumps(other_conds_dict, ensure_ascii=False)

        new_criteria = SearchCriteria(
            session_id=session_id,
            location_text=loc_text,
            latitude=final_lat,
            longitude=final_lng,
            cuisine=criteria_schema.cuisine,
            budget=criteria_schema.budget,
            has_parking=criteria_schema.has_parking,
            other_conditions=other_conds_json,
            is_obfuscated=is_obfuscated,
            created_at=datetime.utcnow(),
        )
        db.add(new_criteria)
        db.commit()
        db.refresh(new_criteria)

        # Bước 8: Lưu phản hồi của AI vào SearchMessages
        ai_msg = SearchMessage(
            session_id=session_id,
            sender_type="ai",
            content=ai_explanation,
            created_at=datetime.utcnow(),
        )
        db.add(ai_msg)
        db.commit()
        db.refresh(ai_msg)

        # Bước 9: Trả về kết quả
        return {
            "session_id": session_id,
            "criteria_id": new_criteria.criteria_id,
            "user_message_id": user_msg.message_id,
            "ai_message_id": ai_msg.message_id,
            "user_message": clean_message,
            "ai_explanation": ai_explanation,
            "extraction_engine": engine_used,
            "location_text": new_criteria.location_text,
            "latitude": new_criteria.latitude,
            "longitude": new_criteria.longitude,
            "cuisine": new_criteria.cuisine,
            "budget": new_criteria.budget,
            "has_parking": new_criteria.has_parking,
            "other_conditions": other_conds_dict,
            "is_obfuscated": new_criteria.is_obfuscated,
            "created_at": new_criteria.created_at,
        }

    @staticmethod
    def _clean_json_string(text: str) -> str:
        """Loại bỏ markdown block ```json ... ``` nếu LLM trả về."""
        cleaned = text.strip()
        if cleaned.startswith("```"):
            cleaned = re.sub(r"^```(?:json)?\n?", "", cleaned, flags=re.IGNORECASE)
            cleaned = re.sub(r"\n?```$", "", cleaned)
        return cleaned.strip()
