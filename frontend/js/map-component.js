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
            if (!v.lat || !v.lng) return;
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

            const marker = L.marker([v.lat, v.lng], { icon }).addTo(this.map);
            const distText = v.distanceKm != null
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

    invalidateSize() {
        if (this.map) setTimeout(() => this.map.invalidateSize(), 150);
    }
}

window.FoodAIMapComponent = FoodAIMapComponent;