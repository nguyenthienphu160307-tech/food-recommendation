/**
 * =============================================================================
 * MODULE: GUEST MODE GUARD (Task TE9C675 - BR-02)
 * Quy tắc cho Khách chưa đăng nhập (Guest):
 *  - Được phép: Tìm kiếm cơ bản, lọc bán kính/tiện ích, xem bản đồ, tối đa 3 lượt chat AI miễn phí.
 *  - Bị chặn bằng Modal nhắc đăng nhập thân thiện:
 *      1. Bấm Lưu yêu thích (♥) hoặc xem danh sách yêu thích.
 *      2. Bấm Viết đánh giá / Chấm sao nhà hàng.
 *      3. Vượt quá 3 lượt chat AI miễn phí.
 * =============================================================================
 */

const GuestModeGuard = {
    MAX_FREE_CHATS: 3,
    COUNT_KEY: 'smart_dining_guest_chat_count',
    GUEST_ID_KEY: 'smart_dining_guest_id',

    isLoggedIn() {
        const token = localStorage.getItem('access_token');
        const foodApiLoggedIn = window.FoodAPI && window.FoodAPI.auth && window.FoodAPI.auth.isLoggedIn();
        return Boolean(token || foodApiLoggedIn);
    },

    getGuestId() {
        let gid = localStorage.getItem(this.GUEST_ID_KEY);
        if (!gid) {
            gid = 'guest_' + Math.random().toString(36).slice(2, 11);
            localStorage.setItem(this.GUEST_ID_KEY, gid);
        }
        return gid;
    },

    getChatCount() {
        return parseInt(localStorage.getItem(this.COUNT_KEY) || '0', 10);
    },

    getRemainingChats() {
        return Math.max(0, this.MAX_FREE_CHATS - this.getChatCount());
    },

    /**
     * Kiểm tra quyền truy cập hành động yêu cầu tài khoản ('favorite' | 'review')
     * Trả về true nếu đã đăng nhập, false nếu là Guest (và tự bật Modal thân thiện).
     */
    requireAuth(actionType = 'favorite') {
        if (this.isLoggedIn()) return true;
        this.showLoginPrompt(actionType);
        return false;
    },

    /**
     * Kiểm tra và trừ 1 lượt chat AI miễn phí của Guest (BR-02)
     */
    consumeGuestChatTurn() {
        if (this.isLoggedIn()) return true;

        const used = this.getChatCount();
        if (used >= this.MAX_FREE_CHATS) {
            this.showLoginPrompt('chat_limit');
            return false;
        }

        localStorage.setItem(this.COUNT_KEY, String(used + 1));
        this.updateGuestChatBadge();
        return true;
    },

    updateGuestChatBadge() {
        const badge = document.getElementById('guest-chat-limit-badge');
        if (!badge) return;

        if (this.isLoggedIn()) {
            badge.style.display = 'none';
            return;
        }

        const left = this.getRemainingChats();
        badge.style.display = 'flex';
        badge.innerHTML = left > 0
            ? `<span>👋 Chế độ Khách: còn <strong>${left}/${this.MAX_FREE_CHATS}</strong> lượt hỏi AI miễn phí</span>`
            : `<span>🔒 Đã hết lượt hỏi miễn phí — <a href="login.html" style="color:#e11d48;font-weight:700;">Đăng nhập ngay</a></span>`;
    },

    /**
     * Hiển thị Modal nhắc đăng nhập thân thiện (BR-02)
     */
    showLoginPrompt(reason = 'favorite', customMessage = null) {
        this._ensureModalExists();

        const copyMap = {
            favorite: {
                icon: '❤️',
                title: 'Lưu quán ngon vào danh sách yêu thích?',
                desc: 'Đăng nhập tài khoản Smart Dining để lưu các quán ăn bạn thích và đồng bộ trên mọi thiết bị nhé!'
            },
            review: {
                icon: '⭐',
                title: 'Chia sẻ trải nghiệm ẩm thực của bạn!',
                desc: 'Hãy đăng nhập nhanh để gửi đánh giá, chấm sao và giúp cộng đồng tìm được những quán ăn chất lượng hơn.'
            },
            chat_limit: {
                icon: '🤖',
                title: 'Bạn đã dùng hết 3 lượt hỏi AI miễn phí',
                desc: 'Đăng nhập hoặc đăng ký miễn phí để trò chuyện không giới hạn với Trợ lý AI và lưu lại lịch sử gợi ý của bạn!'
            }
        };

        const info = copyMap[reason] || copyMap.favorite;
        document.getElementById('guest-modal-icon').textContent = info.icon;
        document.getElementById('guest-modal-title').textContent = info.title;
        document.getElementById('guest-modal-desc').textContent = customMessage || info.desc;
        document.getElementById('guest-login-prompt-modal').classList.add('open');
    },

    closeLoginPrompt() {
        const modal = document.getElementById('guest-login-prompt-modal');
        if (modal) modal.classList.remove('open');
    },

    _ensureModalExists() {
        if (document.getElementById('guest-login-prompt-modal')) return;

        const wrapper = document.createElement('div');
        wrapper.id = 'guest-login-prompt-modal';
        wrapper.className = 'modal-backdrop';
        wrapper.onclick = (e) => {
            if (e.target === wrapper) this.closeLoginPrompt();
        };

        wrapper.innerHTML = `
            <div class="modal-card" style="max-width:430px;text-align:center;padding:28px 24px;">
                <div id="guest-modal-icon" style="font-size:2.4rem;margin-bottom:10px;">❤️</div>
                <h3 id="guest-modal-title" style="font-size:1.15rem;margin-bottom:8px;color:var(--text-primary);"></h3>
                <p id="guest-modal-desc" style="font-size:0.88rem;color:var(--text-secondary);line-height:1.55;margin-bottom:20px;"></p>
                <div style="display:flex;flex-direction:column;gap:10px;">
                    <a href="login.html" class="btn-ai-ask" style="height:42px;justify-content:center;text-decoration:none;border-radius:10px;font-size:0.9rem;">
                        Đăng nhập ngay
                    </a>
                    <a href="register.html" style="height:40px;display:flex;align-items:center;justify-content:center;text-decoration:none;border-radius:10px;border:1px solid var(--border);background:var(--bg-subtle);color:var(--text-primary);font-size:0.86rem;font-weight:600;">
                        Tạo tài khoản miễn phí
                    </a>
                    <button type="button" onclick="GuestModeGuard.closeLoginPrompt()" style="background:transparent;border:none;color:var(--text-muted);font-size:0.82rem;cursor:pointer;padding:6px;">
                        Để sau, tiếp tục tìm kiếm cơ bản
                    </button>
                </div>
            </div>
        `;
        document.body.appendChild(wrapper);
    }
};

window.GuestModeGuard = GuestModeGuard;
document.addEventListener('DOMContentLoaded', () => GuestModeGuard.updateGuestChatBadge());