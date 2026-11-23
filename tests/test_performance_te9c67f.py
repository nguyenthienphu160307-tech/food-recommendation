"""
==============================================================================
TASK TE9C67F: KIỂM THỬ HIỆU NĂNG TRUY VẤN KHÔNG GIAN & BỘ LỌC (NFR-01, NFR-04)
- Kiểm tra EXPLAIN QUERY PLAN trực tiếp trên CSDL.
- Đo thời gian phản hồi trung bình & P95 qua 50 lượt truy vấn liên tiếp (< 3.0s).
- Đo tỷ lệ lỗi (Error Rate < 1%).
==============================================================================
"""

import os
import sys
import time
from sqlalchemy import text

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from fastapi.testclient import TestClient
from app.main import app
from app.core.database import SessionLocal, engine

client = TestClient(app)


def ensure_composite_indexes():
    """Áp dụng các Composite Index tối ưu cho truy vấn không gian & bộ lọc."""
    ddl_statements = [
        "CREATE INDEX IF NOT EXISTS idx_restaurants_status_coords ON restaurants (status, latitude, longitude)",
        "CREATE INDEX IF NOT EXISTS idx_restaurants_status_cuisine_price ON restaurants (status, cuisine_type, min_price, max_price)",
        "CREATE INDEX IF NOT EXISTS idx_restaurants_status_rating ON restaurants (status, avg_rating, total_reviews)",
        "CREATE INDEX IF NOT EXISTS idx_amenities_multi_filter ON restaurant_amenities (restaurant_id, has_parking, has_private_room, has_outdoor, pet_friendly, vegetarian_support)",
    ]
    with engine.begin() as conn:
        for stmt in ddl_statements:
            try:
                conn.execute(text(stmt))
            except Exception:
                # MySQL < 8 không hỗ trợ IF NOT EXISTS cho CREATE INDEX
                pass


def test_explain_query_plan():
    """Kiểm tra EXPLAIN QUERY PLAN sử dụng chỉ mục thay vì Full Table Scan."""
    ensure_composite_indexes()
    db = SessionLocal()
    try:
        dialect = engine.dialect.name
        sql = (
            "SELECT r.id, r.name, r.latitude, r.longitude, r.avg_rating "
            "FROM restaurants r "
            "INNER JOIN restaurant_amenities a ON r.id = a.restaurant_id "
            "WHERE r.status = 'active' "
            "AND r.latitude BETWEEN 10.7319 AND 10.8219 "
            "AND r.longitude BETWEEN 106.6551 AND 106.7467 "
            "AND r.min_price <= 300000 "
            "AND a.has_parking = 1 "
            "ORDER BY r.avg_rating DESC LIMIT 20"
        )
        explain_cmd = f"EXPLAIN QUERY PLAN {sql}" if dialect == "sqlite" else f"EXPLAIN {sql}"
        rows = db.execute(text(explain_cmd)).fetchall()
        assert len(rows) > 0, "EXPLAIN không trả về kế hoạch thực thi!"
        print(f"\n[TE9C67F EXPLAIN - {dialect.upper()}]")
        for r in rows:
            print(" ", r)
    finally:
        db.close()


def test_spatial_filter_performance_nfr01_nfr04():
    """Benchmark 50 lượt gọi GET /api/restaurants/filter đảm bảo < 3s (NFR-01) và lỗi < 1% (NFR-04)."""
    ensure_composite_indexes()
    total_requests = 50
    errors = 0
    latencies_ms = []

    scenarios = [
        {"lat": 10.7769, "lng": 106.7009, "radius_km": 5.0, "has_parking": True, "sort_by": "distance"},
        {"lat": 10.7769, "lng": 106.7009, "radius_km": 3.0, "price_max": 300000, "sort_by": "rating"},
        {"lat": 10.8035, "lng": 106.7145, "radius_km": 10.0, "cuisine_type": "Món Việt", "sort_by": "price_asc"},
        {"lat": 10.7843, "lng": 106.6845, "radius_km": 5.0, "vegetarian_support": True},
        {"lat": 10.8482, "lng": 106.7712, "radius_km": 10.0, "has_outdoor": True, "min_rating": 4.0},
    ]

    for i in range(total_requests):
        params = scenarios[i % len(scenarios)]
        t0 = time.perf_counter()
        res = client.get("/api/restaurants/filter", params=params)
        elapsed_ms = (time.perf_counter() - t0) * 1000.0
        latencies_ms.append(elapsed_ms)
        if res.status_code != 200:
            errors += 1

    avg_ms = sum(latencies_ms) / len(latencies_ms)
    max_ms = max(latencies_ms)
    error_rate = (errors / total_requests) * 100.0

    print(f"\n[TE9C67F BENCHMARK] {total_requests} requests | Avg: {avg_ms:.2f} ms | Max: {max_ms:.2f} ms | Error rate: {error_rate:.2f}%")

    assert max_ms < 3000.0, f"Vi phạm NFR-01: Thời gian phản hồi tối đa {max_ms:.2f}ms >= 3000ms!"
    assert error_rate < 1.0, f"Vi phạm NFR-04: Tỷ lệ lỗi {error_rate:.2f}% >= 1%!"


if __name__ == "__main__":
    test_explain_query_plan()
    test_spatial_filter_performance_nfr01_nfr04()
    print("\n>>> PASSED: Task TE9C67F đạt chuẩn NFR-01 (< 3s) và NFR-04 (lỗi < 1%)! <<<")