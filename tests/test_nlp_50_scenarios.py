"""
Task TE9C67A: Kiểm thử độ chính xác NLP với 50 câu hỏi tiếng Việt thực tế (Mục 9.1 SRS).
Chạy kiểm thử & xem báo cáo: pytest tests/test_nlp_50_scenarios.py -v -s
"""

import asyncio
import pytest
from app.core.prompt_template import extract_criteria_from_prompt_async

# Bộ 50 câu hỏi thực tế đa dạng vùng miền, ngân sách, loại món và tiện ích
NLP_50_TEST_CASES = [
    # --- Nhóm 1: Quận trung tâm TP.HCM + Đồ nướng / Lẩu ---
    ("Tìm quán nướng ở Quận 1 dưới 300k có chỗ đậu ô tô", {"location": "quận 1", "cuisine": "nướng", "budget": 300000, "parking": True}),
    ("Nhóm 6 người muốn ăn BBQ Hàn Quốc Quận 3 có phòng riêng", {"location": "quận 3", "cuisine": "bbq", "private_room": True}),
    ("Quán lẩu ngon ở Bình Thạnh giá khoảng 200k", {"location": "bình thạnh", "cuisine": "lẩu", "budget": 200000}),
    ("Đồ nướng sân vườn Gò Vấp dưới 250k", {"location": "gò vấp", "cuisine": "nướng", "budget": 250000, "outdoor": True}),
    ("Muốn ăn thịt nướng ở Thủ Đức có chỗ gửi xe", {"location": "thủ đức", "cuisine": "nướng", "parking": True}),
    ("Tìm quán lẩu nấm Quận 5 cho 4 người dưới 400k", {"location": "quận 5", "cuisine": "lẩu", "budget": 400000}),
    ("Ăn BBQ ở Quận 7 tầm 350k có phòng VIP", {"location": "quận 7", "cuisine": "bbq", "budget": 350000, "private_room": True}),
    ("Quán nướng ngoài trời Quận 2 cho mang thú cưng", {"location": "quận 2", "cuisine": "nướng", "outdoor": True, "pet": True}),
    ("Lẩu bò ở Tân Bình giá dưới 150k", {"location": "tân bình", "cuisine": "lẩu", "budget": 150000}),
    ("Đi ăn nướng Quận 10 khoảng 300k có bãi đậu xe", {"location": "quận 10", "cuisine": "nướng", "budget": 300000, "parking": True}),

    # --- Nhóm 2: Món Việt / Cơm tấm / Phở / Bún ---
    ("Quán cơm tấm ngon ở Phú Nhuận dưới 80k", {"location": "phú nhuận", "cuisine": "cơm tấm", "budget": 80000}),
    ("Tìm quán phở ở Quận 1 giá tầm 70k", {"location": "quận 1", "cuisine": "việt", "budget": 70000}),
    ("Cơm tấm sườn bì chả Gò Vấp dưới 60k", {"location": "gò vấp", "cuisine": "cơm tấm", "budget": 60000}),
    ("Quán bún bò ngon Quận 3 dưới 100k", {"location": "quận 3", "cuisine": "việt", "budget": 100000}),
    ("Ăn cơm Việt gia đình ở Quận 4 có chỗ đậu xe", {"location": "quận 4", "cuisine": "việt", "parking": True}),
    ("Tìm quán món Việt ở Bình Thạnh khoảng 120k", {"location": "bình thạnh", "cuisine": "việt", "budget": 120000}),
    ("Cơm tấm đêm Quận 10 dưới 90k", {"location": "quận 10", "cuisine": "cơm tấm", "budget": 90000}),
    ("Quán phở ngon ở Thủ Đức giá 50k", {"location": "thủ đức", "cuisine": "việt", "budget": 50000}),
    ("Bún chả ở Tân Phú dưới 75k", {"location": "tân phú", "cuisine": "việt", "budget": 75000}),
    ("Cơm niêu món Việt Quận 7 có phòng riêng cho 8 người", {"location": "quận 7", "cuisine": "việt", "private_room": True}),

    # --- Nhóm 3: Món Chay / Thanh đạm ---
    ("Nhà hàng chay thanh đạm ở Quận 1 dưới 200k", {"location": "quận 1", "cuisine": "chay", "budget": 200000, "veg": True}),
    ("Tìm quán ăn thuần chay Quận 3 có không gian ngoài trời", {"location": "quận 3", "cuisine": "chay", "outdoor": True, "veg": True}),
    ("Quán chay ngon ở Phú Nhuận khoảng 150k", {"location": "phú nhuận", "cuisine": "chay", "budget": 150000, "veg": True}),
    ("Ăn vegan ở Bình Thạnh có chỗ đậu ô tô", {"location": "bình thạnh", "cuisine": "chay", "parking": True, "veg": True}),
    ("Buffet chay Gò Vấp dưới 180k", {"location": "gò vấp", "cuisine": "chay", "budget": 180000, "veg": True}),
    ("Quán chay yên tĩnh có phòng riêng ở Quận 5", {"location": "quận 5", "cuisine": "chay", "private_room": True, "veg": True}),
    ("Tìm chỗ ăn chay Quận 10 dưới 100k", {"location": "quận 10", "cuisine": "chay", "budget": 100000, "veg": True}),
    ("Nhà hàng có món chay ở Quận 7 cho gia đình", {"location": "quận 7", "veg": True}),

    # --- Nhóm 4: Hải sản / Món Nhật / Món Âu / Cà phê ---
    ("Quán hải sản tươi sống Quận 4 dưới 500k", {"location": "quận 4", "cuisine": "hải sản", "budget": 500000}),
    ("Nhà hàng Nhật sushi ở Quận 1 tầm 450k có phòng riêng", {"location": "quận 1", "budget": 450000, "private_room": True}),
    ("Hải sản bình dân ở Quận 8 dưới 300k", {"location": "quận 8", "cuisine": "hải sản", "budget": 300000}),
    ("Quán ăn có sân vườn ở Thủ Đức dưới 250k", {"location": "thủ đức", "budget": 250000, "outdoor": True}),
    ("Nhà hàng tiếp khách Quận 1 có phòng VIP và bãi đậu ô tô", {"location": "quận 1", "private_room": True, "parking": True}),
    ("Quán ăn cho phép mang chó mèo ở Quận 2", {"location": "quận 2", "pet": True}),
    ("Tìm quán ăn gia đình ở Quận 6 dưới 200k", {"location": "quận 6", "budget": 200000}),
    ("Quán nhậu hải sản ngoài trời Bình Tân dưới 350k", {"location": "bình tân", "cuisine": "hải sản", "budget": 350000, "outdoor": True}),

    # --- Nhóm 5: Đa dạng vùng miền (Hà Nội, Đà Nẵng) & Ngân sách cao/thấp ---
    ("Tìm quán phở ngon ở Hoàn Kiếm dưới 100k", {"location": "hoàn kiếm", "cuisine": "việt", "budget": 100000}),
    ("Quán nướng ở Cầu Giấy có chỗ đậu xe dưới 300k", {"location": "cầu giấy", "cuisine": "nướng", "budget": 300000, "parking": True}),
    ("Nhà hàng chay ở Đống Đa khoảng 150k", {"location": "đống đa", "cuisine": "chay", "budget": 150000, "veg": True}),
    ("Ăn lẩu ở Ba Đình có phòng riêng dưới 400k", {"location": "ba đình", "cuisine": "lẩu", "budget": 400000, "private_room": True}),
    ("Quán cơm tấm ở Quận 11 dưới 70k", {"location": "quận 11", "cuisine": "cơm tấm", "budget": 70000}),
    ("Tìm quán ăn Quận 12 có bãi đậu ô tô dưới 200k", {"location": "quận 12", "budget": 200000, "parking": True}),
    ("Quán nướng ở Tân Phú dưới 220k", {"location": "tân phú", "cuisine": "nướng", "budget": 220000}),
    ("Nhà hàng sang trọng Quận 1 ngân sách 1000k có phòng riêng", {"location": "quận 1", "budget": 1000000, "private_room": True}),

    # --- Nhóm 6: Câu hỏi ngắn / tự nhiên không nêu địa điểm ---
    ("Muốn ăn đồ nướng dưới 250k có chỗ đậu ô tô", {"cuisine": "nướng", "budget": 250000, "parking": True}),
    ("Tìm quán chay gần đây dưới 120k", {"cuisine": "chay", "budget": 120000, "veg": True}),
    ("Quán nào có phòng riêng yên tĩnh tầm 300k", {"budget": 300000, "private_room": True}),
    ("Chỗ nào ăn cơm tấm dưới 65k", {"cuisine": "cơm tấm", "budget": 65000}),
    ("Quán ăn ngoài trời thân thiện thú cưng dưới 300k", {"budget": 300000, "outdoor": True, "pet": True}),
    ("Đi ăn lẩu có chỗ đậu ô tô khoảng 250k", {"cuisine": "lẩu", "budget": 250000, "parking": True}),
]


