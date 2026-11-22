"""
==============================================================================
MULTI-TURN STATE MACHINE & CONTEXT MANAGER (TASK TE9C669 / HÌNH 8.2 SRS)
==============================================================================
Bộ quản lý Ngữ cảnh Hội thoại đa lượt và Cỗ máy Trạng thái (State Machine):
Thực thi đúng State Diagram Vòng đời tìm kiếm (Hình 8.2 trong SRS):
  [Start] -> 1. SESSION_IDLE (Khởi tạo phiên)
          -> 2. PARSING_INTENT (Phân tích NLP câu hỏi)
          -> 3. SPATIAL_FILTERING (Truy vấn không gian GPS & tiện ích)
          -> (Nếu 0 kết quả) -> 4. QUERY_RELAXATION (Nới lỏng điều kiện)
          -> 5. RANKING_AND_AI (Xếp hạng & sinh lời giải thích)
          -> 6. RESULT_PRESENTED (Hiển thị kết quả & bản đồ)
          -> (Hỏi tiếp multi-turn) -> 7. CONTEXT_REFINING (Hợp nhất tiêu chí)
          -> (Loop lại 2. PARSING_INTENT -> ...)
          -> (Chọn quán / Kết thúc / Timeout) -> 8. SESSION_CLOSED (Đóng phiên) -> [End]

Quy tắc Hợp nhất Tiêu chí (Criteria Merging):
- Khi hỏi tiếp (ví dụ: 'Quán nào rẻ hơn?', 'Đổi sang Quận 3', 'Có phòng riêng không?'):
  + Tự động kế thừa các tiêu chí đã có ở lượt trước.
  + Hợp nhất tiêu chí mới một cách thông minh (vị trí, ẩm thực, ngân sách trần, tiện ích).
  + Tự động Geocode lại tọa độ nếu có địa danh mới.
==============================================================================
"""

import json
import logging
import re
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple

from fastapi import HTTPException, status
from sqlalchemy import or_
from sqlalchemy.orm import Session, joinedload

from app.core.prompt_template import build_ai_explanation
from app.models.restaurant import Restaurant, RestaurantAmenity
from app.models.search import SearchCriteria, SearchMessage, SearchSession
from app.schemas.ai_search import DiningCriteriaSchema, OtherConditionsSchema
from app.services.geo_service import calculate_bounding_box, calculate_haversine_distance
from app.services.geocoding_service import GeocodingService
from app.services.llm_service import LLMService
from app.services.privacy_service import LocationPrivacyService

logger = logging.getLogger(__name__)


class SearchSessionState(str, Enum):
    """8 Trạng thái trong Sơ đồ Trạng thái Vòng đời Tìm kiếm (Hình 8.2 SRS)."""
    SESSION_IDLE = "SESSION_IDLE"               # 1. Khởi tạo Phiên (Session Idle) - Chờ câu hỏi hoặc vị trí GPS
    PARSING_INTENT = "PARSING_INTENT"           # 2. Đang phân tích NLP (Parsing Intent) - Trích xuất vị trí, món, ngân sách, tiện ích
    SPATIAL_FILTERING = "SPATIAL_FILTERING"     # 3. Truy vấn Không gian (Spatial Filtering) - Quét bán kính GPS & lọc tiện ích
    QUERY_RELAXATION = "QUERY_RELAXATION"       # 4. Nới lỏng Điều kiện (Query Relaxation) - Mở rộng bán kính / ngân sách khi 0 kết quả
    RANKING_AND_AI = "RANKING_AND_AI"           # 5. Xếp hạng & Giải thích (Ranking & AI) - Chấm điểm độ khớp & sinh lý do đề xuất
    RESULT_PRESENTED = "RESULT_PRESENTED"       # 6. Hiển thị Kết quả (Result Presented) - Hiển thị danh sách quán & Bản đồ
    CONTEXT_REFINING = "CONTEXT_REFINING"       # 7. Hội thoại Nhiều lượt (Context Refining) - Cập nhật SearchCriteria trong cùng phiên
    SESSION_CLOSED = "SESSION_CLOSED"           # 8. Đóng Phiên (Session Closed) - Lưu lịch sử SearchSessions (status=closed)


