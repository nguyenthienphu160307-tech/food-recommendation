/**
 * SMART DINING - MAIN FRONTEND SCRIPT (TSK-12)
 * Manages Theme, Navigation, Mobile Drawer, Auth State, and Toast Notifications
 */

const STORAGE_KEYS = {
    THEME: 'smart_dining_theme',
    AUTH_USER: 'smart_dining_user',
    AUTH_TOKEN: 'smart_dining_token'
};

// =====================================================================
// 1. THEME CONTROLLER (LIGHT / DARK MODE)
// =====================================================================
function initTheme() {
    const savedTheme = localStorage.getItem(STORAGE_KEYS.THEME) || 'light';
    setTheme(savedTheme);

    const toggleBtns = document.querySelectorAll('.btn-theme-toggle');
    toggleBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const currentTheme = document.documentElement.getAttribute('data-theme') || 'light';
            const nextTheme = currentTheme === 'dark' ? 'light' : 'dark';
            setTheme(nextTheme);
        });
    });
}

function setTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem(STORAGE_KEYS.THEME, theme);
    
    // Update theme toggle button icons
    document.querySelectorAll('.btn-theme-toggle').forEach(btn => {
        btn.innerHTML = theme === 'dark'
            ? `<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/></svg>`
            : `<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>`;
    });
}

// =====================================================================
// 2. TOAST NOTIFICATION SYSTEM
// =====================================================================
function showToast(type = 'info', message = '', title = '') {
    let container = document.getElementById('toast-container');
    if (!container) {
        container = document.createElement('div');
        container.id = 'toast-container';
        container.className = 'toast-container';
        document.body.appendChild(container);
    }

    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;

    let iconSvg = '';
    let defaultTitle = '';
    if (type === 'success') {
        defaultTitle = 'Thành công';
        iconSvg = `<svg class="toast-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>`;
    } else if (type === 'error') {
        defaultTitle = 'Có lỗi xảy ra';
        iconSvg = `<svg class="toast-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="15" y1="9" x2="9" y2="15"/><line x1="9" y1="9" x2="15" y2="15"/></svg>`;
    } else if (type === 'warning') {
        defaultTitle = 'Cảnh báo';
        iconSvg = `<svg class="toast-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>`;
    } else {
        defaultTitle = 'Thông báo';
        iconSvg = `<svg class="toast-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/></svg>`;
    }

    toast.innerHTML = `
        ${iconSvg}
        <div class="toast-content">
            <div class="toast-title">${title || defaultTitle}</div>
            <div class="toast-message">${message}</div>
        </div>
        <button type="button" class="toast-close" onclick="this.parentElement.remove()">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
        </button>
    `;

    container.appendChild(toast);

    setTimeout(() => {
        toast.style.animation = 'toastSlideOut 0.3s forwards';
        setTimeout(() => toast.remove(), 300);
    }, 4000);
}

// =====================================================================
// 3. AUTHENTICATION STATE & NAVBAR SYNC
// =====================================================================
function getAuthUser() {
    try {
        const raw = localStorage.getItem(STORAGE_KEYS.AUTH_USER);
        return raw ? JSON.parse(raw) : null;
    } catch (_) {
        return null;
    }
}

function setAuthSession(user, token) {
    if (user) {
        localStorage.setItem(STORAGE_KEYS.AUTH_USER, JSON.stringify(user));
    }
    if (token) {
        localStorage.setItem(STORAGE_KEYS.AUTH_TOKEN, token);
    }
    renderAuthState();
}

function clearAuthSession() {
    localStorage.removeItem(STORAGE_KEYS.AUTH_USER);
    localStorage.removeItem(STORAGE_KEYS.AUTH_TOKEN);
    renderAuthState();
}

function renderAuthState() {
    const user = getAuthUser();
    const guestArea = document.getElementById('nav-guest-area');
    const userArea = document.getElementById('nav-user-area');
    const drawerGuest = document.getElementById('drawer-guest-area');
    const drawerUser = document.getElementById('drawer-user-area');

    if (user) {
        if (guestArea) guestArea.style.display = 'none';
        if (userArea) {
            userArea.style.display = 'flex';
            const nameEl = userArea.querySelector('.user-display-name');
            if (nameEl) nameEl.textContent = user.full_name || user.email || 'Người dùng';
        }
        if (drawerGuest) drawerGuest.style.display = 'none';
        if (drawerUser) {
            drawerUser.style.display = 'flex';
            const drawerName = drawerUser.querySelector('.drawer-user-name');
            if (drawerName) drawerName.textContent = user.full_name || user.email || 'Người dùng';
        }
    } else {
        if (guestArea) guestArea.style.display = 'flex';
        if (userArea) userArea.style.display = 'none';
        if (drawerGuest) drawerGuest.style.display = 'flex';
        if (drawerUser) drawerUser.style.display = 'none';
    }
}

function toggleUserDropdown() {
    const menu = document.getElementById('user-dropdown-menu');
    if (menu) menu.classList.toggle('is-open');
}

function handleLogout() {
    clearAuthSession();
    showToast('info', 'Bạn đã đăng xuất an toàn khỏi hệ thống.', 'Đăng xuất thành công');
    setTimeout(() => {
        window.location.href = '/login';
    }, 600);
}

// =====================================================================
// 4. MOBILE DRAWER NAVIGATION CONTROLLER (NFR-06)
// =====================================================================
function openMobileDrawer() {
    const backdrop = document.getElementById('mobile-drawer-backdrop');
    if (backdrop) backdrop.classList.add('is-open');
    document.body.style.overflow = 'hidden';
}

function closeMobileDrawer() {
    const backdrop = document.getElementById('mobile-drawer-backdrop');
    if (backdrop) backdrop.classList.remove('is-open');
    document.body.style.overflow = '';
}

// Close dropdowns on outer click
document.addEventListener('click', (e) => {
    const dropdown = document.getElementById('user-dropdown-menu');
    const userChip = document.querySelector('.user-chip-btn');
    if (dropdown && userChip && !userChip.contains(e.target) && !dropdown.contains(e.target)) {
        dropdown.classList.remove('is-open');
    }
});

window.addEventListener('DOMContentLoaded', () => {
    initTheme();
    renderAuthState();
});