def _check_case_match(criteria, expected: dict) -> bool:
    """Kiểm tra mức độ khớp ý định chính của một câu hỏi."""
    if "location" in expected:
        loc = (criteria.location_text or "").lower()
        if expected["location"] not in loc:
            return False
    if "budget" in expected:
        if criteria.budget != expected["budget"]:
            return False
    if "parking" in expected:
        if bool(criteria.has_parking) != expected["parking"]:
            return False
    other = criteria.other_conditions
    if "private_room" in expected:
        if bool(other.has_private_room) != expected["private_room"]:
            return False
    if "outdoor" in expected:
        if bool(other.has_outdoor) != expected["outdoor"]:
            return False
    if "pet" in expected:
        if bool(other.pet_friendly) != expected["pet"]:
            return False
    if "veg" in expected:
        if bool(other.vegetarian_support) != expected["veg"] and "chay" not in (criteria.cuisine or "").lower():
            return False
    return True


def test_nlp_accuracy_50_vietnamese_queries():
    """Đánh giá độ chính xác NLP trên 50 câu hỏi thực tế (yêu cầu >= 70%)."""
    assert len(NLP_50_TEST_CASES) == 50

    async def _run_all():
        passed = 0
        failed_cases = []
        for idx, (prompt, expected) in enumerate(NLP_50_TEST_CASES, 1):
            criteria, engine = await extract_criteria_from_prompt_async(prompt)
            if _check_case_match(criteria, expected):
                passed += 1
            else:
                failed_cases.append((idx, prompt, expected, criteria.model_dump()))
        return passed, failed_cases

    passed, failed_cases = asyncio.run(_run_all())
    accuracy = (passed / len(NLP_50_TEST_CASES)) * 100.0

    print(f"\n[TE9C67A NLP BENCHMARK] Đạt: {passed}/50 câu ({accuracy:.1f}%)")
    if failed_cases:
        print(f"Số câu chưa khớp hoàn toàn: {len(failed_cases)}")
        for idx, p, exp, got in failed_cases[:5]:
            print(f"  - #{idx}: '{p}' | Expected={exp} | Got={got}")

    assert accuracy >= 70.0, f"Độ chính xác NLP ({accuracy:.1f}%) thấp hơn ngưỡng tối thiểu 70%!"