/**
 * ==============================================================================
 * MAP COMPONENT (Bản đồ số Web / Mobile)
 * Tích hợp Leaflet SDK + Google Maps Tiles (Streets & Satellite) + OpenStreetMap
 * Hỗ trợ:
 * - Điều khiển Zoom, Định tâm mặc định, Định vị GPS
 * - Vẽ vòng tròn bán kính tìm kiếm (1km, 3km, 5km, 10km)
 * - Hiển thị Marker nhà hàng kèm khoảng cách chính xác & Popup thông tin chi tiết
 * - Đồng bộ 2 chiều với danh sách quán (khi cuộn danh sách, hover hoặc click)
 * ==============================================================================
 */

class FoodAIMapComponent {
    /**
     * @param {Object} options Cấu hình khởi tạo bản đồ
     * @param {string} options.containerId ID thẻ chứa bản đồ (mặc định 'main-map')
     * @param {Array<number>} options.defaultCenter Tọa độ trung tâm mặc định [lat, lng]
     * @param {Array<number>} options.currentCenter Tọa độ hiện tại [lat, lng]
     * @param {number} options.defaultZoom Mức zoom mặc định (mặc định 13)
     * @param {number} options.minZoom Mức zoom nhỏ nhất (mặc định 5)
     * @param {number} options.maxZoom Mức zoom lớn nhất (mặc định 20)
     * @param {number} options.defaultRadiusKm Bán kính tìm kiếm mặc định (1, 3, 5, 10 km; mặc định 5)
     * @param {Array<number>} options.radiusOptions Danh sách mốc bán kính (mặc định [1, 3, 5, 10])
     * @param {Function} options.onLocationChange Callback khi đổi vị trí ghim cá nhân: fn({ lat, lng })
     * @param {Function} options.onRadiusChange Callback khi đổi bán kính tìm kiếm: fn(radiusKm)
     * @param {Function} options.onVenueClick Callback khi bấm vào marker nhà hàng: fn(venue)
     */
    constructor(options = {}) {
        this.containerId = options.containerId || 'main-map';
        this.defaultCenter = options.defaultCenter || [10.776889, 106.700806];
        this.currentCenter = options.currentCenter || [...this.defaultCenter];
        this.defaultZoom = options.defaultZoom || 13;
        this.minZoom = options.minZoom || 5;
        this.maxZoom = options.maxZoom || 20;

        this.searchRadiusKm = options.defaultRadiusKm !== undefined ? options.defaultRadiusKm : 5;
        this.radiusOptions = options.radiusOptions || [1, 3, 5, 10];

        this.onLocationChange = options.onLocationChange || null;
        this.onRadiusChange = options.onRadiusChange || null;
        this.onVenueClick = options.onVenueClick || null;

        // Trạng thái nội bộ
        this.map = null;
        this.baseLayers = {};
        this.activeLayerName = 'googleStreets';
        this.userMarker = null;
        this.accuracyCircle = null;
        this.radiusCircle = null;
        this.radiusLabelMarker = null;
        this.venueMarkers = new Map(); // id -> L.Marker
        this.venueDataMap = new Map(); // id -> venue
        this.activeVenueId = null;
        this.isLocating = false;

        this.init();
    }

