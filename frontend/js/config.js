// ==========================================
// 3. TÌM NHÀ HÀNG XUNG QUANH (API GET /api/geo/nearby-restaurants)
// ==========================================
async function fetchNearbyRestaurants(userLat, userLng, radiusKm = 5.0) {
    try {
        // Gắn Query Parameters vào URL
        const url = new URL(`${API_BASE_URL}/geo/nearby-restaurants`);
        url.searchParams.append('lat', userLat);
        url.searchParams.append('lng', userLng);
        url.searchParams.append('radius_km', radiusKm);

        const response = await fetch(url, {
            method: 'GET',
            headers: { 'Accept': 'application/json' }
        });

        if (response.ok) {
            const data = await response.json();
            console.log("Thống kê Bounding Box:", data.stats);
            
            // Hàm này bạn tự viết để render danh sách nhà hàng ra HTML (Leaflet Marker, danh sách...)
            renderRestaurantList(data.restaurants); 
        } else {
            const errorData = await response.json();
            console.error("Lỗi lọc vị trí:", errorData.detail);
        }
    } catch (error) {
        console.error("Lỗi khi kết nối API Geo:", error);
    }
}

// Giả sử có một nút để kích hoạt tìm kiếm
document.getElementById('btn-find-food').addEventListener('click', () => {
    // Lấy tọa độ từ form Profile hoặc HTML5 Geolocation
    const lat = parseFloat(document.getElementById('user-lat').value) || 10.786;
    const lng = parseFloat(document.getElementById('user-lng').value) || 106.701;
    const radius = parseFloat(document.getElementById('search-radius').value) || 5;
    
    fetchNearbyRestaurants(lat, lng, radius);
});