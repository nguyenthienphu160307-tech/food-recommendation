/**
 * ==============================================================================
 * MAP COMPONENT (Task TSK-10, TE9C65E / TSK-21, TSK-22)
 * Tích hợp Leaflet SDK + Google Maps Tiles (Đường phố & Vệ tinh)
 * Hiển thị vòng tròn bán kính (1km, 3km, 5km, 10km), kéo ghim thủ công & Popup
 * ==============================================================================
 */

class FoodAIMapComponent {
    constructor(options = {}) {
        this.containerId = options.containerId || 'main-map';
        this.defaultCenter = options.defaultCenter || [10.776889, 106.700806];
        this.currentCenter = options.currentCenter || [...this.defaultCenter];
        this.defaultZoom = options.defaultZoom || 14;
        this.minZoom = options.minZoom || 5;
        this.maxZoom = options.maxZoom || 20;
        this.radiusKm = options.radiusKm || 5; // Bán kính mặc định 5km

        this.onLocationChange = options.onLocationChange || null;
        this.onVenueClick = options.onVenueClick || null;

        this.map = null;
        this.baseLayers = {};
        this.activeLayerName = 'googleStreets';
        this.userMarker = null;
        this.radiusCircle = null;
        this.venueMarkers = new Map();

        this.init();
    }

    init() {
        const container = document.getElementById(this.containerId);
        if (!container) return;

        this.map = L.map(this.containerId, {
            center: this.currentCenter,
            zoom: this.defaultZoom,
            minZoom: this.minZoom,
            maxZoom: this.maxZoom,
            zoomControl: false,
            attributionControl: true
        });

        this._setupBaseLayers();
        this._initUserMarkerAndRadiusCircle();
        this._setupCustomControls();

        // Cho phép click bất kỳ điểm nào trên bản đồ để chọn vị trí thủ công (UC-03)
        this.map.on('click', (e) => {
            this.setUserPosition(e.latlng.lat, e.latlng.lng, true, 'map_click');
        });

        window.addEventListener('resize', () => this.invalidateSize());
    }

    _setupBaseLayers() {
        this.baseLayers['googleStreets'] = L.tileLayer(
            'https://{s}.google.com/vt/lyrs=m&x={x}&y={y}&z={z}&hl=vi',
            { maxZoom: this.maxZoom, subdomains: ['mt0', 'mt1', 'mt2', 'mt3'], attribution: '&copy; Google Maps' }
        );

        this.baseLayers['googleHybrid'] = L.tileLayer(
            'https://{s}.google.com/vt/lyrs=s,h&x={x}&y={y}&z={z}&hl=vi',
            { maxZoom: this.maxZoom, subdomains: ['mt0', 'mt1', 'mt2', 'mt3'], attribution: '&copy; Google Maps Satellite' }
        );

        this.baseLayers['osm'] = L.tileLayer(
            'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
            { maxZoom: 19, attribution: '&copy; OpenStreetMap' }
        );

        this.baseLayers['googleStreets'].addTo(this.map);
    }

    switchBaseLayer(layerKey) {
        if (!this.baseLayers[layerKey] || layerKey === this.activeLayerName) return;
        if (this.baseLayers[this.activeLayerName]) {
            this.map.removeLayer(this.baseLayers[this.activeLayerName]);
        }
        this.baseLayers[layerKey].addTo(this.map);
        this.activeLayerName = layerKey;

        document.querySelectorAll('.map-layer-btn').forEach(btn => {
            btn.classList.toggle('active', btn.dataset.layer === layerKey);
        });
    }

