import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def run_prompt_schema_tests():
    print("================================================================")
    print("   KIỂM THỬ TASK TE9C65A: PROMPT TEMPLATE & JSON SCHEMA (NLP)   ")
    print("================================================================\n")

    # 1. Kiểm tra API lấy JSON Schema & Prompt Template
    res_schema = client.get("/api/search/prompt-schema")
    assert res_schema.status_code == 200
    schema_data = res_schema.json()
    props = schema_data["json_schema"]["properties"]
    for required_field in ["location_text", "cuisine", "budget", "has_parking", "other_conditions"]:
        assert required_field in props, f"Thiếu trường {required_field} trong JSON Schema!"
    print("[PASS 1] JSON Schema chứa đầy đủ: location_text, cuisine, budget, has_parking, other_conditions.")

    q1 = "Nhóm 4 người muốn ăn đồ nướng ở Quận 1 có chỗ đậu ô tô dưới 300k/người, cần phòng riêng"
    res1 = client.post("/api/search/extract-criteria", json={"prompt": q1})
    assert res1.status_code == 200
    c1 = res1.json()["extracted_criteria"]
    assert c1["location_text"] == "Quận 1"
    assert c1["cuisine"] == "BBQ Hàn Quốc"
    assert c1["budget"] == 300000
    assert c1["has_parking"] is True
    assert c1["other_conditions"]["has_private_room"] is True
    assert c1["other_conditions"]["group_size"] == 4
    print(f"[PASS 2] Bóc tách thành công câu hỏi 1:\n -> {c1}")

    q2 = "Tìm quán chay thanh đạm ở Gò Vấp tầm 150 nghìn cho phép mang thú cưng"
    res2 = client.post("/api/search/extract-criteria", json={"prompt": q2})
    assert res2.status_code == 200
    c2 = res2.json()["extracted_criteria"]
    assert c2["location_text"] == "Gò Vấp"
    assert c2["cuisine"] == "Món Chay"
    assert c2["budget"] == 150000
    assert c2["other_conditions"]["vegetarian_support"] is True
    assert c2["other_conditions"]["pet_friendly"] is True
    print(f"[PASS 3] Bóc tách thành công câu hỏi 2:\n -> {c2}")

    print("\n>>> TẤT CẢ KỊCH BẢN KIỂM THỬ TE9C65A ĐỀU VƯỢT QUA (ALL PASSED)! <<<")


if __name__ == "__main__":
    run_prompt_schema_tests()