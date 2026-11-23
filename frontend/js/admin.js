/**
 * ==============================================================================
 * JAVASCRIPT: LOGIC ADMIN PORTAL & ROUTE GUARD (TASK TE9C656)
 * - Kiểm tra phân quyền truy cập Frontend (Route Guard: 401 & 403)
 * - Quản lý Người dùng & Nghiệp vụ Khóa tài khoản BR-07
 * - Quản lý 50 Nhà hàng TP.HCM (Ẩn/Hiện, Lọc theo Quận)
 * - Xử lý Báo cáo vi phạm & Thống kê KPI Dashboard
 * - Hỗ trợ thanh chuyển đổi vai trò Demo Role Switcher trực quan
 * ==============================================================================
 */

// Key lưu trữ vai trò demo để kiểm thử Route Guard
const DEMO_ROLE_KEY = 'foodai_demo_role';
const ADMIN_USERS_KEY = 'foodai_admin_users_data';
const ADMIN_VENUES_KEY = 'foodai_admin_venues_data';
const ADMIN_REPORTS_KEY = 'foodai_admin_reports_data';

// Dữ liệu người dùng mẫu ban đầu
const INITIAL_USERS = [
    {
        id: 1,
        email: "admin.master@foodai.vn",
        phone_number: "0909999888",
        full_name: "Lê Quản Trị Viên",
        role: "admin",
        status: "active",
        created_at: "01/10/2026 08:30",
        avatar: "https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=150&q=80"
    },
    {
        id: 2,
        email: "user.demo@foodai.vn",
        phone_number: "0912345678",
        full_name: "Nguyễn Văn Người Dùng",
        role: "user",
        status: "active",
        created_at: "15/10/2026 14:15",
        avatar: "https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?auto=format&fit=crop&w=150&q=80"
    },
    {
        id: 3,
        email: "user.spam99@foodai.vn",
        phone_number: "0987654321",
        full_name: "Trần Văn Spam",
        role: "user",
        status: "locked",
        created_at: "20/10/2026 10:00",
        avatar: "https://images.unsplash.com/photo-1570295999919-56ceb5ecca61?auto=format&fit=crop&w=150&q=80"
    },
    {
        id: 4,
        email: "mai.anh@gmail.com",
        phone_number: "0933221100",
        full_name: "Phạm Mai Anh",
        role: "user",
        status: "active",
        created_at: "25/10/2026 19:45",
        avatar: "https://images.unsplash.com/photo-1494790108377-be9c29b29330?auto=format&fit=crop&w=150&q=80"
    }
];

// Dữ liệu báo cáo vi phạm mẫu ban đầu
const INITIAL_REPORTS = [
    {
        id: 1,
        type: "Sai thông tin giá",
        target_name: "Quán Nướng Khói Sài Gòn",
        reporter_name: "Nguyễn Minh Tuấn",
        content: "Giá thực tế tại quán cao hơn so với thông tin hiển thị trên app khoảng 30.000đ/món.",
        created_at: "09/11/2026 14:20",
        status: "pending"
    },
    {
        id: 2,
        type: "Tài khoản spam đánh giá",
        target_name: "user.spam99@foodai.vn",
        reporter_name: "Trần Thị Mai",
        content: "Người dùng này liên tục copy 1 nội dung bình luận rác và rate 1 sao vô cớ cho các quán chay.",
        created_at: "09/11/2026 18:05",
        status: "pending"
    },
    {
        id: 3,
        type: "Quán đã đóng cửa",
        target_name: "Lẩu Nướng Gió Biển",
        reporter_name: "Lê Văn Hùng",
        content: "Địa điểm này đã trả mặt bằng và dừng hoạt động từ tuần trước.",
        created_at: "08/11/2026 10:15",
        status: "pending"
    },
    {
        id: 4,
        type: "Bình luận xúc phạm",
        target_name: "Đánh giá tại Sushi Hokkaido Sachi",
        reporter_name: "Chủ nhà hàng",
        content: "Bình luận chứa từ ngữ khiếm nhã, thóa mạ nhân viên phục vụ.",
        created_at: "07/11/2026 09:30",
        status: "resolved"
    }
];

// Trạng thái ứng dụng
let currentRole = localStorage.getItem(DEMO_ROLE_KEY) || 'admin';
let usersData = [];
let venuesData = [];
let reportsData = [];

/**
 * ==============================================================================
 * 1. FRONTEND ROUTE GUARD (BẢO VỆ ROUTE ADMIN)
 * ==============================================================================
 */
function checkAdminRouteGuard() {
    const guard401 = document.getElementById('guard-401');
    const guard403 = document.getElementById('guard-403');
    const userEmailSpan = document.getElementById('guard-user-email');

    // Đồng bộ kiểm tra tài khoản đã đăng nhập trong LocalStorage
    let user = null;
    try {
        const raw = localStorage.getItem('current_user') 
                 || localStorage.getItem('smart_dining_user')
                 || localStorage.getItem('foodai_demo_profile_state');
        if (raw) user = JSON.parse(raw);
    } catch (_) {}

    const token = localStorage.getItem('access_token') || localStorage.getItem('smart_dining_token');

    if (user && token) {
        if (user.role === 'admin' || user.role === 'ADMIN') {
            currentRole = 'admin';
        } else {
            currentRole = 'user';
            if (userEmailSpan) userEmailSpan.innerText = user.email || user.full_name || 'user@foodai.vn';
        }
    } else if (!token && !user) {
        const demoRole = localStorage.getItem(DEMO_ROLE_KEY);
        if (demoRole) currentRole = demoRole;
    }

    if (currentRole === 'guest') {
        // Chặn 401: Khách chưa đăng nhập
        guard401.classList.add('active');
        guard403.classList.remove('active');
        console.warn('[Route Guard] Chặn truy cập 401: Khách chưa đăng nhập.');
        return false;
    } else if (currentRole === 'user') {
        // Chặn 403: User thường cố truy cập
        guard401.classList.remove('active');
        guard403.classList.add('active');
        if (userEmailSpan && user) userEmailSpan.innerText = user.email || 'user.demo@foodai.vn';
        console.warn('[Route Guard] Chặn truy cập 403 Forbidden: Tài khoản không có vai trò Admin.');
        return false;
    } else {
        // Quyền Admin hợp lệ
        guard401.classList.remove('active');
        guard403.classList.remove('active');
        console.log('[Route Guard] Xác thực thành công: Quyền Quản trị viên (Admin).');
        return true;
    }
}

