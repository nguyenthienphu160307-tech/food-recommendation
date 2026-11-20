/**
 * =============================================================================
 * MODULE: AI CHAT & MAP SPLIT-SCREEN SYNC (Task TE9C674)
 * Khi AI trả về Top N quán trong khung chat, bản đồ bên cạnh tự động:
 *  1. Di chuyển (flyTo / flyToBounds) tới cụm nhà hàng được đề xuất.
 *  2. Làm nổi bật các ghim Top #1..#N kèm điểm phù hợp.
 *  3. Cho phép bấm từng quán trong khung chat để flyTo chính xác ghim quán đó.
 * =============================================================================
 */

const AIChatMapSync = {
    API_URL: 'http://127.0.0.1:8000/api/search/ai-recommend',
    isSplitMode: false,

    toggleSplitScreen() {
        const drawer = document.getElementById('ai-drawer');
        if (!drawer) return;
        this.isSplitMode = !this.isSplitMode;
        drawer.classList.toggle('split-screen-mode', this.isSplitMode);
        const btn = document.getElementById('btn-toggle-split-chat');
        if (btn) {
            btn.title = this.isSplitMode ? 'Thu gọn khung chat nổi' : 'Mở chế độ Split-screen cạnh Bản đồ';
            btn.textContent = this.isSplitMode ? '◧ Thu gọn' : '◫ Split Map';
        }
    },

    /**
     * Gọi API POST /api/search/ai-recommend (TE9C670) -> fallback local nếu backend chưa có data
     */
    async fetchTopRecommendations(promptText, currentPos, radiusKm = 5, topN = 5, sessionId = null, localFallbackVenues = []) {
        const headers = { 'Content-Type': 'application/json' };
        const token = localStorage.getItem('access_token');
        if (token) headers['Authorization'] = `Bearer ${token}`;

        // Truyền guest_id để hỗ trợ kiểm tra giới hạn BR-02 (TE9C675)
        if (window.GuestModeGuard) {
            headers['X-Guest-Id'] = window.GuestModeGuard.getGuestId();
        }

        try {
            const res = await fetch(this.API_URL, {
                method: 'POST',
                headers,
                body: JSON.stringify({
                    prompt: promptText,
                    user_lat: currentPos?.lat ?? 10.776889,
                    user_lng: currentPos?.lng ?? 106.700806,
                    radius_km: radiusKm,
                    top_n: topN,
                    session_id: sessionId
                })
            });

            if (res.status === 403) {
                const errData = await res.json().catch(() => ({}));
                if (window.GuestModeGuard) {
                    window.GuestModeGuard.showLoginPrompt('chat_limit', errData.detail?.message || errData.detail);
                }
                return { blocked: true, recommendations: [] };
            }

            if (res.ok) {
                const data = await res.json();
                if (Array.isArray(data.recommendations) && data.recommendations.length > 0) {
                    return {
                        blocked: false,
                        explanation: data.ai_explanation,
                        resolvedLocation: data.resolved_location,
                        recommendations: data.recommendations.map(r => ({
                            id: r.id,
                            name: r.name,
                            address: r.address,
                            lat: r.latitude,
                            lng: r.longitude,
                            cuisineLabel: r.cuisine_type,
                            priceMin: r.min_price,
                            priceMax: r.max_price,
                            rating: r.rating ?? r.avg_rating ?? 4.5,
                            distanceKm: r.distance_km,
                            matchScore: Math.round(r.match_score ?? r.final_score ?? 88),
                            image: r.cover_image_url || 'https://images.unsplash.com/photo-1544025162-d76694265947?auto=format&fit=crop&w=600&q=80',
                            parking: r.amenities?.has_parking ?? false,
                            private_room: r.amenities?.has_private_room ?? false,
                            vegetarian: r.amenities?.vegetarian_support ?? false
                        }))
                    };
                }
            }
        } catch (err) {
            console.warn('[TE9C674] Backend /api/search/ai-recommend chưa sẵn sàng, dùng dữ liệu local:', err.message);
        }

        // Fallback cục bộ từ danh sách venues đang có trên trang
        const lower = promptText.toLowerCase();
        const filtered = (localFallbackVenues || []).filter(v => {
            if (lower.includes('nướng') || lower.includes('bbq')) {
                return (v.category === 'bbq') || (v.cuisineLabel || '').toLowerCase().includes('nướng');
            }
            if (lower.includes('lẩu')) {
                return (v.category === 'hotpot') || (v.cuisineLabel || '').toLowerCase().includes('lẩu');
            }
            if (lower.includes('chay')) {
                return v.vegetarian || (v.category === 'vegan');
            }
            return true;
        });

        const topList = (filtered.length > 0 ? filtered : localFallbackVenues).slice(0, topN);
        return {
            blocked: false,
            explanation: `Mình đã tìm thấy Top ${topList.length} nhà hàng phù hợp nhất cho yêu cầu <strong>"${promptText}"</strong> và tự động di chuyển bản đồ đến các vị trí đề xuất!`,
            resolvedLocation: null,
            recommendations: topList
        };
    },

    /**
     * Render Top N thẻ quán vào khung chat + đồng bộ flyTo & highlight ghim trên bản đồ
     */
    syncResultsToChatAndMap(feedEl, mapComponent, result, onRenderGridCallback = null) {
        if (!result || result.blocked) return;
        const topVenues = result.recommendations || [];

        let cardsHtml = '';
        if (topVenues.length > 0) {
            cardsHtml = `
                <div class="ai-chat-top-list">
                    ${topVenues.map((v, idx) => {
                        const dist = v.distanceKm != null ? `${Number(v.distanceKm).toFixed(1)} km` : '';
                        const score = v.matchScore ? `• ${v.matchScore}% hợp` : '';
                        return `
                            <div class="ai-chat-venue-card" onclick="AIChatMapSync.focusFromChat(${v.id})">
                                <div class="ai-chat-venue-info">
                                    <strong>#${idx + 1}. ${v.name}</strong>
                                    <small>★ ${Number(v.rating || 4.5).toFixed(1)} ${dist ? '• ' + dist : ''} ${score}</small>
                                </div>
                                <button type="button" class="ai-chat-fly-btn">📍 Xem</button>
                            </div>
                        `;
                    }).join('')}
                </div>
            `;
        }

        const bubble = document.createElement('div');
        bubble.className = 'bubble bubble-ai';
        bubble.innerHTML = `
            <div>${result.explanation || 'Đây là các địa điểm phù hợp nhất quanh bạn:'}</div>
            ${cardsHtml}
        `;
        feedEl.appendChild(bubble);
        feedEl.scrollTop = feedEl.scrollHeight;

        // Cập nhật lại lưới hiển thị nếu có callback
        if (typeof onRenderGridCallback === 'function' && topVenues.length > 0) {
            onRenderGridCallback(topVenues);
        }

        // Đồng bộ bản đồ: flyTo & làm nổi bật các ghim Top N
        if (mapComponent && typeof mapComponent.highlightRecommendedVenues === 'function') {
            mapComponent.highlightRecommendedVenues(topVenues);
        }
    },

    focusFromChat(venueId) {
        if (typeof window.mapComponent !== 'undefined' && window.mapComponent) {
            window.mapComponent.focusVenue(venueId);
        }
        if (typeof window.scrollToAndHighlightCard === 'function') {
            window.scrollToAndHighlightCard(venueId);
        }
    }
};

window.AIChatMapSync = AIChatMapSync;