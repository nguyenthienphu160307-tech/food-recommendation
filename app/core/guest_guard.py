"""
Task TE9C675: Thực thi Quy tắc giới hạn cho Khách chưa đăng nhập (Guest Mode - BR-02).
- Cho phép tìm kiếm cơ bản không cần đăng nhập.
- Giới hạn tối đa 3 lượt chat AI miễn phí cho mỗi Guest (theo X-Guest-Id hoặc IP).
"""

from typing import Dict, Optional
from fastapi import HTTPException, Request, status

GUEST_MAX_FREE_CHAT_TURNS = 3
_guest_chat_usage: Dict[str, int] = {}


def enforce_guest_chat_limit(request: Request) -> Optional[int]:
    """
    Kiểm tra nếu request KHÔNG có Bearer token (Guest) thì áp giới hạn 3 lượt chat miễn phí.
    Trả về số lượt còn lại nếu là Guest, hoặc None nếu là User đã đăng nhập.
    """
    auth_header = request.headers.get("Authorization", "")
    if auth_header.startswith("Bearer ") and len(auth_header.split(" ", 1)[1].strip()) > 10:
        return None  # Đã đăng nhập -> không giới hạn

    guest_key = (
        request.headers.get("X-Guest-Id")
        or (request.client.host if request.client else "anonymous")
    )
    used = _guest_chat_usage.get(guest_key, 0)
    if used >= GUEST_MAX_FREE_CHAT_TURNS:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "code": "GUEST_CHAT_LIMIT_REACHED",
                "limit": GUEST_MAX_FREE_CHAT_TURNS,
                "message": (
                    f"Bạn đã sử dụng hết {GUEST_MAX_FREE_CHAT_TURNS} lượt hỏi AI miễn phí dành cho Khách. "
                    "Vui lòng đăng nhập hoặc đăng ký tài khoản để tiếp tục sử dụng không giới hạn!"
                ),
                "login_url": "/frontend/login.html",
            },
        )

    _guest_chat_usage[guest_key] = used + 1
    return GUEST_MAX_FREE_CHAT_TURNS - _guest_chat_usage[guest_key]


def reset_guest_chat_usage() -> None:
    """Dùng cho unit test để reset bộ đếm."""
    _guest_chat_usage.clear()