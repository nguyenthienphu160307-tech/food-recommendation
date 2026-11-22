import json
from typing import List, Optional
from fastapi import APIRouter, Depends, status, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.search import SearchCriteria, SearchSession, SearchMessage
from app.services.chat_session_service import ChatSessionService
from app.services.geocoding_service import GeocodingService
from app.services.privacy_service import LocationPrivacyService
from app.services.llm_service import LLMService
from app.services.multi_turn_state_machine import MultiTurnStateMachine, SearchSessionState
from app.schemas.ai_search import (
    LLMParseAndSaveRequest,
    LLMParseAndSaveResponse,
    MultiTurnChatRequest,
    MultiTurnChatResponse,
    SessionStateResponse,
    DiningCriteriaSchema,
)
from app.schemas.search import (
    CreateSessionRequest,
    SessionResponse,
    CloseSessionRequest,
    CloseSessionResponse,
    SessionStatusResponse,
    TimeoutCleanupRequest,
    TimeoutCleanupResponse,
    SendMessageRequest,
    MessageResponse,
    SessionHistoryResponse,
    GeocodeRequest,
    GeocodeResponse,
    ExtractCriteriaRequest,
    SearchCriteriaCreateRequest,
    SearchCriteriaResponse,
    PurgeLocationResponse,
    RemoveCriterionRequest,
    RemoveCriterionResponse,
)

router = APIRouter(prefix="/api/chat", tags=["Trợ lý Chat AI & Geocoding (Module 2 & 3)"])
search_history_router = APIRouter(prefix="/api/search", tags=["Tìm kiếm & Lịch sử (Search History - TSK-46)"])


@router.post(
    "/sessions",
    response_model=SessionResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Khởi tạo phiên Chat AI mới (User & Guest - TSK-16)"
)
def create_session(
    payload: Optional[CreateSessionRequest] = None,
    db: Session = Depends(get_db)
):
    """
    API Khởi tạo phiên chat tìm kiếm quán ăn (TSK-16):
    - Hỗ trợ User đã đăng nhập (truyền `user_id`).
    - Hỗ trợ Khách vãng lai (`user_id = None` theo quy tắc BR-02).
    - Tạo bản ghi mới trong bảng `SearchSessions` với trạng thái `active`.
    """
    user_id = payload.user_id if payload else None
    session_obj = ChatSessionService.create_session(db, user_id=user_id)
    return SessionResponse(
        session_id=session_obj.session_id,
        user_id=session_obj.user_id,
        status=session_obj.status,
        current_state=getattr(session_obj, "current_state", "SESSION_IDLE") or "SESSION_IDLE",
        started_at=session_obj.started_at,
        total_messages=0
    )


@router.get(
    "/sessions/{session_id}",
    response_model=SessionHistoryResponse,
    summary="Lấy chi tiết phiên và toàn bộ lịch sử tin nhắn theo thứ tự thời gian (TSK-16 / TSK-45)"
)
def get_session_history(
    session_id: int,
    db: Session = Depends(get_db)
):
    """
    Lấy thông tin phiên chat và danh sách toàn bộ tin nhắn đã trao đổi:
    - Sắp xếp tăng dần theo thời gian thực (created_at ASC).
    - Phân biệt rõ tin nhắn người dùng (sender_type='user') và trợ lý ảo (sender_type='ai').
    - Hỗ trợ tải lại ngữ cảnh phiên cũ để tiếp tục trò chuyện (TSK-45 / UC-10).
    """
    session_obj = ChatSessionService.get_session(db, session_id)
    messages = ChatSessionService.get_session_messages(db, session_id)
    title_prev = ChatSessionService.get_session_preview_title(session_obj)
    last_msg_at = messages[-1].created_at if messages else session_obj.started_at

    return SessionHistoryResponse(
        session=SessionResponse(
            session_id=session_obj.session_id,
            user_id=session_obj.user_id,
            status=session_obj.status,
            current_state=getattr(session_obj, "current_state", "SESSION_IDLE") or "SESSION_IDLE",
            started_at=session_obj.started_at,
            total_messages=len(messages),
            title_preview=title_prev,
            last_message_at=last_msg_at
        ),
        messages=[
            MessageResponse(
                message_id=m.message_id,
                session_id=m.session_id,
                sender_type=m.sender_type,
                content=m.content,
                created_at=m.created_at
            )
            for m in messages
        ]
    )