/**
 * Xử lý đăng nhập tài khoản Quản trị viên
 */
async function handleAdminLogin(event) {
    if (event) event.preventDefault();
    const emailInput = document.getElementById('admin-login-email');
    const passwordInput = document.getElementById('admin-login-password');
    if (!emailInput || !passwordInput) return;

    const email = emailInput.value.trim();
    const password = passwordInput.value;

    try {
        // Gửi request tới Backend API /api/auth/login nếu có server đang chạy
        const res = await fetch('http://127.0.0.1:8000/api/auth/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ account: email, password: password })
        });
        if (res.ok) {
            const data = await res.json();
            const role = data.user?.role || (data.user?.roles && data.user.roles[0]) || '';
            if (role !== 'admin') {
                alert('Tài khoản này không có quyền Quản trị viên (Admin).');
                return;
            }
            const tokenStr = data.token || data.tokens?.access_token || '';
            localStorage.setItem('access_token', tokenStr);
            localStorage.setItem('smart_dining_token', tokenStr);
            localStorage.setItem('current_user', JSON.stringify(data.user));
            localStorage.setItem('smart_dining_user', JSON.stringify(data.user));
            localStorage.setItem(DEMO_ROLE_KEY, 'admin');
            currentRole = 'admin';
            document.getElementById('guard-401').classList.remove('active');
            document.getElementById('guard-403').classList.remove('active');
            if (typeof renderAdminPortal === 'function') renderAdminPortal();
            if (typeof showAdminToast === 'function') showAdminToast('Đăng nhập Quản trị viên thành công!', 'success');
            return;
        }
    } catch (_) {
        // Fallback xử lý offline client-side
    }

    if ((email === 'admin@foodai.vn' || email === 'admin.master@foodai.vn') && password === 'admin123') {
        currentRole = 'admin';
        localStorage.setItem(DEMO_ROLE_KEY, 'admin');
        document.getElementById('guard-401').classList.remove('active');
        document.getElementById('guard-403').classList.remove('active');
        loadAllAdminData();
        showToast('Đăng nhập Quản trị viên thành công!', 'success');
    } else {
        alert('Email hoặc mật khẩu không chính xác! Gợi ý: admin@foodai.vn / admin123');
    }
}

/**
 * Tiện ích chuyển đổi vai trò Demo Role Switcher phục vụ kiểm thử
 * @param {'admin' | 'user' | 'guest'} role 
 */
function simulateRoleSwitch(role) {
    currentRole = role;
    localStorage.setItem(DEMO_ROLE_KEY, role);
    const hasAccess = checkAdminRouteGuard();
    if (hasAccess) {
        showToast('Đã kích hoạt quyền Quản trị viên (Admin)', 'success');
        loadAllAdminData();
    } else if (role === 'user') {
        showToast('Đang giả lập User thường -> Kích hoạt màn hình chặn 403 Forbidden', 'error');
    } else {
        showToast('Đang giả lập Khách -> Kích hoạt màn hình chặn 401 Unauthorized', 'warning');
    }
}

/**
 * Đăng xuất Quản trị viên
 */
function adminLogout() {
    if (confirm('Bạn có chắc chắn muốn đăng xuất khỏi Bảng điều khiển Quản trị?')) {
        localStorage.removeItem(DEMO_ROLE_KEY);
        window.location.href = 'index.html';
    }
}

/**
 * ==============================================================================
 * 2. TẢI VÀ QUẢN LÝ DỮ LIỆU
 * ==============================================================================
 */
