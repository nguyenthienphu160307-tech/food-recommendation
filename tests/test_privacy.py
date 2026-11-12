"""
test_privacy.py — Kiểm thử Cơ chế Bảo vệ Quyền riêng tư Vị trí GPS (TSK-20)
============================================================================
Kiểm thử toàn diện 8 ca kiểm thử theo tiêu chuẩn BR-08 và NFR-07:
  - BR-08  : Làm mờ tọa độ GPS theo khu vực xấp xỉ (~1,1 km) khi chưa cho phép chia sẻ chính xác.
  - NFR-07 : Thu thập tối thiểu dữ liệu; tự động xóa log tọa độ tạm thời khi đóng phiên chat.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# SQLite in-memory engine độc lập cho kiểm thử
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
test_engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

# Nạp models và khởi tạo schema SQLite
from app.core.database import Base
import app.models
from app.models.user import User, UserProfile
from app.models.search import SearchSession, SearchCriteria
from app.services.privacy_service import LocationPrivacyService
from app.services.chat_session_service import ChatSessionService
from app.routers.search import save_session_criteria, purge_session_location
from app.schemas.search import SearchCriteriaCreateRequest
from app.routers.user import get_privacy_settings, update_privacy_settings
from app.schemas.search import PrivacySettingsUpdateRequest

Base.metadata.create_all(bind=test_engine)


def test_01_obfuscate_coordinates_approximate():
    """Kiểm thử thuật toán làm mờ tọa độ GPS theo khu vực gần đúng (BR-08)"""
    print("\n[TEST 01] Kiểm thử làm mờ tọa độ GPS (mode='approximate'):")
    lat_orig = 10.776944
    lng_orig = 106.700833

    lat_obf, lng_obf, is_obf = LocationPrivacyService.obfuscate_coordinates(
        lat_orig, lng_orig, mode="approximate"
    )

    print(f"  Gốc       : ({lat_orig}, {lng_orig})")
    print(f"  Làm mờ    : ({lat_obf}, {lng_obf}) | is_obfuscated={is_obf}")

    assert is_obf is True, "Cờ is_obfuscated phải là True khi ở mode approximate."
    # Tọa độ làm mờ phải nằm trong khoảng sai số cho phép (~1.1km + jitter <= 0.02 độ)
    assert abs(lat_obf - round(lat_orig, 2)) <= LocationPrivacyService.JITTER_RANGE + 0.001
    assert abs(lng_obf - round(lng_orig, 2)) <= LocationPrivacyService.JITTER_RANGE + 0.001
    print("  => PASSED: Tọa độ đã được làm mờ đúng chuẩn khu vực xấp xỉ!")


def test_02_obfuscate_exact_mode_no_change():
    """Kiểm thử giữ nguyên tọa độ khi người dùng cho phép chia sẻ chính xác"""
    print("\n[TEST 02] Kiểm thử giữ nguyên tọa độ (mode='exact'):")
    lat_orig = 10.8016
    lng_orig = 106.7115

    lat_out, lng_out, is_obf = LocationPrivacyService.obfuscate_coordinates(
        lat_orig, lng_orig, mode="exact"
    )

    assert is_obf is False, "is_obfuscated phải là False khi chia sẻ chính xác."
    assert lat_out == lat_orig, "Vĩ độ không được thay đổi."
    assert lng_out == lng_orig, "Kinh độ không được thay đổi."
    print("  => PASSED: Tọa độ gốc được giữ nguyên vẹn khi chia sẻ chính xác.")


def test_03_get_default_privacy_settings():
    """Kiểm thử giá trị mặc định của cài đặt quyền riêng tư (BR-08, NFR-07)"""
    print("\n[TEST 03] Kiểm thử giá trị quyền riêng tư mặc định:")
    db = TestingSessionLocal()
    try:
        # Tạo user mới kèm profile
        user = User(email="privacy_test1@example.com", hashed_password="hashed_pwd_123")
        db.add(user)
        db.commit()
        db.refresh(user)

        profile = UserProfile(user_id=user.id, full_name="Nguyễn Văn Bảo Mật")
        db.add(profile)
        db.commit()

        settings = LocationPrivacyService.get_privacy_settings(user.id, db)
        print(f"  Cài đặt mặc định: {settings}")

        assert settings["share_exact_location"] is False, "Mặc định KHÔNG chia sẻ tọa độ chính xác (BR-08)."
        assert settings["auto_purge_location"] is True, "Mặc định TỰ ĐỘNG xóa log tọa độ tạm (NFR-07)."
        print("  => PASSED: Mặc định bảo vệ tối đa quyền riêng tư người dùng.")
    finally:
        db.close()


def test_04_update_privacy_settings():
    """Kiểm thử cập nhật cài đặt quyền riêng tư qua Service và API (PUT /api/users/privacy)"""
    print("\n[TEST 04] Kiểm thử cập nhật cài đặt quyền riêng tư:")
    db = TestingSessionLocal()
    try:
        user = db.query(User).filter(User.email == "privacy_test1@example.com").first()

        # Người dùng đồng ý chia sẻ tọa độ chính xác và tắt tự động xóa
        req = PrivacySettingsUpdateRequest(
            user_id=user.id,
            share_exact_location=True,
            auto_purge_location=False
        )
        resp = update_privacy_settings(payload=req, db=db)

        assert resp.share_exact_location is True
        assert resp.auto_purge_location is False

        # Kiểm tra đọc lại
        verify_settings = LocationPrivacyService.get_privacy_settings(user.id, db)
        assert verify_settings["share_exact_location"] is True
        assert verify_settings["auto_purge_location"] is False
        print(f"  Cập nhật thành công: share_exact={resp.share_exact_location}, auto_purge={resp.auto_purge_location}")
        print("  => PASSED: Cập nhật quyền riêng tư lưu trữ chính xác trong DB.")
    finally:
        db.close()


def test_05_apply_privacy_to_coordinates():
    """Kiểm thử áp dụng quyền riêng tư tự động theo User Profile và Guest mode"""
    print("\n[TEST 05] Kiểm thử logic tự động apply_privacy_to_coordinates:")
    db = TestingSessionLocal()
    try:
        # Tạo user 2 với share_exact_location=False (mặc định)
        user2 = User(email="privacy_test2@example.com", hashed_password="hashed_pwd_456")
        db.add(user2)
        db.commit()
        db.refresh(user2)
        profile2 = UserProfile(user_id=user2.id, full_name="Trần Thị Riêng Tư", share_exact_location=False)
        db.add(profile2)
        db.commit()

        lat, lng = 10.7769, 106.7009

        # 1. Với User có share_exact_location=False -> Bắt buộc làm mờ
        res_obf = LocationPrivacyService.apply_privacy_to_coordinates(lat, lng, user2.id, db)
        assert res_obf["is_obfuscated"] is True
        assert res_obf["latitude"] is not None
        assert abs(res_obf["latitude"] - 10.78) < 0.02
        print(f"  User 2 (share_exact=False): is_obfuscated={res_obf['is_obfuscated']}, lat={res_obf['latitude']}")

        # 2. Với Guest (user_id=None) -> Mặc định làm mờ tọa độ bảo vệ quyền riêng tư (BR-08)
        res_guest = LocationPrivacyService.apply_privacy_to_coordinates(lat, lng, None, db)
        assert res_guest["is_obfuscated"] is True
        assert res_guest["latitude"] is not None
        assert abs(res_guest["latitude"] - 10.78) < 0.02
        print("  Guest (user_id=None): Tọa độ được tự động làm mờ bảo vệ riêng tư (is_obfuscated=True).")

        print("  => PASSED: Cơ chế lọc tọa độ hoạt động chính xác cho cả User và Guest.")
    finally:
        db.close()


def test_06_save_criteria_with_obfuscation():
    """Kiểm thử lưu SearchCriteria qua endpoint API áp dụng tự động làm mờ tọa độ"""
    print("\n[TEST 06] Kiểm thử lưu SearchCriteria với tọa độ làm mờ:")
    db = TestingSessionLocal()
    try:
        user = db.query(User).filter(User.email == "privacy_test2@example.com").first()

        # Tạo session chat cho user2
        session = ChatSessionService.create_session(db, user_id=user.id)

        req = SearchCriteriaCreateRequest(
            location_text="Bình Thạnh",
            latitude=10.8016,
            longitude=106.7115,
            cuisine="Lẩu bò",
            budget=200000,
            user_id=user.id
        )

        crit_resp = save_session_criteria(session_id=session.session_id, payload=req, db=db)

        print(f"  Criteria ID: {crit_resp.criteria_id}")
        print(f"  Location Text: {crit_resp.location_text}")
        print(f"  Saved Lat/Lng: ({crit_resp.latitude}, {crit_resp.longitude})")
        print(f"  is_obfuscated: {crit_resp.is_obfuscated}")

        assert crit_resp.is_obfuscated is True, "SearchCriteria phải đánh dấu is_obfuscated=True."
        assert crit_resp.latitude is not None
        assert crit_resp.longitude is not None
        print("  => PASSED: SearchCriteria lưu thành công với cờ is_obfuscated=True!")
    finally:
        db.close()


def test_07_purge_session_location():
    """Kiểm thử xóa tọa độ GPS tạm thời thủ công (POST /api/chat/sessions/{id}/purge-location)"""
    print("\n[TEST 07] Kiểm thử xóa log tọa độ tạm thời (NFR-07):")
    db = TestingSessionLocal()
    try:
        # Lấy session vừa tạo ở test_06
        user = db.query(User).filter(User.email == "privacy_test2@example.com").first()
        session = db.query(SearchSession).filter(SearchSession.user_id == user.id).first()

        # Gọi purge_session_location endpoint
        purge_resp = purge_session_location(session_id=session.session_id, db=db)
        print(f"  Số bản ghi đã xóa tọa độ: {purge_resp.purged_count}")
        print(f"  Thông báo: {purge_resp.message}")

        assert purge_resp.purged_count >= 1, "Phải xóa ít nhất 1 bản ghi có is_obfuscated=True."

        # Kiểm tra trong DB: latitude và longitude đã về None
        crit_in_db = db.query(SearchCriteria).filter(SearchCriteria.session_id == session.session_id).first()
        assert crit_in_db.latitude is None, "Latitude phải là None sau khi purge."
        assert crit_in_db.longitude is None, "Longitude phải là None sau khi purge."
        assert crit_in_db.location_text == "Bình Thạnh", "Tên địa danh vẫn được bảo tồn để tham khảo ngữ cảnh."
        print("  => PASSED: Đã xóa sạch tọa độ GPS tạm thời, bảo vệ quyền riêng tư!")
    finally:
        db.close()


def test_08_auto_purge_on_session_close():
    """Kiểm thử tự động xóa log tọa độ khi đóng phiên chat (ChatSessionService.close_session)"""
    print("\n[TEST 08] Kiểm thử auto-purge khi đóng phiên chat (NFR-07):")
    db = TestingSessionLocal()
    try:
        user = db.query(User).filter(User.email == "privacy_test2@example.com").first()
        # Đảm bảo auto_purge_location=True
        profile = user.profile
        profile.auto_purge_location = True
        db.commit()

        # Tạo phiên chat mới
        new_session = ChatSessionService.create_session(db, user_id=user.id)

        # Lưu criteria có làm mờ tọa độ
        ChatSessionService.save_criteria(
            db=db,
            session_id=new_session.session_id,
            location_text="Quận 1",
            latitude=10.7769,
            longitude=106.7009,
            cuisine="Cơm tấm",
            is_obfuscated=True
        )

        # Kiểm tra trước khi đóng phiên: tọa độ tồn tại
        crit_before = db.query(SearchCriteria).filter(SearchCriteria.session_id == new_session.session_id).first()
        assert crit_before.latitude is not None

        # Đóng phiên chat -> Phải tự động kích hoạt purge
        closed_session = ChatSessionService.close_session(db, new_session.session_id)
        assert closed_session.status == "closed"

        # Kiểm tra sau khi đóng phiên: tọa độ đã bị tự động xóa
        crit_after = db.query(SearchCriteria).filter(SearchCriteria.session_id == new_session.session_id).first()
        assert crit_after.latitude is None, "Latitude phải tự động về None sau khi đóng phiên."
        assert crit_after.longitude is None, "Longitude phải tự động về None sau khi đóng phiên."
        print("  => PASSED: Auto-purge tự động xóa sạch tọa độ ngay khi phiên chat kết thúc!")
    finally:
        db.close()


if __name__ == "__main__":
    print("=" * 70)
    print("BẮT ĐẦU CHẠY BỘ KIỂM THỬ QUYỀN RIÊNG TƯ VỊ TRÍ GPS (TSK-20)")
    print("=" * 70)

    test_01_obfuscate_coordinates_approximate()
    test_02_obfuscate_exact_mode_no_change()
    test_03_get_default_privacy_settings()
    test_04_update_privacy_settings()
    test_05_apply_privacy_to_coordinates()
    test_06_save_criteria_with_obfuscation()
    test_07_purge_session_location()
    test_08_auto_purge_on_session_close()

    print("\n" + "=" * 70)
    print("KẾT QUẢ: 8/8 BÀI KIỂM THỬ ĐÃ VƯỢT QUA XUẤT SẮC (ALL PASSED)!")
    print("=" * 70)
