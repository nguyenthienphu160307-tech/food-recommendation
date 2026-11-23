import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# Thiết lập database SQLite in-memory độc lập cho kiểm thử
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
test_engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

# Nạp models và tạo schema SQLite
from app.core.database import Base
import app.models
from app.models.search import SearchSession, SearchCriteria
from app.services.geocoding_service import GeocodingService
from app.services.chat_session_service import ChatSessionService
from app.routers.search import (
    geocode_location,
    extract_criteria_from_chat,
    save_session_criteria,
    get_session_criteria
)
from app.schemas.search import (
    GeocodeRequest,
    ExtractCriteriaRequest,
    SearchCriteriaCreateRequest
)

Base.metadata.create_all(bind=test_engine)


def test_01_geocoding_direct_districts():
    """Kiểm thử Geocoding trực tiếp tên các quận trung tâm TP.HCM (TSK-18)"""
    print("\n[TEST 01] Kiểm thử Geocoding trực tiếp tên các quận:")

    cases = [
        ("Quận 1", 10.7769, 106.7009),
        ("Bình Thạnh", 10.8016, 106.7115),
        ("Gò Vấp", 10.8388, 106.6653),
        ("Thủ Đức", 10.8494, 106.7537),
        ("Tân Bình", 10.8015, 106.6526),
        ("Quận 7", 10.7340, 106.7218),
    ]

    for name, exp_lat, exp_lng in cases:
        res = GeocodingService.geocode(name, enable_online_fallback=False)
        assert res["is_found"] is True, f"Không tìm thấy tọa độ cho: {name}"
        assert abs(res["latitude"] - exp_lat) < 0.01, f"Sai lệch vĩ độ {name}: {res['latitude']} vs {exp_lat}"
        assert abs(res["longitude"] - exp_lng) < 0.01, f"Sai lệch kinh độ {name}: {res['longitude']} vs {exp_lng}"
        print(f"  ✓ {name} -> ({res['latitude']:.4f}, {res['longitude']:.4f}) [{res['source']}]")


def test_02_geocoding_landmarks():
    """Kiểm thử Geocoding các địa danh ẩm thực / landmark nổi tiếng"""
    print("\n[TEST 02] Kiểm thử Geocoding Landmarks:")

    landmarks = [
        ("Hồ Con Rùa", 10.7828, 106.6958),
        ("Phố đi bộ Nguyễn Huệ", 10.7738, 106.7048),
        ("Chợ Bến Thành", 10.7725, 106.6980),
        ("Landmark 81", 10.7950, 106.7219)
    ]

    for name, exp_lat, exp_lng in landmarks:
        res = GeocodingService.geocode(name, enable_online_fallback=False)
        assert res["is_found"] is True
        assert abs(res["latitude"] - exp_lat) < 0.01
        assert abs(res["longitude"] - exp_lng) < 0.01
        print(f"  ✓ {name} -> ({res['latitude']:.4f}, {res['longitude']:.4f})")


def test_03_extract_location_from_natural_chat():
    """Kiểm thử bóc tách tên địa danh từ câu chat tự nhiên tiếng Việt"""
    print("\n[TEST 03] Kiểm thử bóc tách địa danh từ câu hội thoại:")

    chat_cases = [
        ("Tìm quán lẩu nấm ở Bình Thạnh", "Bình Thạnh"),
        ("Muốn ăn đồ nướng quanh Quận 1 có chỗ đỗ xe", "Quận 1"),
        ("Cho mình vài quán cà phê view đẹp ở Hồ Con Rùa", "Hồ Con Rùa"),
        ("Có quán ăn nào ngon tại Gò Vấp không", "Gò Vấp")
    ]

    for chat, expected_loc in chat_cases:
        extracted = GeocodingService.extract_location_from_text(chat)
        assert extracted is not None, f"Không trích xuất được địa danh từ: '{chat}'"
        assert expected_loc.lower() in extracted.lower(), f"Trích xuất sai: '{extracted}' vs '{expected_loc}'"
        print(f"  ✓ '{chat}' -> Trích xuất: '{extracted}'")


def test_04_extract_full_criteria():
    """Kiểm thử trích xuất đa tiêu chí: Địa danh, Tọa độ, Ẩm thực, Ngân sách, Tiện ích"""
    print("\n[TEST 04] Kiểm thử bóc tách toàn diện tiêu chí (Full Criteria):")

    msg = "Tìm quán lẩu ở Bình Thạnh dưới 300k có chỗ đậu xe"
    res = GeocodingService.extract_full_criteria(msg)

    assert res["location_text"] is not None
    assert "Bình Thạnh" in res["location_text"]
    assert res["latitude"] is not None
    assert abs(res["latitude"] - 10.8016) < 0.01
    assert res["cuisine"] == "lẩu"
    assert res["budget"] == 300000
    assert res["has_parking"] is True
    print(f"  ✓ Bóc tách thành công: Location={res['location_text']}, Lat={res['latitude']:.4f}, Cuisine={res['cuisine']}, Budget={res['budget']}đ, Parking={res['has_parking']}")


