import os
from datetime import datetime
from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.user import User, UserProfile
from app.models.search import SearchSession, SearchMessage, SearchCriteria


class ChatSessionService:
    """
    Tầng Service / Repository xử lý nghiệp vụ Phiên Chat AI & Tiêu chí Tìm kiếm (TSK-16, TSK-18, TE9C66C):
    - Khởi tạo phiên cho cả User đã đăng nhập và Khách vãng lai (user_id = NULL).
    - Lưu trữ và truy vấn tin nhắn hội thoại theo thời gian thực.
    - Quản lý vòng đời phiên chat (active, closed) và trạng thái State Machine.
    - Quản lý và xử lý tự động hết thời gian chờ (Session Idle Timeout).
    - Lưu trữ và truy xuất tiêu chí tìm kiếm kèm tọa độ Geocoding (SearchCriteria).
    """

    DEFAULT_TIMEOUT_MINUTES: int = int(os.getenv("SESSION_TIMEOUT_MINUTES", "30"))

    @staticmethod
    def create_session(db: Session, user_id: Optional[int] = None) -> SearchSession:
        """
        Khởi tạo phiên chat mới:
        - Nếu có user_id: kiểm tra xem tài khoản có tồn tại trong bảng Users hay không.
        - Nếu user_id là None: hỗ trợ chế độ Khách (Guest Mode theo BR-02).
        """
        if user_id is not None:
            user = db.query(User).filter(User.id == user_id).first()
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Không tìm thấy người dùng với ID={user_id} để khởi tạo phiên chat."
                )

        new_session = SearchSession(
            user_id=user_id,
            status="active",
            current_state="SESSION_IDLE",
            started_at=datetime.utcnow()
        )
        db.add(new_session)
        db.commit()
        db.refresh(new_session)
        return new_session

    @staticmethod
    def get_session(db: Session, session_id: int) -> SearchSession:
        """Lấy thông tin phiên chat theo ID. Nếu không có -> Ném lỗi 404."""
        session_obj = db.query(SearchSession).filter(SearchSession.session_id == session_id).first()
        if not session_obj:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Không tìm thấy phiên chat với ID={session_id}."
            )
        return session_obj

    @classmethod
    def get_last_activity_time(cls, session: SearchSession) -> datetime:
        """
        Lấy mốc thời gian hoạt động gần nhất của phiên:
        - Thời điểm của tin nhắn mới nhất trong phiên (nếu có).
        - Nếu chưa có tin nhắn nào, lấy thời điểm khởi tạo started_at.
        """
        if session.messages:
            last_msg = session.messages[-1]
            if last_msg.created_at:
                return last_msg.created_at
        return session.started_at or datetime.utcnow()

    @classmethod
    def is_session_timed_out(
        cls,
        session: SearchSession,
        timeout_minutes: Optional[int] = None
    ) -> bool:
        """
        Kiểm tra xem phiên có bị hết thời gian chờ (idle timeout) hay không:
        - Phiên đã đóng ('closed') -> Không tính timeout (đã đóng).
        - Phiên đang hoạt động ('active') -> So sánh thời gian không hoạt động với ngưỡng timeout.
        """
        if session.status != "active":
            return False

        threshold_mins = timeout_minutes if (timeout_minutes and timeout_minutes > 0) else cls.DEFAULT_TIMEOUT_MINUTES
        last_activity = cls.get_last_activity_time(session)
        idle_seconds = (datetime.utcnow() - last_activity).total_seconds()
        return idle_seconds > (threshold_mins * 60)

    @classmethod
    def check_and_apply_timeout(
        cls,
        db: Session,
        session: SearchSession,
        timeout_minutes: Optional[int] = None
    ) -> bool:
        """
        Kiểm tra và tự động áp dụng đóng phiên nếu đã hết thời gian chờ:
        - Chuyển status = 'closed', current_state = 'SESSION_CLOSED'.
        - Ghi nhận ended_at và closed_reason = 'timeout'.
        - Tự động xóa dữ liệu vị trí tạm thời theo chính sách bảo mật (NFR-07 / BR-08).
        - Trả về True nếu phiên vừa bị timeout, False nếu còn hợp lệ.
        """
        if session.status == "active" and cls.is_session_timed_out(session, timeout_minutes):
            session.status = "closed"
            session.current_state = "SESSION_CLOSED"
            session.ended_at = datetime.utcnow()
            session.closed_reason = "timeout"
            db.commit()
            db.refresh(session)

            # Auto-purge tọa độ tạm thời nếu cần
            cls._trigger_auto_purge_if_needed(db, session)
            return True
        return False

    @classmethod
    def close_session(
        cls,
        db: Session,
        session_id: int,
        reason: str = "user_ended",
        selected_restaurant_id: Optional[int] = None,
        note: Optional[str] = None
    ) -> SearchSession:
        """
        Đóng phiên tìm kiếm (chuyển status='active' -> 'closed' - TE9C66C):
        - Hỗ trợ các lý do: 'user_ended', 'restaurant_selected', 'timeout', 'manual'.
        - Cập nhật current_state = 'SESSION_CLOSED' đồng bộ State Diagram (Hình 8.2).
        - Lưu mốc thời gian ended_at, closed_reason.
        - TSK-20: Tự động xóa log tọa độ GPS tạm thời nếu người dùng bật auto_purge (NFR-07).
        """
        session_obj = cls.get_session(db, session_id)

        # Idempotent: nếu đã đóng trước đó, chỉ cập nhật nếu thiếu thông tin
        if session_obj.status == "closed":
            if not session_obj.ended_at:
                session_obj.ended_at = datetime.utcnow()
            if not session_obj.closed_reason and reason:
                session_obj.closed_reason = reason
            db.commit()
            db.refresh(session_obj)
            return session_obj

        session_obj.status = "closed"
        session_obj.current_state = "SESSION_CLOSED"
        session_obj.ended_at = datetime.utcnow()
        session_obj.closed_reason = reason or "user_ended"
        db.commit()
        db.refresh(session_obj)

        # TSK-20: Auto-purge tọa độ tạm thời
        cls._trigger_auto_purge_if_needed(db, session_obj)

        return session_obj

    @classmethod
    def cleanup_expired_sessions(
        cls,
        db: Session,
        timeout_minutes: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Quét và đóng hàng loạt các phiên tìm kiếm đã quá hạn thời gian chờ (Timeout Sweep - TE9C66C):
        - Quét tất cả các SearchSession đang có status = 'active'.
        - Tự động đóng các phiên vượt quá ngưỡng timeout_minutes.
        - Trả về thống kê số lượng và danh sách ID các phiên đã đóng.
        """
        threshold_mins = timeout_minutes if (timeout_minutes and timeout_minutes > 0) else cls.DEFAULT_TIMEOUT_MINUTES
        active_sessions = db.query(SearchSession).filter(SearchSession.status == "active").all()

        closed_ids: List[int] = []
        now = datetime.utcnow()

        for s in active_sessions:
            if cls.is_session_timed_out(s, threshold_mins):
                s.status = "closed"
                s.current_state = "SESSION_CLOSED"
                s.ended_at = now
                s.closed_reason = "timeout"
                cls._trigger_auto_purge_if_needed(db, s)
                closed_ids.append(s.session_id)

        if closed_ids:
            db.commit()

        return {
            "closed_count": len(closed_ids),
            "closed_session_ids": closed_ids,
            "timeout_minutes": threshold_mins,
            "message": f"Đã quét và tự động đóng {len(closed_ids)} phiên tìm kiếm hết thời gian chờ (ngưỡng: {threshold_mins} phút)."
        }

    @classmethod
    def get_session_status(
        cls,
        db: Session,
        session_id: int,
        timeout_minutes: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Truy vấn trạng thái chi tiết của phiên tìm kiếm kèm thông số thời gian hoạt động (TE9C66C):
        - Tự động kiểm tra và cập nhật timeout nếu phiên đã quá hạn.
        - Tính toán thời gian không hoạt động (idle_seconds) và tổng thời lượng (duration_seconds).
        """
        session_obj = cls.get_session(db, session_id)

        # Kiểm tra và áp dụng timeout nếu đang active nhưng đã quá hạn
        cls.check_and_apply_timeout(db, session_obj, timeout_minutes)

        last_activity = cls.get_last_activity_time(session_obj)
        now = datetime.utcnow()
        idle_seconds = max(0.0, (now - last_activity).total_seconds())

        duration_seconds = None
        if session_obj.ended_at and session_obj.started_at:
            duration_seconds = max(0.0, (session_obj.ended_at - session_obj.started_at).total_seconds())
        elif session_obj.started_at:
            duration_seconds = max(0.0, (now - session_obj.started_at).total_seconds())

        total_msgs = len(session_obj.messages) if session_obj.messages else 0

        return {
            "session_id": session_obj.session_id,
            "user_id": session_obj.user_id,
            "status": session_obj.status,
            "current_state": getattr(session_obj, "current_state", "SESSION_IDLE") or "SESSION_IDLE",
            "is_active": (session_obj.status == "active"),
            "is_timed_out": (session_obj.closed_reason == "timeout"),
            "started_at": session_obj.started_at,
            "last_activity_at": last_activity,
            "ended_at": session_obj.ended_at,
            "idle_seconds": round(idle_seconds, 2),
            "duration_seconds": round(duration_seconds, 2) if duration_seconds is not None else None,
            "closed_reason": session_obj.closed_reason,
            "total_messages": total_msgs,
        }

    @staticmethod
    def _trigger_auto_purge_if_needed(db: Session, session_obj: SearchSession):
        """Tiện ích kiểm tra và thực hiện xóa tọa độ tạm thời khi đóng phiên (NFR-07 / TSK-20)"""
        should_purge = True
        if session_obj.user_id is not None:
            profile = db.query(UserProfile).filter(
                UserProfile.user_id == session_obj.user_id
            ).first()
            if profile and not profile.auto_purge_location:
                should_purge = False

        if should_purge:
            try:
                from app.services.privacy_service import LocationPrivacyService
                LocationPrivacyService.purge_session_location(session_obj.session_id, db)
            except Exception:
                pass

    @classmethod
    def save_message(
        cls,
        db: Session,
        session_id: int,
        sender_type: str,
        content: str
    ) -> SearchMessage:
        """
        Lưu tin nhắn mới vào phiên chat theo thời gian thực:
        - Kiểm tra phiên tồn tại và còn đang ở trạng thái 'active'.
        - Tự động kiểm tra timeout: nếu đã hết thời gian chờ -> tự động đóng và ném lỗi 400.
        - Không cho gửi tin nhắn vào phiên đã bị đóng ('closed').
        """
        session_obj = cls.get_session(db, session_id)

        # Kiểm tra tự động timeout khi có truy cập mới
        if session_obj.status == "active" and cls.is_session_timed_out(session_obj):
            cls.check_and_apply_timeout(db, session_obj)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Phiên tìm kiếm này đã hết thời gian chờ (Timeout) và đã tự động đóng. Vui lòng tạo phiên mới."
            )

        if session_obj.status != "active":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Phiên chat này đã kết thúc (closed). Không thể gửi thêm tin nhắn mới."
            )

        new_message = SearchMessage(
            session_id=session_id,
            sender_type=sender_type.lower().strip(),
            content=content.strip(),
            created_at=datetime.utcnow()
        )
        db.add(new_message)
        db.commit()
        db.refresh(new_message)
        return new_message

    @staticmethod
    def get_session_messages(db: Session, session_id: int) -> List[SearchMessage]:
        """
        Lấy toàn bộ lịch sử tin nhắn trong phiên theo thứ tự thời gian tăng dần (created_at ASC):
        - Phục vụ cung cấp ngữ cảnh đầy đủ cho LLM (Multi-turn Context).
        """
        ChatSessionService.get_session(db, session_id)

        return (
            db.query(SearchMessage)
            .filter(SearchMessage.session_id == session_id)
            .order_by(SearchMessage.created_at.asc())
            .all()
        )

    @classmethod
    def list_sessions(
        cls,
        db: Session,
        user_id: Optional[int] = None,
        status: Optional[str] = None,
        limit: int = 20,
        offset: int = 0,
        auto_timeout_check: bool = True
    ) -> List[SearchSession]:
        """
        Lấy danh sách các phiên chat gần đây (sắp xếp mới nhất lên đầu):
        - Hỗ trợ lọc theo user_id (User hoặc Khách).
        - Hỗ trợ lọc theo trạng thái: 'active', 'closed' hoặc None (tất cả).
        - Tùy chọn tự động quét timeout các phiên active trước khi trả về.
        """
        if auto_timeout_check:
            try:
                cls.cleanup_expired_sessions(db)
            except Exception:
                pass

        query = db.query(SearchSession)
        if user_id is not None:
            query = query.filter(SearchSession.user_id == user_id)
        if status and status.lower() in ("active", "closed"):
            query = query.filter(SearchSession.status == status.lower())

        return query.order_by(SearchSession.session_id.desc()).offset(offset).limit(limit).all()

    @staticmethod
    def save_criteria(
        db: Session,
        session_id: int,
        location_text: Optional[str] = None,
        latitude: Optional[float] = None,
        longitude: Optional[float] = None,
        cuisine: Optional[str] = None,
        budget: Optional[int] = None,
        has_parking: Optional[bool] = False,
        other_conditions: Optional[str] = None,
        is_obfuscated: bool = False,
    ) -> SearchCriteria:
        """
        Lưu hoặc cập nhật tiêu chí tìm kiếm kèm tọa độ GPS vào bảng SearchCriteria (TSK-18).
        TSK-20: Thêm tham số is_obfuscated để đánh dấu tọa độ đã được làm mờ.
        """
        ChatSessionService.get_session(db, session_id)

        new_criteria = SearchCriteria(
            session_id=session_id,
            location_text=location_text,
            latitude=latitude,
            longitude=longitude,
            cuisine=cuisine,
            budget=budget,
            has_parking=has_parking,
            other_conditions=other_conditions,
            is_obfuscated=is_obfuscated,
            created_at=datetime.utcnow()
        )
        db.add(new_criteria)
        db.commit()
        db.refresh(new_criteria)
        return new_criteria

    @staticmethod
    def get_latest_criteria(db: Session, session_id: int) -> Optional[SearchCriteria]:
        """Lấy tiêu chí tìm kiếm mới nhất của một phiên chat"""
        ChatSessionService.get_session(db, session_id)
        return (
            db.query(SearchCriteria)
            .filter(SearchCriteria.session_id == session_id)
            .order_by(SearchCriteria.criteria_id.desc())
            .first()
        )