function initDataStorage() {
    // 0. Nạp số liệu Thống kê & Báo cáo Admin Dashboard từ API (TE9C67E - FR-15)
    fetchDashboardStatsFromAPI();

    // 1. Users
    const storedUsers = localStorage.getItem(ADMIN_USERS_KEY);
    usersData = storedUsers ? JSON.parse(storedUsers) : [...INITIAL_USERS];

    // Nạp đồng bộ từ API GET /api/admin/users nếu có auth_token
    const token = localStorage.getItem('auth_token');
    if (token) {
        fetch('/api/admin/users', {
            headers: { 'Authorization': `Bearer ${token}` }
        })
        .then(res => res.ok ? res.json() : null)
        .then(apiData => {
            if (apiData && Array.isArray(apiData.data) && apiData.data.length > 0) {
                usersData = apiData.data.map(u => ({
                    id: u.id,
                    email: u.email,
                    phone_number: u.phone_number,
                    full_name: u.full_name,
                    role: u.role || (u.roles && u.roles[0]) || 'user',
                    status: u.status,
                    created_at: u.created_at,
                    avatar: u.avatar_url || 'https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?auto=format&fit=crop&w=150&q=80'
                }));
                localStorage.setItem(ADMIN_USERS_KEY, JSON.stringify(usersData));
                renderUsersTable();
                renderStatsOverview();
            }
        })
        .catch(err => console.warn('Không thể nạp users từ API:', err));
    }

    // 2. Venues (từ venues-data.js đã seed 50 quán và đồng bộ từ Backend API)
    let parsedVenues = [];
    try {
        const storedVenues = localStorage.getItem(ADMIN_VENUES_KEY);
        if (storedVenues) {
            parsedVenues = JSON.parse(storedVenues);
        }
    } catch (_) {}

    if (Array.isArray(parsedVenues) && parsedVenues.length > 0) {
        venuesData = parsedVenues;
    } else if (typeof SEED_VENUES !== 'undefined' && Array.isArray(SEED_VENUES) && SEED_VENUES.length > 0) {
        venuesData = SEED_VENUES.map(v => ({ ...v, status: 'active' }));
        localStorage.setItem(ADMIN_VENUES_KEY, JSON.stringify(venuesData));
    } else {
        venuesData = [];
    }

    // Tự động đồng bộ từ Backend API /api/restaurants (CSDL SQLite) nếu server đang chạy
    fetch('/api/restaurants?limit=100')
        .then(res => res.ok ? res.json() : null)
        .then(apiRes => {
            const apiItems = Array.isArray(apiRes) ? apiRes : (apiRes && (apiRes.data || apiRes.items));
            if (Array.isArray(apiItems) && apiItems.length > 0) {
                const backendVenues = apiItems.map(r => ({
                    id: r.id,
                    name: r.name,
                    address: r.address || '',
                    lat: r.latitude ?? r.lat ?? 10.7769,
                    lng: r.longitude ?? r.lng ?? 106.7009,
                    priceMin: r.min_price || 50000,
                    priceMax: r.max_price || 300000,
                    rating: r.avg_rating || 4.5,
                    reviews: r.total_reviews || 0,
                    cuisineLabel: r.cuisine_type || 'Món Việt',
                    openHours: r.open_hours || '08:00 - 22:00',
                    status: r.status || 'active',
                    image: (r.cover_image_url && !r.cover_image_url.includes('example.com'))
                        ? r.cover_image_url
                        : 'https://images.unsplash.com/photo-1555396273-367ea4eb4db5?w=800',
                    parking: Boolean(r.amenities?.has_parking ?? r.has_parking),
                    private_room: Boolean(r.amenities?.has_private_room ?? r.has_private_room),
                    outdoor: Boolean(r.amenities?.has_outdoor ?? r.has_outdoor),
                    vegetarian: Boolean(r.amenities?.vegetarian_support ?? r.vegetarian_support)
                }));

                const existingIds = new Set(backendVenues.map(v => v.id));
                const seedFallbacks = (typeof SEED_VENUES !== 'undefined' && Array.isArray(SEED_VENUES))
                    ? SEED_VENUES.filter(v => !existingIds.has(v.id)).map(v => ({ ...v, status: 'active' }))
                    : [];

                venuesData = [...backendVenues, ...seedFallbacks];
                localStorage.setItem(ADMIN_VENUES_KEY, JSON.stringify(venuesData));
                renderVenuesTable();
                renderStatsOverview();
            }
        })
        .catch(err => console.warn('[Admin] Không thể nạp nhà hàng từ API:', err));

    // 3. Reports
    const storedReports = localStorage.getItem(ADMIN_REPORTS_KEY);
    reportsData = storedReports ? JSON.parse(storedReports) : [...INITIAL_REPORTS];
}

function loadAllAdminData() {
    renderStatsOverview();
    renderUsersTable();
    renderVenuesTable();
    renderReportsTable();
}

let adminDashboardStats = null;

/**
 * Tải số liệu thống kê Dashboard từ Backend API (TE9C67E - FR-15)
 */
