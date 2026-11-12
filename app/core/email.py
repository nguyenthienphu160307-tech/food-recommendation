import os
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()

# Cấu hình SMTP lấy từ file .env
MAIL_SERVER = os.getenv("MAIL_SERVER", "smtp.gmail.com")
MAIL_PORT = int(os.getenv("MAIL_PORT", "587"))
MAIL_USERNAME = os.getenv("MAIL_USERNAME", "").strip()
MAIL_PASSWORD = os.getenv("MAIL_PASSWORD", "").strip()
MAIL_FROM = os.getenv("MAIL_FROM", MAIL_USERNAME)
MAIL_FROM_NAME = os.getenv("MAIL_FROM_NAME", "Smart Dining")


def send_otp_email(to_email: str, otp_code: str) -> bool:
    """
    Gửi mã OTP trực tiếp vào hòm thư cá nhân của người dùng qua máy chủ SMTP Gmail.
    Không in OTP ra console, đảm bảo tính bảo mật và trải nghiệm thực tế.
    """
    if not MAIL_USERNAME or not MAIL_PASSWORD:
        return False

    try:
        # 1. Tạo đối tượng MIME Email
        msg = MIMEMultipart("alternative")
        msg["Subject"] = f"[{otp_code}] Mã xác thực tài khoản - Smart Dining"
        msg["From"] = f"{MAIL_FROM_NAME} <{MAIL_FROM}>"
        msg["To"] = to_email

        # 2. Giao diện Email HTML thiết kế chuyên nghiệp
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <style>
                body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f7fafc; margin: 0; padding: 20px; }}
                .container {{ max-width: 520px; margin: auto; background: #ffffff; border-radius: 12px; padding: 32px; border: 1px solid #e2e8f0; box-shadow: 0 4px 15px rgba(0,0,0,0.05); }}
                .logo {{ text-align: center; margin-bottom: 24px; }}
                .logo h1 {{ color: #e53e3e; margin: 0; font-size: 26px; font-weight: 700; }}
                .content {{ color: #2d3748; line-height: 1.6; font-size: 15px; }}
                .otp-box {{ background-color: #fff5f5; border: 2px dashed #feb2b2; border-radius: 8px; text-align: center; padding: 18px; margin: 24px 0; }}
                .otp-code {{ font-size: 34px; font-weight: 800; letter-spacing: 8px; color: #c53030; }}
                .expire-note {{ font-size: 13px; color: #718096; margin-top: 8px; }}
                .warning {{ background-color: #fefcbf; border-left: 4px solid #ecc94b; padding: 12px 16px; border-radius: 4px; font-size: 13px; color: #744210; margin-top: 16px; }}
                .footer {{ margin-top: 32px; font-size: 12px; color: #a0aec0; text-align: center; border-top: 1px solid #edf2f7; padding-top: 16px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="logo">
                    <h1>🍽️ Smart Dining</h1>
                </div>
                <div class="content">
                    <p>Xin chào bạn,</p>
                    <p>Bạn vừa yêu cầu mã xác thực đăng ký tài khoản trên <b>Hệ thống Smart Dining</b>.</p>
                    
                    <div class="otp-box">
                        <div class="otp-code">{otp_code}</div>
                        <div class="expire-note">Hiệu lực trong vòng <b>5 phút</b></div>
                    </div>

                    <div class="warning">
                        ⚠️ <b>Lưu ý an toàn:</b> Tuyệt đối không chia sẻ mã này cho bất kỳ ai. Quản trị viên Smart Dining sẽ không bao giờ hỏi mã OTP của bạn.
                    </div>
                </div>
                <div class="footer">
                    <p>Nếu bạn không thực hiện yêu cầu này, vui lòng bỏ qua email.</p>
                    <p>&copy; 2026 Smart Dining System. All rights reserved.</p>
                </div>
            </div>
        </body>
        </html>
        """

        part = MIMEText(html_content, "html", "utf-8")
        msg.attach(part)

        # 3. Kết nối an toàn TLS tới máy chủ SMTP Gmail và gửi thư
        context = ssl.create_default_context()
        with smtplib.SMTP(MAIL_SERVER, MAIL_PORT) as server:
            server.starttls(context=context)
            server.login(MAIL_USERNAME, MAIL_PASSWORD)
            server.sendmail(MAIL_FROM, to_email, msg.as_string())

        return True

    except Exception:
        return False
