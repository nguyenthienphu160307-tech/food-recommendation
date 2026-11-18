import math
from datetime import datetime
from typing import Optional, List
from sqlalchemy.orm import Session, joinedload
from fastapi import HTTPException, status

from app.models.user import User, UserProfile
from app.models.search import SearchSession, SearchMessage, SearchCriteria
from app.models.restaurant import Restaurant, RestaurantAmenity, RestaurantImage
from app.services.open_hours_service import check_restaurant_open_status, get_vietnam_now
from app.services.recommendation_service import (
    calculate_distance_km,
    calculate_match_score,
    DEFAULT_USER_LAT,
    DEFAULT_USER_LON,
)
from app.schemas.search import (
    SuggestedRestaurantHistoryItem,
    SearchHistorySessionItem,
    SearchHistoryResponse,
    SearchCriteriaResponse,
)


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
        - TSK-20: Nếu người dùng bật auto_purge_location → tự động xóa tọa độ GPS tạm thời (NFR-07).
        """
        session_obj = ChatSessionService.get_session(db, session_id)
        if session_obj.status == "closed":
            return session_obj

        session_obj.status = "closed"
        db.commit()
        db.refresh(session_obj)

        # TSK-20: Auto-purge tọa độ tạm thời nếu là khách vãng lai hoặc người dùng bật auto_purge (NFR-07)
        should_purge = True
        if session_obj.user_id is not None:
            profile = db.query(UserProfile).filter(
                UserProfile.user_id == session_obj.user_id
            ).first()
            if profile and not profile.auto_purge_location:
                should_purge = False

        if should_purge:
            from app.services.privacy_service import LocationPrivacyService
            LocationPrivacyService.purge_session_location(session_id, db)

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
        limit: int = 30
    ) -> List[SearchSession]:
        """
        Lấy danh sách các phiên chat gần đây (sắp xếp mới nhất lên đầu - TSK-45):
        - Hỗ trợ lọc theo user_id cho người dùng đã đăng nhập (BR-02).
        - Sử dụng eager loading messages để tối ưu hiệu năng không bị N+1.
        """
        from sqlalchemy.orm import joinedload
        query = db.query(SearchSession).options(joinedload(SearchSession.messages))
        if user_id is not None:
            query = query.filter(SearchSession.user_id == user_id)
        return query.order_by(SearchSession.session_id.desc()).limit(limit).all()

    @staticmethod
    def delete_session(db: Session, session_id: int) -> bool:
        """
        Xóa một phiên chat cũ khỏi CSDL (TSK-45):
        - Tự động xóa cascade toàn bộ tin nhắn (SearchMessages) và tiêu chí (SearchCriteria).
        """
        session_obj = ChatSessionService.get_session(db, session_id)
        db.delete(session_obj)
        db.commit()
        return True

    @staticmethod
    def get_session_preview_title(session_obj: SearchSession) -> str:
        """
        Tạo tiêu đề tóm tắt cuộc trò chuyện từ câu hỏi đầu tiên của người dùng:
        - Ví dụ: 'Tìm quán lẩu nướng Quận 1 có bãi ô tô...'
        """
        if session_obj.messages:
            first_user_msg = next(
                (m for m in session_obj.messages if m.sender_type == "user" and m.content),
                None
            )
            if first_user_msg:
                content = first_user_msg.content.strip().replace("\n", " ")
                if len(content) > 42:
                    return content[:40] + "..."
                return content
        return f"Cuộc trò chuyện #{session_obj.session_id}"

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

    @staticmethod
    def get_user_search_history(
        db: Session,
        user_id: int,
        page: int = 1,
        limit: int = 10,
        status_filter: Optional[str] = "all"
    ) -> SearchHistoryResponse:
        """
        API Nghiệp vụ Lấy Lịch sử Tìm kiếm & Khôi phục Kết quả Đã Gợi ý (Task TSK-46 / FR-12, UC-10):
        1. Kiểm tra xác thực người dùng tồn tại (BR-01).
        2. Truy vấn SearchSessions kèm SearchCriteria và SearchMessages (Eager Loading chống N+1).
        3. Tự động liên kết tiêu chí tìm kiếm (ẩm thực, ngân sách, tiện ích, vị trí) với bảng Restaurants
           để tái hiện danh sách các nhà hàng đã được gợi ý cho phiên đó.
        4. Tính toán % Match Score và trạng thái giờ mở cửa thực tế (BR-03, BR-05).
        5. Phân trang chuẩn RESTful (page, limit, total_pages, total_sessions).
        """
        # 1. Kiểm tra tài khoản người dùng tồn tại (BR-01)
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Không tìm thấy người dùng với ID={user_id} để truy vấn lịch sử tìm kiếm."
            )

        # 2. Xây dựng truy vấn danh sách phiên tìm kiếm
        query = (
            db.query(SearchSession)
            .filter(SearchSession.user_id == user_id)
            .options(
                joinedload(SearchSession.messages),
                joinedload(SearchSession.criteria)
            )
        )
        if status_filter and status_filter != "all":
            query = query.filter(SearchSession.status == status_filter)

        total_sessions = query.count()
        total_pages = math.ceil(total_sessions / limit) if total_sessions > 0 else 1
        offset = (page - 1) * limit
        sessions = (
            query.order_by(SearchSession.session_id.desc())
            .offset(offset)
            .limit(limit)
            .all()
        )

        now_vn = get_vietnam_now()

        # 3. Định dạng dữ liệu từng phiên kèm tiêu chí & danh sách nhà hàng gợi ý
        history_items: List[SearchHistorySessionItem] = []
        for s in sessions:
            title_prev = ChatSessionService.get_session_preview_title(s)
            
            # Lấy tiêu chí mới nhất của phiên
            latest_crit = s.criteria[0] if s.criteria else None
            criteria_response = None
            if latest_crit:
                criteria_response = SearchCriteriaResponse(
                    criteria_id=latest_crit.criteria_id,
                    session_id=latest_crit.session_id,
                    location_text=latest_crit.location_text,
                    latitude=latest_crit.latitude,
                    longitude=latest_crit.longitude,
                    cuisine=latest_crit.cuisine,
                    budget=latest_crit.budget,
                    has_parking=latest_crit.has_parking,
                    other_conditions=latest_crit.other_conditions,
                    is_obfuscated=latest_crit.is_obfuscated,
                    created_at=latest_crit.created_at,
                )

            # Tọa độ GPS tâm tìm kiếm của phiên
            center_lat = (
                latest_crit.latitude
                if latest_crit and latest_crit.latitude is not None
                else DEFAULT_USER_LAT
            )
            center_lon = (
                latest_crit.longitude
                if latest_crit and latest_crit.longitude is not None
                else DEFAULT_USER_LON
            )

            # 4. Truy vấn các nhà hàng gợi ý tương ứng với tiêu chí phiên tìm kiếm này
            rest_query = (
                db.query(Restaurant)
                .options(
                    joinedload(Restaurant.images),
                    joinedload(Restaurant.amenities)
                )
                .filter(Restaurant.status == "active")
            )

            if latest_crit:
                if latest_crit.cuisine:
                    rest_query = rest_query.filter(
                        Restaurant.cuisine_type.ilike(f"%{latest_crit.cuisine}%")
                    )
                if latest_crit.budget and latest_crit.budget > 0:
                    rest_query = rest_query.filter(
                        Restaurant.min_price <= float(latest_crit.budget)
                    )
                if latest_crit.has_parking:
                    rest_query = rest_query.join(Restaurant.amenities).filter(
                        RestaurantAmenity.has_parking == True
                    )

            matched_restaurants = rest_query.limit(5).all()

            # Nếu bộ lọc quá chặt không có quán nào, fallback lấy top 3 quán đánh giá cao nhất
            if not matched_restaurants:
                matched_restaurants = (
                    db.query(Restaurant)
                    .options(
                        joinedload(Restaurant.images),
                        joinedload(Restaurant.amenities)
                    )
                    .filter(Restaurant.status == "active")
                    .order_by(Restaurant.avg_rating.desc())
                    .limit(3)
                    .all()
                )

            # Chuyển đổi thành SuggestedRestaurantHistoryItem
            suggested_list: List[SuggestedRestaurantHistoryItem] = []
            for r in matched_restaurants:
                cover_url = None
                if r.images:
                    cover_img = next((img for img in r.images if img.is_cover), None)
                    cover_url = cover_img.image_url if cover_img else r.images[0].image_url

                # Kiểm tra giờ mở cửa BR-03
                open_info = check_restaurant_open_status(r.open_hours, check_dt=now_vn)

                # Tính khoảng cách GPS
                dist = None
                if r.latitude is not None and r.longitude is not None:
                    dist = calculate_distance_km(
                        center_lat, center_lon, float(r.latitude), float(r.longitude)
                    )

                # Chấm điểm % Match Score BR-05
                score = calculate_match_score(
                    distance_km=dist if dist is not None else 3.0,
                    avg_rating=r.avg_rating or 4.5,
                    amenities=r.amenities,
                    is_open=open_info["is_open"],
                )

                suggested_list.append(
                    SuggestedRestaurantHistoryItem(
                        id=r.id,
                        name=r.name,
                        address=r.address,
                        cuisine_type=r.cuisine_type,
                        avg_rating=r.avg_rating or 4.5,
                        min_price=r.min_price or 0.0,
                        max_price=r.max_price or 0.0,
                        cover_image_url=cover_url,
                        is_open=open_info["is_open"],
                        match_score=score,
                        distance_km=dist,
                    )
                )

            history_items.append(
                SearchHistorySessionItem(
                    session_id=s.session_id,
                    user_id=s.user_id,
                    status=s.status,
                    started_at=s.started_at,
                    title_preview=title_prev,
                    total_messages=len(s.messages) if s.messages else 0,
                    criteria=criteria_response,
                    suggested_restaurants=suggested_list,
                )
            )

        return SearchHistoryResponse(
            total_sessions=total_sessions,
            page=page,
            limit=limit,
            total_pages=total_pages,
            data=history_items,
        )