# Đồ thị chuyển trạng thái hợp lệ tuân thủ Hình 8.2
VALID_STATE_TRANSITIONS: Dict[SearchSessionState, List[SearchSessionState]] = {
    SearchSessionState.SESSION_IDLE: [
        SearchSessionState.PARSING_INTENT,
        SearchSessionState.SESSION_CLOSED,
    ],
    SearchSessionState.PARSING_INTENT: [
        SearchSessionState.SPATIAL_FILTERING,
        SearchSessionState.SESSION_CLOSED,
    ],
    SearchSessionState.SPATIAL_FILTERING: [
        SearchSessionState.QUERY_RELAXATION,    # Khi kết quả = 0
        SearchSessionState.RANKING_AND_AI,        # Khi có kết quả
        SearchSessionState.SESSION_CLOSED,
    ],
    SearchSessionState.QUERY_RELAXATION: [
        SearchSessionState.RANKING_AND_AI,        # Tìm thấy ứng viên thay thế
        SearchSessionState.SESSION_CLOSED,
    ],
    SearchSessionState.RANKING_AND_AI: [
        SearchSessionState.RESULT_PRESENTED,     # Trả về Top N quán
        SearchSessionState.SESSION_CLOSED,
    ],
    SearchSessionState.RESULT_PRESENTED: [
        SearchSessionState.CONTEXT_REFINING,     # Hỏi tiếp (Multi-turn)
        SearchSessionState.PARSING_INTENT,       # Gửi câu hỏi mới trực tiếp
        SearchSessionState.SESSION_CLOSED,       # Chọn quán / Kết thúc / Timeout
    ],
    SearchSessionState.CONTEXT_REFINING: [
        SearchSessionState.PARSING_INTENT,       # Hợp nhất tiêu chí & phân tích NLP tiếp
        SearchSessionState.SPATIAL_FILTERING,
        SearchSessionState.SESSION_CLOSED,
    ],
    SearchSessionState.SESSION_CLOSED: [],       # Terminal State
}