async function fetchDashboardStatsFromAPI() {
    const token = localStorage.getItem('auth_token');
    if (!token) return;

    try {
        const res = await fetch('/api/admin/dashboard/stats?days=7&top_limit=5', {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        if (res.ok) {
            const result = await res.json();
            if (result && result.data) {
                adminDashboardStats = result.data;
                renderDashboardStats(result.data);
            }
        }
    } catch (err) {
        console.warn('[Admin] Lỗi khi nạp thống kê dashboard:', err);
    }
}

/**
 * Render dữ liệu Thống kê & Báo cáo nâng cao (Task TE9C67E)
 */
function renderDashboardStats(data) {
    if (!data) return;

    // 1. Cập nhật thẻ KPI
    if (data.users) {
        const uEl = document.getElementById('stat-total-users');
        if (uEl) uEl.innerText = data.users.total;
        const bEl = document.getElementById('badge-users-count');
        if (bEl) bEl.innerText = data.users.total;
    }

    if (data.restaurants) {
        const rEl = document.getElementById('stat-total-venues');
        if (rEl) rEl.innerText = data.restaurants.total;
        const rbEl = document.getElementById('badge-venues-count');
        if (rbEl) rbEl.innerText = data.restaurants.total;
        const ratingEl = document.getElementById('stat-avg-rating');
        if (ratingEl) ratingEl.innerText = data.restaurants.avg_rating || '4.5';
    }

    // 2. Render Biểu đồ cột Xu hướng Tìm kiếm AI theo ngày
    const trendsContainer = document.getElementById('ai-search-trends-container');
    if (trendsContainer && Array.isArray(data.ai_search_trends)) {
        trendsContainer.innerHTML = '';
        const trends = data.ai_search_trends;
        const maxVal = Math.max(...trends.map(t => t.search_count), 1);
        const totalInPeriod = data.total_ai_searches_in_period || trends.reduce((acc, t) => acc + t.search_count, 0);

        const summaryEl = document.getElementById('ai-search-trend-summary');
        if (summaryEl) summaryEl.innerText = `Tổng: ${totalInPeriod} lượt tìm kiếm`;

        trends.forEach(item => {
            const heightPct = Math.max(12, Math.round((item.search_count / maxVal) * 100));
            const parts = item.date.split('-');
            const shortDate = parts.length === 3 ? `${parts[2]}/${parts[1]}` : item.date;

            const col = document.createElement('div');
            col.style.cssText = 'flex:1;display:flex;flex-direction:column;align-items:center;height:100%;justify-content:flex-end;gap:6px;';
            col.innerHTML = `
                <span style="font-size:0.75rem;font-weight:700;color:var(--brand-rose);">${item.search_count}</span>
                <div style="width:100%;max-width:32px;height:${heightPct}%;background:linear-gradient(180deg,#f43f5e,#be123c);border-radius:6px 6px 0 0;transition:height 0.4s ease;" title="${item.date}: ${item.search_count} lượt"></div>
                <span style="font-size:0.7rem;color:var(--text-muted);">${shortDate}</span>
            `;
            trendsContainer.appendChild(col);
        });
    }

    // 3. Render Top loại ẩm thực được tìm nhiều nhất
    const topCuisinesContainer = document.getElementById('top-cuisines-list');
    if (topCuisinesContainer && Array.isArray(data.top_cuisines)) {
        topCuisinesContainer.innerHTML = '';
        if (data.top_cuisines.length === 0) {
            topCuisinesContainer.innerHTML = `<div style="text-align:center;color:var(--text-muted);padding:20px;font-size:0.85rem;">Chưa có dữ liệu tìm kiếm ẩm thực.</div>`;
        } else {
            data.top_cuisines.forEach(c => {
                const item = document.createElement('div');
                item.className = 'dist-bar-item';
                item.innerHTML = `
                    <div class="dist-bar-header">
                        <span>🍲 ${c.cuisine}</span>
                        <span>${c.search_count} lượt (${c.percentage}%)</span>
                    </div>
                    <div class="dist-bar-track">
                        <div class="dist-bar-fill" style="width: ${c.percentage}%; background: linear-gradient(90deg, #f59e0b, #ef4444);"></div>
                    </div>
                `;
                topCuisinesContainer.appendChild(item);
            });
        }
    }

    // 4. Render Top nhà hàng được yêu thích nhất
    const topFavContainer = document.getElementById('top-favorites-list');
    if (topFavContainer && Array.isArray(data.top_favorited_restaurants)) {
        topFavContainer.innerHTML = '';
        if (data.top_favorited_restaurants.length === 0) {
            topFavContainer.innerHTML = `<div style="text-align:center;color:var(--text-muted);padding:20px;font-size:0.85rem;">Chưa có lượt bookmark nhà hàng nào.</div>`;
        } else {
            data.top_favorited_restaurants.forEach((r, idx) => {
                const item = document.createElement('div');
                item.style.cssText = 'display:flex;align-items:center;justify-content:space-between;padding:10px 12px;background:var(--bg-subtle);border-radius:10px;gap:12px;';
                const img = r.cover_image_url || 'https://images.unsplash.com/photo-1555396273-367ea4eb4db5?w=200';
                item.innerHTML = `
                    <div style="display:flex;align-items:center;gap:10px;min-width:0;">
                        <span style="font-weight:800;color:var(--brand-rose);font-size:0.9rem;width:20px;">#${idx + 1}</span>
                        <img src="${img}" style="width:42px;height:42px;border-radius:8px;object-fit:cover;flex-shrink:0;">
                        <div style="min-width:0;">
                            <div style="font-weight:700;font-size:0.88rem;color:var(--text-primary);white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">${r.name}</div>
                            <div style="font-size:0.75rem;color:var(--text-muted);">${r.cuisine_type || 'Món Việt'} • ⭐ ${r.avg_rating || 0}</div>
                        </div>
                    </div>
                    <div style="flex-shrink:0;text-align:right;">
                        <span style="display:inline-block;padding:4px 8px;border-radius:999px;background:rgba(225,29,72,0.1);color:#e11d48;font-size:0.78rem;font-weight:700;">❤️ ${r.favorite_count}</span>
                    </div>
                `;
                topFavContainer.appendChild(item);
            });
        }
    }
}

/**
 * Render Tab 1: Tổng quan Dashboard & Biểu đồ phân bố
 */
function renderStatsOverview() {
    if (adminDashboardStats) {
        renderDashboardStats(adminDashboardStats);
    } else {
        fetchDashboardStatsFromAPI();
    }

    // Cập nhật số liệu KPI Cards
    const totalUsers = usersData.length;
    const activeUsers = usersData.filter(u => u.status === 'active').length;
    const lockedUsers = usersData.filter(u => u.status === 'locked').length;

    const totalVenues = venuesData.length;
    const pendingReports = reportsData.filter(r => r.status === 'pending').length;

    const uEl = document.getElementById('stat-total-users');
    if (uEl) uEl.innerText = totalUsers;
    const buEl = document.getElementById('badge-users-count');
    if (buEl) buEl.innerText = totalUsers;

    const vEl = document.getElementById('stat-total-venues');
    if (vEl) vEl.innerText = totalVenues;
    const bvEl = document.getElementById('badge-venues-count');
    if (bvEl) bvEl.innerText = totalVenues;

    const prEl = document.getElementById('stat-pending-reports');
    if (prEl) prEl.innerText = pendingReports;
    const bprEl = document.getElementById('badge-reports-count');
    if (bprEl) bprEl.innerText = pendingReports;

    // Phân bố nhà hàng theo Quận
    const districtCounts = {};
    venuesData.forEach(v => {
        const d = v.district || (v.address.includes('Quận 1') ? 'Quận 1' : v.address.includes('Quận 3') ? 'Quận 3' : v.address.includes('Bình Thạnh') ? 'Bình Thạnh' : 'Thủ Đức');
        districtCounts[d] = (districtCounts[d] || 0) + 1;
    });

    const distListContainer = document.getElementById('district-distribution-list');
    if (distListContainer) {
        distListContainer.innerHTML = '';
        Object.entries(districtCounts).forEach(([district, count]) => {
            const pct = Math.round((count / (totalVenues || 1)) * 100);
            const item = document.createElement('div');
            item.className = 'dist-bar-item';
            item.innerHTML = `
                <div class="dist-bar-header">
                    <span>📍 ${district}</span>
                    <span>${count} quán (${pct}%)</span>
                </div>
                <div class="dist-bar-track">
                    <div class="dist-bar-fill" style="width: ${pct}%;"></div>
                </div>
            `;
            distListContainer.appendChild(item);
        });
    }

    // Tỷ lệ thể loại ẩm thực
    const cuisineCounts = {};
    venuesData.forEach(v => {
        const c = v.cuisineLabel || 'Khác';
        cuisineCounts[c] = (cuisineCounts[c] || 0) + 1;
    });

    const cuisineListContainer = document.getElementById('cuisine-distribution-list');
    if (cuisineListContainer) {
        cuisineListContainer.innerHTML = '';
        Object.entries(cuisineCounts).slice(0, 5).forEach(([cuisine, count]) => {
            const pct = Math.round((count / (totalVenues || 1)) * 100);
            const item = document.createElement('div');
            item.className = 'dist-bar-item';
            item.innerHTML = `
                <div class="dist-bar-header">
                    <span>🍽️ ${cuisine}</span>
                    <span>${count} quán (${pct}%)</span>
                </div>
                <div class="dist-bar-track">
                    <div class="dist-bar-fill" style="width: ${pct}%; background: linear-gradient(90deg, #3b82f6, #60a5fa);"></div>
                </div>
            `;
            cuisineListContainer.appendChild(item);
        });
    }
}

/**
 * ==============================================================================
 * 3. QUẢN LÝ NGƯỜI DÙNG & NGHIỆP VỤ BR-07
 * ==============================================================================
 */
function renderUsersTable(customList = null) {
    const list = customList || usersData;
    const tbody = document.getElementById('users-table-body');
    tbody.innerHTML = '';

    if (list.length === 0) {
        tbody.innerHTML = `<tr><td colspan="6" style="text-align:center;padding:30px;color:var(--text-muted);">Không tìm thấy người dùng phù hợp.</td></tr>`;
        return;
    }

    list.forEach(u => {
        const tr = document.createElement('tr');
        const isLocked = u.status === 'locked';
        const isAdmin = u.role === 'admin';

        tr.innerHTML = `
            <td>
                <div class="cell-user-info">
                    <img src="${u.avatar || 'https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?auto=format&fit=crop&w=150&q=80'}" class="cell-avatar" alt="${u.full_name}">
                    <div>
                        <div class="cell-name">${u.full_name}</div>
                        <div class="cell-sub">${u.email}</div>
                    </div>
                </div>
            </td>
            <td>${u.phone_number || 'Chưa cập nhật'}</td>
            <td>
                <span class="role-badge ${isAdmin ? 'role-admin' : 'role-user'}">
                    ${isAdmin ? 'Quản trị viên' : 'User'}
                </span>
            </td>
            <td>
                <span class="status-badge ${isLocked ? 'status-locked' : 'status-active'}">
                    ${isLocked ? '⛔ Bị khóa (BR-07)' : '✓ Đang hoạt động'}
                </span>
            </td>
            <td>${u.created_at || 'Mới'}</td>
            <td style="text-align:right;">
                ${isAdmin ? '<span style="font-size:0.75rem;color:var(--text-muted);font-style:italic;">Tài khoản Quản trị</span>' : `
                    <button type="button" class="btn-action ${isLocked ? 'btn-unlock' : 'btn-lock'}" onclick="toggleUserLock(${u.id})">
                        ${isLocked ? '🔓 Mở khóa' : '🔒 Khóa tài khoản'}
                    </button>
                `}
            </td>
        `;
        tbody.appendChild(tr);
    });
}

/**
 * Nghiệp vụ BR-07: Khóa hoặc Mở khóa tài khoản người dùng vi phạm (TE9C678)
 * @param {number} userId 
 */
async function toggleUserLock(userId) {
    const user = usersData.find(u => u.id === userId);
    if (!user) return;

    if (user.role === 'admin') {
        showToast('Không thể khóa tài khoản Quản trị viên.', 'error');
        return;
    }

    const newStatus = user.status === 'active' ? 'locked' : 'active';
    const actionName = newStatus === 'locked' ? 'KHÓA' : 'MỞ KHÓA';

    if (newStatus === 'locked') {
        if (!confirm(`Bạn có chắc muốn KHÓA tài khoản '${user.full_name}' (${user.email}) theo quy định BR-07?\nTất cả phiên đăng nhập và tìm kiếm đang hoạt động của người dùng sẽ bị thu hồi ngay lập tức.`)) {
            return;
        }
    }

    // Gọi API Backend PATCH /api/admin/users/:id/status (TE9C678)
    const token = localStorage.getItem('auth_token');
    if (token) {
        try {
            const res = await fetch(`/api/admin/users/${userId}/status`, {
                method: 'PATCH',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({
                    status: newStatus,
                    reason: `Thao tác ${actionName.toLowerCase()} tài khoản bởi Quản trị viên`
                })
            });
            if (!res.ok) {
                const errData = await res.json();
                showToast(errData.detail || 'Không thể cập nhật trạng thái người dùng trên server.', 'error');
                return;
            }
        } catch (err) {
            console.warn('Lỗi gọi API PATCH user status:', err);
        }
    }

    user.status = newStatus;
    if (newStatus === 'locked') {
        showToast(`Đã khóa tài khoản '${user.full_name}' thành công theo quy tắc BR-07!`, 'error');
    } else {
        showToast(`Đã mở khóa tài khoản '${user.full_name}' hoạt động trở lại!`, 'success');
    }

    localStorage.setItem(ADMIN_USERS_KEY, JSON.stringify(usersData));
    handleUserSearch();
    renderStatsOverview();
}

/**
 * Tìm kiếm và lọc người dùng theo thời gian thực
 */
function handleUserSearch() {
    const kw = document.getElementById('user-search-input').value.trim().toLowerCase();
    const statusFilter = document.getElementById('user-status-filter').value;
    const roleFilter = document.getElementById('user-role-filter').value;

    let filtered = [...usersData];

    if (kw) {
        filtered = filtered.filter(u =>
            u.full_name.toLowerCase().includes(kw) ||
            u.email.toLowerCase().includes(kw) ||
            (u.phone_number && u.phone_number.includes(kw))
        );
    }

    if (statusFilter) {
        filtered = filtered.filter(u => u.status === statusFilter);
    }

    if (roleFilter) {
        filtered = filtered.filter(u => u.role === roleFilter);
    }

    renderUsersTable(filtered);
}

/**
 * ==============================================================================
 * 4. QUẢN LÝ NHÀ HÀNG (RESTAURANTS MANAGEMENT)
 * ==============================================================================
 */
function renderVenuesTable(customList = null) {
    const list = customList || venuesData;
    const tbody = document.getElementById('venues-table-body');
    tbody.innerHTML = '';

    if (list.length === 0) {
        tbody.innerHTML = `<tr><td colspan="6" style="text-align:center;padding:30px;color:var(--text-muted);">Không tìm thấy nhà hàng nào.</td></tr>`;
        return;
    }

    list.slice(0, 50).forEach(v => {
        const tr = document.createElement('tr');
        const isInactive = v.status === 'inactive' || v.status === 'hidden' || v.status === 'closed';

        tr.innerHTML = `
            <td>
                <div class="cell-venue-info">
                    <img src="${v.image || 'https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?auto=format&fit=crop&w=150&q=80'}" class="cell-venue-thumb" alt="${v.name}">
                    <div>
                        <div class="cell-name">${v.name}</div>
                        <div class="cell-sub">📍 ${v.address}</div>
                        <div class="cell-sub" style="color:#6366f1;font-size:0.7rem;">GPS: ${Number(v.lat || v.latitude || 0).toFixed(4)}, ${Number(v.lng || v.longitude || 0).toFixed(4)}</div>
                    </div>
                </div>
            </td>
            <td>
                <strong>${v.cuisineLabel || v.cuisine_type || 'Ẩm thực'}</strong><br>
                <span class="cell-sub">${(v.priceMin || v.min_price || 50000).toLocaleString()}đ - ${(v.priceMax || v.max_price || 200000).toLocaleString()}đ</span><br>
                <span class="cell-sub" style="color:#059669;">⏰ ${v.openHours || v.open_hours || '08:00 - 22:00'}</span>
            </td>
            <td>
                <span style="color:#f59e0b;font-weight:700;">★ ${v.rating || v.avg_rating || 4.5}</span>
                <span class="cell-sub">(${v.reviews || v.total_reviews || 100} đánh giá)</span>
            </td>
            <td>
                <div style="display:flex;gap:4px;flex-wrap:wrap;font-size:0.72rem;">
                    ${v.parking || (v.amenities && v.amenities.has_parking) ? '<span style="background:#e0f2fe;color:#0284c7;padding:1px 5px;border-radius:4px;">Đỗ xe</span>' : ''}
                    ${v.private_room || (v.amenities && v.amenities.has_private_room) ? '<span style="background:#f3e8ff;color:#7e22ce;padding:1px 5px;border-radius:4px;">Phòng VIP</span>' : ''}
                    ${v.vegetarian || (v.amenities && v.amenities.vegetarian_support) ? '<span style="background:#dcfce7;color:#15803d;padding:1px 5px;border-radius:4px;">Món chay</span>' : ''}
                </div>
            </td>
            <td>
                <span class="status-badge ${isInactive ? 'status-locked' : 'status-active'}">
                    ${isInactive ? '⛔ Tạm ngưng' : '✓ Hoạt động'}
                </span>
            </td>
            <td style="text-align:right;">
                <div style="display:flex;gap:6px;justify-content:flex-end;">
                    <button type="button" class="btn-action" onclick="openRestaurantModal(${v.id})" title="Chỉnh sửa thông tin">
                        ✏️ Sửa
                    </button>
                    <button type="button" class="btn-action" onclick="toggleVenueVisibility(${v.id})" title="Đổi trạng thái active/inactive">
                        ${isInactive ? 'Kích hoạt' : 'Tạm ngưng'}
                    </button>
                    <button type="button" class="btn-action btn-lock" onclick="deleteRestaurant(${v.id})" title="Xóa vĩnh viễn">
                        🗑️ Xóa
                    </button>
                </div>
            </td>
        `;
        tbody.appendChild(tr);
    });
}

/**
 * Đổi trạng thái active / inactive của nhà hàng (FR-13)
 */
async function toggleVenueVisibility(venueId) {
    const v = venuesData.find(item => item.id === venueId);
    if (!v) return;

    const newStatus = (v.status === 'inactive' || v.status === 'hidden') ? 'active' : 'inactive';
    v.status = newStatus;

    // Gửi API backend nếu có token
    try {
        const token = localStorage.getItem('auth_token');
        if (token) {
            await fetch(`/api/admin/restaurants/${venueId}/status`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({ status: newStatus })
            });
        }
    } catch (_) {}

    localStorage.setItem(ADMIN_VENUES_KEY, JSON.stringify(venuesData));
    handleVenueSearch();
    renderStatsOverview();
    showToast(`Đã đổi trạng thái '${v.name}' sang: ${newStatus === 'active' ? 'HOẠT ĐỘNG' : 'TẠM NGƯNG'}`, 'success');
}

/**
 * Mở Modal Form thêm mới hoặc chỉnh sửa Nhà hàng (FR-13)
 */
function openRestaurantModal(venueId = null) {
    const modal = document.getElementById('restaurant-modal');
    const title = document.getElementById('modal-restaurant-title');
    const form = document.getElementById('restaurant-form');
    if (!modal || !form) return;

    form.reset();

    if (venueId) {
        // Chế độ chỉnh sửa
        const v = venuesData.find(item => item.id === venueId);
        if (!v) return;

        title.innerText = `Chỉnh sửa Nhà hàng #${v.id} (FR-13)`;
        document.getElementById('form-venue-id').value = v.id;
        document.getElementById('form-venue-name').value = v.name || '';
        document.getElementById('form-venue-address').value = v.address || '';
        document.getElementById('form-venue-lat').value = v.lat || v.latitude || 10.7768;
        document.getElementById('form-venue-lng').value = v.lng || v.longitude || 106.7008;
        document.getElementById('form-venue-min-price').value = v.priceMin || v.min_price || 50000;
        document.getElementById('form-venue-max-price').value = v.priceMax || v.max_price || 200000;
        document.getElementById('form-venue-cuisine').value = v.cuisineLabel || v.cuisine_type || 'Món Việt';
        document.getElementById('form-venue-hours').value = v.openHours || v.open_hours || '08:00 - 22:00';
        document.getElementById('form-venue-status').value = v.status || 'active';
        document.getElementById('form-venue-image').value = v.image || '';

        document.getElementById('form-amenity-parking').checked = !!(v.parking || (v.amenities && v.amenities.has_parking));
        document.getElementById('form-amenity-room').checked = !!(v.private_room || (v.amenities && v.amenities.has_private_room));
        document.getElementById('form-amenity-outdoor').checked = !!(v.outdoor || (v.amenities && v.amenities.has_outdoor));
        document.getElementById('form-amenity-vegan').checked = !!(v.vegetarian || (v.amenities && v.amenities.vegetarian_support));
    } else {
        // Chế độ thêm mới
        title.innerText = 'Thêm Nhà Hàng Mới (FR-13)';
        document.getElementById('form-venue-id').value = '';
        document.getElementById('form-venue-lat').value = '10.776889';
        document.getElementById('form-venue-lng').value = '106.700806';
        document.getElementById('form-venue-min-price').value = '50000';
        document.getElementById('form-venue-max-price').value = '250000';
        document.getElementById('form-venue-hours').value = '08:00 - 22:00';
        document.getElementById('form-venue-status').value = 'active';
    }

    modal.style.display = 'flex';
}

function closeRestaurantModal() {
    const modal = document.getElementById('restaurant-modal');
    if (modal) modal.style.display = 'none';
}

/**
 * Xử lý lưu form Thêm mới / Cập nhật Nhà hàng (POST & PUT)
 */
async function handleSaveRestaurant(event) {
    if (event) event.preventDefault();

    const venueId = document.getElementById('form-venue-id').value;
    const name = document.getElementById('form-venue-name').value.trim();
    const address = document.getElementById('form-venue-address').value.trim();
    const lat = parseFloat(document.getElementById('form-venue-lat').value);
    const lng = parseFloat(document.getElementById('form-venue-lng').value);
    const minPrice = parseFloat(document.getElementById('form-venue-min-price').value) || 0;
    const maxPrice = parseFloat(document.getElementById('form-venue-max-price').value) || 0;
    const cuisine = document.getElementById('form-venue-cuisine').value.trim() || 'Món Việt';
    const hours = document.getElementById('form-venue-hours').value.trim() || '08:00 - 22:00';
    const statusVal = document.getElementById('form-venue-status').value;
    const imageUrl = document.getElementById('form-venue-image').value.trim();

    const amenities = {
        has_parking: document.getElementById('form-amenity-parking').checked,
        has_private_room: document.getElementById('form-amenity-room').checked,
        has_outdoor: document.getElementById('form-amenity-outdoor').checked,
        vegetarian_support: document.getElementById('form-amenity-vegan').checked
    };

    if (maxPrice < minPrice) {
        alert('Khoảng giá không hợp lệ: Giá cao nhất phải lớn hơn hoặc bằng giá thấp nhất!');
        return;
    }

    const payload = {
        name,
        address,
        latitude: lat,
        longitude: lng,
        min_price: minPrice,
        max_price: maxPrice,
        cuisine_type: cuisine,
        open_hours: hours,
        status: statusVal,
        image_url: imageUrl || 'https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?auto=format&fit=crop&w=600&q=80',
        amenities
    };

    const token = localStorage.getItem('auth_token');

    if (venueId) {
        // Cập nhật nhà hàng hiện có (PUT)
        const idNum = parseInt(venueId, 10);
        const idx = venuesData.findIndex(v => v.id === idNum);
        if (idx !== -1) {
            venuesData[idx] = {
                ...venuesData[idx],
                name,
                address,
                lat,
                lng,
                priceMin: minPrice,
                priceMax: maxPrice,
                cuisineLabel: cuisine,
                openHours: hours,
                status: statusVal,
                image: payload.image_url,
                parking: amenities.has_parking,
                private_room: amenities.has_private_room,
                vegetarian: amenities.vegetarian_support
            };
        }

        try {
            if (token) {
                await fetch(`/api/admin/restaurants/${idNum}`, {
                    method: 'PUT',
                    headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` },
                    body: JSON.stringify(payload)
                });
            }
        } catch (_) {}

        showToast(`Đã cập nhật thông tin nhà hàng '${name}' thành công!`, 'success');
    } else {
        // Thêm mới nhà hàng (POST)
        const newId = venuesData.length > 0 ? Math.max(...venuesData.map(v => v.id || 0)) + 1 : 1;
        const newVenue = {
            id: newId,
            name,
            address,
            lat,
            lng,
            priceMin: minPrice,
            priceMax: maxPrice,
            rating: 5.0,
            reviews: 1,
            cuisineLabel: cuisine,
            openHours: hours,
            status: statusVal,
            image: payload.image_url,
            parking: amenities.has_parking,
            private_room: amenities.has_private_room,
            vegetarian: amenities.vegetarian_support
        };
        venuesData.unshift(newVenue);

        try {
            if (token) {
                await fetch('/api/admin/restaurants', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` },
                    body: JSON.stringify(payload)
                });
            }
        } catch (_) {}

        showToast(`Đã thêm mới nhà hàng '${name}' vào hệ thống!`, 'success');
    }

    localStorage.setItem(ADMIN_VENUES_KEY, JSON.stringify(venuesData));
    closeRestaurantModal();
    handleVenueSearch();
    renderStatsOverview();
}

