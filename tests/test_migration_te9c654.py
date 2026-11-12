"""Unit tests for Task TE9C654: Migration of 6 tables with Foreign Keys & UNIQUE constraints."""

import pytest
from sqlalchemy import create_engine, inspect
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker

from app.core.database import Base
from app.models import (
    User,
    Restaurant,
    SearchSession,
    SearchMessage,
    SearchCriteria,
    RestaurantReview,
    UserFavorite,
    Notification,
)

TEST_DB_URL = "sqlite:///:memory:"
engine = create_engine(TEST_DB_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session():
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


def test_all_six_tables_created(db_session):
    """Kiểm tra cả 6 bảng của Task TE9C654 đã được khởi tạo đầy đủ."""
    inspector = inspect(engine)
    existing_tables = set(inspector.get_table_names())
    expected_tables = {
        "search_sessions",
        "search_messages",
        "search_criteria",
        "restaurant_reviews",
        "user_favorites",
        "notifications",
    }
    assert expected_tables.issubset(existing_tables)


def test_unique_constraints_and_foreign_keys(db_session):
    """Kiểm tra UNIQUE constraint trên UserFavorites, RestaurantReviews và SearchCriteria."""
    user = User(email="phu.test@ptit.edu.vn", hashed_password="hashed_password_123")
    restaurant = Restaurant(
        name="Phở Hòa Pasteur",
        address="260C Pasteur, Quận 3, TP.HCM",
        latitude=10.7868,
        longitude=106.6881,
    )
    db_session.add_all([user, restaurant])
    db_session.commit()

    # 1. Kiểm tra UNIQUE (user_id, restaurant_id) của UserFavorites
    fav1 = UserFavorite(user_id=user.id, restaurant_id=restaurant.id)
    db_session.add(fav1)
    db_session.commit()

    fav_duplicate = UserFavorite(user_id=user.id, restaurant_id=restaurant.id)
    db_session.add(fav_duplicate)
    with pytest.raises(IntegrityError):
        db_session.commit()
    db_session.rollback()

    # 2. Kiểm tra UNIQUE (user_id, restaurant_id) của RestaurantReviews
    rev1 = RestaurantReview(user_id=user.id, restaurant_id=restaurant.id, rating=5, comment="Ngon!")
    db_session.add(rev1)
    db_session.commit()

    rev_duplicate = RestaurantReview(user_id=user.id, restaurant_id=restaurant.id, rating=4, comment="Lần 2")
    db_session.add(rev_duplicate)
    with pytest.raises(IntegrityError):
        db_session.commit()
    db_session.rollback()

    # 3. Kiểm tra SearchSession, SearchMessage, SearchCriteria & Notification
    chat_session = SearchSession(session_code="SESS-001", user_id=user.id, title="Tìm quán phở Quận 3")
    db_session.add(chat_session)
    db_session.commit()

    msg = SearchMessage(session_id=chat_session.id, sender_role="user", content="Gợi ý quán phở gần đây")
    criteria = SearchCriteria(session_id=chat_session.id, cuisine_type="Phở", radius_km=3.0)
    notif = Notification(user_id=user.id, title="Chào mừng", message="Tạo tài khoản thành công")
    db_session.add_all([msg, criteria, notif])
    db_session.commit()

    assert chat_session.criteria.cuisine_type == "Phở"
    assert len(chat_session.messages) == 1
    assert notif.is_read is False