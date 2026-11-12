from datetime import datetime
from typing import Optional, List
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.user import User
from app.models.search import SearchSession, SearchMessage, SearchCriteria


class ChatSessionService:
    """
    Tầng Service / Repository xử lý nghiệp vụ Phiên Chat AI & Tiêu chí Tìm kiếm (TSK-16, TSK-18):
    - Khởi tạo phiên cho cả User đã đăng nhập và Khách vãng lai (user_id = NULL).
    - Lưu trữ và truy vấn tin nhắn hội thoại theo thời gian thực.
    - Quản lý vòng đời phiên chat (active, closed).
    - Lưu trữ và truy xuất tiêu chí tìm kiếm kèm tọa độ Geocoding (SearchCriteria).
    """

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

    @staticmethod
    def close_session(db: Session, session_id: int) -> SearchSession:
        """
        Đóng phiên chat (chuyển status='closed'):
        - Dùng khi người dùng chọn xong quán hoặc kết thúc phiên hội thoại.
        """
        session_obj = ChatSessionService.get_session(db, session_id)
        if session_obj.status == "closed":
            return session_obj

        session_obj.status = "closed"
        db.commit()
        db.refresh(session_obj)
        return session_obj

    @staticmethod
    def save_message(
        db: Session,
        session_id: int,
        sender_type: str,
        content: str
    ) -> SearchMessage:
        """
        Lưu tin nhắn mới vào phiên chat theo thời gian thực:
        - Kiểm tra phiên tồn tại và còn đang ở trạng thái 'active'.
        - Không cho gửi tin nhắn vào phiên đã bị đóng ('closed').
        """
        session_obj = ChatSessionService.get_session(db, session_id)

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

    @staticmethod
    def list_sessions(
        db: Session,
        user_id: Optional[int] = None,
        limit: int = 20
    ) -> List[SearchSession]:
        """Lấy danh sách các phiên chat gần đây (sắp xếp mới nhất lên đầu)"""
        query = db.query(SearchSession)
        if user_id is not None:
            query = query.filter(SearchSession.user_id == user_id)
        return query.order_by(SearchSession.session_id.desc()).limit(limit).all()

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
    ) -> SearchCriteria:
        """
        Lưu hoặc cập nhật tiêu chí tìm kiếm kèm tọa độ GPS vào bảng SearchCriteria (TSK-18).
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
