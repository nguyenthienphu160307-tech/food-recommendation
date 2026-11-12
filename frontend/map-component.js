/**
 * ==============================================================================
 * MAP COMPONENT (Bản đồ số Web / Mobile)
 * Tích hợp Leaflet SDK + Google Maps Tiles (Streets & Satellite) + OpenStreetMap
 * Hỗ trợ điều khiển Zoom, Định tâm mặc định, Định vị GPS và Tương tác đa nền tảng
 * ==============================================================================
 */

class FoodAIMapComponent {
    /**
     * @param {Object} options Cấu hình khởi tạo bản đồ
     * @param {string} options.containerId ID thẻ chứa bản đồ (mặc định 'main-map')
     * @param {Array<number>} options.defaultCenter Tọa độ trung tâm mặc định [lat, lng] (mặc định TP.HCM Q1 [10.776889, 106.700806])
     * @param {number} options.defaultZoom Mức zoom mặc định (mặc định 13)
     * @param {number} options.minZoom Mức zoom nhỏ nhất (mặc định 5)
     * @param {number} options.maxZoom Mức zoom lớn nhất (mặc định 20)
     * @param {Function} options.onLocationChange Callback khi đổi vị trí ghim cá nhân: fn({ lat, lng })
     * @param {Function} options.onVenueClick Callback khi bấm vào marker nhà hàng: fn(venue)
     */
    constructor(options = {}) {
        this.containerId = options.containerId || 'main-map';
        this.defaultCenter = options.defaultCenter || [10.776889, 106.700806]; // Mặc định TP.HCM (Quận 1)
        this.currentCenter = options.currentCenter || [...this.defaultCenter];
        this.defaultZoom = options.defaultZoom || 13;
        this.minZoom = options.minZoom || 5;
        this.maxZoom = options.maxZoom || 20;

        this.onLocationChange = options.onLocationChange || null;
        this.onVenueClick = options.onVenueClick || null;

        // Trạng thái nội bộ
        this.map = null;
        this.baseLayers = {};
        this.activeLayerName = 'googleStreets';
        this.userMarker = null;
        this.accuracyCircle = null;
        this.venueMarkers = new Map(); // id -> L.Marker
        this.isLocating = false;

        this.init();
    }

    /**
     * Khởi tạo bản đồ Leaflet, các lớp bản đồ nền và các bộ điều khiển
     */
    init() {
        const container = document.getElementById(this.containerId);
        if (!container) {
            console.error(`[MapComponent] Không tìm thấy phần tử HTML với ID: #${this.containerId}`);
            return;
        }

        // 1. Khởi tạo Leaflet Map instance
        this.map = L.map(this.containerId, {
            center: this.currentCenter,
            zoom: this.defaultZoom,
            minZoom: this.minZoom,
            maxZoom: this.maxZoom,
            zoomControl: false, // Tắt zoom control mặc định để dùng custom UI đẹp mắt
            attributionControl: true,
            tap: true, // Tối ưu cảm ứng mobile
            touchZoom: true,
            scrollWheelZoom: true
        });

        // 2. Cấu hình các lớp bản đồ nền (Tile Layers)
        this._setupBaseLayers();

        // 3. Khởi tạo Ghim vị trí người dùng (User Location Marker)
        this._initUserMarker();

        // 4. Khởi tạo Bộ điều khiển giao diện (Zoom, Re-center, GPS, Layer Switcher, Scale)
        this._setupCustomControls();

        // 5. Lắng nghe sự kiện click trên bản đồ để cập nhật vị trí tìm kiếm
        this.map.on('click', (e) => {
            this.setUserPosition(e.latlng.lat, e.latlng.lng, true);
        });

        // Tự động điều chỉnh kích thước khi cửa sổ thay đổi
        window.addEventListener('resize', () => {
            this.invalidateSize();
        });

        console.log('[MapComponent] Đã khởi tạo Bản đồ số thành công tại tọa độ:', this.currentCenter);
    }