/**
 * Xóa vĩnh viễn nhà hàng (DELETE - FR-13)
 */
async function deleteRestaurant(venueId) {
    const v = venuesData.find(item => item.id === venueId);
    if (!v) return;

    if (!confirm(`Bạn có chắc chắn muốn XÓA VĨNH VIỄN nhà hàng '${v.name}' (ID=${venueId}) khỏi hệ thống? Thao tác này không thể hoàn tác.`)) {
        return;
    }

    const token = localStorage.getItem('auth_token');
    try {
        if (token) {
            await fetch(`/api/admin/restaurants/${venueId}`, {
                method: 'DELETE',
                headers: { 'Authorization': `Bearer ${token}` }
            });
        }
    } catch (_) {}

    venuesData = venuesData.filter(item => item.id !== venueId);
    localStorage.setItem(ADMIN_VENUES_KEY, JSON.stringify(venuesData));
    handleVenueSearch();
    renderStatsOverview();
    showToast(`Đã xóa vĩnh viễn nhà hàng '${v.name}' thành công.`, 'error');
}

function handleVenueSearch() {
    const kw = document.getElementById('venue-search-input').value.trim().toLowerCase();
    const districtFilter = document.getElementById('venue-district-filter').value;
    const statusFilter = document.getElementById('venue-status-filter').value;

    let filtered = [...venuesData];

    if (kw) {
        filtered = filtered.filter(v =>
            v.name.toLowerCase().includes(kw) ||
            v.address.toLowerCase().includes(kw)
        );
    }

    if (districtFilter) {
        filtered = filtered.filter(v => v.address.includes(districtFilter) || (v.district && v.district.includes(districtFilter)));
    }

    if (statusFilter) {
        filtered = filtered.filter(v => v.status === statusFilter);
    }

    renderVenuesTable(filtered);
}

