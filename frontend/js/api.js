// URL mặc định của FastAPI chạy trên local
const API_BASE_URL = 'http://127.0.0.1:8000/api';

// ==========================================
// 1. GỬI OTP (GỌI API POST /api/auth/send-otp)
// ==========================================
async function sendOTP() {
    const emailInput = document.getElementById('reg-email').value;
    
    if (!emailInput) {
        alert("Vui lòng nhập Email!");
        return;
    }

    try {
        const response = await fetch(`${API_BASE_URL}/auth/send-otp`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email: emailInput })
        });

        const data = await response.json();

        if (response.ok) {
            alert(data.message); // Hiển thị "Mã OTP đã được gửi..."
            // Chuyển UI sang bước nhập mã OTP & Mật khẩu
            document.getElementById('step-otp').style.display = 'block';
            document.getElementById('step-email').style.display = 'none';
        } else {
            // Hiển thị lỗi từ backend (VD: Email đã tồn tại)
            alert(data.detail); 
        }
    } catch (error) {
        console.error("Lỗi khi kết nối API Send OTP:", error);
    }
}

// ==========================================
// 2. ĐĂNG KÝ (GỌI API POST /api/auth/register)
// ==========================================
async function registerAccount() {
    const email = document.getElementById('reg-email').value;
    const fullName = document.getElementById('reg-fullname').value;
    const password = document.getElementById('reg-password').value;
    const otpCode = document.getElementById('reg-otp').value;

    try {
        const response = await fetch(`${API_BASE_URL}/auth/register`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                email: email,
                full_name: fullName,
                password: password,
                otp_code: otpCode
            })
        });

        const data = await response.json();

        if (response.ok) {
            alert("Đăng ký thành công! Chào mừng " + data.data.full_name);
            // Có thể tự động chuyển sang form đăng nhập hoặc lưu token
        } else {
            // Xử lý báo lỗi (Sai OTP, OTP hết hạn...)
            let errorMsg = data.detail;
            if (Array.isArray(errorMsg)) {
                errorMsg = errorMsg.map(err => err.msg).join('\n'); // Lỗi Pydantic
            }
            alert("Lỗi đăng ký:\n" + errorMsg);
        }
    } catch (error) {
        console.error("Lỗi khi kết nối API Register:", error);
    }
}