    /**
     * Cấu hình các lớp bản đồ nền:
     * - Google Maps Streets (Đường phố tiếng Việt)
     * - Google Maps Satellite / Hybrid (Vệ tinh có gắn nhãn)
     * - OpenStreetMap (Bản đồ mở quốc tế)
     */
    _setupBaseLayers() {
        // Google Maps Đường phố
        this.baseLayers['googleStreets'] = L.tileLayer(
            'https://{s}.google.com/vt/lyrs=m&x={x}&y={y}&z={z}&hl=vi',
            {
                maxZoom: this.maxZoom,
                subdomains: ['mt0', 'mt1', 'mt2', 'mt3'],
                attribution: '&copy; Google Maps'
            }
        );

        // Google Maps Vệ tinh (Hybrid)
        this.baseLayers['googleHybrid'] = L.tileLayer(
            'https://{s}.google.com/vt/lyrs=s,h&x={x}&y={y}&z={z}&hl=vi',
            {
                maxZoom: this.maxZoom,
                subdomains: ['mt0', 'mt1', 'mt2', 'mt3'],
                attribution: '&copy; Google Maps Satellite'
            }
        );

        // OpenStreetMap Standard
        this.baseLayers['osm'] = L.tileLayer(
            'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
            {
                maxZoom: 19,
                attribution: '&copy; OpenStreetMap contributors'
            }
        );

        // Mặc định nạp Google Streets
        this.baseLayers['googleStreets'].addTo(this.map);
    }

    /**
     * Chuyển đổi lớp bản đồ nền
     * @param {'googleStreets' | 'googleHybrid' | 'osm'} layerKey 
     */
    switchBaseLayer(layerKey) {
        if (!this.baseLayers[layerKey] || layerKey === this.activeLayerName) return;

        // Gỡ lớp cũ
        if (this.baseLayers[this.activeLayerName]) {
            this.map.removeLayer(this.baseLayers[this.activeLayerName]);
        }

        // Thêm lớp mới
        this.baseLayers[layerKey].addTo(this.map);
        this.activeLayerName = layerKey;

        // Cập nhật trạng thái active trên UI switcher (nếu có)
        const buttons = document.querySelectorAll('.map-layer-btn');
        buttons.forEach(btn => {
            if (btn.dataset.layer === layerKey) {
                btn.classList.add('active');
            } else {
                btn.classList.remove('active');
            }
        });
    }

    /**
     * Khởi tạo marker vị trí của người dùng với hiệu ứng radar pulsing
     */
    _initUserMarker() {
        const userIcon = L.divIcon({
            className: 'user-marker-container',
            html: `
                <div class="user-pulse-ring"></div>
                <div class="user-center-dot"></div>
            `,
            iconSize: [28, 28],
            iconAnchor: [14, 14],
            popupAnchor: [0, -16]
        });

        this.userMarker = L.marker(this.currentCenter, {
            icon: userIcon,
            draggable: true,
            zIndexOffset: 1000
        }).addTo(this.map);

        this.userMarker.bindPopup(`
            <div style="font-size:0.85rem;line-height:1.4;">
                <strong style="color:#e11d48;display:flex;align-items:center;gap:4px;">
                    📍 Vị trí tìm kiếm của bạn
                </strong>
                <p style="margin:4px 0 0;color:#6b7280;font-size:0.78rem;">
                    Kéo thả ghim hoặc nhấp vào bất kỳ đâu trên bản đồ để đổi vị trí.
                </p>
            </div>
        `);

        // Lắng nghe khi kéo thả xong ghim vị trí
        this.userMarker.on('dragend', (e) => {
            const pos = e.target.getLatLng();
            this.setUserPosition(pos.lat, pos.lng, true);
        });
    }

