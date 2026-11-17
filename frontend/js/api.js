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

// Cấu hình URL mặc định của Backend (FastAPI chạy ở port 8000)
// filepath: frontend/api.js
const API_BASE_URL = "http://127.0.0.1:8000/api";

async function apiRequest(endpoint, method = "GET", bodyData = null) {
    const headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    };

    const token = localStorage.getItem("access_token");
    if (token) {
        headers["Authorization"] = `Bearer ${token}`;
    }

    const config = {
        method: method,
        headers: headers
    };

    if (bodyData && ["POST", "PUT", "PATCH"].includes(method)) {
        config.body = JSON.stringify(bodyData);
    }

    try {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, config);
        const data = await response.json();

        if (!response.ok) {
            let errorMessage = "Có lỗi xảy ra từ máy chủ!";
            if (Array.isArray(data.detail)) {
                errorMessage = data.detail.map(err => err.msg).join("\n");
            } else if (data.detail) {
                errorMessage = data.detail;
            }
            throw new Error(errorMessage);
        }

        return data;
    } catch (error) {
        console.error(`[API Error] ${method} ${endpoint}:`, error.message);
        throw error;
    }
}

const AuthAPI = {
    sendOTP: (email) => apiRequest("/auth/send-otp", "POST", { email: email }),
    
    register: (fullName, email, password, otpCode) => 
        apiRequest("/auth/register", "POST", {
            full_name: fullName,
            email: email,
            password: password,
            otp_code: otpCode
        }),

    login: async (account, password) => {
        const result = await apiRequest("/auth/login", "POST", { account, password });
        if (result.tokens) {
            localStorage.setItem("access_token", result.tokens.access_token);
            localStorage.setItem("current_user", JSON.stringify(result.user));
        }
        return result;
    },

    logout: async () => {
        try {
            await apiRequest("/auth/logout", "POST");
        } finally {
            localStorage.removeItem("access_token");
            localStorage.removeItem("current_user");
        }
    }
};

const GeoAPI = {
    findNearby: (lat, lng, radius = 15) => 
        apiRequest(`/geo/nearby-restaurants?lat=${lat}&lng=${lng}&radius_km=${radius}`, "GET"),

    listRestaurants: (search = "", category = "all") => {
        const params = new URLSearchParams();
        if (search) params.append("search", search);
        if (category && category !== "all") params.append("category", category);
        return apiRequest(`/geo/restaurants?${params.toString()}`, "GET");
    },

    createRestaurant: (payload) =>
        apiRequest("/geo/restaurants", "POST", payload),

    updateRestaurant: (id, payload) =>
        apiRequest(`/geo/restaurants/${id}`, "PUT", payload),

    deleteRestaurant: (id) =>
        apiRequest(`/geo/restaurants/${id}`, "DELETE")
};