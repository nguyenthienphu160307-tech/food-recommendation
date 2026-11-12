"""
privacy_service.py — Dịch vụ bảo vệ quyền riêng tư vị trí GPS (TSK-20)
=======================================================================
Tuân thủ:
  - BR-08  : Người dùng được phép chỉ chia sẻ khu vực xấp xỉ thay vì tọa độ chính xác.
  - NFR-07 : Thu thập tối thiểu dữ liệu; tự động xóa log tọa độ sau khi phiên kết thúc.

Chiến lược làm mờ tọa độ (Obfuscation Strategy):
  - Làm tròn latitude/longitude về 2 chữ số thập phân (~1,1 km độ chính xác).
  - Cộng thêm nhiễu Gaussian nhỏ ±0.005 độ để tránh phân tích ngược.
  - Trường `is_obfuscated = True` đánh dấu bản ghi đã được xử lý quyền riêng tư.
"""

import random
from typing import Optional, Tuple
from sqlalchemy.orm import Session

from app.models.user import UserProfile
from app.models.search import SearchCriteria


class LocationPrivacyService:
    """
    Tầng Service xử lý toàn bộ nghiệp vụ Quyền riêng tư Vị trí GPS (TSK-20).
    """

    # Bán kính nhiễu tối đa (đơn vị: độ kinh / vĩ độ, ~0.5 km)
    JITTER_RANGE = 0.005

    @staticmethod
    def obfuscate_coordinates(
        lat: float,
        lng: float,
        mode: str = "approximate"
    ) -> Tuple[float, float, bool]:
        """
        Làm mờ tọa độ GPS để bảo vệ quyền riêng tư người dùng (BR-08).

        Args:
            lat   : Vĩ độ gốc (latitude).
            lng   : Kinh độ gốc (longitude).
            mode  : "approximate" → làm tròn + thêm nhiễu;
                    "exact"       → trả nguyên tọa độ gốc.

        Returns:
            Tuple (lat_out, lng_out, is_obfuscated):
              - lat_out / lng_out : tọa độ sau xử lý.
              - is_obfuscated     : True nếu đã làm mờ, False nếu giữ nguyên.
        """
        if mode != "approximate":
            return lat, lng, False

        # Làm tròn về 2 chữ số thập phân → độ chính xác ~1,1 km
        lat_rounded = round(lat, 2)
        lng_rounded = round(lng, 2)

        # Thêm nhiễu ngẫu nhiên Gaussian nhỏ để tránh suy ngược tọa độ gốc
        jitter_lat = random.uniform(-LocationPrivacyService.JITTER_RANGE,
                                     LocationPrivacyService.JITTER_RANGE)
        jitter_lng = random.uniform(-LocationPrivacyService.JITTER_RANGE,
                                     LocationPrivacyService.JITTER_RANGE)

        lat_out = round(lat_rounded + jitter_lat, 6)
        lng_out = round(lng_rounded + jitter_lng, 6)

        return lat_out, lng_out, True

    @staticmethod
    def apply_privacy_to_coordinates(
        lat: Optional[float],
        lng: Optional[float],
        user_id: Optional[int],
        db: Session
    ) -> dict:
        """
        Áp dụng cài đặt quyền riêng tư của người dùng lên cặp tọa độ trước khi lưu DB (BR-08).

        - Nếu tọa độ là None: giữ nguyên None.
        - Nếu `user_id` là None (khách vãng lai): mặc định áp dụng làm mờ tọa độ (~1,1 km).
        - Nếu `share_exact_location = False`: gọi obfuscate_coordinates() làm mờ tọa độ.
        - Nếu `share_exact_location = True` : giữ nguyên tọa độ gốc theo sự đồng ý của người dùng.

        Returns:
            dict với các key: latitude, longitude, is_obfuscated
        """
        if lat is None or lng is None:
            return {"latitude": None, "longitude": None, "is_obfuscated": False}

        # Khách vãng lai: mặc định bảo vệ quyền riêng tư bằng cách làm mờ tọa độ (BR-08)
        if user_id is None:
            lat_out, lng_out, obfuscated = LocationPrivacyService.obfuscate_coordinates(
                lat, lng, mode="approximate"
            )
            return {"latitude": lat_out, "longitude": lng_out, "is_obfuscated": obfuscated}

        profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()

        # Mặc định nếu chưa có profile hoặc chưa bật: share_exact_location = False → làm mờ
        share_exact = profile.share_exact_location if profile else False

        if share_exact:
            return {"latitude": lat, "longitude": lng, "is_obfuscated": False}
        else:
            lat_out, lng_out, obfuscated = LocationPrivacyService.obfuscate_coordinates(
                lat, lng, mode="approximate"
            )
            return {"latitude": lat_out, "longitude": lng_out, "is_obfuscated": obfuscated}

    @staticmethod
    def purge_session_location(session_id: int, db: Session) -> int:
        """
        Xóa tọa độ GPS tạm thời của một phiên chat đã đóng (NFR-07).

        Quy tắc: Chỉ xóa các bản ghi `SearchCriteria` có `is_obfuscated = True`.
        Tọa độ chính xác (is_obfuscated = False) được giữ lại theo sự đồng ý của người dùng.

        Args:
            session_id : ID phiên chat cần xóa tọa độ.
            db         : SQLAlchemy Session.

        Returns:
            Số bản ghi đã được xóa tọa độ.
        """
        criteria_list = (
            db.query(SearchCriteria)
            .filter(
                SearchCriteria.session_id == session_id,
                SearchCriteria.is_obfuscated == True  # noqa: E712
            )
            .all()
        )

        purged_count = 0
        for crit in criteria_list:
            crit.latitude = None
            crit.longitude = None
            purged_count += 1

        if purged_count > 0:
            db.commit()

        return purged_count

    @staticmethod
    def get_privacy_settings(user_id: int, db: Session) -> dict:
        """
        Lấy cài đặt quyền riêng tư vị trí GPS hiện tại của người dùng.

        Returns:
            dict: { share_exact_location: bool, auto_purge_location: bool }
        """
        profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
        if not profile:
            # Trả về giá trị mặc định an toàn nếu chưa có hồ sơ
            return {
                "share_exact_location": False,
                "auto_purge_location": True,
                "profile_exists": False
            }
        return {
            "share_exact_location": profile.share_exact_location,
            "auto_purge_location": profile.auto_purge_location,
            "profile_exists": True
        }

    @staticmethod
    def update_privacy_settings(
        user_id: int,
        share_exact_location: Optional[bool],
        auto_purge_location: Optional[bool],
        db: Session
    ) -> UserProfile:
        """
        Cập nhật cài đặt quyền riêng tư vị trí của người dùng.

        Args:
            user_id              : ID người dùng.
            share_exact_location : True = cho phép lưu tọa độ chính xác; False = chỉ lưu khu vực xấp xỉ.
            auto_purge_location  : True = tự động xóa tọa độ khi đóng phiên.
            db                   : SQLAlchemy Session.

        Returns:
            UserProfile đã được cập nhật.

        Raises:
            ValueError: Nếu không tìm thấy hồ sơ người dùng.
        """
        profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
        if not profile:
            raise ValueError(f"Không tìm thấy hồ sơ người dùng với user_id={user_id}.")

        if share_exact_location is not None:
            profile.share_exact_location = share_exact_location
        if auto_purge_location is not None:
            profile.auto_purge_location = auto_purge_location

        db.commit()
        db.refresh(profile)
        return profile