    /**
     * Cài đặt các nút điều khiển tiện ích: Zoom In/Out, Re-center, GPS Locate, Layer switcher, Scale
     */
    _setupCustomControls() {
        // Thước đo tỷ lệ (Scale Control) ở góc dưới bên trái
        L.control.scale({
            imperial: false,
            metric: true,
            position: 'bottomleft'
        }).addTo(this.map);

        // Tạo Custom Control chứa các nút hành động (Góc trên bên phải)
        const ActionsControl = L.Control.extend({
            options: { position: 'topright' },
            onAdd: (map) => {
                const container = L.DomUtil.create('div', 'custom-map-controls leaflet-bar');
                // Ngăn chặn sự kiện click/scroll lan ra bản đồ
                L.DomEvent.disableClickPropagation(container);
                L.DomEvent.disableScrollPropagation(container);

                container.innerHTML = `
                    <div class="map-ctrl-group">
                        <button type="button" class="map-ctrl-btn" id="map-btn-zoom-in" title="Phóng to (+)">
                            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                                <line x1="12" y1="5" x2="12" y2="19"></line>
                                <line x1="5" y1="12" x2="19" y2="12"></line>
                            </svg>
                        </button>
                        <button type="button" class="map-ctrl-btn" id="map-btn-zoom-out" title="Thu nhỏ (-)">
                            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                                <line x1="5" y1="12" x2="19" y2="12"></line>
                            </svg>
                        </button>
                    </div>

                    <div class="map-ctrl-group" style="margin-top: 8px;">
                        <button type="button" class="map-ctrl-btn" id="map-btn-locate" title="Định vị vị trí của tôi (GPS)">
                            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                <path d="M12 2v3m0 14v3M2 12h3m14 0h3"></path>
                                <circle cx="12" cy="12" r="7"></circle>
                                <circle cx="12" cy="12" r="3" fill="currentColor"></circle>
                            </svg>
                        </button>
                        <button type="button" class="map-ctrl-btn" id="map-btn-recenter" title="Định tâm về tọa độ mặc định">
                            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                <circle cx="12" cy="12" r="10"></circle>
                                <polygon points="16.24 7.76 14.12 14.12 7.76 16.24 9.88 9.88 16.24 7.76" fill="currentColor"></polygon>
                            </svg>
                        </button>
                    </div>

                    <div class="map-ctrl-group map-layer-switcher" style="margin-top: 8px;">
                        <button type="button" class="map-ctrl-btn map-layer-toggle" id="map-btn-layers" title="Đổi lớp bản đồ nền">
                            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                <polygon points="12 2 2 7 12 12 22 7 12 2"></polygon>
                                <polyline points="2 17 12 22 22 17"></polyline>
                                <polyline points="2 12 12 17 22 12"></polyline>
                            </svg>
                        </button>
                        <div class="map-layer-menu" id="map-layer-menu">
                            <button type="button" class="map-layer-btn active" data-layer="googleStreets">
                                🗺️ Bản đồ Đường phố
                            </button>
                            <button type="button" class="map-layer-btn" data-layer="googleHybrid">
                                🛰️ Vệ tinh Google
                            </button>
                            <button type="button" class="map-layer-btn" data-layer="osm">
                                🌐 OpenStreetMap
                            </button>
                        </div>
                    </div>
                `;
                return container;
            }
        });

        this.map.addControl(new ActionsControl());

        // Gắn sự kiện cho các nút điều khiển
        setTimeout(() => {
            const btnZoomIn = document.getElementById('map-btn-zoom-in');
            const btnZoomOut = document.getElementById('map-btn-zoom-out');
            const btnLocate = document.getElementById('map-btn-locate');
            const btnRecenter = document.getElementById('map-btn-recenter');
            const btnLayers = document.getElementById('map-btn-layers');
            const layerMenu = document.getElementById('map-layer-menu');

            if (btnZoomIn) btnZoomIn.onclick = () => this.zoomIn();
            if (btnZoomOut) btnZoomOut.onclick = () => this.zoomOut();
            if (btnLocate) btnLocate.onclick = () => this.locateUser();
            if (btnRecenter) btnRecenter.onclick = () => this.centerToDefault();

            if (btnLayers && layerMenu) {
                btnLayers.onclick = (e) => {
                    e.stopPropagation();
                    layerMenu.classList.toggle('open');
                };

                // Đóng menu khi bấm ra ngoài
                document.addEventListener('click', (e) => {
                    if (!layerMenu.contains(e.target) && e.target !== btnLayers) {
                        layerMenu.classList.remove('open');
                    }
                });

                layerMenu.querySelectorAll('.map-layer-btn').forEach(btn => {
                    btn.onclick = () => {
                        const l = btn.dataset.layer;
                        this.switchBaseLayer(l);
                        layerMenu.classList.remove('open');
                    };
                });
            }
        }, 50);
    }