@router.post(
    "/sessions/{session_id}/messages",
    response_model=MessageResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Lưu tin nhắn mới vào phiên chat theo thời gian thực"
)
def send_message(
    session_id: int,
    payload: SendMessageRequest,
    db: Session = Depends(get_db)
):
    """
    Lưu trữ tin nhắn vào bảng `SearchMessages`:
    - Ghi nhận ngay lập tức theo thời gian thực.
    - Chặn gửi tin nhắn nếu phiên đã ở trạng thái 'closed' (HTTP 400).
    """
    msg_obj = ChatSessionService.save_message(
        db=db,
        session_id=session_id,
        sender_type=payload.sender_type,
        content=payload.content
    )
    return MessageResponse(
        message_id=msg_obj.message_id,
        session_id=msg_obj.session_id,
        sender_type=msg_obj.sender_type,
        content=msg_obj.content,
        created_at=msg_obj.created_at
    )


@router.put(
    "/sessions/{session_id}/close",
    response_model=CloseSessionResponse,
    summary="Đóng phiên hội thoại chat (status='closed' - PUT)"
)
@router.post(
    "/sessions/{session_id}/close",
    response_model=CloseSessionResponse,
    summary="Đóng phiên hội thoại chat (status='closed' - POST)"
)
def close_session(
    session_id: int,
    payload: Optional[CloseSessionRequest] = None,
    db: Session = Depends(get_db)
):
    """
    Chuyển trạng thái phiên sang 'closed' (TE9C66C):
    - Được gọi khi người dùng đã tìm được quán ưng ý, chủ động kết thúc hoặc hết thời gian chờ (Timeout).
    - Cập nhật status='closed', current_state='SESSION_CLOSED', ended_at và closed_reason.
    - Hỗ trợ ghi nhận selected_restaurant_id nếu người dùng chốt quán.
    """
    reason = payload.reason if payload and payload.reason else "user_ended"
    selected_restaurant_id = payload.selected_restaurant_id if payload else None
    note = payload.note if payload else None

    session_obj = ChatSessionService.close_session(
        db=db,
        session_id=session_id,
        reason=reason,
        selected_restaurant_id=selected_restaurant_id,
        note=note,
    )

    total_msgs = len(session_obj.messages) if session_obj.messages else 0
    duration_sec = None
    if session_obj.ended_at and session_obj.started_at:
        duration_sec = round((session_obj.ended_at - session_obj.started_at).total_seconds(), 2)

    return CloseSessionResponse(
        session_id=session_obj.session_id,
        status=session_obj.status,
        current_state=getattr(session_obj, "current_state", "SESSION_CLOSED") or "SESSION_CLOSED",
        started_at=session_obj.started_at,
        ended_at=session_obj.ended_at,
        duration_seconds=duration_sec,
        closed_reason=session_obj.closed_reason or reason,
        selected_restaurant_id=selected_restaurant_id,
        total_messages=total_msgs,
        message=f"Phiên chat #{session_id} đã được đóng thành công (lý do: {session_obj.closed_reason or reason})."
    )


@router.get(
    "/sessions/{session_id}/status",
    response_model=SessionStatusResponse,
    summary="Truy vấn trạng thái phiên tìm kiếm và thông số hoạt động (TE9C66C)"
)
def get_session_status(
    session_id: int,
    timeout_minutes: Optional[int] = Query(None, description="Ngưỡng phút tùy chọn để kiểm tra timeout"),
    db: Session = Depends(get_db)
):
    """
    Truy vấn trạng thái chi tiết của phiên tìm kiếm:
    - Kiểm tra xem phiên đang active hay closed.
    - Tự động áp dụng đóng phiên nếu đã vượt quá thời gian chờ (Timeout).
    - Cung cấp thời gian không hoạt động (idle_seconds) và thời lượng hoạt động (duration_seconds).
    """
    status_info = ChatSessionService.get_session_status(db, session_id, timeout_minutes=timeout_minutes)
    return SessionStatusResponse(**status_info)


@router.post(
    "/sessions/cleanup-timeout",
    response_model=TimeoutCleanupResponse,
    summary="Quét và tự động đóng các phiên tìm kiếm hết thời gian chờ (TE9C66C)"
)
def cleanup_expired_sessions(
    payload: Optional[TimeoutCleanupRequest] = None,
    timeout_minutes: Optional[int] = Query(None, description="Ngưỡng phút tính timeout"),
    db: Session = Depends(get_db)
):
    """
    Quét toàn bộ các phiên đang ở trạng thái 'active':
    - Nếu thời gian không hoạt động vượt quá ngưỡng (mặc định 30 phút), tự động cập nhật:
      + status='closed'
      + current_state='SESSION_CLOSED'
      + closed_reason='timeout'
      + ended_at=now
    - Trả về danh sách và số lượng phiên đã tự động đóng.
    """
    mins = (payload.timeout_minutes if payload and payload.timeout_minutes else None) or timeout_minutes
    result = ChatSessionService.cleanup_expired_sessions(db, timeout_minutes=mins)
    return TimeoutCleanupResponse(**result)


