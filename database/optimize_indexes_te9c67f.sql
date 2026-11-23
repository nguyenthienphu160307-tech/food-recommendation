-- TASK TE9C67F: TỐI ƯU HÓA CHỈ MỤC & KIỂM TRA EXPLAIN QUERY PLAN (NFR-01, NFR-04)
-- Mục tiêu: Trang danh sách & bộ lọc tải < 3 giây, tỷ lệ lỗi < 1%

-- 1. Chỉ mục phức hợp (Composite Index) cho truy vấn Không gian (Bounding Box) kèm trạng thái active
CREATE INDEX idx_restaurants_status_coords
ON restaurants (status, latitude, longitude);

-- 2. Chỉ mục phức hợp cho bộ lọc kết hợp Ẩm thực + Khoảng giá
CREATE INDEX idx_restaurants_status_cuisine_price
ON restaurants (status, cuisine_type, min_price, max_price);

-- 3. Chỉ mục phức hợp cho sắp xếp theo Điểm đánh giá cao nhất
CREATE INDEX idx_restaurants_status_rating
ON restaurants (status, avg_rating, total_reviews);

-- 4. Chỉ mục phức hợp cho bảng tiện ích (5 cờ lọc đồng thời)
CREATE INDEX idx_amenities_multi_filter
ON restaurant_amenities (restaurant_id, has_parking, has_private_room, has_outdoor, pet_friendly, vegetarian_support);

-- KIỂM TRA EXPLAIN QUERY PLAN (Chạy trực tiếp trên MySQL Workbench / phpMyAdmin)
EXPLAIN
SELECT r.id, r.name, r.latitude, r.longitude, r.avg_rating, r.min_price, r.max_price
FROM restaurants r
INNER JOIN restaurant_amenities a ON r.id = a.restaurant_id
WHERE r.status = 'active'
  AND r.latitude BETWEEN 10.7319 AND 10.8219
  AND r.longitude BETWEEN 106.6551 AND 106.7467
  AND r.min_price <= 300000
  AND a.has_parking = 1
ORDER BY r.avg_rating DESC
LIMIT 20;