    /**
     * Phóng to bản đồ
     */
    zoomIn() {
        if (this.map) this.map.zoomIn();
    }

    /**
     * Thu nhỏ bản đồ
     */
    zoomOut() {
        if (this.map) this.map.zoomOut();
    }

    /**
     * Định tâm bản đồ về tọa độ mặc định ban đầu (TP.HCM Q1)
     */
    centerToDefault() {
        if (!this.map) return;
        this.setUserPosition(this.defaultCenter[0], this.defaultCenter[1], true);
        this.map.flyTo(this.defaultCenter, this.defaultZoom, {
            duration: 1.0,
            easeLinearity: 0.25
        });
        this.showToast('Đã định tâm về tọa độ mặc định (TP.HCM)', 'info');
    }

    /**
     * Cập nhật vị trí của người dùng
     * @param {number} lat Vĩ độ
     * @param {number} lng Kinh độ
     * @param {boolean} triggerCallback Kích hoạt callback onLocationChange
     */
    setUserPosition(lat, lng, triggerCallback = true) {
        this.currentCenter = [lat, lng];
        if (this.userMarker) {
            this.userMarker.setLatLng(this.currentCenter);
        }

        if (triggerCallback && typeof this.onLocationChange === 'function') {
            this.onLocationChange({ lat, lng });
        }
    }

    /**
     * Định vị vị trí hiện tại của người dùng qua HTML5 Geolocation API
     */
    locateUser() {
        if (!navigator.geolocation) {
            this.showToast('Trình duyệt của bạn không hỗ trợ định vị GPS.', 'warning');
            return;
        }

        const locateBtn = document.getElementById('map-btn-locate');
        if (locateBtn) locateBtn.classList.add('locating');

        this.showToast('Đang tìm kiếm vị trí GPS của bạn...', 'info');

        navigator.geolocation.getCurrentPosition(
            (position) => {
                if (locateBtn) locateBtn.classList.remove('locating');
                const lat = position.coords.latitude;
                const lng = position.coords.longitude;
                const accuracy = position.coords.accuracy;

                // Xóa vòng tròn độ chính xác cũ nếu có
                if (this.accuracyCircle) {
                    this.map.removeLayer(this.accuracyCircle);
                }

                // Vẽ vòng tròn độ chính xác bán kính GPS
                this.accuracyCircle = L.circle([lat, lng], {
                    radius: accuracy,
                    color: '#e11d48',
                    fillColor: '#e11d48',
                    fillOpacity: 0.12,
                    weight: 1
                }).addTo(this.map);

                // Cập nhật vị trí ghim và bay mượt đến vị trí đó
                this.setUserPosition(lat, lng, true);
                this.map.flyTo([lat, lng], 15, {
                    duration: 1.2
                });

                this.showToast(`Đã định vị thành công (Độ chính xác: ~${Math.round(accuracy)}m)`, 'success');
            },
            (error) => {
                if (locateBtn) locateBtn.classList.remove('locating');
                let msg = 'Không thể lấy vị trí GPS hiện tại.';
                if (error.code === error.PERMISSION_DENIED) {
                    msg = 'Quyền truy cập vị trí bị từ chối. Vui lòng cho phép quyền GPS trên trình duyệt.';
                } else if (error.code === error.TIMEOUT) {
                    msg = 'Yêu cầu định vị GPS hết thời gian chờ.';
                }
                this.showToast(msg, 'warning');
            },
            {
                enableHighAccuracy: true,
                timeout: 10000,
                maximumAge: 30000
            }
        );
    }

