import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.database import SessionLocal
from app.models.user import User, UserProfile, Role, UserRole
from app.core.security import hash_password, create_access_token

client = TestClient(app)


def test_user_profile_returns_actual_name_and_dynamic_avatar():
    """Kiểm tra API /api/users/profile trả về đúng full_name và avatar thực tế của tài khoản."""
    db = SessionLocal()
    try:
        # 1. Tạo hoặc lấy tài khoản test
        test_email = "test_profile_user@example.com"
        user = db.query(User).filter(User.email == test_email).first()
        if not user:
            user = User(
                email=test_email,
                phone_number="0911223399",
                hashed_password=hash_password("TestPassword123@"),
                status="active"
            )
            db.add(user)
            db.flush()

            profile = UserProfile(
                user_id=user.id,
                full_name="test"
            )
            db.add(profile)
            db.commit()
            db.refresh(user)

        token = create_access_token(user.id, claims={"email": user.email, "role": "user"})

        # 2. Gọi GET /api/users/profile với JWT token của user 'test'
        response = client.get(
            "/api/users/profile",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["full_name"] == "test"
        assert data["email"] == test_email
        assert "Nguyễn Văn An" not in data["full_name"]
        assert "photo-1534528741775-53994a69daeb" not in data["avatar_url"]

        # 3. Gọi GET /api/users/profile theo email query param
        res_by_email = client.get(f"/api/users/profile?email={test_email}")
        assert res_by_email.status_code == 200
        data_by_email = res_by_email.json()
        assert data_by_email["full_name"] == "test"
        assert data_by_email["email"] == test_email

        # 4. Cập nhật hồ sơ bằng PUT /api/users/profile
        update_payload = {
            "full_name": "Test Updated Name",
            "gender": "Nam",
            "default_address": "Khu Công Nghệ Cao, TP. Thủ Đức",
            "default_lat": 10.85,
            "default_lng": 106.78
        }
        res_put = client.put(
            "/api/users/profile",
            json=update_payload,
            headers={"Authorization": f"Bearer {token}"}
        )
        assert res_put.status_code == 200
        put_data = res_put.json()
        assert put_data["full_name"] == "Test Updated Name"
        assert put_data["default_address"] == "Khu Công Nghệ Cao, TP. Thủ Đức"

    finally:
        # Dọn dẹp
        db.query(UserProfile).filter(UserProfile.user_id == user.id).delete()
        db.query(User).filter(User.id == user.id).delete()
        db.commit()
        db.close()