    /**
     * Tính khoảng cách đường chim bay chính xác (km) bằng công thức Haversine
     */
    static calcDistanceKm(lat1, lng1, lat2, lng2) {
        const R = 6371.0;
        const dLat = (lat2 - lat1) * Math.PI / 180;
        const dLng = (lng2 - lng1) * Math.PI / 180;
        const a = Math.sin(dLat / 2) ** 2 +
            Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) *
            Math.sin(dLng / 2) ** 2;
        return R * 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
    }

    /**
     * Định dạng khoảng cách gọn trên ghim bản đồ (VD: 650m hoặc 2.4km)
     */
    static formatPinDistance(km) {
        if (km === undefined || km === null || isNaN(km)) return '';
        if (km < 1) return `${Math.max(10, Math.round(km * 1000))}m`;
        return `${km.toFixed(1)}km`;
    }

    /**
     * Khởi tạo bản đồ Leaflet, các lớp bản đồ nền, vòng tròn bán kính và bộ điều khiển
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
            zoomControl: false,
            attributionControl: true,
            tap: true,
            touchZoom: true,
            scrollWheelZoom: true
        });

        // 2. Cấu hình các lớp bản đồ nền (Tile Layers)
        this._setupBaseLayers();

        // 3. Khởi tạo Ghim vị trí người dùng (User Location Marker)
        this._initUserMarker();

        // 4. Vẽ vòng tròn bán kính tìm kiếm ban đầu
        this.drawRadiusCircle(false);

        // 5. Khởi tạo Bộ điều khiển giao diện (Bán kính, Zoom, Re-center, GPS, Layer Switcher, Scale)
        this._setupRadiusControl();
        this._setupCustomControls();

        // 6. Lắng nghe sự kiện click trên bản đồ để cập nhật vị trí tìm kiếm
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
     * Cấu hình các lớp bản đồ nền: Google Streets, Google Hybrid, OpenStreetMap
     */
    _setupBaseLayers() {
        this.baseLayers['googleStreets'] = L.tileLayer(
            'https://{s}.google.com/vt/lyrs=m&x={x}&y={y}&z={z}&hl=vi',
            {
                maxZoom: this.maxZoom,
                subdomains: ['mt0', 'mt1', 'mt2', 'mt3'],
                attribution: '&copy; Google Maps'
            }
        );

        this.baseLayers['googleHybrid'] = L.tileLayer(
            'https://{s}.google.com/vt/lyrs=s,h&x={x}&y={y}&z={z}&hl=vi',
            {
                maxZoom: this.maxZoom,
                subdomains: ['mt0', 'mt1', 'mt2', 'mt3'],
                attribution: '&copy; Google Maps Satellite'
            }
        );

        this.baseLayers['osm'] = L.tileLayer(
            'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
            {
                maxZoom: 19,
                attribution: '&copy; OpenStreetMap contributors'
            }
        );

        this.baseLayers['googleStreets'].addTo(this.map);
    }

    /**
     * Chuyển đổi lớp bản đồ nền
     * @param {'googleStreets' | 'googleHybrid' | 'osm'} layerKey
     */
    switchBaseLayer(layerKey) {
        if (!this.baseLayers[layerKey] || layerKey === this.activeLayerName) return;

        if (this.baseLayers[this.activeLayerName]) {
            this.map.removeLayer(this.baseLayers[this.activeLayerName]);
        }

        this.baseLayers[layerKey].addTo(this.map);
        this.activeLayerName = layerKey;

        const buttons = document.querySelectorAll('.map-layer-btn');
        buttons.forEach(btn => {
            btn.classList.toggle('active', btn.dataset.layer === layerKey);
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
                    Kéo thả ghim hoặc nhấp vào bản đồ để đổi tâm vòng tròn bán kính.
                </p>
            </div>
        `);

        this.userMarker.on('dragend', (e) => {
            const pos = e.target.getLatLng();
            this.setUserPosition(pos.lat, pos.lng, true);
        });
    }

    /**
     * Bộ điều khiển chọn nhanh bán kính (1km, 3km, 5km, 10km) ở góc trên bên trái bản đồ
     */
    _setupRadiusControl() {
        const RadiusControl = L.Control.extend({
            options: { position: 'topleft' },
            onAdd: () => {
                const container = L.DomUtil.create('div', 'map-radius-control leaflet-bar');
                L.DomEvent.disableClickPropagation(container);
                L.DomEvent.disableScrollPropagation(container);

                const buttonsHtml = this.radiusOptions.map(km => `
                    <button type="button"
                            class="radius-pill-btn ${this.searchRadiusKm === km ? 'active' : ''}"
                            data-radius="${km}">
                        ${km} km
                    </button>
                `).join('');

                container.innerHTML = `
                    <div class="map-radius-header">
                        <span>🎯 Bán kính tìm kiếm</span>
                        <span class="map-radius-count" id="map-radius-venue-count">0 quán</span>
                    </div>
                    <div class="map-radius-pills" id="map-radius-pills">
                        ${buttonsHtml}
                    </div>
                `;

                container.querySelectorAll('.radius-pill-btn').forEach(btn => {
                    btn.addEventListener('click', () => {
                        const km = parseFloat(btn.dataset.radius);
                        this.setSearchRadius(km, true, true);
                    });
                });

                return container;
            }
        });

        this.map.addControl(new RadiusControl());
    }

    /**
     * Vẽ hoặc cập nhật vòng tròn bán kính tìm kiếm quanh tâm hiện tại
     * @param {boolean} fitBounds Tự động căn chỉnh khung nhìn vừa khít vòng tròn
     */
    drawRadiusCircle(fitBounds = false) {
        if (!this.map) return;

        if (this.radiusCircle) {
            this.map.removeLayer(this.radiusCircle);
            this.radiusCircle = null;
        }
        if (this.radiusLabelMarker) {
            this.map.removeLayer(this.radiusLabelMarker);
            this.radiusLabelMarker = null;
        }

        if (!this.searchRadiusKm || this.searchRadiusKm <= 0) return;

        const [lat, lng] = this.currentCenter;
        const radiusMeters = this.searchRadiusKm * 1000;

        // Vẽ vòng tròn bán kính tìm kiếm
        this.radiusCircle = L.circle([lat, lng], {
            radius: radiusMeters,
            color: '#e11d48',
            weight: 2,
            opacity: 0.8,
            dashArray: '6, 6',
            fillColor: '#e11d48',
            fillOpacity: 0.08,
            interactive: false
        }).addTo(this.map);

        // Gắn nhãn bán kính ngay mép trên vòng tròn (1 độ vĩ độ ~ 111.32 km)
        const northEdgeLat = lat + (this.searchRadiusKm / 111.32);
        this.radiusLabelMarker = L.marker([northEdgeLat, lng], {
            interactive: false,
            opacity: 0,
            icon: L.divIcon({ className: '', iconSize: [0, 0] })
        }).addTo(this.map);

        this.radiusLabelMarker.bindTooltip(`Bán kính ${this.searchRadiusKm} km`, {
            permanent: true,
            direction: 'center',
            className: 'radius-circle-label'
        }).openTooltip();

        if (fitBounds && this.radiusCircle) {
            this.map.fitBounds(this.radiusCircle.getBounds(), {
                padding: [30, 30],
                maxZoom: 16,
                animate: true
            });
        }
    }

    /**
     * Thay đổi bán kính tìm kiếm (1km, 3km, 5km, 10km)
     * @param {number} radiusKm Bán kính mới (km)
     * @param {boolean} fitBounds Căn chỉnh zoom vừa với vòng tròn
     * @param {boolean} triggerCallback Kích hoạt callback onRadiusChange
     */
    setSearchRadius(radiusKm, fitBounds = true, triggerCallback = true) {
        this.searchRadiusKm = radiusKm;

        // Đồng bộ trạng thái active trên các nút bán kính của bản đồ
        document.querySelectorAll('.radius-pill-btn').forEach(btn => {
            btn.classList.toggle('active', parseFloat(btn.dataset.radius) === radiusKm);
        });

        this.drawRadiusCircle(fitBounds);

        if (triggerCallback && typeof this.onRadiusChange === 'function') {
            this.onRadiusChange(radiusKm);
        }
    }

    /**
     * Cập nhật bộ đếm số lượng nhà hàng đang hiển thị trong vòng tròn bán kính
     */
    updateRadiusCount(count) {
        const badge = document.getElementById('map-radius-venue-count');
        if (badge) {
            badge.innerText = `${count} quán`;
        }
    }

    /**
     * Cài đặt các nút điều khiển tiện ích: Zoom In/Out, Re-center, GPS Locate, Layer switcher, Scale
     */
    _setupCustomControls() {
        L.control.scale({
            imperial: false,
            metric: true,
            position: 'bottomleft'
        }).addTo(this.map);

        const ActionsControl = L.Control.extend({
            options: { position: 'topright' },
            onAdd: () => {
                const container = L.DomUtil.create('div', 'custom-map-controls leaflet-bar');
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

    zoomIn() {
        if (this.map) this.map.zoomIn();
    }

    zoomOut() {
        if (this.map) this.map.zoomOut();
    }

    /**
     * Định tâm bản đồ về tọa độ mặc định ban đầu
     */
    centerToDefault() {
        if (!this.map) return;
        this.setUserPosition(this.defaultCenter[0], this.defaultCenter[1], true);
        if (this.radiusCircle) {
            this.map.fitBounds(this.radiusCircle.getBounds(), { padding: [30, 30], maxZoom: 15, animate: true });
        } else {
            this.map.flyTo(this.defaultCenter, this.defaultZoom, { duration: 1.0, easeLinearity: 0.25 });
        }
        this.showToast('Đã định tâm về tọa độ mặc định (TP.HCM)', 'info');
    }

    /**
     * Cập nhật vị trí tâm tìm kiếm của người dùng và di chuyển vòng tròn bán kính
     */
    setUserPosition(lat, lng, triggerCallback = true) {
        this.currentCenter = [lat, lng];
        if (this.userMarker) {
            this.userMarker.setLatLng(this.currentCenter);
        }

        // Di chuyển vòng tròn bán kính theo vị trí mới
        this.drawRadiusCircle(false);

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

                if (this.accuracyCircle) {
                    this.map.removeLayer(this.accuracyCircle);
                }

                this.accuracyCircle = L.circle([lat, lng], {
                    radius: accuracy,
                    color: '#3b82f6',
                    fillColor: '#3b82f6',
                    fillOpacity: 0.12,
                    weight: 1,
                    interactive: false
                }).addTo(this.map);

                this.setUserPosition(lat, lng, true);
                if (this.radiusCircle) {
                    this.map.fitBounds(this.radiusCircle.getBounds(), { padding: [30, 30], maxZoom: 16, animate: true });
                } else {
                    this.map.flyTo([lat, lng], 15, { duration: 1.2 });
                }

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
     * Hiển thị danh sách các quán ăn lên bản đồ dưới dạng Marker kèm khoảng cách chính xác & Popup chi tiết
     * @param {Array<Object>} venues Danh sách quán ăn
     */
    setVenueMarkers(venues = []) {
        if (!this.map) return;

        // Xóa các marker cũ
        this.venueMarkers.forEach((marker) => {
            this.map.removeLayer(marker);
        });
        this.venueMarkers.clear();
        this.venueDataMap.clear();

        // Icon marker quán ăn kèm khoảng cách chính xác
        const createVenueIcon = (venue, distKm, isActive = false) => {
            const cat = (venue.category || '').toLowerCase();
            const cuisine = (venue.cuisineLabel || '').toLowerCase();
            let catEmoji = '🍽️';
            if (cat.includes('bbq') || cuisine.includes('nướng')) catEmoji = '🥩';
            else if (cat.includes('hotpot') || cuisine.includes('lẩu')) catEmoji = '🍲';
            else if (cat.includes('cafe') || cuisine.includes('cà phê')) catEmoji = '☕';
            else if (cat.includes('vegan') || cat.includes('chay') || cuisine.includes('chay')) catEmoji = '🥗';
            else if (cat.includes('western') || cuisine.includes('âu')) catEmoji = '🍕';
            else if (cat.includes('seafood') || cuisine.includes('hải sản')) catEmoji = '🦐';
            else if (cat.includes('japanese') || cuisine.includes('nhật')) catEmoji = '🍣';

            const distLabel = FoodAIMapComponent.formatPinDistance(distKm);
            const ratingVal = Number(venue.rating || 4.5).toFixed(1);

            return L.divIcon({
                className: `venue-marker-pin${isActive ? ' active-pin' : ''}`,
                html: `
                    <div class="pin-bubble" data-venue-id="${venue.id}">
                        <span class="pin-emoji">${catEmoji}</span>
                        <span class="pin-rating">★${ratingVal}</span>
                        ${distLabel ? `<span class="pin-dist">${distLabel}</span>` : ''}
                    </div>
                    <div class="pin-arrow"></div>
                `,
                iconSize: [96, 46],
                iconAnchor: [48, 44],
                popupAnchor: [0, -42]
            });
        };

        venues.forEach((v) => {
            const lat = parseFloat(v.lat !== undefined ? v.lat : v.latitude);
            const lng = parseFloat(v.lng !== undefined ? v.lng : v.longitude);
            if (isNaN(lat) || isNaN(lng)) return;

            // Tính khoảng cách chính xác theo vị trí tâm hiện tại
            const distKm = (v.distanceKm !== undefined)
                ? v.distanceKm
                : (v.distance_km !== undefined
                    ? v.distance_km
                    : FoodAIMapComponent.calcDistanceKm(this.currentCenter[0], this.currentCenter[1], lat, lng));

            const isActive = this.activeVenueId === v.id;
            const icon = createVenueIcon(v, distKm, isActive);
            const marker = L.marker([lat, lng], {
                icon,
                zIndexOffset: isActive ? 850 : 0
            }).addTo(this.map);

            const travelMins = Math.max(2, Math.round(distKm * 3.2));
            const exactDistText = distKm < 1
                ? `${Math.round(distKm * 1000)} m`
                : `${distKm.toFixed(2)} km`;
            const imageUrl = v.image || v.image_url || "https://images.unsplash.com/photo-1544025162-d76694265947?auto=format&fit=crop&w=600&q=80";
            const priceMin = Number(v.priceMin || v.price_min || 50000);
            const priceMax = Number(v.priceMax || v.price_max || 300000);
            const gmapsUrl = `https://www.google.com/maps/dir/?api=1&origin=${this.currentCenter[0]},${this.currentCenter[1]}&destination=${lat},${lng}&travelmode=two-wheeler`;

            const popupContent = `
                <div class="map-venue-popup">
                    <div class="popup-img-wrap">
                        <img src="${imageUrl}" alt="${v.name}" loading="lazy">
                        <span class="popup-rating">★ ${Number(v.rating || 4.5).toFixed(1)}</span>
                        <span class="popup-dist-badge">📍 Cách ${exactDistText} • ~${travelMins}p</span>
                    </div>
                    <div class="popup-body">
                        <h4 class="popup-title">${v.name}</h4>
                        <div class="popup-meta">
                            <span>🍽️ ${v.cuisineLabel || v.category || 'Ẩm thực'}</span>
                            ${v.openHours ? `<span>• 🕒 ${v.openHours}</span>` : ''}
                        </div>
                        <div class="popup-address" title="${v.address}">${v.address}</div>
                        <div class="popup-footer">
                            <span class="popup-price">${priceMin.toLocaleString()}đ - ${priceMax.toLocaleString()}đ</span>
                            <div class="popup-actions">
                                <a href="${gmapsUrl}" target="_blank" class="popup-btn-directions" title="Chỉ đường Google Maps">
                                    Chỉ đường ↗
                                </a>
                                <button type="button" class="popup-btn-detail" onclick="window.onMapPopupSelectVenue(${v.id})">
                                    Chi tiết
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            `;

            marker.bindPopup(popupContent, {
                maxWidth: 310,
                minWidth: 275,
                className: 'custom-venue-popup-wrapper'
            });

            marker.on('click', () => {
                this.highlightVenue(v.id, { panTo: false, openPopup: false });
                if (typeof this.onVenueClick === 'function') {
                    this.onVenueClick(v);
                }
            });

            this.venueMarkers.set(v.id, marker);
            this.venueDataMap.set(v.id, v);
        });

        this.updateRadiusCount(this.venueMarkers.size);
    }

    /**
     * Làm nổi bật marker của quán ăn khi người dùng cuộn danh sách hoặc hover thẻ quán
     * @param {number|string} venueId ID quán ăn
     * @param {Object} options { panTo: boolean, openPopup: boolean }
     */
    highlightVenue(venueId, options = { panTo: true, openPopup: false }) {
        if (!this.map) return;

        // Gỡ nổi bật khỏi marker trước đó
        if (this.activeVenueId !== null && this.activeVenueId !== venueId) {
            const prevMarker = this.venueMarkers.get(this.activeVenueId);
            if (prevMarker) {
                prevMarker.setZIndexOffset(0);
                const el = prevMarker.getElement();
                if (el) el.classList.remove('active-pin');
            }
        }

        this.activeVenueId = venueId;
        const marker = this.venueMarkers.get(venueId);
        if (!marker) return;

        marker.setZIndexOffset(850);
        const el = marker.getElement();
        if (el) el.classList.add('active-pin');

        if (options.panTo) {
            const latlng = marker.getLatLng();
            // Pan mượt nếu ghim nằm ngoài khung nhìn hiện tại hoặc sát mép
            const bounds = this.map.getBounds();
            if (!bounds.pad(-0.12).contains(latlng)) {
                this.map.panTo(latlng, { animate: true, duration: 0.45 });
            }
        }

        if (options.openPopup) {
            marker.openPopup();
        }
    }

    /**
     * Di chuyển bản đồ và mở popup của quán ăn tương ứng
     * @param {number|string} venueId ID quán ăn
     */
    focusVenue(venueId) {
        const marker = this.venueMarkers.get(venueId);
        if (marker) {
            this.highlightVenue(venueId, { panTo: false, openPopup: false });
            const latlng = marker.getLatLng();
            this.map.flyTo(latlng, Math.max(this.map.getZoom(), 15), {
                duration: 0.75
            });
            setTimeout(() => {
                marker.openPopup();
            }, 500);
        }
    }

    invalidateSize() {
        if (this.map) {
            setTimeout(() => {
                this.map.invalidateSize();
            }, 150);
        }
    }

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
        toast.innerHTML = `<span>${message}</span>`;
        toastContainer.appendChild(toast);

        setTimeout(() => {
            toast.classList.add('fade-out');
            setTimeout(() => toast.remove(), 400);
        }, 3000);
    }
}

window.FoodAIMapComponent = FoodAIMapComponent;