    /**
     * Khởi tạo ghim vị trí người dùng (cho phép kéo thả) kèm vòng tròn bán kính đỏ (TSK-22)
     */
    _initUserMarkerAndRadiusCircle() {
        const userIcon = L.divIcon({
            className: 'user-marker-container',
            html: `<div class="user-pulse-ring"></div><div class="user-center-dot"></div>`,
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
            <div style="font-size:0.84rem;line-height:1.45;">
                <strong style="color:#e11d48;">📍 Vị trí tìm kiếm của bạn</strong>
                <p style="margin:4px 0 0;color:#6b7280;font-size:0.78rem;">
                    Kéo thả ghim này hoặc chạm vào bản đồ để đổi vị trí thủ công (UC-03).
                </p>
            </div>
        `);

        // Vẽ vòng tròn bán kính tìm kiếm màu đỏ xung quanh vị trí người dùng
        this.radiusCircle = L.circle(this.currentCenter, {
            radius: this.radiusKm * 1000,
            color: '#e11d48',
            weight: 2,
            fillColor: '#e11d48',
            fillOpacity: 0.10
        }).addTo(this.map);

        // Xử lý kéo thả ghim vị trí thủ công (UC-03)
        this.userMarker.on('dragend', (e) => {
            const pos = e.target.getLatLng();
            this.setUserPosition(pos.lat, pos.lng, true, 'map_drag');
        });
    }

    /**
     * Đổi bán kính vòng tròn đỏ trên bản đồ (1km, 3km, 5km, 10km)
     */
    setRadiusKm(radiusKm) {
        this.radiusKm = Number(radiusKm) || 5;
        if (this.radiusCircle) {
            this.radiusCircle.setRadius(this.radiusKm * 1000);
            this.map.fitBounds(this.radiusCircle.getBounds(), { padding: [20, 20], maxZoom: 16 });
        }
    }

    setUserPosition(lat, lng, triggerCallback = true, source = 'manual') {
        lat = parseFloat(lat);
        lng = parseFloat(lng);
        if (!Number.isFinite(lat) || !Number.isFinite(lng)) return;
        this.currentCenter = [Number(lat), Number(lng)];
        if (this.userMarker) this.userMarker.setLatLng(this.currentCenter);
        if (this.radiusCircle) this.radiusCircle.setLatLng(this.currentCenter);

        const coordsEl = document.getElementById('map-live-coords');
        if (coordsEl) {
            coordsEl.textContent = `GPS: ${this.currentCenter[0].toFixed(5)}, ${this.currentCenter[1].toFixed(5)}`;
        }

        if (triggerCallback && typeof this.onLocationChange === 'function') {
            this.onLocationChange({ lat: this.currentCenter[0], lng: this.currentCenter[1], source });
        }
    }

    flyToPosition(lat, lng, zoom = 14) {
        lat = parseFloat(lat);
        lng = parseFloat(lng);
        if (!Number.isFinite(lat) || !Number.isFinite(lng)) return;
        this.setUserPosition(lat, lng, false);
        if (this.map) {
            this.map.flyTo([lat, lng], zoom, { duration: 1.0 });
        }
    }

    _setupCustomControls() {
        L.control.scale({ imperial: false, metric: true, position: 'bottomleft' }).addTo(this.map);

        const ActionsControl = L.Control.extend({
            options: { position: 'topleft' },
            onAdd: () => {
                const container = L.DomUtil.create('div', 'custom-map-controls leaflet-bar');
                L.DomEvent.disableClickPropagation(container);
                L.DomEvent.disableScrollPropagation(container);

                container.innerHTML = `
                    <div class="map-ctrl-group">
                        <button type="button" class="map-ctrl-btn" id="map-btn-zoom-in" title="Phóng to (+)">+</button>
                        <button type="button" class="map-ctrl-btn" id="map-btn-zoom-out" title="Thu nhỏ (-)">−</button>
                    </div>
                `;
                return container;
            }
        });

        this.map.addControl(new ActionsControl());

        setTimeout(() => {
            const btnIn = document.getElementById('map-btn-zoom-in');
            const btnOut = document.getElementById('map-btn-zoom-out');
            if (btnIn) btnIn.onclick = () => this.map.zoomIn();
            if (btnOut) btnOut.onclick = () => this.map.zoomOut();
        }, 50);
    }

    locateUser() {
        if (window.smartDiningLocationManager) {
            window.smartDiningLocationManager.requestBrowserGPS(true);
        }
    }

    setVenueMarkers(venues = []) {
        if (!this.map) return;

        this.venueMarkers.forEach(m => this.map.removeLayer(m));
        this.venueMarkers.clear();

        venues.forEach((v) => {
            const lat = parseFloat(v.lat ?? v.latitude);
            const lng = parseFloat(v.lng ?? v.longitude);
            if (!Number.isFinite(lat) || !Number.isFinite(lng)) return;
            const shortPrice = `${Math.round((v.priceMin || 50000) / 1000)}k`;

            const icon = L.divIcon({
                className: 'venue-marker-pin',
                html: `
                    <div class="pin-bubble" style="background:#e11d48;color:#fff;border:2px solid #fff;">
                        <span>🍴 ${shortPrice}</span>
                    </div>
                    <div class="pin-arrow" style="border-top-color:#e11d48;"></div>
                `,
                iconSize: [54, 36],
                iconAnchor: [27, 34],
                popupAnchor: [0, -32]
            });

            const marker = L.marker([lat, lng], { icon }).addTo(this.map);                      const distText = v.distanceKm != null
                ? (v.distanceKm < 1 ? `${Math.round(v.distanceKm * 1000)} m` : `${v.distanceKm.toFixed(2)} km`)
                : '';

            const popupContent = `
                <div class="map-venue-popup">
                    <div class="popup-img-wrap">
                        <img src="${v.image}" alt="${v.name}" loading="lazy">
                        <span class="popup-rating">★ ${v.rating}</span>
                    </div>
                    <div class="popup-body">
                        <h4 class="popup-title">${v.name}</h4>
                        <div class="popup-meta">
                            <span>${v.cuisineLabel || 'Ẩm thực'}</span>
                            ${distText ? `<span>•</span><strong style="color:#e11d48;">Cách ${distText}</strong>` : ''}
                        </div>
                        <div class="popup-address">${v.address}</div>
                        <div class="popup-footer">
                            <span class="popup-price">${(v.priceMin || 0).toLocaleString()}đ - ${(v.priceMax || 0).toLocaleString()}đ</span>
                            <button type="button" class="popup-btn-detail" onclick="window.onMapPopupSelectVenue(${v.id})">
                                Thực đơn →
                            </button>
                        </div>
                    </div>
                </div>
            `;

            marker.bindPopup(popupContent, { maxWidth: 290, minWidth: 250, className: 'custom-venue-popup-wrapper' });
            marker.on('click', () => {
                if (typeof this.onVenueClick === 'function') this.onVenueClick(v);
            });

            this.venueMarkers.set(v.id, marker);
        });
    }

    focusVenue(venueId) {
        const marker = this.venueMarkers.get(venueId);
        if (marker) {
            this.map.flyTo(marker.getLatLng(), Math.max(this.map.getZoom(), 15), { duration: 0.7 });
            setTimeout(() => marker.openPopup(), 500);
        }
    }
    /**
     * Đồng bộ highlight 1 ghim khi hover/cuộn thẻ nhà hàng
     */
    highlightVenue(venueId, options = { panTo: false, openPopup: false }) {
        this.venueMarkers.forEach((marker, id) => {
            const el = marker.getElement();
            if (!el) return;
            el.classList.toggle('marker-active-sync', id === venueId);
            marker.setZIndexOffset(id === venueId ? 850 : 0);
        });

        const target = this.venueMarkers.get(venueId);
        if (target && this.map) {
            if (options.panTo) {
                this.map.panTo(target.getLatLng(), { animate: true, duration: 0.45 });
            }
            if (options.openPopup) {
                target.openPopup();
            }
        }
    }

    /**
     * Task TE9C674: Khi AI trả về Top N quán trong khung chat,
     * bản đồ tự động flyTo / flyToBounds và làm nổi bật các ghim được đề xuất.
     */
    highlightRecommendedVenues(topVenues = []) {
        if (!this.map || !Array.isArray(topVenues) || topVenues.length === 0) return;

        // 1. Xóa highlight AI cũ trên các ghim hiện có
        this.clearAIHighlights();

        const validVenues = topVenues.filter(v => (v.lat ?? v.latitude) && (v.lng ?? v.longitude));
        if (validVenues.length === 0) return;

        // 2. Đảm bảo tất cả quán Top N đều có marker trên bản đồ, gắn badge Top #1..#N
        const boundsLatLngs = [];
        validVenues.forEach((v, idx) => {
            const lat = Number(v.lat ?? v.latitude);
            const lng = Number(v.lng ?? v.longitude);
            const rank = idx + 1;
            boundsLatLngs.push([lat, lng]);

            // Xóa marker cũ của quán này nếu đã tồn tại để vẽ lại dạng ghim AI nổi bật
            if (this.venueMarkers.has(v.id)) {
                this.map.removeLayer(this.venueMarkers.get(v.id));
            }

            const shortPrice = `${Math.round((v.priceMin ?? v.min_price ?? 50000) / 1000)}k`;
            const aiIcon = L.divIcon({
                className: 'venue-marker-pin ai-recommended-pin',
                html: `
                    <div class="pin-bubble ai-pin-bubble">
                        <span class="ai-rank-badge">#${rank}</span>
                        <span>🍴 ${shortPrice}</span>
                    </div>
                    <div class="pin-arrow ai-pin-arrow"></div>
                `,
                iconSize: [74, 42],
                iconAnchor: [37, 40],
                popupAnchor: [0, -38]
            });

            const marker = L.marker([lat, lng], {
                icon: aiIcon,
                zIndexOffset: 1000 - idx
            }).addTo(this.map);

            const score = v.matchScore ?? v.match_score ?? 90;
            const distKm = v.distanceKm ?? v.distance_km;
            const distText = distKm != null
                ? (distKm < 1 ? `${Math.round(distKm * 1000)} m` : `${Number(distKm).toFixed(2)} km`)
                : '';
            const imgUrl = v.image || v.cover_image_url || 'https://images.unsplash.com/photo-1544025162-d76694265947?auto=format&fit=crop&w=600&q=80';
            const rating = Number(v.rating ?? v.avg_rating ?? 4.5).toFixed(1);
            const pMin = Number(v.priceMin ?? v.min_price ?? 50000).toLocaleString();
            const pMax = Number(v.priceMax ?? v.max_price ?? 300000).toLocaleString();

            const popupContent = `
                <div class="map-venue-popup">
                    <div class="popup-img-wrap">
                        <img src="${imgUrl}" alt="${v.name}" loading="lazy">
                        <span class="popup-rating">✨ Top ${rank} • ${Math.round(score)}%</span>
                    </div>
                    <div class="popup-body">
                        <h4 class="popup-title">${v.name}</h4>
                        <div class="popup-meta">
                            <span>★ ${rating}</span>
                            <span>•</span>
                            <span>${v.cuisineLabel || v.cuisine_type || 'Ẩm thực'}</span>
                            ${distText ? `<span>•</span><strong style="color:#e11d48;">Cách ${distText}</strong>` : ''}
                        </div>
                        <div class="popup-address">${v.address || ''}</div>
                        <div class="popup-footer">
                            <span class="popup-price">${pMin}đ - ${pMax}đ</span>
                            <button type="button" class="popup-btn-detail" onclick="window.onMapPopupSelectVenue(${v.id})">
                                Thực đơn →
                            </button>
                        </div>
                    </div>
                </div>
            `;

            marker.bindPopup(popupContent, { maxWidth: 300, minWidth: 255, className: 'custom-venue-popup-wrapper' });
            marker.on('click', () => {
                if (typeof this.onVenueClick === 'function') this.onVenueClick(v);
            });

            this.venueMarkers.set(v.id, marker);
        });

        // 3. Tự động di chuyển bản đồ (flyTo nếu 1 quán, flyToBounds nếu nhiều quán)
        if (boundsLatLngs.length === 1) {
            this.map.flyTo(boundsLatLngs[0], 15, { duration: 1.1 });
        } else {
            const bounds = L.latLngBounds(boundsLatLngs);
            this.map.flyToBounds(bounds, { padding: [55, 55], maxZoom: 15, duration: 1.1 });
        }

        // 4. Mở popup quán Top 1 sau khi bản đồ bay tới nơi
        const top1Marker = this.venueMarkers.get(validVenues[0].id);
        if (top1Marker) {
            setTimeout(() => top1Marker.openPopup(), 950);
        }
    }

    clearAIHighlights() {
        this.venueMarkers.forEach((marker) => {
            const el = marker.getElement();
            if (el) el.classList.remove('ai-recommended-pin');
        });
    }

    invalidateSize() {
        if (this.map) setTimeout(() => this.map.invalidateSize(), 150);
    }
}

window.FoodAIMapComponent = FoodAIMapComponent;