/**
 * ==============================================================================
 * 5. QUẢN LÝ BÁO CÁO & KHIẾU NẠI (REPORTS MODERATION)
 * ==============================================================================
 */
function renderReportsTable(customList = null) {
    const list = customList || reportsData;
    const tbody = document.getElementById('reports-table-body');
    tbody.innerHTML = '';

    if (list.length === 0) {
        tbody.innerHTML = `<tr><td colspan="7" style="text-align:center;padding:30px;color:var(--text-muted);">Không có báo cáo nào.</td></tr>`;
        return;
    }

    list.forEach(r => {
        const tr = document.createElement('tr');
        const isPending = r.status === 'pending';

        tr.innerHTML = `
            <td><strong>${r.type}</strong></td>
            <td><span style="color:var(--brand-red);font-weight:600;">${r.target_name}</span></td>
            <td>${r.reporter_name}</td>
            <td style="max-width:280px;line-height:1.4;">${r.content}</td>
            <td style="white-space:nowrap;font-size:0.75rem;color:var(--text-muted);">${r.created_at}</td>
            <td>
                <span class="status-badge ${isPending ? 'status-pending' : 'status-resolved'}">
                    ${isPending ? '⏳ Chờ xử lý' : '✓ Đã giải quyết'}
                </span>
            </td>
            <td style="text-align:right;">
                ${isPending ? `
                    <div style="display:flex;gap:6px;justify-content:flex-end;">
                        <button type="button" class="btn-action btn-unlock" onclick="resolveReport(${r.id}, 'resolved')">Duyệt xử lý</button>
                        <button type="button" class="btn-action" onclick="resolveReport(${r.id}, 'dismissed')">Bác bỏ</button>
                    </div>
                ` : '<span style="font-size:0.75rem;color:var(--text-muted);">Đã hoàn tất</span>'}
            </td>
        `;
        tbody.appendChild(tr);
    });
}