@router.get(
    "/sessions",
    response_model=List[SessionResponse],
    summary="Lấy danh sách các phiên chat gần đây (TE9C66C)"
)
def list_sessions(
    user_id: Optional[int] = None,
    status: Optional[str] = Query(None, description="Lọc trạng thái: 'active', 'closed' hoặc để trống (tất cả)"),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    auto_timeout_check: bool = Query(True, description="Tự động quét và đóng các phiên quá hạn trước khi trả về"),
    db: Session = Depends(get_db)
):
    """
    Lấy danh sách các phiên chat gần nhất:
    - Hỗ trợ lọc theo user_id (User hoặc Khách).
    - Hỗ trợ lọc theo trạng thái: 'active' (đang mở) hoặc 'closed' (đã đóng).
    - Phân trang bằng offset và limit.
    """
    sessions = ChatSessionService.list_sessions(
        db,
        user_id=user_id,
        status=status,
        limit=limit,
        offset=offset,
        auto_timeout_check=auto_timeout_check
    )
    return [
        SessionResponse(
            session_id=s.session_id,
            user_id=s.user_id,
            status=s.status,
            current_state=getattr(s, "current_state", "SESSION_IDLE") or "SESSION_IDLE",
            started_at=s.started_at,
            ended_at=s.ended_at,
            closed_reason=s.closed_reason,
            total_messages=len(s.messages) if s.messages else 0
        )
    return res_list


@router.delete(
    "/sessions/{session_id}",
    status_code=status.HTTP_200_OK,
    summary="Xóa một phiên chat cũ khỏi lịch sử (TSK-45)"
)
def delete_session(
    session_id: int,
    db: Session = Depends(get_db)
):
    """Xóa hoàn toàn phiên chat cũ và toàn bộ tin nhắn liên quan (TSK-45)"""
    ChatSessionService.delete_session(db, session_id)
    return {
        "status": "success",
        "session_id": session_id,
        "message": f"Đã xóa phiên chat #{session_id} thành công."
    }


# =====================================================================
# API GEOCODING & TIÊU CHÍ TÌM KIẾM (TASK TSK-18 / PBI-08)
# =====================================================================

@router.post(
    "/geocode",
    response_model=GeocodeResponse,
    status_code=status.HTTP_200_OK,
    summary="Chuyển đổi tên khu vực/quận sang tọa độ GPS (TSK-18)"
)
def geocode_location(payload: GeocodeRequest):
    """
    API Service Geocoding (Task TSK-18 / PBI-08):
    - Nhận tên địa danh/quận/huyện hoặc trích xuất từ câu tự nhiên.
    - Tra cứu qua Từ điển Tọa độ Nội bộ siêu tốc (< 10ms).
    - Hỗ trợ fallback trực tuyến qua OpenStreetMap khi cần.
    - Trả về cặp tọa độ chuẩn (latitude, longitude) và địa chỉ chuẩn hóa.
    """
    # Nếu người dùng truyền vào cả câu dài (ví dụ: "Tìm quán ở Bình Thạnh"), tự động bóc tách tên địa danh
    extracted_name = GeocodingService.extract_location_from_text(payload.location_name)
    query_target = extracted_name if extracted_name else payload.location_name

    res = GeocodingService.geocode(
        location_name=query_target,
        enable_online_fallback=payload.enable_online_fallback
    )

    return GeocodeResponse(
        location_name=res["location_name"],
        latitude=res["latitude"],
        longitude=res["longitude"],
        formatted_address=res["formatted_address"],
        is_found=res["is_found"],
        source=res["source"]
    )


@router.post(
    "/extract",
    summary="Bóc tách toàn diện tiêu chí (Địa danh, Tọa độ, Ẩm thực, Ngân sách, Tiện ích) từ câu chat"
)
def extract_criteria_from_chat(payload: ExtractCriteriaRequest):
    """
    API bóc tách thực thể ngôn ngữ tự nhiên:
    - Nhận câu chat tiếng Việt.
    - Trích xuất: địa danh, tọa độ GPS (geocoding), món ăn, ngân sách, chỗ đậu xe.
    """
    criteria_data = GeocodingService.extract_full_criteria(payload.message)
    return {
        "status": "success",
        "raw_message": payload.message,
        "criteria": criteria_data
    }


@router.post(
    "/sessions/{session_id}/criteria",
    response_model=SearchCriteriaResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Lưu hoặc cập nhật tiêu chí tìm kiếm kèm tọa độ GPS vào SearchCriteria (TSK-18)"
)
def save_session_criteria(
    session_id: int,
    payload: SearchCriteriaCreateRequest,
    db: Session = Depends(get_db)
):
    """
    Lưu tiêu chí tìm kiếm vào bảng `SearchCriteria`:
    - Nếu có `location_text` nhưng thiếu `latitude`/`longitude`, tự động gọi GeocodingService để bù tọa độ.
    - TSK-20: Tự động áp dụng cơ chế làm mờ tọa độ theo cài đặt quyền riêng tư của người dùng (BR-08).
    - Gắn liền với `session_id` để làm tâm bán kính cho Module 3 & 4.
    """
    lat = payload.latitude
    lng = payload.longitude

    # Tự động Geocode nếu chưa có tọa độ
    if payload.location_text and (lat is None or lng is None):
        geo = GeocodingService.geocode(payload.location_text)
        lat = geo["latitude"]
        lng = geo["longitude"]

    # TSK-20: Áp dụng cơ chế bảo vệ quyền riêng tư GPS (BR-08)
    # user_id lấy từ payload (nếu có) hoặc từ session
    user_id = payload.user_id if payload.user_id else None
    if user_id is None:
        # Lấy user_id từ phiên chat nếu payload không truyền
        try:
            session_obj = ChatSessionService.get_session(db, session_id)
            user_id = session_obj.user_id
        except Exception:
            user_id = None

    privacy_result = LocationPrivacyService.apply_privacy_to_coordinates(
        lat=lat, lng=lng, user_id=user_id, db=db
    )
    lat = privacy_result["latitude"]
    lng = privacy_result["longitude"]
    is_obfuscated = privacy_result["is_obfuscated"]

    crit_obj = ChatSessionService.save_criteria(
        db=db,
        session_id=session_id,
        location_text=payload.location_text,
        latitude=lat,
        longitude=lng,
        cuisine=payload.cuisine,
        budget=payload.budget,
        has_parking=payload.has_parking,
        other_conditions=payload.other_conditions,
        is_obfuscated=is_obfuscated,
    )

    return SearchCriteriaResponse(
        criteria_id=crit_obj.criteria_id,
        session_id=crit_obj.session_id,
        location_text=crit_obj.location_text,
        latitude=crit_obj.latitude,
        longitude=crit_obj.longitude,
        cuisine=crit_obj.cuisine,
        budget=crit_obj.budget,
        has_parking=crit_obj.has_parking,
        other_conditions=crit_obj.other_conditions,
        is_obfuscated=crit_obj.is_obfuscated,
        created_at=crit_obj.created_at
    )


@router.post(
    "/sessions/{session_id}/purge-location",
    response_model=PurgeLocationResponse,
    status_code=status.HTTP_200_OK,
    summary="Xóa thủ công log tọa độ GPS tạm thời của phiên chat (TSK-20 / NFR-07)"
)
def purge_session_location(
    session_id: int,
    db: Session = Depends(get_db)
):
    """
    Thủ công kích hoạt xóa tọa độ GPS tạm thời cho một phiên chat cụ thể (TSK-20):
    - Chỉ xóa các bản ghi `SearchCriteria` có `is_obfuscated = True`.
    - Trả về số lượng bản ghi đã được xóa tọa độ.
    - Phù hợp với quy tắc NFR-07 (Data Minimization).
    """
    # Kiểm tra phiên tồn tại
    ChatSessionService.get_session(db, session_id)

    purged_count = LocationPrivacyService.purge_session_location(session_id, db)

    return PurgeLocationResponse(
        session_id=session_id,
        purged_count=purged_count,
        message=f"Đã xóa thành công tọa độ GPS của {purged_count} bản ghi trong phiên #{session_id}."
    )


@router.get(
    "/sessions/{session_id}/criteria",
    response_model=Optional[SearchCriteriaResponse],
    summary="Lấy tiêu chí tìm kiếm mới nhất của phiên chat"
)
def get_session_criteria(
    session_id: int,
    db: Session = Depends(get_db)
):
    """Truy vấn tiêu chí tìm kiếm hiện tại của phiên chat từ bảng `SearchCriteria`"""
    crit_obj = ChatSessionService.get_latest_criteria(db, session_id)
    if not crit_obj:
        return None

    return SearchCriteriaResponse(
        criteria_id=crit_obj.criteria_id,
        session_id=crit_obj.session_id,
        location_text=crit_obj.location_text,
        latitude=crit_obj.latitude,
        longitude=crit_obj.longitude,
        cuisine=crit_obj.cuisine,
        budget=crit_obj.budget,
        has_parking=crit_obj.has_parking,
        other_conditions=crit_obj.other_conditions,
        is_obfuscated=getattr(crit_obj, "is_obfuscated", False),
        created_at=crit_obj.created_at
    )


@router.post(
    "/sessions/{session_id}/criteria/remove-field",
    response_model=RemoveCriterionResponse,
    status_code=status.HTTP_200_OK,
    summary="Xóa nhanh một tiêu chí đã bóc tách khỏi phiên hội thoại (POST - TE9C673)"
)
def remove_criterion_field(
    session_id: int,
    payload: RemoveCriterionRequest,
    db: Session = Depends(get_db)
):
    """
    Xóa nhanh một tiêu chí đã bóc tách (Parsed Criteria Chips - TE9C673):
    - Cho phép người dùng bấm xóa nhanh từng tiêu chí (Vị trí, Món, Ngân sách, Đậu ô tô, v.v.).
    - Tự động lưu bản ghi SearchCriteria mới và tính toán lại danh sách nhà hàng phù hợp nhất.
    """
    result = MultiTurnStateMachine.remove_criterion_and_update(
        session_id=session_id,
        field=payload.field,
        db=db,
    )
    return RemoveCriterionResponse(**result)


@router.delete(
    "/sessions/{session_id}/criteria/{field}",
    response_model=RemoveCriterionResponse,
    status_code=status.HTTP_200_OK,
    summary="Xóa nhanh một tiêu chí đã bóc tách khỏi phiên hội thoại (DELETE - TE9C673)"
)
def delete_criterion_field(
    session_id: int,
    field: str,
    db: Session = Depends(get_db)
):
    """
    Xóa nhanh một tiêu chí đã bóc tách theo RESTful DELETE (TE9C673):
    - Ví dụ: DELETE /api/chat/sessions/1/criteria/cuisine hoặc /location hoặc /has_parking.
    """
    result = MultiTurnStateMachine.remove_criterion_and_update(
        session_id=session_id,
        field=field,
        db=db,
    )
    return RemoveCriterionResponse(**result)


# =====================================================================
# TÍCH HỢP LLM/NLP PHÂN TÍCH CHAT SANG SEARCHCRITERIA (TASK TE9C668)
# =====================================================================

@router.post(
    "/sessions/{session_id}/parse-and-save",
    response_model=LLMParseAndSaveResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Phân tích câu chat tự nhiên bằng LLM/NLP và lưu vào SearchCriteria (TE9C668)"
)
def parse_and_save_session_message(
    session_id: int,
    payload: LLMParseAndSaveRequest,
    db: Session = Depends(get_db)
):
    """
    API Tích hợp LLM/NLP bóc tách câu chat tự nhiên sang SearchCriteria (TE9C668):
    - Kết nối dịch vụ LLM (OpenAI API / Gemini API) với fallback Rule-based Tiếng Việt.
    - Truyền câu hỏi của người dùng kèm ngữ cảnh Multi-turn của phiên.
    - Bóc tách tiêu chí: location_text, cuisine, budget, has_parking, other_conditions.
    - Tự động Geocode tọa độ GPS (latitude, longitude) từ location_text.
    - Áp dụng làm mờ tọa độ bảo vệ quyền riêng tư nếu người dùng cấu hình (BR-08 / TSK-20).
    - Lưu câu hỏi vào bảng `SearchMessages` (sender_type='user').
    - Lưu kết quả bóc tách vào bảng `SearchCriteria`.
    - Lưu câu phản hồi giải thích của AI vào bảng `SearchMessages` (sender_type='ai').
    """
    result = LLMService.parse_and_save_to_criteria(
        db=db,
        session_id=session_id,
        user_message=payload.message,
        provider=payload.provider or "auto",
        user_id=payload.user_id,
    )
    return LLMParseAndSaveResponse(**result)






@router.post(
    "/parse-and-save",
    response_model=LLMParseAndSaveResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Phân tích câu chat bằng LLM và tự động tạo phiên mới nếu chưa có (TE9C668)"
)
def parse_and_save_auto_session(
    payload: LLMParseAndSaveRequest,
    session_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """
    Tiện ích khởi tạo phiên và bóc tách tiêu chí trong 1 request duy nhất (TE9C668):
    - Nếu `session_id` là None: tự động tạo SearchSession mới.
    - Gọi LLMService để phân tích và lưu SearchCriteria.
    """
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


# =====================================================================
# MULTI-TURN STATE MACHINE & CONTEXT MANAGER (TASK TE9C669 / HÌNH 8.2)
# =====================================================================

@router.post(
    "/sessions/{session_id}/multi-turn",
    response_model=MultiTurnChatResponse,
    status_code=status.HTTP_200_OK,
    summary="Xử lý câu hỏi tiếp theo đa lượt theo State Diagram Hình 8.2 (TE9C669)"
)
def process_multi_turn_chat(
    session_id: int,
    payload: MultiTurnChatRequest,
    db: Session = Depends(get_db)
):
    """
    API Hội thoại nhiều lượt (Multi-turn State Machine - TE9C669 / Hình 8.2 SRS):
    - Nhận câu hỏi tiếp nối của người dùng (VD: 'Quán nào rẻ hơn?', 'Đổi sang Quận 3', 'Có phòng riêng không?').
    - Thực thi vòng đời State Diagram:
      + State 6 (Result Presented) -> State 7 (Context Refining): Hợp nhất tiêu chí mới vào SearchCriteria hiện tại.
      + State 2 (Parsing Intent): Phân tích NLP trích xuất thực thể mới.
      + State 3 (Spatial Filtering): Quét bán kính GPS và lọc tiện ích.
      + State 4 (Query Relaxation): Tự động nới lỏng bán kính/ngân sách khi 0 kết quả.
      + State 5 (Ranking & AI): Xếp hạng độ khớp, sinh lý do đề xuất và lưu DB.
      + State 6 (Result Presented): Trả về danh sách quán và trạng thái mới.
      + Nếu người dùng muốn kết thúc -> State 8 (Session Closed).
    """
    result = MultiTurnStateMachine.process_turn(
        session_id=session_id,
        user_message=payload.message,
        db=db,
        user_id=payload.user_id,
        provider=payload.provider or "auto",
    )
    return MultiTurnChatResponse(**result)


@router.get(
    "/sessions/{session_id}/state",
    response_model=SessionStateResponse,
    summary="Truy vấn trạng thái hiện tại trong State Machine & lịch sử tiêu chí (TE9C669)"
)
def get_session_state_machine_info(
    session_id: int,
    db: Session = Depends(get_db)
):
    """
    Lấy thông tin trạng thái State Machine hiện tại của phiên hội thoại (Hình 8.2):
    - Trạng thái hiện tại: SESSION_IDLE, RESULT_PRESENTED, CONTEXT_REFINING, SESSION_CLOSED...
    - Tổng số lượt tin nhắn đã trao đổi.
    - Toàn bộ lịch sử các phiên bản SearchCriteria đã được merge qua các lượt chat.
    """
    session = ChatSessionService.get_session(db, session_id)
    current_st = MultiTurnStateMachine.get_current_state(session)
    messages = ChatSessionService.get_session_messages(db, session_id)

    # Lấy toàn bộ tiêu chí đã lưu theo thứ tự thời gian tăng dần
    criteria_list = (
        db.query(SearchCriteria)
        .filter(SearchCriteria.session_id == session_id)
        .order_by(SearchCriteria.created_at.asc())
        .all()
    )

    history = []
    for c in criteria_list:
        other_d = {}
        if c.other_conditions:
            try:
                other_d = json.loads(c.other_conditions)
            except Exception:
                pass
        history.append({
            "criteria_id": c.criteria_id,
            "location_text": c.location_text,
            "latitude": c.latitude,
            "longitude": c.longitude,
            "cuisine": c.cuisine,
            "budget": c.budget,
            "has_parking": c.has_parking,
            "other_conditions": other_d,
            "is_obfuscated": c.is_obfuscated,
            "created_at": c.created_at,
        })

    latest = history[-1] if history else None

    return SessionStateResponse(
        session_id=session.session_id,
        current_state=current_st.value,
        status=session.status,
        started_at=session.started_at,
        total_messages=len(messages),
        total_criteria_versions=len(history),
        latest_criteria=latest,
        criteria_history=history,
    )






