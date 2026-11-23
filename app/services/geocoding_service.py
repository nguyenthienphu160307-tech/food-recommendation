import re
import unicodedata
from typing import Optional, Dict, Any, Tuple
import urllib.request
import urllib.parse
import json


class GeocodingService:
    """
    Service Geocoding chuyển đổi tên khu vực/quận sang tọa độ GPS (Task TSK-18 / PBI-08):
    1. Tích hợp Từ điển Tọa độ Nội bộ (Offline Local Gazetteer) phản hồi siêu tốc (< 10ms).
    2. Hỗ trợ đầy đủ 24 quận huyện và TP Thủ Đức (TP.HCM), các quận trung tâm Hà Nội, cùng các Landmark ẩm thực nổi tiếng.
    3. Hỗ trợ chuẩn hóa ngôn ngữ tiếng Việt (loại bỏ từ nối, dấu, tiền tố 'quận', 'q.', 'ở', 'tại', 'gần').
    4. Fallback trực tuyến sang OpenStreetMap (Nominatim) khi người dùng nhập địa chỉ cụ thể ngoài từ điển.
    5. Tự động bóc tách thực thể địa danh và tiêu chí ẩm thực (cuisine, budget, parking) từ câu chat tự nhiên.
    """

    # Tọa độ tâm mặc định của trung tâm TP.HCM (Quận 1)
    DEFAULT_CENTER: Tuple[float, float] = (10.7769, 106.7009)

    # 1. Từ điển Địa danh Nội bộ (Offline Gazetteer Cache)
    GAZETTEER: Dict[str, Dict[str, Any]] = {
        # --- TP. HỒ CHÍ MINH (24 Quận Huyện & TP Thủ Đức) ---
        "quan 1": {"lat": 10.7769, "lng": 106.7009, "formatted": "Quận 1, TP. Hồ Chí Minh"},
        "q1": {"lat": 10.7769, "lng": 106.7009, "formatted": "Quận 1, TP. Hồ Chí Minh"},
        "quan 3": {"lat": 10.7844, "lng": 106.6843, "formatted": "Quận 3, TP. Hồ Chí Minh"},
        "q3": {"lat": 10.7844, "lng": 106.6843, "formatted": "Quận 3, TP. Hồ Chí Minh"},
        "quan 4": {"lat": 10.7578, "lng": 106.7013, "formatted": "Quận 4, TP. Hồ Chí Minh"},
        "q4": {"lat": 10.7578, "lng": 106.7013, "formatted": "Quận 4, TP. Hồ Chí Minh"},
        "quan 5": {"lat": 10.7540, "lng": 106.6634, "formatted": "Quận 5, TP. Hồ Chí Minh"},
        "q5": {"lat": 10.7540, "lng": 106.6634, "formatted": "Quận 5, TP. Hồ Chí Minh"},
        "quan 6": {"lat": 10.7481, "lng": 106.6352, "formatted": "Quận 6, TP. Hồ Chí Minh"},
        "q6": {"lat": 10.7481, "lng": 106.6352, "formatted": "Quận 6, TP. Hồ Chí Minh"},
        "quan 7": {"lat": 10.7340, "lng": 106.7218, "formatted": "Quận 7, TP. Hồ Chí Minh"},
        "q7": {"lat": 10.7340, "lng": 106.7218, "formatted": "Quận 7, TP. Hồ Chí Minh"},
        "quan 8": {"lat": 10.7241, "lng": 106.6286, "formatted": "Quận 8, TP. Hồ Chí Minh"},
        "q8": {"lat": 10.7241, "lng": 106.6286, "formatted": "Quận 8, TP. Hồ Chí Minh"},
        "quan 10": {"lat": 10.7679, "lng": 106.6669, "formatted": "Quận 10, TP. Hồ Chí Minh"},
        "q10": {"lat": 10.7679, "lng": 106.6669, "formatted": "Quận 10, TP. Hồ Chí Minh"},
        "quan 11": {"lat": 10.7629, "lng": 106.6504, "formatted": "Quận 11, TP. Hồ Chí Minh"},
        "q11": {"lat": 10.7629, "lng": 106.6504, "formatted": "Quận 11, TP. Hồ Chí Minh"},
        "quan 12": {"lat": 10.8672, "lng": 106.6414, "formatted": "Quận 12, TP. Hồ Chí Minh"},
        "q12": {"lat": 10.8672, "lng": 106.6414, "formatted": "Quận 12, TP. Hồ Chí Minh"},
        "binh thanh": {"lat": 10.8016, "lng": 106.7115, "formatted": "Quận Bình Thạnh, TP. Hồ Chí Minh"},
        "go vap": {"lat": 10.8388, "lng": 106.6653, "formatted": "Quận Gò Vấp, TP. Hồ Chí Minh"},
        "phu nhuan": {"lat": 10.7992, "lng": 106.6803, "formatted": "Quận Phú Nhuận, TP. Hồ Chí Minh"},
        "tan binh": {"lat": 10.8015, "lng": 106.6526, "formatted": "Quận Tân Bình, TP. Hồ Chí Minh"},
        "tan phu": {"lat": 10.7900, "lng": 106.6280, "formatted": "Quận Tân Phú, TP. Hồ Chí Minh"},
        "binh tan": {"lat": 10.7654, "lng": 106.6038, "formatted": "Quận Bình Tân, TP. Hồ Chí Minh"},
        "thu duc": {"lat": 10.8494, "lng": 106.7537, "formatted": "TP. Thủ Đức, TP. Hồ Chí Minh"},
        "nha be": {"lat": 10.6953, "lng": 106.7289, "formatted": "Huyện Nhà Bè, TP. Hồ Chí Minh"},
        "hoc mon": {"lat": 10.8839, "lng": 106.5872, "formatted": "Huyện Hóc Môn, TP. Hồ Chí Minh"},
        "cu chi": {"lat": 10.9731, "lng": 106.4938, "formatted": "Huyện Củ Chi, TP. Hồ Chí Minh"},
        "binh chanh": {"lat": 10.6874, "lng": 106.5939, "formatted": "Huyện Bình Chánh, TP. Hồ Chí Minh"},
        "can gio": {"lat": 10.4114, "lng": 106.9546, "formatted": "Huyện Cần Giờ, TP. Hồ Chí Minh"},

        # --- LANDMARK & ĐỊA DANH ẨM THỰC NỔI TIẾNG (TP.HCM) ---
        "ho con rua": {"lat": 10.7828, "lng": 106.6958, "formatted": "Hồ Con Rùa, Phường 6, Quận 3, TP.HCM"},
        "pho di bo nguyen hue": {"lat": 10.7738, "lng": 106.7048, "formatted": "Phố đi bộ Nguyễn Huệ, Quận 1, TP.HCM"},
        "nguyen hue": {"lat": 10.7738, "lng": 106.7048, "formatted": "Đường Nguyễn Huệ, Quận 1, TP.HCM"},
        "cho ben thanh": {"lat": 10.7725, "lng": 106.6980, "formatted": "Chợ Bến Thành, Quận 1, TP.HCM"},
        "ben thanh": {"lat": 10.7725, "lng": 106.6980, "formatted": "Khu vực Bến Thành, Quận 1, TP.HCM"},
        "landmark 81": {"lat": 10.7950, "lng": 106.7219, "formatted": "Landmark 81, Vinhomes Central Park, Bình Thạnh"},
        "bui vien": {"lat": 10.7675, "lng": 106.6934, "formatted": "Phố Tây Bùi Viện, Quận 1, TP.HCM"},
        "pho tay": {"lat": 10.7675, "lng": 106.6934, "formatted": "Phố Tây Bùi Viện, Quận 1, TP.HCM"},
        "phan van tri": {"lat": 10.8250, "lng": 106.6850, "formatted": "Đường Phan Văn Trị, Gò Vấp, TP.HCM"},
        "quang trung": {"lat": 10.8350, "lng": 106.6650, "formatted": "Đường Quang Trung, Gò Vấp, TP.HCM"},
        "thao cam vien": {"lat": 10.7875, "lng": 106.7053, "formatted": "Thảo Cầm Viên, Quận 1, TP.HCM"},
        "tan son nhat": {"lat": 10.8185, "lng": 106.6588, "formatted": "Sân bay Tân Sơn Nhất, Quận Tân Bình, TP.HCM"},
        "cho lon": {"lat": 10.7510, "lng": 106.6540, "formatted": "Khu ẩm thực Chợ Lớn, Quận 5, TP.HCM"},

        # --- HÀ NỘI (Các Quận Trung Tâm) ---
        "hoan kiem": {"lat": 21.0285, "lng": 105.8542, "formatted": "Quận Hoàn Kiếm, Hà Nội"},
        "ba dinh": {"lat": 21.0341, "lng": 105.8242, "formatted": "Quận Ba Đình, Hà Nội"},
        "dong da": {"lat": 21.0181, "lng": 105.8268, "formatted": "Quận Đống Đa, Hà Nội"},
        "hai ba trung": {"lat": 21.0069, "lng": 105.8524, "formatted": "Quận Hai Bà Trưng, Hà Nội"},
        "cau giay": {"lat": 21.0313, "lng": 105.7940, "formatted": "Quận Cầu Giấy, Hà Nội"},
        "tay ho": {"lat": 21.0583, "lng": 105.8236, "formatted": "Quận Tây Hồ, Hà Nội"},
        "thanh xuan": {"lat": 20.9937, "lng": 105.8083, "formatted": "Quận Thanh Xuân, Hà Nội"}
    }

    @staticmethod
    def strip_accents(text: str) -> str:
        """Loại bỏ dấu tiếng Việt để phục vụ so khớp mờ linh hoạt"""
        if not text:
            return ""
        text = text.replace("đ", "d").replace("Đ", "d")
        normalized = unicodedata.normalize("NFD", text)
        result = "".join(ch for ch in normalized if unicodedata.category(ch) != "Mn")
        return result.lower().strip()

    @classmethod
    def clean_query(cls, text: str) -> str:
        """
        Chuẩn hóa chuỗi truy vấn địa danh:
        - Xóa các từ phụ ngữ: 'ở', 'tại', 'quanh', 'gần', 'khu vực', 'quận', 'q.', 'huyện'.
        - Xóa dấu chấm câu và khoảng trắng dư thừa.
        """
        s = cls.strip_accents(text)
        # Bỏ dấu câu
        s = re.sub(r"[^\w\s]", " ", s)
        # Bỏ tiền tố thường gặp trong câu tìm kiếm tiếng Việt
        prefixes = [
            r"^\s*tim\s+quan\s+.*?\s+(o|tai|quanh|gan|khu\s+vuc)\s+",
            r"^\s*(o|tai|quanh|gan|khu\s+vuc)\s+",
            r"^\s*quan\s+",
            r"^\s*q\s+",
            r"^\s*huyen\s+",
            r"^\s*tp\s+",
            r"^\s*thanh\s+pho\s+"
        ]
        for p in prefixes:
            s = re.sub(p, "", s)
        return re.sub(r"\s+", " ", s).strip()

    @classmethod
    def extract_location_from_text(cls, text: str) -> Optional[str]:
        """
        Tự động bóc tách tên địa danh / khu vực từ câu chat tự nhiên tiếng Việt.
        Ví dụ:
        - "Tìm quán lẩu ở Bình Thạnh" -> "Bình Thạnh"
        - "Muốn ăn đồ nướng quanh Quận 1 có phòng riêng" -> "Quận 1"
        - "Cà phê gần Hồ Con Rùa" -> "Hồ Con Rùa"
        """
        if not text:
            return None

        # 1. Quét tìm các địa danh ưu tiên từ từ điển (dài nhất trước)
        lower_raw = text.lower()
        cleaned_raw = cls.strip_accents(lower_raw)

        # Sắp xếp từ khóa gazetteer theo độ dài giảm dần
        sorted_keys = sorted(cls.GAZETTEER.keys(), key=lambda k: len(k), reverse=True)
        for key in sorted_keys:
            # Kiểm tra từ khóa xuất hiện nguyên vẹn dạng từ đơn/cụm từ
            pattern = r"\b" + re.escape(key) + r"\b"
            if re.search(pattern, cleaned_raw):
                return cls.GAZETTEER[key]["formatted"].split(",")[0].strip()

        # 2. Quét biểu thức chính quy nhận dạng địa danh sau các giới từ chỉ vị trí
        loc_patterns = [
            r"(?:ở|tại|quanh|gần|khu vực)\s+(quận\s+\d+|quận\s+[a-zA-Z\u00C0-\u024F\u1E00-\u1EFF\s]+)",
            r"(quận\s+\d+|quận\s+[a-zA-Z\u00C0-\u024F\u1E00-\u1EFF]+)",
            r"(q\.\s*\d+|q\s*\d+)"
        ]
        for pat in loc_patterns:
            m = re.search(pat, text, re.IGNORECASE)
            if m:
                extracted = m.group(1).strip()
                return extracted

        return None

    @classmethod
    def geocode(cls, location_name: str, enable_online_fallback: bool = True) -> Dict[str, Any]:
        """
        Chuyển đổi tên khu vực / quận sang tọa độ GPS (TSK-18):
        - Bước 1: Tra cứu trong Offline Gazetteer Cache (< 10ms).
        - Bước 2: So khớp tiền tố / hậu tố linh hoạt.
        - Bước 3: Nếu không thấy và enable_online_fallback=True -> gọi OpenStreetMap Nominatim.
        """
        if not location_name or not location_name.strip():
            return {
                "location_name": "",
                "latitude": cls.DEFAULT_CENTER[0],
                "longitude": cls.DEFAULT_CENTER[1],
                "formatted_address": "Trung tâm TP. Hồ Chí Minh (Mặc định)",
                "is_found": False,
                "source": "default"
            }

        original_input = location_name.strip()
        stripped = cls.strip_accents(original_input)

        # 1. So khớp trực tiếp chính xác
        if stripped in cls.GAZETTEER:
            item = cls.GAZETTEER[stripped]
            return {
                "location_name": original_input,
                "latitude": item["lat"],
                "longitude": item["lng"],
                "formatted_address": item["formatted"],
                "is_found": True,
                "source": "local_gazetteer"
            }

        # 2. Thử chuẩn hóa (bỏ 'quan', 'huyen', 'o', 'tai'...)
        cleaned = cls.clean_query(original_input)
        if cleaned in cls.GAZETTEER:
            item = cls.GAZETTEER[cleaned]
            return {
                "location_name": original_input,
                "latitude": item["lat"],
                "longitude": item["lng"],
                "formatted_address": item["formatted"],
                "is_found": True,
                "source": "local_gazetteer"
            }

        # Thử thêm tiền tố 'quan ' nếu chuỗi là số hoặc tên quận đơn (ví dụ '1', 'binh thanh')
        if f"quan {cleaned}" in cls.GAZETTEER:
            item = cls.GAZETTEER[f"quan {cleaned}"]
            return {
                "location_name": original_input,
                "latitude": item["lat"],
                "longitude": item["lng"],
                "formatted_address": item["formatted"],
                "is_found": True,
                "source": "local_gazetteer"
            }

        # Thử duyệt qua các key xem có key nào là substring không
        for key, item in cls.GAZETTEER.items():
            if key in stripped or stripped in key:
                return {
                    "location_name": original_input,
                    "latitude": item["lat"],
                    "longitude": item["lng"],
                    "formatted_address": item["formatted"],
                    "is_found": True,
                    "source": "local_gazetteer_partial"
                }

        # 3. Fallback trực tuyến sang OpenStreetMap Nominatim (nếu cho phép)
        if enable_online_fallback:
            try:
                query = urllib.parse.quote(f"{original_input}, Việt Nam")
                url = f"https://nominatim.openstreetmap.org/search?q={query}&format=json&limit=1"
                req = urllib.request.Request(
                    url,
                    headers={"User-Agent": "SmartDiningApp/1.0 (contact: student@foodai.vn)"}
                )
                with urllib.request.urlopen(req, timeout=2.0) as resp:
                    if resp.status == 200:
                        data = json.loads(resp.read().decode("utf-8"))
                        if data and len(data) > 0:
                            top = data[0]
                            return {
                                "location_name": original_input,
                                "latitude": float(top["lat"]),
                                "longitude": float(top["lon"]),
                                "formatted_address": top.get("display_name", original_input),
                                "is_found": True,
                                "source": "openstreetmap_nominatim"
                            }
            except Exception:
                pass  # Khi offline hoặc timeout thì dùng fallback an toàn

        # 4. Fallback mặc định an toàn về trung tâm TP.HCM
        return {
            "location_name": original_input,
            "latitude": cls.DEFAULT_CENTER[0],
            "longitude": cls.DEFAULT_CENTER[1],
            "formatted_address": f"{original_input} (Tọa độ tham chiếu TP.HCM)",
            "is_found": False,
            "source": "fallback_default"
        }

    @classmethod
    def extract_full_criteria(cls, text: str) -> Dict[str, Any]:
        """
        Bóc tách toàn diện tiêu chí từ câu chat tự nhiên:
        - Địa danh & Tọa độ GPS (Geocoding)
        - Ẩm thực (Cuisine)
        - Ngân sách (Budget)
        - Tiện ích (Parking, Private room, Vegetarian)
        """
        if not text:
            return {}

        lower = text.lower()
        cleaned_no_accent = cls.strip_accents(lower)

        # 1. Trích xuất địa danh & Geocoding
        extracted_loc = cls.extract_location_from_text(text)
        geo_result = cls.geocode(extracted_loc or "") if extracted_loc else None

        # 2. Trích xuất loại ẩm thực
        cuisine = None
        cuisines_map = {
            "lẩu": ["lau", "hotpot", "lau nam", "lau bo", "lau thai", "lau ca"],
            "nướng": ["nuong", "bbq", "thit nuong", "nuong than", "nuong ngoai troi"],
            "cà phê": ["ca phe", "cafe", "coffee", "tra sua", "nuoc ep"],
            "chay": ["chay", "thuan chay", "vegan", "vegetarian"],
            "hải sản": ["hai san", "seafood", "cua", "oc", "tom", "ca"],
            "sushi": ["sushi", "sashimi", "nhat ban", "do nhat"],
            "cơm": ["com tam", "com van phong", "com niu", "com ga"]
        }
        for c_label, synonyms in cuisines_map.items():
            if any(syn in cleaned_no_accent for syn in synonyms):
                cuisine = c_label
                break

        # 3. Trích xuất ngân sách (VD: "dưới 200k", "tầm 300.000", "500k")
        budget = None
        # Ưu tiên tìm số có đơn vị tiền tệ rõ ràng (k, nghìn, tr, triệu, vnd, đ)
        budget_matches = re.finditer(r"(\d+[\.,]?\d*)\s*(k|nghin|ngàn|ngan|tram|trăm|trieu|triệu|tr|vnd|đ|dong|đồng)", cleaned_no_accent)
        for bm in budget_matches:
            try:
                num_str = bm.group(1).replace(".", "").replace(",", "")
                val = float(num_str)
                unit = bm.group(2).lower()
                if unit in ["k", "nghin", "ngan"]:
                    val *= 1000
                elif unit in ["trieu", "triệu", "tr"]:
                    val *= 1000000
                elif unit in ["tram", "trăm"]:
                    val *= 100000
                if val >= 20000:
                    budget = int(val)
                    break
            except Exception:
                continue

        # Nếu chưa tìm thấy, tìm số sau các từ khóa chỉ ngân sách (tầm, dưới, khoảng, giá)
        if not budget:
            kw_match = re.search(r"(?:tam|duoi|khoang|gia|ngan sach|chi phi)\s*(\d+[\.,]?\d*)\s*(k|nghin|ngan|vnd|đ)?", cleaned_no_accent)
            if kw_match:
                try:
                    num_str = kw_match.group(1).replace(".", "").replace(",", "")
                    val = float(num_str)
                    unit = (kw_match.group(2) or "").strip().lower()
                    if unit in ["k", "nghin", "ngan"]:
                        val *= 1000
                    elif val < 1000:
                        val *= 1000
                    if val >= 20000:
                        budget = int(val)
                except Exception:
                    pass

        # 4. Trích xuất tiện ích
        has_parking = any(w in cleaned_no_accent for w in ["dau xe", "do xe", "giu xe", "bai xe", "oto", "o to"])
        has_private_room = any(w in cleaned_no_accent for w in ["phong rieng", "vip", "kin dao", "rieng tu"])
        has_outdoor = any(w in cleaned_no_accent for w in ["ngoai troi", "thoang mat", "san vuon", "rooftop"])
        vegetarian_support = any(w in cleaned_no_accent for w in ["mon chay", "an chay", "do chay"])

        return {
            "location_text": extracted_loc,
            "latitude": geo_result["latitude"] if geo_result else None,
            "longitude": geo_result["longitude"] if geo_result else None,
            "formatted_address": geo_result["formatted_address"] if geo_result else None,
            "cuisine": cuisine,
            "budget": budget,
            "has_parking": has_parking,
            "other_conditions": {
                "has_parking": has_parking,
                "has_private_room": has_private_room,
                "has_outdoor": has_outdoor,
                "vegetarian_support": vegetarian_support
            }
        }
