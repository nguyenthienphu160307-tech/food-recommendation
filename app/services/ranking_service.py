"""
Module: Weighted Ranking Engine (TE9C66D)
Description: Thuật toán chấm điểm và xếp hạng nhà hàng dựa trên hệ số đa tiêu chí (BR-06).
"""

from typing import List, Dict, Any

class RankingEngine:
    """
    Bộ máy chấm điểm nhà hàng (Weighted Ranking).
    Tính điểm tổng hợp (Max 100 điểm) dựa trên 4 thành phần:
    - 40%: Độ khớp loại món (Cuisine) & Giá (Budget)
    - 30%: Khoảng cách gần (Distance)
    - 20%: Điểm đánh giá (Rating)
    - 10%: Tiện ích khớp (Amenities)
    """

    WEIGHT_CUISINE_BUDGET = 40.0
    WEIGHT_DISTANCE = 30.0
    WEIGHT_RATING = 20.0
    WEIGHT_AMENITIES = 10.0

    @classmethod
    def calculate_score(
        cls,
        restaurant: Dict[str, Any],
        radius_km: float,
        target_cuisine: str = None,
        target_budget: int = None,
        required_amenities: Dict[str, bool] = None
    ) -> float:
        total_score = 0.0

        # ---------------------------------------------------------
        # 1. Điểm khoảng cách (Max 30đ)
        # Sử dụng nội suy tuyến tính: Khoảng cách = 0 -> 30 điểm. Khoảng cách = radius_km -> 0 điểm.
        # ---------------------------------------------------------
        dist_km = restaurant.get("distance_km", radius_km)
        if dist_km <= radius_km and radius_km > 0:
            total_score += cls.WEIGHT_DISTANCE * (1.0 - (dist_km / radius_km))

        # ---------------------------------------------------------
        # 2. Điểm đánh giá (Max 20đ)
        # Rating 5.0 -> 20 điểm. Rating 0.0 -> 0 điểm.
        # ---------------------------------------------------------
        rating = restaurant.get("rating", 0.0)
        total_score += (rating / 5.0) * cls.WEIGHT_RATING

        # ---------------------------------------------------------
        # 3. Điểm khớp Món & Giá (Max 40đ)
        # Chia đều: 20đ cho Món (Cuisine) và 20đ cho Giá (Budget)
        # ---------------------------------------------------------
        cuisine_score = 20.0
        budget_score = 20.0

        # Kiểm tra khớp loại món
        if target_cuisine and target_cuisine.strip() and target_cuisine.lower() != "all":
            res_cuisine = restaurant.get("category", "")
            if not res_cuisine or target_cuisine.lower() not in res_cuisine.lower():
                cuisine_score = 0.0

        # Kiểm tra khớp ngân sách
        if target_budget:
            min_price = restaurant.get("min_price", 0)
            max_price = restaurant.get("max_price", 0)
            if min_price > target_budget:
                budget_score = 0.0  # Món rẻ nhất vẫn vượt ngân sách -> 0 điểm
            elif max_price > target_budget:
                budget_score = 10.0 # Có món hợp ngân sách nhưng một số món vượt -> 10 điểm

        total_score += (cuisine_score + budget_score)

        # ---------------------------------------------------------
        # 4. Điểm tiện ích (Max 10đ)
        # ---------------------------------------------------------
        amenities_score = cls.WEIGHT_AMENITIES
        if required_amenities:
            # Chỉ lấy các tiện ích mà User thực sự yêu cầu (giá trị True)
            req_keys = [k for k, v in required_amenities.items() if v]
            total_req = len(req_keys)
            if total_req > 0:
                res_amenities = restaurant.get("amenities", {})
                # Đếm số lượng tiện ích nhà hàng đáp ứng được
                matched_req = sum(1 for k in req_keys if res_amenities.get(k))
                amenities_score = (matched_req / total_req) * cls.WEIGHT_AMENITIES

        total_score += amenities_score
        return round(total_score, 1)

    @classmethod
    def rank_and_sort(
        cls,
        restaurants: List[Dict[str, Any]],
        radius_km: float = 5.0,
        target_cuisine: str = None,
        target_budget: int = None,
        required_amenities: Dict[str, bool] = None
    ) -> List[Dict[str, Any]]:
        """
        Tính điểm (Match Score) cho toàn bộ nhà hàng và sắp xếp từ cao xuống thấp.
        Sẽ được gọi ở module Filter/Ranking tiếp theo (TE9C66E).
        """
        for r in restaurants:
            r["match_score"] = cls.calculate_score(
                restaurant=r,
                radius_km=radius_km,
                target_cuisine=target_cuisine,
                target_budget=target_budget,
                required_amenities=required_amenities
            )

        # Xếp hạng giảm dần theo match_score
        restaurants.sort(key=lambda x: x.get("match_score", 0), reverse=True)
        return restaurants