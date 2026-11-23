/**
 * =============================================================================
 * MODULE: LOCATION MANAGER (Task TE9C65E / TSK-21 - UC-03)
 * Chức năng:
 *  1. Gọi HTML5 Geolocation API (navigator.geolocation) lấy tọa độ GPS thực tế.
 *  2. Bắt và phân loại ngoại lệ GPS (PERMISSION_DENIED, TIMEOUT, UNAVAILABLE).
 *  3. Tự động bật Modal chọn Quận/Huyện TP.HCM hoặc hướng dẫn kéo ghim trên bản đồ
 *     khi người dùng từ chối cấp quyền vị trí.
 *  4. Hỗ trợ chọn bán kính tìm kiếm (1km, 3km, 5km, 10km) đồng bộ với Map & API.
 * =============================================================================
 */

(function (global) {
    'use strict';

    const LOCATION_STORAGE_KEY = 'smart_dining_active_location';

    /**
     * Danh mục tọa độ tâm chuẩn (WGS84) của các Quận/Huyện & TP. Thủ Đức (TP.HCM)
     * Phục vụ fallback tức thì khi người dùng từ chối GPS hoặc muốn đổi khu vực.
     */
    const HCM_DISTRICTS = [
        { id: 'q1', name: 'Quận 1', address: 'Phường Bến Nghé, Quận 1, TP.HCM', lat: 10.7769, lng: 106.7009 },
        { id: 'q3', name: 'Quận 3', address: 'Phường Võ Thị Sáu, Quận 3, TP.HCM', lat: 10.7843, lng: 106.6845 },
        { id: 'q4', name: 'Quận 4', address: 'Phường 12, Quận 4, TP.HCM', lat: 10.7578, lng: 106.7013 },
        { id: 'q5', name: 'Quận 5', address: 'Phường 8, Quận 5, TP.HCM', lat: 10.7540, lng: 106.6634 },
        { id: 'q6', name: 'Quận 6', address: 'Phường 11, Quận 6, TP.HCM', lat: 10.7480, lng: 106.6352 },
        { id: 'q7', name: 'Quận 7', address: 'Phường Tân Phú, Quận 7, TP.HCM', lat: 10.7340, lng: 106.7218 },
        { id: 'q8', name: 'Quận 8', address: 'Phường 5, Quận 8, TP.HCM', lat: 10.7241, lng: 106.6286 },
        { id: 'q10', name: 'Quận 10', address: 'Phường 12, Quận 10, TP.HCM', lat: 10.7745, lng: 106.6675 },
        { id: 'q11', name: 'Quận 11', address: 'Phường 5, Quận 11, TP.HCM', lat: 10.7630, lng: 106.6433 },
        { id: 'q12', name: 'Quận 12', address: 'Phường Thới An, Quận 12, TP.HCM', lat: 10.8672, lng: 106.6413 },
        { id: 'binhthanh', name: 'Quận Bình Thạnh', address: 'Phường 25, Quận Bình Thạnh, TP.HCM', lat: 10.8035, lng: 106.7145 },
        { id: 'govap', name: 'Quận Gò Vấp', address: 'Đường Thống Nhất, Phường 16, Quận Gò Vấp, TP.HCM', lat: 10.8386, lng: 106.6650 },
        { id: 'phunhuan', name: 'Quận Phú Nhuận', address: 'Phường 7, Quận Phú Nhuận, TP.HCM', lat: 10.7992, lng: 106.6805 },
        { id: 'tanbinh', name: 'Quận Tân Bình', address: 'Phường 13, Quận Tân Bình, TP.HCM', lat: 10.8015, lng: 106.6526 },
        { id: 'tanphu', name: 'Quận Tân Phú', address: 'Phường Tân Sơn Nhì, Quận Tân Phú, TP.HCM', lat: 10.7905, lng: 106.6282 },
        { id: 'binhtan', name: 'Quận Bình Tân', address: 'Phường Bình Trị Đông B, Quận Bình Tân, TP.HCM', lat: 10.7653, lng: 106.6038 },
        { id: 'thuduc_thaodien', name: 'TP. Thủ Đức (Thảo Điền)', address: 'Phường Thảo Điền, TP. Thủ Đức, TP.HCM', lat: 10.8045, lng: 106.7365 },
        { id: 'thuduc_binhtho', name: 'TP. Thủ Đức (Bình Thọ / Hiệp Phú)', address: 'Phường Hiệp Phú, TP. Thủ Đức, TP.HCM', lat: 10.8482, lng: 106.7712 }
    ];

    class LocationManager {
        /**
         * @param {Object} options Cấu hình khởi tạo bộ quản lý vị trí
         * @param {Function} options.onLocationResolved Callback khi xác định được vị trí: fn({ lat, lng, address, source, radiusKm })
         * @param {Function} options.onRadiusChanged Callback khi đổi bán kính tìm kiếm: fn(radiusKm)
         */
        constructor(options = {}) {
            this.onLocationResolved = options.onLocationResolved || null;
            this.onRadiusChanged = options.onRadiusChanged || null;
            this.currentRadiusKm = options.defaultRadiusKm || 5;
            this.currentLocation = this._loadSavedLocation() || {
                lat: 10.7769,
                lng: 106.7009,
                address: 'Quận 1, TP. Hồ Chí Minh',
                source: 'default'
            };

            this._injectModalDOM();
        }

        /**
         * Đọc vị trí đã lưu trong phiên làm việc trước (nếu có)
         */
        _loadSavedLocation() {
            try {
                const raw = sessionStorage.getItem(LOCATION_STORAGE_KEY);
                return raw ? JSON.parse(raw) : null;
            } catch (_) {
                return null;
            }
        }

        /**
         * Lưu vị trí hiện hành vào sessionStorage để đồng bộ giữa các thao tác
         */
        _saveLocation(loc) {
            this.currentLocation = loc;
            try {
                sessionStorage.setItem(LOCATION_STORAGE_KEY, JSON.stringify(loc));
            } catch (_) {}
        }

        /**
         * Gọi navigator.geolocation để lấy vị trí GPS thực tế của trình duyệt.
         * Nếu người dùng từ chối (PERMISSION_DENIED) hoặc lỗi thiết bị, tự động mở Modal chọn Quận/Huyện (UC-03).
         * @param {boolean} showModalOnDeny Có bật Modal chọn thủ công khi bị từ chối GPS hay không
         */
        requestBrowserGPS(showModalOnDeny = true) {
            if (!navigator.geolocation) {
                this._updateStatusBanner(
                    'Trình duyệt của bạn không hỗ trợ định vị GPS. Vui lòng chọn Quận/Huyện hoặc kéo ghim trên bản đồ.',
                    'warning'
                );
                if (showModalOnDeny) this.openManualModal('Trình duyệt không hỗ trợ HTML5 Geolocation.');
                return;
            }

            this._setLocatingUIState(true);

            navigator.geolocation.getCurrentPosition(
                async (position) => {
                    this._setLocatingUIState(false);
                    const lat = Number(position.coords.latitude.toFixed(6));
                    const lng = Number(position.coords.longitude.toFixed(6));
                    const accuracy = Math.round(position.coords.accuracy || 50);

                    // Phân giải tọa độ sang địa chỉ đường phố tiếng Việt
                    const address = await this.reverseGeocode(lat, lng);

                    const resolved = {
                        lat,
                        lng,
                        accuracy,
                        address: address || `Vị trí GPS (${lat.toFixed(4)}, ${lng.toFixed(4)})`,
                        source: 'gps',
                        radiusKm: this.currentRadiusKm
                    };

                    this._saveLocation(resolved);
                    this.closeManualModal();

                    if (typeof this.onLocationResolved === 'function') {
                        this.onLocationResolved(resolved);
                    }
                },
                (error) => {
                    this._setLocatingUIState(false);
                    let errorReason = 'Không thể xác định vị trí GPS tự động.';

                    switch (error.code) {
                        case error.PERMISSION_DENIED:
                            errorReason = 'Bạn đã từ chối cấp quyền truy cập vị trí GPS. Hãy chọn Quận/Huyện bên dưới hoặc kéo thả ghim đỏ trên bản đồ.';
                            break;
                        case error.POSITION_UNAVAILABLE:
                            errorReason = 'Thiết bị không thu được tín hiệu định vị. Vui lòng chọn khu vực thủ công.';
                            break;
                        case error.TIMEOUT:
                            errorReason = 'Yêu cầu lấy vị trí GPS đã quá thời gian chờ (Timeout). Vui lòng chọn khu vực thủ công.';
                            break;
                    }

                    if (showModalOnDeny) {
                        this.openManualModal(errorReason);
                    }
                },
                {
                    enableHighAccuracy: true,
                    timeout: 8000,
                    maximumAge: 0
                }
            );
        }

        /**
         * Chuyển đổi tọa độ (lat, lng) thành tên đường/phường/quận tiếng Việt qua Nominatim OSM
         */
        async reverseGeocode(lat, lng) {
            try {
                const url = `https://nominatim.openstreetmap.org/reverse?format=json&lat=${lat}&lon=${lng}&zoom=18&addressdetails=1&accept-language=vi`;
                const res = await fetch(url, { headers: { 'Accept': 'application/json' } });
                if (!res.ok) return null;
                const data = await res.json();
                if (data && data.display_name) {
                    // Rút gọn chuỗi địa chỉ cho gọn đẹp trên thanh Topbar
                    const parts = data.display_name.split(',').map(s => s.trim());
                    return parts.slice(0, 4).join(', ');
                }
                return null;
            } catch (_) {
                return null;
            }
        }

        /**
         * Thiết lập vị trí thủ công khi người dùng chọn Quận/Huyện trong Modal hoặc kéo ghim trên bản đồ
         */
        async selectManualLocation({ lat, lng, address = null, source = 'manual_district' }) {
            const numLat = Number(parseFloat(lat).toFixed(6));
            const numLng = Number(parseFloat(lng).toFixed(6));
            if (Number.isNaN(numLat) || Number.isNaN(numLng)) return;

            let resolvedAddress = address;
            if (!resolvedAddress) {
                resolvedAddress = await this.reverseGeocode(numLat, numLng);
            }

            const resolved = {
                lat: numLat,
                lng: numLng,
                accuracy: 100,
                address: resolvedAddress || `Tọa độ (${numLat.toFixed(4)}, ${numLng.toFixed(4)})`,
                source,
                radiusKm: this.currentRadiusKm
            };

            this._saveLocation(resolved);
            this.closeManualModal();

            if (typeof this.onLocationResolved === 'function') {
                this.onLocationResolved(resolved);
            }
        }

        /**
         * Cập nhật bán kính tìm kiếm (1km, 3km, 5km, 10km)
         */
        setRadiusKm(radiusKm) {
            this.currentRadiusKm = Number(radiusKm) || 5;
            if (typeof this.onRadiusChanged === 'function') {
                this.onRadiusChanged(this.currentRadiusKm);
            }
        }

        /**
         * Mở Modal chọn Quận/Huyện hoặc nhập tọa độ thủ công (UC-03)
         */
        openManualModal(reasonMessage = '') {
            const modal = document.getElementById('uc03-location-modal');
            const alertBox = document.getElementById('uc03-gps-alert');
            if (!modal) return;

            if (alertBox) {
                if (reasonMessage) {
                    alertBox.textContent = reasonMessage;
                    alertBox.style.display = 'block';
                } else {
                    alertBox.style.display = 'none';
                }
            }

            // Điền tọa độ hiện tại vào 2 ô input tinh chỉnh
            const latInput = document.getElementById('uc03-manual-lat');
            const lngInput = document.getElementById('uc03-manual-lng');
            if (latInput) latInput.value = this.currentLocation.lat.toFixed(6);
            if (lngInput) lngInput.value = this.currentLocation.lng.toFixed(6);

            modal.classList.add('open');
        }

        /**
         * Đóng Modal chọn vị trí thủ công
         */
        closeManualModal() {
            const modal = document.getElementById('uc03-location-modal');
            if (modal) modal.classList.remove('open');
        }

        _setLocatingUIState(isLocating) {
            const pill = document.getElementById('current-address-label');
            if (pill && isLocating) {
                pill.textContent = 'Đang lấy vị trí GPS...';
            }
        }

        _updateStatusBanner(msg, type) {
            console.warn(`[LocationManager - ${type}] ${msg}`);
        }

        /**
         * Khởi tạo DOM cho Modal chọn vị trí thủ công (Quận/Huyện + Nhập tọa độ + Nút thử lại GPS)
         */
        _injectModalDOM() {
            if (document.getElementById('uc03-location-modal')) return;

            const modalBackdrop = document.createElement('div');
            modalBackdrop.id = 'uc03-location-modal';
            modalBackdrop.className = 'modal-backdrop';
            modalBackdrop.onclick = (e) => {
                if (e.target === modalBackdrop) this.closeManualModal();
            };

            const districtButtonsHtml = HCM_DISTRICTS.map(d => `
                <button type="button" class="uc03-district-btn" data-id="${d.id}"
                    onclick="window.smartDiningLocationManager.selectManualLocation({ lat: ${d.lat}, lng: ${d.lng}, address: '${d.address}', source: 'manual_district' })">
                    <strong>📍 ${d.name}</strong>
                    <small>${d.address}</small>
                </button>
            `).join('');

            modalBackdrop.innerHTML = `
                <div class="modal-card" style="width: 640px; max-width: 96vw;">
                    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px;padding-bottom:12px;border-bottom:1px solid var(--border);">
                        <div>
                            <h3 style="font-size:1.15rem;font-weight:700;color:var(--text-primary);">
                                📍 Chọn vị trí tìm kiếm quán ăn (UC-03)
                            </h3>
                            <p style="font-size:0.82rem;color:var(--text-muted);margin-top:2px;">
                                Định vị GPS tự động hoặc chọn nhanh Quận/Huyện tại TP. Hồ Chí Minh
                            </p>
                        </div>
                        <button type="button" onclick="window.smartDiningLocationManager.closeManualModal()"
                            style="background:none;border:none;font-size:1.3rem;cursor:pointer;color:var(--text-muted);">✕</button>
                    </div>

                    <div id="uc03-gps-alert" style="display:none;background:#fef2f2;border:1px solid #fecaca;color:#b91c1c;padding:10px 14px;border-radius:10px;font-size:0.83rem;margin-bottom:14px;line-height:1.45;"></div>

                    <div style="display:flex;gap:10px;margin-bottom:16px;flex-wrap:wrap;">
                        <button type="button" class="btn-ai-ask" style="height:40px;padding:0 18px;border-radius:10px;flex:1;justify-content:center;"
                            onclick="window.smartDiningLocationManager.requestBrowserGPS(false)">
                            🎯 Lấy vị trí GPS hiện tại của tôi
                        </button>
                        <button type="button" onclick="window.smartDiningLocationManager.closeManualModal()"
                            style="height:40px;padding:0 16px;border-radius:10px;border:1px solid var(--border);background:var(--bg-subtle);color:var(--text-primary);font-size:0.83rem;font-weight:600;cursor:pointer;">
                            ✋ Tự kéo ghim trực tiếp trên Bản đồ
                        </button>
                    </div>

                    <div style="margin-bottom:16px;">
                        <label style="display:block;font-size:0.8rem;font-weight:700;text-transform:uppercase;color:var(--text-muted);margin-bottom:8px;">
                            Hoặc chọn nhanh Quận / Huyện tại TP. Hồ Chí Minh:
                        </label>
                        <div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(180px,1fr));gap:8px;max-height:240px;overflow-y:auto;padding-right:4px;">
                            ${districtButtonsHtml}
                        </div>
                    </div>

                    <div style="padding-top:12px;border-top:1px solid var(--border);display:flex;align-items:flex-end;gap:10px;flex-wrap:wrap;">
                        <div style="flex:1;min-width:130px;">
                            <label style="font-size:0.76rem;color:var(--text-muted);font-weight:600;">Vĩ độ (Latitude)</label>
                            <input type="number" step="0.0001" id="uc03-manual-lat" style="width:100%;height:36px;padding:0 10px;border:1px solid var(--border);border-radius:8px;background:var(--bg-subtle);color:var(--text-primary);font-size:0.85rem;">
                        </div>
                        <div style="flex:1;min-width:130px;">
                            <label style="font-size:0.76rem;color:var(--text-muted);font-weight:600;">Kinh độ (Longitude)</label>
                            <input type="number" step="0.0001" id="uc03-manual-lng" style="width:100%;height:36px;padding:0 10px;border:1px solid var(--border);border-radius:8px;background:var(--bg-subtle);color:var(--text-primary);font-size:0.85rem;">
                        </div>
                        <button type="button" class="btn-ai-ask" style="height:36px;border-radius:8px;"
                            onclick="window.smartDiningLocationManager.selectManualLocation({ lat: document.getElementById('uc03-manual-lat').value, lng: document.getElementById('uc03-manual-lng').value, source: 'manual_coords' })">
                            Áp dụng tọa độ
                        </button>
                    </div>
                </div>
            `;

            // Bổ sung style cho các nút Quận/Huyện
            const style = document.createElement('style');
            style.textContent = `
                .uc03-district-btn {
                    display: flex; flex-direction: column; align-items: flex-start;
                    padding: 9px 12px; border-radius: 10px; border: 1px solid var(--border);
                    background: var(--bg-surface); color: var(--text-primary);
                    cursor: pointer; text-align: left; transition: all 0.15s ease;
                }
                .uc03-district-btn:hover {
                    border-color: var(--brand-red); background: #fff1f2; color: #be123c;
                }
                .uc03-district-btn strong { font-size: 0.84rem; margin-bottom: 2px; }
                .uc03-district-btn small { font-size: 0.72rem; color: var(--text-muted); line-height: 1.25; }
            `;
            document.head.appendChild(style);
            document.body.appendChild(modalBackdrop);
        }
    }

    global.LocationManager = LocationManager;
    global.HCM_DISTRICTS = HCM_DISTRICTS;
})(window);