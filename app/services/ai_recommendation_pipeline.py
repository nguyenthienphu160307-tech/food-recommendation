from typing import Any, Dict, List, Optional, Tuple
from sqlalchemy import or_
from sqlalchemy.orm import Session, joinedload

from app.models.restaurant import Restaurant, RestaurantAmenity
from app.schemas.ai_search import DiningCriteriaSchema
from app.services.geo_service import calculate_bounding_box, calculate_haversine_distance
from app.services.geocoding_service import GeocodingService
from app.services.ranking_service import RankingEngine


class AIRecommendationPipeline:
    """
    Task TE9C670: Chuyển đổi SearchCriteria (Module 2) thành tham số Spatial & Filter,
    xếp hạng bằng RankingEngine.rank_and_sort (Module 4) và trả về Top N nhà hàng.
    """

    @staticmethod
    def resolve_coordinates(
        criteria: DiningCriteriaSchema,
        user_lat: Optional[float],
        user_lng: Optional[float],
    ) -> Tuple[float, float, str]:
        if criteria.location_text:
            geo = GeocodingService.geocode(criteria.location_text)
            lat_val = geo.get("latitude") if geo else None
            lng_val = geo.get("longitude") if geo else None
            if lat_val is not None and lng_val is not None:
                return float(lat_val), float(lng_val), f"geocoded:{criteria.location_text}"

        if user_lat is not None and user_lng is not None:
            return float(user_lat), float(user_lng), "user_gps"

        default_lat, default_lng = GeocodingService.DEFAULT_CENTER
        return default_lat, default_lng, "default_hcm_q1"

    @staticmethod
    def _serialize_candidate(r: Restaurant, dist_km: float) -> Dict[str, Any]:
        cover_img = None
        if r.images:
            cover_img = next((img.image_url for img in r.images if img.is_cover), None)
            if not cover_img:
                cover_img = r.images[0].image_url

        return {
            "id": r.id,
            "name": r.name,
            "address": r.address,
            "cuisine_type": r.cuisine_type,
            "min_price": r.min_price,
            "max_price": r.max_price,
            "rating": r.avg_rating or 0.0,
            "latitude": r.latitude,
            "longitude": r.longitude,
            "distance_km": round(dist_km, 2),
            "cover_image_url": cover_img,
            "amenities": {
                "has_parking": r.amenities.has_parking if r.amenities else False,
                "has_private_room": r.amenities.has_private_room if r.amenities else False,
                "has_outdoor": r.amenities.has_outdoor if r.amenities else False,
                "pet_friendly": r.amenities.pet_friendly if r.amenities else False,
                "vegetarian_support": r.amenities.vegetarian_support if r.amenities else False,
            },
        }

    @classmethod
    def query_and_rank(
        cls,
        db: Session,
        criteria: DiningCriteriaSchema,
        user_lat: Optional[float] = None,
        user_lng: Optional[float] = None,
        radius_km: float = 5.0,
        top_n: int = 5,
    ) -> Dict[str, Any]:
        center_lat, center_lng, loc_source = cls.resolve_coordinates(criteria, user_lat, user_lng)
        other = criteria.other_conditions

        required_amenities = {
            "has_parking": bool(criteria.has_parking),
            "has_private_room": bool(other.has_private_room) if other else False,
            "pet_friendly": bool(other.pet_friendly) if other else False,
            "vegetarian_support": bool(other.vegetarian_support) if other else False,
            "has_outdoor": bool(other.has_outdoor) if other else False,
        }

        bbox = calculate_bounding_box(center_lat, center_lng, radius_km)
        query = (
            db.query(Restaurant)
            .options(joinedload(Restaurant.images), joinedload(Restaurant.amenities))
            .filter(
                Restaurant.status == "active",
                Restaurant.latitude.between(bbox.min_lat, bbox.max_lat),
                Restaurant.longitude.between(bbox.min_lng, bbox.max_lng),
            )
        )

        conditions = []
        if criteria.cuisine:
            c_raw = criteria.cuisine.strip()
            c_lower = c_raw.lower()
            conditions = [
                Restaurant.cuisine_type.ilike(f"%{c_raw}%"),
                Restaurant.name.ilike(f"%{c_raw}%"),
            ]
            if "bbq" in c_lower or "nướng" in c_lower or "hàn quốc" in c_lower:
                conditions.extend([
                    Restaurant.cuisine_type.ilike("%lẩu nướng%"),
                    Restaurant.cuisine_type.ilike("%bbq%"),
                    Restaurant.cuisine_type.ilike("%món hàn%"),
                    Restaurant.name.ilike("%bbq%"),
                    Restaurant.name.ilike("%nướng%"),
                ])
            elif "lẩu" in c_lower:
                conditions.extend([
                    Restaurant.cuisine_type.ilike("%lẩu%"),
                    Restaurant.name.ilike("%lẩu%"),
                ])
            elif "cơm tấm" in c_lower:
                conditions.extend([
                    Restaurant.name.ilike("%cơm tấm%"),
                    Restaurant.cuisine_type.ilike("%cơm tấm%"),
                ])
            elif "âu" in c_lower or "pizza" in c_lower or "steak" in c_lower:
                conditions.extend([
                    Restaurant.cuisine_type.ilike("%món âu%"),
                    Restaurant.name.ilike("%pizza%"),
                    Restaurant.name.ilike("%steak%"),
                ])
            elif "nhật" in c_lower or "sushi" in c_lower:
                conditions.extend([
                    Restaurant.cuisine_type.ilike("%nhật%"),
                    Restaurant.name.ilike("%sushi%"),
                ])
            elif "hoa" in c_lower or "dimsum" in c_lower:
                conditions.extend([
                    Restaurant.cuisine_type.ilike("%hoa%"),
                    Restaurant.name.ilike("%dim tu tac%"),
                    Restaurant.name.ilike("%san fu lou%"),
                ])
            elif "cà phê" in c_lower or "cafe" in c_lower:
                conditions.extend([
                    Restaurant.cuisine_type.ilike("%cà phê%"),
                    Restaurant.name.ilike("%coffee%"),
                ])
            elif "hải sản" in c_lower:
                conditions.extend([
                    Restaurant.cuisine_type.ilike("%hải sản%"),
                    Restaurant.name.ilike("%hải sản%"),
                    Restaurant.name.ilike("%ốc%"),
                ])
            query = query.filter(or_(*conditions))

        if criteria.budget:
            query = query.filter(Restaurant.min_price <= criteria.budget)

        if any(required_amenities.values()):
            query = query.join(RestaurantAmenity, Restaurant.id == RestaurantAmenity.restaurant_id)
            if required_amenities["has_parking"]:
                query = query.filter(RestaurantAmenity.has_parking.is_(True))
            if required_amenities["has_private_room"]:
                query = query.filter(RestaurantAmenity.has_private_room.is_(True))
            if required_amenities["pet_friendly"]:
                query = query.filter(RestaurantAmenity.pet_friendly.is_(True))
            if required_amenities["vegetarian_support"]:
                query = query.filter(RestaurantAmenity.vegetarian_support.is_(True))
            if required_amenities["has_outdoor"]:
                query = query.filter(RestaurantAmenity.has_outdoor.is_(True))

        candidates: List[Dict[str, Any]] = []
        for r in query.all():
            dist_km = calculate_haversine_distance(center_lat, center_lng, r.latitude, r.longitude)
            if dist_km <= radius_km:
                candidates.append(cls._serialize_candidate(r, dist_km))

        # Nới lỏng bộ lọc nếu điều kiện tiện ích quá ngặt nghèo dẫn đến 0 kết quả
        if not candidates and any(required_amenities.values()):
            relaxed_q = (
                db.query(Restaurant)
                .options(joinedload(Restaurant.images), joinedload(Restaurant.amenities))
                .filter(
                    Restaurant.status == "active",
                    Restaurant.latitude.between(bbox.min_lat, bbox.max_lat),
                    Restaurant.longitude.between(bbox.min_lng, bbox.max_lng),
                )
            )
            if criteria.cuisine and conditions:
                relaxed_q = relaxed_q.filter(or_(*conditions))
            for r in relaxed_q.all():
                dist_km = calculate_haversine_distance(center_lat, center_lng, r.latitude, r.longitude)
                if dist_km <= radius_km:
                    candidates.append(cls._serialize_candidate(r, dist_km))

        ranked = RankingEngine.rank_and_sort(
            restaurants=candidates,
            radius_km=radius_km,
            target_cuisine=criteria.cuisine,
            target_budget=criteria.budget,
            required_amenities=required_amenities,
        )

        return {
            "resolved_location": {
                "latitude": center_lat,
                "longitude": center_lng,
                "radius_km": radius_km,
                "source": loc_source,
            },
            "total_candidates": len(candidates),
            "recommendations": ranked[:top_n],
        }