def test_05_router_geocode_endpoint():
    """Kiểm thử Router POST /api/chat/geocode (TSK-18)"""
    print("\n[TEST 05] Kiểm thử Router Endpoint geocode_location:")

    # 1. Tên quận trực tiếp
    req1 = GeocodeRequest(location_name="Quận 1", enable_online_fallback=False)
    res1 = geocode_location(req1)
    assert res1.is_found is True
    assert abs(res1.latitude - 10.7769) < 0.01
    print(f"  ✓ geocode_location('Quận 1') -> Lat={res1.latitude:.4f}, Lng={res1.longitude:.4f}")

    # 2. Câu chat tự nhiên
    req2 = GeocodeRequest(location_name="Quán nướng ngon ở Gò Vấp", enable_online_fallback=False)
    res2 = geocode_location(req2)
    assert res2.is_found is True
    assert abs(res2.latitude - 10.8388) < 0.01
    print(f"  ✓ geocode_location('Quán nướng ngon ở Gò Vấp') -> Lat={res2.latitude:.4f}, Lng={res2.longitude:.4f}")


def test_06_router_extract_endpoint():
    """Kiểm thử Router POST /api/chat/extract"""
    print("\n[TEST 06] Kiểm thử Router Endpoint extract_criteria_from_chat:")

    req = ExtractCriteriaRequest(message="Ăn đồ nướng ở Quận 3 tầm 250k có phòng riêng")
    res = extract_criteria_from_chat(req)
    crit = res["criteria"]
    assert "Quận 3" in crit["location_text"]
    assert crit["cuisine"] == "nướng"
    assert crit["budget"] == 250000
    assert crit["other_conditions"]["has_private_room"] is True
    print(f"  ✓ extract_criteria_from_chat -> Cuisine={crit['cuisine']}, Budget={crit['budget']}đ, Private Room={crit['other_conditions']['has_private_room']}")


def test_07_save_and_get_criteria_in_db():
    """Kiểm thử lưu và truy xuất SearchCriteria gắn liền với SearchSessions trong CSDL"""
    print("\n[TEST 07] Kiểm thử lưu SearchCriteria gắn liền với phiên chat:")

    db = TestingSessionLocal()
    try:
        # 1. Tạo phiên chat mới (Guest Mode: user_id = None)
        sess = ChatSessionService.create_session(db, user_id=None)
        assert sess.session_id is not None
        sess_id = sess.session_id

        # 2. Lưu tiêu chí qua Router Endpoint kèm Geocoding tự động bù tọa độ
        payload = SearchCriteriaCreateRequest(
            location_text="Bình Thạnh",
            cuisine="lẩu nấm",
            budget=350000,
            has_parking=True,
            other_conditions="{\"has_private_room\": true}"
        )
        saved = save_session_criteria(session_id=sess_id, payload=payload, db=db)
        assert saved.session_id == sess_id
        assert saved.location_text == "Bình Thạnh"
        assert saved.latitude is not None
        assert abs(saved.latitude - 10.8016) < 0.01
        assert abs(saved.longitude - 106.7115) < 0.01
        print(f"  ✓ Lưu SearchCriteria vào CSDL thành công: criteria_id={saved.criteria_id}, lat={saved.latitude:.4f}, lng={saved.longitude:.4f}")

        # 3. Lấy lại tiêu chí đã lưu
        retrieved = get_session_criteria(session_id=sess_id, db=db)
        assert retrieved is not None
        assert retrieved.criteria_id == saved.criteria_id
        assert retrieved.cuisine == "lẩu nấm"
        assert retrieved.has_parking is True
        print(f"  ✓ get_session_criteria({sess_id}) -> Khớp 100% dữ liệu đã lưu trong CSDL!")
    finally:
        db.close()


def test_08_fallback_for_unknown_location():
    """Kiểm thử trường hợp địa danh hoàn toàn không xác định (an toàn không sập server)"""
    print("\n[TEST 08] Kiểm thử cơ chế Fallback an toàn:")

    res = GeocodingService.geocode("Mặt Trăng", enable_online_fallback=False)
    assert res["is_found"] is False
    assert res["latitude"] == GeocodingService.DEFAULT_CENTER[0]
    assert res["longitude"] == GeocodingService.DEFAULT_CENTER[1]
    print(f"  ✓ Địa danh không xác định trả về tọa độ trung tâm TP.HCM an toàn: ({res['latitude']}, {res['longitude']})")


if __name__ == "__main__":
    print("=" * 70)
    print("BẮT ĐẦU CHẠY BỘ KIỂM THỬ TASK TSK-18 (SERVICE GEOCODING & SEARCH CRITERIA)")
    print("=" * 70)

    test_01_geocoding_direct_districts()
    test_02_geocoding_landmarks()
    test_03_extract_location_from_natural_chat()
    test_04_extract_full_criteria()
    test_05_router_geocode_endpoint()
    test_06_router_extract_endpoint()
    test_07_save_and_get_criteria_in_db()
    test_08_fallback_for_unknown_location()

    print("\n" + "=" * 70)
    print(">>> TẤT CẢ 8/8 CA KIỂM THỬ TASK TSK-18 ĐỀU ĐẠT CHUẨN (ALL TESTS PASSED)! <<<")
    print("=" * 70)
