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
        const token = (result.tokens && result.tokens.access_token) || result.token;
        if (token) {
            localStorage.setItem("access_token", token);
            localStorage.setItem("smart_dining_token", token);
        }
        if (result.user) {
            localStorage.setItem("current_user", JSON.stringify(result.user));
            localStorage.setItem("smart_dining_user", JSON.stringify(result.user));
            localStorage.setItem("foodai_demo_profile_state", JSON.stringify({
                full_name: result.user.full_name,
                email: result.user.email,
                role: result.user.role
            }));
        }
        return result;
    },

    logout: async () => {
        try {
            await apiRequest("/auth/logout", "POST");
        } catch (_) {
        } finally {
            localStorage.removeItem("access_token");
            localStorage.removeItem("current_user");
            localStorage.removeItem("smart_dining_token");
            localStorage.removeItem("smart_dining_user");
            localStorage.removeItem("user");
            localStorage.removeItem("foodai_demo_profile_state");
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

// ==========================================
// 3. ADAPTER TƯƠNG THÍCH CHO index.html (window.FoodAPI)
// ==========================================
window.FoodAPI = {
    auth: {
        getUser: () => {
            try {
                const raw = localStorage.getItem("current_user")
                         || localStorage.getItem("smart_dining_user")
                         || localStorage.getItem("user")
                         || localStorage.getItem("foodai_demo_profile_state");
                return raw ? JSON.parse(raw) : null;
            } catch (_) { return null; }
        },
        isLoggedIn: () => !!(localStorage.getItem("access_token") || localStorage.getItem("smart_dining_token")),
        logout: () => AuthAPI.logout()
    },
    profile: {
        get: () => apiRequest("/users/profile", "GET")
    },
    restaurants: {
        listAll: async () => {
            const res = await apiRequest("/restaurants?limit=200", "GET");
            return Array.isArray(res) ? res : (res.items || res.data || []);
        },
        categoryOf: (r) => {
            const text = `${r.cuisine_type || ""} ${r.name || ""}`.toLowerCase();
            if (text.includes("nướng") || text.includes("bbq")) return "bbq";
            if (text.includes("lẩu")) return "hotpot";
            if (text.includes("hải sản") || text.includes("ốc")) return "seafood";
            if (text.includes("chay")) return "vegan";
            if (text.includes("nhật") || text.includes("sushi")) return "japanese";
            return "other";
        },
        toVenue: (r) => {
            const rawImg = r.cover_image_url || r.cover_image || r.image_url || "";
            const isInvalidImg = !rawImg || rawImg.includes("example.com");
            const safeImg = isInvalidImg
                ? "https://images.unsplash.com/photo-1555396273-367ea4eb4db5?w=800"
                : rawImg;

            return {
                id: r.id,
                name: r.name,
                address: r.address || "",
                lat: parseFloat(r.latitude ?? r.lat ?? 10.776889),
                lng: parseFloat(r.longitude ?? r.lng ?? 106.700806),
                category: window.FoodAPI.restaurants.categoryOf(r),
                cuisineLabel: r.cuisine_type || "Ẩm thực",
                priceMin: r.min_price || 50000,
                priceMax: r.max_price || 300000,
                rating: r.avg_rating || 4.5,
                reviews: r.total_reviews || 0,
                parking: Boolean(r.amenities?.has_parking ?? r.has_parking),
                has_parking: Boolean(r.amenities?.has_parking ?? r.has_parking),
                private_room: Boolean(r.amenities?.has_private_room ?? r.has_private_room),
                has_private_room: Boolean(r.amenities?.has_private_room ?? r.has_private_room),
                outdoor: Boolean(r.amenities?.has_outdoor ?? r.has_outdoor),
                has_outdoor: Boolean(r.amenities?.has_outdoor ?? r.has_outdoor),
                pet_friendly: Boolean(r.amenities?.pet_friendly ?? r.pet_friendly),
                has_pet_friendly: Boolean(r.amenities?.pet_friendly ?? r.pet_friendly),
                vegetarian: Boolean(r.amenities?.vegetarian_support ?? r.vegetarian_support),
                vegetarian_support: Boolean(r.amenities?.vegetarian_support ?? r.vegetarian_support),
                openHours: r.open_hours || "08:00 - 22:00",
                image: safeImg,
                cover_image_url: safeImg,
                menu: r.menu || []
            };
        }
    }
};