    /**
     * Hiển thị danh sách các quán ăn lên bản đồ dưới dạng Marker
     * @param {Array<Object>} venues Danh sách quán ăn
     */
    setVenueMarkers(venues = []) {
        if (!this.map) return;

        // Xóa các marker cũ
        this.venueMarkers.forEach((marker) => {
            this.map.removeLayer(marker);
        });
        this.venueMarkers.clear();

        // Icon marker quán ăn chuẩn
        const createVenueIcon = (rating, category) => {
            let catEmoji = '🍽️';
            if (category === 'bbq') catEmoji = '🥩';
            else if (category === 'hotpot') catEmoji = '🍲';
            else if (category === 'cafe') catEmoji = '☕';
            else if (category === 'vegetarian') catEmoji = '🥗';
            else if (category === 'western') catEmoji = '🍕';

            return L.divIcon({
                className: 'venue-marker-pin',
                html: `
                    <div class="pin-bubble">
                        <span class="pin-emoji">${catEmoji}</span>
                        <span class="pin-rating">★${rating}</span>
                    </div>
                    <div class="pin-arrow"></div>
                `,
                iconSize: [44, 46],
                iconAnchor: [22, 44],
                popupAnchor: [0, -42]
            });
        };

        venues.forEach((v) => {
            if (!v.lat || !v.lng) return;

            const icon = createVenueIcon(v.rating, v.category);
            const marker = L.marker([v.lat, v.lng], { icon }).addTo(this.map);

            const travelMins = Math.max(3, Math.round((v.distanceKm || 1) * 3.2));
            const popupContent = `
                <div class="map-venue-popup">
                    <div class="popup-img-wrap">
                        <img src="${v.image}" alt="${v.name}" loading="lazy">
                        <span class="popup-rating">★ ${v.rating}</span>
                    </div>
                    <div class="popup-body">
                        <h4 class="popup-title">${v.name}</h4>
                        <div class="popup-meta">
                            <span>📍 ${v.cuisineLabel || 'Ẩm thực'}</span>
                            <span>•</span>
                            <strong style="color:#e11d48;">${(v.distanceKm || 0).toFixed(1)} km</strong> (~${travelMins}p)
                        </div>
                        <div class="popup-address">${v.address}</div>
                        <div class="popup-footer">
                            <span class="popup-price">${(v.priceMin || 0).toLocaleString()}đ - ${(v.priceMax || 0).toLocaleString()}đ</span>
                            <button type="button" class="popup-btn-detail" onclick="window.onMapPopupSelectVenue(${v.id})">
                                Chi tiết →
                            </button>
                        </div>
                    </div>
                </div>
            `;

            marker.bindPopup(popupContent, {
                maxWidth: 290,
                minWidth: 260,
                className: 'custom-venue-popup-wrapper'
            });

            marker.on('click', () => {
                if (typeof this.onVenueClick === 'function') {
                    this.onVenueClick(v);
                }
            });

            this.venueMarkers.set(v.id, marker);
        });
    }

    /**
     * Di chuyển bản đồ và mở popup của quán ăn tương ứng
     * @param {number|string} venueId ID quán ăn
     */
    focusVenue(venueId) {
        const marker = this.venueMarkers.get(venueId);
        if (marker) {
            const latlng = marker.getLatLng();
            this.map.flyTo(latlng, Math.max(this.map.getZoom(), 15), {
                duration: 0.8
            });
            setTimeout(() => {
                marker.openPopup();
            }, 600);
        }
    }

    /**
     * Kích hoạt vẽ lại bản đồ khi thay đổi kích thước container hoặc chuyển tab trên mobile
     */
    invalidateSize() {
        if (this.map) {
            setTimeout(() => {
                this.map.invalidateSize();
            }, 150);
        }
    }

    /**
     * Hiển thị thông báo Toast nhỏ trên màn hình
     */
    showToast(message, type = 'info') {
        let toastContainer = document.getElementById('map-toast-container');
        if (!toastContainer) {
            toastContainer = document.createElement('div');
            toastContainer.id = 'map-toast-container';
            toastContainer.className = 'map-toast-container';
            document.body.appendChild(toastContainer);
        }

        const toast = document.createElement('div');
        toast.className = `map-toast-item toast-${type}`;
        toast.innerHTML = `
            <span>${message}</span>
        `;
        toastContainer.appendChild(toast);

        setTimeout(() => {
            toast.classList.add('fade-out');
            setTimeout(() => toast.remove(), 400);
        }, 3000);
    }
}

// Xuất ra phạm vi toàn cục để dùng trực tiếp trong file HTML
window.FoodAIMapComponent = FoodAIMapComponent;