class MultiTurnStateMachine:
    """Cỗ máy quản lý trạng thái hội thoại đa lượt và hợp nhất tiêu chí (TE9C669)."""

    @classmethod
    def get_current_state(cls, session: SearchSession) -> SearchSessionState:
        """Lấy trạng thái hiện tại của phiên hội thoại."""
        if session.status == "closed":
            return SearchSessionState.SESSION_CLOSED

        state_str = getattr(session, "current_state", None)
        if not state_str:
            return SearchSessionState.SESSION_IDLE

        try:
            return SearchSessionState(state_str)
        except ValueError:
            return SearchSessionState.SESSION_IDLE

    @classmethod
    def transition_to(
        cls,
        session: SearchSession,
        target_state: SearchSessionState,
        db: Session,
    ) -> SearchSessionState:
        """
        Thực hiện chuyển trạng thái theo đúng State Diagram:
        - Kiểm tra tính hợp lệ của bước chuyển.
        - Cập nhật trường current_state và status trong CSDL.
        """
        current = cls.get_current_state(session)
        allowed = VALID_STATE_TRANSITIONS.get(current, [])

        # Cho phép chuyển trạng thái nếu nằm trong đồ thị chuyển hợp lệ
        if target_state not in allowed and target_state != current:
            logger.warning(
                f"[StateMachine] Invalid transition from {current} to {target_state}. Forcing transition for session #{session.session_id}."
            )

        session.current_state = target_state.value
        if target_state == SearchSessionState.SESSION_CLOSED:
            session.status = "closed"
            if not session.ended_at:
                session.ended_at = datetime.utcnow()
            if not session.closed_reason:
                session.closed_reason = "manual"

        db.commit()
        db.refresh(session)
        return target_state

    @classmethod
    def merge_criteria(
        cls,
        current_crit: Optional[SearchCriteria],
        incoming_crit: DiningCriteriaSchema,
        raw_message: str,
    ) -> Dict[str, Any]:
        """
        Thuật toán hợp nhất thông minh tiêu chí qua các lượt hội thoại (Multi-turn Refinement):
        1. Vị trí (location_text, lat, lng):
           - Nếu có địa danh mới -> Cập nhật địa danh mới và tự động Geocode lại tọa độ.
           - Nếu không đổi địa danh -> Kế thừa địa danh & tọa độ của lượt trước.
        2. Loại ẩm thực (cuisine):
           - Nếu nhắc món mới -> Cập nhật.
           - Nếu không -> Kế thừa.
        3. Ngân sách (budget):
           - Bắt các câu giảm giá tương đối ("rẻ hơn", "giá thấp hơn", "hạt dẻ hơn"):
             + Nếu lượt trước đã có budget: giảm 25% (làm tròn đẹp đến 10.000đ).
             + Nếu lượt trước chưa có: đặt mốc tiết kiệm 150.000đ.
           - Nếu chỉ định mức giá cụ thể mới -> Cập nhật.
           - Nếu không nhắc -> Kế thừa.
        4. Chỗ đậu ô tô (has_parking):
           - "có chỗ đậu xe" -> True; "không cần đậu xe" -> False; không nhắc -> Kế thừa.
        5. Tiện ích mở rộng (other_conditions):
           - Hợp nhất từng cờ boolean độc lập (phòng riêng, thú cưng, ngoài trời, món chay, số người).
        """
        text = raw_message.lower()

        # Giá trị mặc định nếu chưa có lượt trước
        loc_text = incoming_crit.location_text
        lat = None
        lng = None
        cuisine = incoming_crit.cuisine
        budget = incoming_crit.budget
        has_parking = incoming_crit.has_parking

        other_merged: Dict[str, Any] = {
            "has_private_room": None,
            "pet_friendly": None,
            "vegetarian_support": None,
            "has_outdoor": None,
            "group_size": None,
        }

        # Đọc dữ liệu từ lượt trước nếu có
        if current_crit:
            loc_text = current_crit.location_text
            lat = current_crit.latitude
            lng = current_crit.longitude
            cuisine = current_crit.cuisine
            budget = current_crit.budget
            has_parking = current_crit.has_parking

            if current_crit.other_conditions:
                try:
                    loaded = json.loads(current_crit.other_conditions)
                    if isinstance(loaded, dict):
                        other_merged.update(loaded)
                except Exception:
                    pass

        # 1. Xử lý Vị trí (Location)
        # Nhận diện các mẫu câu đổi địa điểm rõ ràng: "đổi sang Quận 3", "qua Bình Thạnh", "tìm ở Gò Vấp"
        is_location_change = bool(
            incoming_crit.location_text and
            (not current_crit or incoming_crit.location_text.lower() != (current_crit.location_text or "").lower())
        )
        if is_location_change:
            loc_text = incoming_crit.location_text
            # Geocode lại tọa độ cho địa danh mới
            geo = GeocodingService.geocode(loc_text)
            lat = geo.get("latitude")
            lng = geo.get("longitude")

        # 2. Xử lý Ẩm thực (Cuisine)
        if incoming_crit.cuisine:
            cuisine = incoming_crit.cuisine

        # 3. Xử lý Ngân sách (Budget)
        is_cheaper_intent = any(k in text for k in [
            "rẻ hơn", "re hon", "thấp hơn", "thap hon", "tiết kiệm hơn", "hạt dẻ", "hat de", "ít tiền hơn", "bình dân hơn"
        ])
        has_explicit_budget_in_text = bool(
            re.search(r"(\d+(?:[\.,]\d+)?)\s*(?:k|nghìn|ngàn|nghin|ngan|triệu|tr| củ)\b", text) or
            re.search(r"(\d{5,7})\s*(?:đ|vnd|vnđ|đồng)?\b", text)
        )

        if is_cheaper_intent and not has_explicit_budget_in_text:
            if budget and budget > 50000:
                # Giảm 25% ngân sách hiện tại, làm tròn xuống bội số 10.000đ
                reduced = int((budget * 0.75) // 10000 * 10000)
                budget = max(50000, reduced)
            else:
                budget = 150000  # Mốc mặc định hợp lý cho câu hỏi "rẻ hơn"
        elif incoming_crit.budget:
            budget = incoming_crit.budget

        # 4. Xử lý Chỗ đậu ô tô (Parking)
        if incoming_crit.has_parking is not None:
            has_parking = incoming_crit.has_parking
        elif any(k in text for k in ["chỗ đậu ô tô", "đậu xe", "bãi xe", "đỗ xe", "gửi ô tô"]):
            has_parking = False if any(neg in text for neg in ["không cần", "khong can", "bỏ", "khỏi"]) else True

        # 5. Xử lý Other Conditions (Hợp nhất từng trường)
        inc_other = incoming_crit.other_conditions

        # Phòng riêng
        if inc_other.has_private_room is not None:
            other_merged["has_private_room"] = inc_other.has_private_room
        elif any(k in text for k in ["phòng riêng", "phong rieng", "phòng vip", "yên tĩnh"]):
            other_merged["has_private_room"] = False if any(neg in text for neg in ["không cần", "khong can", "bỏ", "khỏi"]) else True

        # Thú cưng
        if inc_other.pet_friendly is not None:
            other_merged["pet_friendly"] = inc_other.pet_friendly
        elif any(k in text for k in ["thú cưng", "thu cung", "chó", "mèo", "pet"]):
            other_merged["pet_friendly"] = False if any(neg in text for neg in ["không mang", "cấm", "bỏ"]) else True

        # Món chay
        if inc_other.vegetarian_support is not None:
            other_merged["vegetarian_support"] = inc_other.vegetarian_support
        elif any(k in text for k in ["chay", "món chay", "thuần chay"]):
            other_merged["vegetarian_support"] = False if any(neg in text for neg in ["không ăn chay", "bỏ"]) else True

        # Ngoài trời
        if inc_other.has_outdoor is not None:
            other_merged["has_outdoor"] = inc_other.has_outdoor
        elif any(k in text for k in ["ngoài trời", "ngoai troi", "sân vườn", "thoáng mát", "rooftop"]):
            other_merged["has_outdoor"] = False if any(neg in text for neg in ["không cần", "bỏ"]) else True

        # Số người ăn
        if inc_other.group_size is not None:
            other_merged["group_size"] = inc_other.group_size

        return {
            "location_text": loc_text,
            "latitude": lat,
            "longitude": lng,
            "cuisine": cuisine,
            "budget": budget,
            "has_parking": has_parking,
            "other_conditions": other_merged,
        }

    @classmethod
    def filter_restaurants_spatial(
        cls,
        db: Session,
        lat: Optional[float],
        lng: Optional[float],
        radius_km: float,
        cuisine: Optional[str] = None,
        budget: Optional[int] = None,
        has_parking: Optional[bool] = None,
        other_conditions: Optional[Dict[str, Any]] = None,
        limit: int = 5,
    ) -> List[Tuple[Restaurant, float]]:
        """
        Thực thi Truy vấn Không gian (State 3 - Spatial Filtering):
        - Quét theo bán kính GPS (Haversine + Bounding Box).
        - Lọc theo loại món, khoảng giá ngân sách, và 5 tiện ích.
        """
        other = other_conditions or {}
        query = (
            db.query(Restaurant)
            .options(
                joinedload(Restaurant.amenities),
                joinedload(Restaurant.images),
            )
            .filter(Restaurant.status == "active")
        )

        # Lọc ẩm thực
        if cuisine:
            cuisine_norm = cuisine.lower()
            if "nướng" in cuisine_norm or "bbq" in cuisine_norm:
                query = query.filter(or_(Restaurant.cuisine_type.ilike("%nướng%"), Restaurant.cuisine_type.ilike("%lẩu%")))
            elif "chay" in cuisine_norm:
                query = query.filter(Restaurant.cuisine_type.ilike("%chay%"))
            elif "cơm" in cuisine_norm:
                query = query.filter(Restaurant.cuisine_type.ilike("%cơm%"))
            else:
                query = query.filter(Restaurant.cuisine_type.ilike(f"%{cuisine}%"))

        # Lọc ngân sách (quán có mức giá tối thiểu min_price <= budget)
        if budget and budget > 0:
            query = query.filter(Restaurant.min_price <= float(budget))

        # Lọc tiện ích RestaurantAmenities
        if has_parking is True:
            query = query.join(Restaurant.amenities).filter(RestaurantAmenity.has_parking.is_(True))
        if other.get("has_private_room") is True:
            query = query.join(Restaurant.amenities).filter(RestaurantAmenity.has_private_room.is_(True))
        if other.get("has_outdoor") is True:
            query = query.join(Restaurant.amenities).filter(RestaurantAmenity.has_outdoor.is_(True))
        if other.get("pet_friendly") is True:
            query = query.join(Restaurant.amenities).filter(RestaurantAmenity.pet_friendly.is_(True))
        if other.get("vegetarian_support") is True:
            query = query.join(Restaurant.amenities).filter(RestaurantAmenity.vegetarian_support.is_(True))

        candidates = query.all()

        # Tính khoảng cách GPS và lọc bán kính
        matched: List[Tuple[Restaurant, float]] = []
        center_lat = lat or 10.7769
        center_lng = lng or 106.7009

        for r in candidates:
            dist = calculate_haversine_distance(center_lat, center_lng, r.latitude, r.longitude)
            if dist <= radius_km:
                matched.append((r, round(dist, 2)))

        # Sắp xếp theo: Điểm đánh giá giảm dần, khoảng cách tăng dần
        matched.sort(key=lambda item: (-item[0].avg_rating, item[1]))
        return matched[:limit]

    @classmethod
    def execute_relaxation(
        cls,
        db: Session,
        lat: Optional[float],
        lng: Optional[float],
        current_radius: float,
        cuisine: Optional[str] = None,
        budget: Optional[int] = None,
        has_parking: Optional[bool] = None,
        other_conditions: Optional[Dict[str, Any]] = None,
    ) -> Tuple[List[Tuple[Restaurant, float]], Dict[str, Any]]:
        """
        Thực thi Nới lỏng Điều kiện (State 4 - Query Relaxation khi Kết quả = 0):
        1. Bước 1: Mở rộng bán kính tìm kiếm (3km -> 5km -> 10km).
        2. Bước 2: Nâng trần ngân sách thêm 25% - 35%.
        3. Bước 3: Nới lỏng các tiện ích thứ cấp (ngoài trời, thú cưng) giữ tiện ích cốt lõi.
        """
        relaxation_notes = {
            "expanded_radius_km": None,
            "expanded_budget": None,
            "relaxed_amenities": False,
        }

        # 1. Thử mở rộng bán kính lên 5km hoặc 10km
        expanded_radii = [5.0, 10.0, 15.0]
        for rad in expanded_radii:
            if rad > current_radius:
                res = cls.filter_restaurants_spatial(
                    db=db,
                    lat=lat,
                    lng=lng,
                    radius_km=rad,
                    cuisine=cuisine,
                    budget=budget,
                    has_parking=has_parking,
                    other_conditions=other_conditions,
                )
                if res:
                    relaxation_notes["expanded_radius_km"] = rad
                    return res, relaxation_notes

        # 2. Thử nới lỏng ngân sách (+30%)
        if budget:
            relaxed_budget = int(budget * 1.3)
            res = cls.filter_restaurants_spatial(
                db=db,
                lat=lat,
                lng=lng,
                radius_km=10.0,
                cuisine=cuisine,
                budget=relaxed_budget,
                has_parking=has_parking,
                other_conditions=other_conditions,
            )
            if res:
                relaxation_notes["expanded_radius_km"] = 10.0
                relaxation_notes["expanded_budget"] = relaxed_budget
                return res, relaxation_notes

        # 3. Nới lỏng tiện ích mở rộng (chỉ giữ vị trí và loại món)
        res = cls.filter_restaurants_spatial(
            db=db,
            lat=lat,
            lng=lng,
            radius_km=10.0,
            cuisine=cuisine,
            budget=None,
            has_parking=None,
            other_conditions=None,
        )
        relaxation_notes["expanded_radius_km"] = 10.0
        relaxation_notes["relaxed_amenities"] = True
        return res, relaxation_notes

    @classmethod
    def process_turn(
        cls,
        session_id: int,
        user_message: str,
        db: Session,
        user_id: Optional[int] = None,
        provider: str = "auto",
    ) -> Dict[str, Any]:
        """
        Xử lý trọn vẹn 1 lượt hội thoại tuân thủ State Diagram (Hình 8.2):
        1. Kiểm tra session. Nếu đã đóng -> Trả về lỗi 400.
        2. Nếu người dùng muốn kết thúc ("cảm ơn", "chọn được rồi", "kết thúc", "đóng phiên"):
           -> Chuyển thẳng sang State 8 (SESSION_CLOSED).
        3. Kiểm tra xem là lượt đầu (State 1 -> State 2) hay lượt hỏi tiếp (State 6 -> State 7 -> State 2).
        4. Bóc tách tiêu chí mới bằng LLM/NLP và hợp nhất vào SearchCriteria hiện tại.
        5. State 3: Truy vấn Không gian (Spatial Filtering).
        6. Nếu kết quả = 0 -> State 4: Nới lỏng Điều kiện (Query Relaxation).
        7. State 5: Xếp hạng & Giải thích (Ranking & AI).
        8. Lưu SearchCriteria mới và lưu SearchMessages.
        9. State 6: Hiển thị Kết quả (Result Presented).
        """
        session = db.query(SearchSession).filter(SearchSession.session_id == session_id).first()
        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Không tìm thấy phiên chat với ID={session_id}.",
            )

        current_st = cls.get_current_state(session)
        from app.services.chat_session_service import ChatSessionService

        # Kiểm tra tự động timeout khi có truy cập mới (TE9C66C)
        if session.status == "active" and ChatSessionService.is_session_timed_out(session):
            ChatSessionService.check_and_apply_timeout(db, session)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Phiên tìm kiếm này đã hết thời gian chờ (Timeout) và đã tự động đóng. Vui lòng khởi tạo phiên mới.",
            )

        if current_st == SearchSessionState.SESSION_CLOSED or session.status == "closed":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Phiên chat này đã kết thúc (closed). Không thể gửi thêm tin nhắn mới.",
            )

        clean_msg = (user_message or "").strip()
        if not clean_msg:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Nội dung câu hỏi không được để trống.",
            )

        # Kiểm tra ý định kết thúc phiên
        is_closing_intent = any(k in clean_msg.lower() for k in [
            "kết thúc", "ket thuc", "đóng phiên", "dong phien", "tạm biệt", "tam biet", "chọn được quán rồi", "cảm ơn bạn nhé"
        ])
        if is_closing_intent:
            ChatSessionService.close_session(db, session_id, reason="user_ended")
            # Lưu tin nhắn kết thúc
            user_msg = SearchMessage(session_id=session_id, sender_type="user", content=clean_msg, created_at=datetime.utcnow())
            ai_msg = SearchMessage(
                session_id=session_id,
                sender_type="ai",
                content="Rất vui được hỗ trợ bạn tìm được quán ăn ưng ý! Chúc bạn có một bữa ăn ngon miệng. Phiên tìm kiếm đã kết thúc.",
                created_at=datetime.utcnow(),
            )
            db.add_all([user_msg, ai_msg])
            db.commit()
            return {
                "session_id": session_id,
                "current_state": SearchSessionState.SESSION_CLOSED.value,
                "status": "closed",
                "ai_message": ai_msg.content,
                "criteria": None,
                "results": [],
                "relaxation_applied": False,
            }

        # Lưu tin nhắn người dùng vào SearchMessages
        user_msg = SearchMessage(session_id=session_id, sender_type="user", content=clean_msg, created_at=datetime.utcnow())
        db.add(user_msg)
        db.commit()
        db.refresh(user_msg)

        # Lấy tiêu chí mới nhất của phiên (nếu có)
        latest_crit = (
            db.query(SearchCriteria)
            .filter(SearchCriteria.session_id == session_id)
            .order_by(SearchCriteria.criteria_id.desc())
            .first()
        )

        # Chuyển trạng thái:
        if latest_crit:
            # Lượt hỏi tiếp (Multi-turn): State 6 -> State 7 (CONTEXT_REFINING)
            cls.transition_to(session, SearchSessionState.CONTEXT_REFINING, db)
        else:
            # Lượt đầu tiên: State 1 -> State 2 (PARSING_INTENT)
            cls.transition_to(session, SearchSessionState.PARSING_INTENT, db)

        # Chuyển sang State 2: PARSING_INTENT để phân tích câu hỏi
        cls.transition_to(session, SearchSessionState.PARSING_INTENT, db)

        current_ctx_dict = None
        if latest_crit:
            other_d = {}
            if latest_crit.other_conditions:
                try:
                    other_d = json.loads(latest_crit.other_conditions)
                except Exception:
                    pass
            current_ctx_dict = {
                "location_text": latest_crit.location_text,
                "cuisine": latest_crit.cuisine,
                "budget": latest_crit.budget,
                "has_parking": latest_crit.has_parking,
                "other_conditions": other_d,
            }

        # Bóc tách câu hỏi với LLM/NLP
        incoming_schema, _, engine_used = LLMService.extract_criteria(
            prompt=clean_msg,
            current_context=current_ctx_dict,
            provider=provider,
        )

        # Hợp nhất tiêu chí mới vào SearchCriteria hiện tại (Merge Engine)
        merged_dict = cls.merge_criteria(
            current_crit=latest_crit,
            incoming_crit=incoming_schema,
            raw_message=clean_msg,
        )

        # Chuyển sang State 3: SPATIAL_FILTERING (Truy vấn Không gian)
        cls.transition_to(session, SearchSessionState.SPATIAL_FILTERING, db)

        matched_restaurants = cls.filter_restaurants_spatial(
            db=db,
            lat=merged_dict["latitude"],
            lng=merged_dict["longitude"],
            radius_km=3.0,  # Bán kính mặc định ban đầu 3km
            cuisine=merged_dict["cuisine"],
            budget=merged_dict["budget"],
            has_parking=merged_dict["has_parking"],
            other_conditions=merged_dict["other_conditions"],
        )

        relaxation_applied = False
        relaxation_info: Dict[str, Any] = {}

        # Nếu kết quả = 0 -> Chuyển sang State 4: QUERY_RELAXATION (Nới lỏng điều kiện)
        if len(matched_restaurants) == 0:
            cls.transition_to(session, SearchSessionState.QUERY_RELAXATION, db)
            relaxed_results, relaxation_info = cls.execute_relaxation(
                db=db,
                lat=merged_dict["latitude"],
                lng=merged_dict["longitude"],
                current_radius=3.0,
                cuisine=merged_dict["cuisine"],
                budget=merged_dict["budget"],
                has_parking=merged_dict["has_parking"],
                other_conditions=merged_dict["other_conditions"],
            )
            matched_restaurants = relaxed_results
            relaxation_applied = True

        # Chuyển sang State 5: RANKING_AND_AI (Xếp hạng & Giải thích)
        cls.transition_to(session, SearchSessionState.RANKING_AND_AI, db)

        # Sinh lời giải thích AI
        explanation_parts = []
        if latest_crit:
            explanation_parts.append("Đã cập nhật yêu cầu tìm kiếm của bạn")
        else:
            explanation_parts.append("Đã phân tích yêu cầu tìm kiếm của bạn")

        criteria_desc = []
        if merged_dict["location_text"]:
            criteria_desc.append(f"tại **{merged_dict['location_text']}**")
        if merged_dict["cuisine"]:
            criteria_desc.append(f"món **{merged_dict['cuisine']}**")
        if merged_dict["budget"]:
            criteria_desc.append(f"ngân sách dưới **{merged_dict['budget']:,}đ**".replace(",", "."))
        if merged_dict["has_parking"]:
            criteria_desc.append("có bãi đỗ ô tô")
        if merged_dict["other_conditions"].get("has_private_room"):
            criteria_desc.append("phòng riêng VIP")
        if merged_dict["other_conditions"].get("vegetarian_support"):
            criteria_desc.append("có món chay")
        if merged_dict["other_conditions"].get("pet_friendly"):
            criteria_desc.append("cho thú cưng")

        if criteria_desc:
            explanation_parts.append("(" + ", ".join(criteria_desc) + ").")
        else:
            explanation_parts.append(".")

        if relaxation_applied:
            rad_exp = relaxation_info.get("expanded_radius_km")
            bud_exp = relaxation_info.get("expanded_budget")
            if rad_exp:
                explanation_parts.append(f"Hệ thống đã tự động nới lỏng bán kính lên **{rad_exp} km**")
            if bud_exp:
                explanation_parts.append(f"và mở rộng ngân sách tới **{bud_exp:,}đ**".replace(",", "."))
            explanation_parts.append("để tìm các địa điểm chất lượng tốt nhất gần bạn.")

        if matched_restaurants:
            top_names = [f"**{r[0].name}** ({r[1]} km - ★{r[0].avg_rating})" for r in matched_restaurants[:3]]
            explanation_parts.append(f"Dưới đây là {len(matched_restaurants)} gợi ý phù hợp nhất: {', '.join(top_names)}.")
        else:
            explanation_parts.append("Hiện chưa tìm thấy nhà hàng nào thỏa mãn đầy đủ các tiêu chí nới lỏng.")

        ai_explanation = " ".join(explanation_parts)

        # Áp dụng quyền riêng tư GPS
        effective_user_id = user_id if user_id is not None else session.user_id
        privacy_res = LocationPrivacyService.apply_privacy_to_coordinates(
            lat=merged_dict["latitude"],
            lng=merged_dict["longitude"],
            user_id=effective_user_id,
            db=db,
        )

        # Lưu bản ghi SearchCriteria mới vào CSDL
        new_criteria = SearchCriteria(
            session_id=session_id,
            location_text=merged_dict["location_text"],
            latitude=privacy_res["latitude"],
            longitude=privacy_res["longitude"],
            cuisine=merged_dict["cuisine"],
            budget=merged_dict["budget"],
            has_parking=merged_dict["has_parking"],
            other_conditions=json.dumps(merged_dict["other_conditions"], ensure_ascii=False),
            is_obfuscated=privacy_res["is_obfuscated"],
            created_at=datetime.utcnow(),
        )
        db.add(new_criteria)

        # Lưu tin nhắn phản hồi của AI vào SearchMessages
        ai_msg = SearchMessage(
            session_id=session_id,
            sender_type="ai",
            content=ai_explanation,
            created_at=datetime.utcnow(),
        )
        db.add(ai_msg)
        db.commit()
        db.refresh(new_criteria)
        db.refresh(ai_msg)

        # Chuyển sang State 6: RESULT_PRESENTED (Hiển thị Kết quả)
        cls.transition_to(session, SearchSessionState.RESULT_PRESENTED, db)

        # Chuẩn bị danh sách nhà hàng trả về
        results_payload = [
            {
                "id": r[0].id,
                "name": r[0].name,
                "address": r[0].address,
                "cuisine_type": r[0].cuisine_type,
                "avg_rating": r[0].avg_rating,
                "min_price": r[0].min_price,
                "max_price": r[0].max_price,
                "distance_km": r[1],
                "cover_image_url": r[0].images[0].image_url if r[0].images else None,
                "has_parking": r[0].amenities.has_parking if r[0].amenities else False,
                "has_private_room": r[0].amenities.has_private_room if r[0].amenities else False,
            }
            for r in matched_restaurants
        ]

        return {
            "session_id": session_id,
            "current_state": SearchSessionState.RESULT_PRESENTED.value,
            "status": session.status,
            "criteria_id": new_criteria.criteria_id,
            "user_message_id": user_msg.message_id,
            "ai_message_id": ai_msg.message_id,
            "ai_message": ai_explanation,
            "extraction_engine": engine_used,
            "relaxation_applied": relaxation_applied,
            "relaxation_info": relaxation_info,
            "merged_criteria": {
                "criteria_id": new_criteria.criteria_id,
                "location_text": new_criteria.location_text,
                "latitude": new_criteria.latitude,
                "longitude": new_criteria.longitude,
                "cuisine": new_criteria.cuisine,
                "budget": new_criteria.budget,
                "has_parking": new_criteria.has_parking,
                "other_conditions": merged_dict["other_conditions"],
                "is_obfuscated": new_criteria.is_obfuscated,
                "created_at": new_criteria.created_at,
            },
            "results": results_payload,
        }