function resolveReport(reportId, newStatus) {
    const report = reportsData.find(r => r.id === reportId);
    if (!report) return;

    report.status = newStatus;
    localStorage.setItem(ADMIN_REPORTS_KEY, JSON.stringify(reportsData));
    renderReportsTable();
    renderStatsOverview();
    showToast(`Đã cập nhật trạng thái báo cáo #${reportId} thành '${newStatus === 'resolved' ? 'Đã giải quyết' : 'Đã bác bỏ'}'`, 'success');
}

function handleReportFilter() {
    const filter = document.getElementById('report-status-filter').value;
    if (!filter) {
        renderReportsTable();
    } else {
        renderReportsTable(reportsData.filter(r => r.status === filter));
    }
}

/**
 * ==============================================================================
 * 6. ĐIỀU HƯỚNG TABS & TIỆN ÍCH
 * ==============================================================================
 */
function switchAdminTab(tabId, navElement) {
    document.querySelectorAll('.tab-pane').forEach(p => p.classList.remove('active'));
    document.querySelectorAll('.nav-item').forEach(i => i.classList.remove('active'));

    const targetPane = document.getElementById(tabId);
    if (targetPane) targetPane.classList.add('active');

    if (navElement) navElement.classList.add('active');

    // Cập nhật tiêu đề trang
    const titles = {
        'tab-overview': 'Tổng quan Dashboard',
        'tab-users': 'Quản lý Tài khoản Người dùng (BR-07)',
        'tab-restaurants': 'Quản lý 50 Nhà hàng TP.HCM',
        'tab-reports': 'Kiểm duyệt Báo cáo & Phản ánh Vi phạm',
        'tab-settings': 'Cài đặt Hệ thống'
    };
    document.getElementById('page-title').innerText = titles[tabId] || 'Quản trị viên';

    // Đóng sidebar nếu đang mở trên mobile
    if (window.innerWidth <= 900) {
        document.getElementById('admin-sidebar').classList.remove('open');
    }
}

function toggleSidebar() {
    document.getElementById('admin-sidebar').classList.toggle('open');
}

function showToast(message, type = 'success') {
    const container = document.getElementById('admin-toast-container');
    if (!container) return;

    const toast = document.createElement('div');
    toast.className = `admin-toast ${type}`;
    toast.innerHTML = `<span>${type === 'success' ? '✓' : type === 'error' ? '✕' : 'ℹ'}</span> <span>${message}</span>`;
    container.appendChild(toast);

    setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transform = 'translateY(-10px)';
        toast.style.transition = 'all 0.3s ease';
        setTimeout(() => toast.remove(), 300);
    }, 3200);
}

// Khởi chạy khi tài liệu sẵn sàng
window.addEventListener('DOMContentLoaded', () => {
    initDataStorage();
    const hasAccess = checkAdminRouteGuard();
    if (hasAccess) {
        loadAllAdminData();
    }
});
