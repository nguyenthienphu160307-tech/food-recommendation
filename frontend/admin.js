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
        if (userEmailSpan) userEmailSpan.innerText = 'user.demo@foodai.vn';
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
        const res = await fetch('/api/auth/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ account: email, password: password })
        });
        if (res.ok) {
            const data = await res.json();
            const roles = data.user?.roles || [];
            if (!roles.includes('admin')) {
                alert('Tài khoản này không có quyền Quản trị viên (Admin).');
                return;
            }
            if (data.tokens?.access_token) {
                localStorage.setItem('auth_token', data.tokens.access_token);
            }
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
    // 1. Users
    const storedUsers = localStorage.getItem(ADMIN_USERS_KEY);
    usersData = storedUsers ? JSON.parse(storedUsers) : [...INITIAL_USERS];

    // 2. Venues (từ venues-data.js đã seed 50 quán)
    const storedVenues = localStorage.getItem(ADMIN_VENUES_KEY);
    if (storedVenues) {
        venuesData = JSON.parse(storedVenues);
    } else if (typeof SEED_VENUES !== 'undefined' && Array.isArray(SEED_VENUES)) {
        venuesData = SEED_VENUES.map(v => ({ ...v, status: 'active' }));
        localStorage.setItem(ADMIN_VENUES_KEY, JSON.stringify(venuesData));
    } else {
        venuesData = [];
    }

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

/**
 * Render Tab 1: Tổng quan Dashboard & Biểu đồ phân bố
 */
function renderStatsOverview() {
    // Cập nhật số liệu KPI Cards
    const totalUsers = usersData.length;
    const activeUsers = usersData.filter(u => u.status === 'active').length;
    const lockedUsers = usersData.filter(u => u.status === 'locked').length;

    const totalVenues = venuesData.length;
    const pendingReports = reportsData.filter(r => r.status === 'pending').length;

    document.getElementById('stat-total-users').innerText = totalUsers;
    document.getElementById('badge-users-count').innerText = totalUsers;
    document.getElementById('stat-total-venues').innerText = totalVenues;
    document.getElementById('badge-venues-count').innerText = totalVenues;
    document.getElementById('stat-pending-reports').innerText = pendingReports;
    document.getElementById('badge-reports-count').innerText = pendingReports;

    // Phân bố nhà hàng theo Quận
    const districtCounts = {};
    venuesData.forEach(v => {
        const d = v.district || (v.address.includes('Quận 1') ? 'Quận 1' : v.address.includes('Quận 3') ? 'Quận 3' : v.address.includes('Bình Thạnh') ? 'Bình Thạnh' : 'Thủ Đức');
        districtCounts[d] = (districtCounts[d] || 0) + 1;
    });

    const distListContainer = document.getElementById('district-distribution-list');
    distListContainer.innerHTML = '';
    Object.entries(districtCounts).forEach(([district, count]) => {
        const pct = Math.round((count / totalVenues) * 100);
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

    // Tỷ lệ thể loại ẩm thực
    const cuisineCounts = {};
    venuesData.forEach(v => {
        const c = v.cuisineLabel || 'Khác';
        cuisineCounts[c] = (cuisineCounts[c] || 0) + 1;
    });

    const cuisineListContainer = document.getElementById('cuisine-distribution-list');
    cuisineListContainer.innerHTML = '';
    Object.entries(cuisineCounts).slice(0, 5).forEach(([cuisine, count]) => {
        const pct = Math.round((count / totalVenues) * 100);
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
 * Nghiệp vụ BR-07: Khóa hoặc Mở khóa tài khoản người dùng vi phạm
 * @param {number} userId 
 */
function toggleUserLock(userId) {
    const user = usersData.find(u => u.id === userId);
    if (!user) return;

    if (user.role === 'admin') {
        showToast('Không thể khóa tài khoản Quản trị viên.', 'error');
        return;
    }

    if (user.status === 'active') {
        if (confirm(`Bạn có chắc muốn KHÓA tài khoản '${user.full_name}' (${user.email}) theo quy định BR-07?`)) {
            user.status = 'locked';
            showToast(`Đã khóa tài khoản '${user.full_name}' thành công theo quy tắc BR-07!`, 'error');
        }
    } else {
        user.status = 'active';
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

    list.slice(0, 30).forEach(v => {
        const tr = document.createElement('tr');
        const isHidden = v.status === 'hidden';

        tr.innerHTML = `
            <td>
                <div class="cell-venue-info">
                    <img src="${v.image || 'https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?auto=format&fit=crop&w=150&q=80'}" class="cell-venue-thumb" alt="${v.name}">
                    <div>
                        <div class="cell-name">${v.name}</div>
                        <div class="cell-sub">📍 ${v.address}</div>
                    </div>
                </div>
            </td>
            <td>
                <strong>${v.cuisineLabel || 'Ẩm thực'}</strong><br>
                <span class="cell-sub">${(v.priceMin || 50000).toLocaleString()}đ - ${(v.priceMax || 200000).toLocaleString()}đ</span>
            </td>
            <td>
                <span style="color:#f59e0b;font-weight:700;">★ ${v.rating || 4.5}</span>
                <span class="cell-sub">(${v.reviews || 100} đánh giá)</span>
            </td>
            <td>
                <div style="display:flex;gap:4px;flex-wrap:wrap;font-size:0.72rem;">
                    ${v.parking ? '<span style="background:#e0f2fe;color:#0284c7;padding:1px 5px;border-radius:4px;">Đỗ xe</span>' : ''}
                    ${v.private_room ? '<span style="background:#f3e8ff;color:#7e22ce;padding:1px 5px;border-radius:4px;">Phòng riêng</span>' : ''}
                    ${v.vegetarian ? '<span style="background:#dcfce7;color:#15803d;padding:1px 5px;border-radius:4px;">Món chay</span>' : ''}
                </div>
            </td>
            <td>
                <span class="status-badge ${isHidden ? 'status-hidden' : 'status-active'}">
                    ${isHidden ? '👁 Ẩn' : '✓ Hiển thị'}
                </span>
            </td>
            <td style="text-align:right;">
                <button type="button" class="btn-action" onclick="toggleVenueVisibility(${v.id})">
                    ${isHidden ? 'Hiện quán' : 'Ẩn quán'}
                </button>
            </td>
        `;
        tbody.appendChild(tr);
    });
}

function toggleVenueVisibility(venueId) {
    const v = venuesData.find(item => item.id === venueId);
    if (!v) return;

    v.status = v.status === 'hidden' ? 'active' : 'hidden';
    localStorage.setItem(ADMIN_VENUES_KEY, JSON.stringify(venuesData));
    handleVenueSearch();
    showToast(`Đã đổi trạng thái nhà hàng '${v.name}' thành: ${v.status === 'hidden' ? 'ẨN' : 'HIỂN THỊ'}`, 'success');
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
