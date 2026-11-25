"""
Seed script: Khởi tạo dữ liệu mẫu 50 nhà hàng / quán ăn tại TP.HCM.
Các khu vực: Quận 1 (15), Quận 3 (10), Bình Thạnh (13), TP. Thủ Đức (12).
Mỗi quán có đầy đủ:
- Tọa độ GPS (WGS84 lat/lng)
- Tiện ích (RestaurantAmenity)
- Danh mục thực đơn & Món ăn (RestaurantMenu, MenuItem)
- Thư viện hình ảnh (RestaurantImage, có đánh dấu is_cover)
Đồng thời tạo file database/seed_restaurants.sql để import nhanh vào MySQL.
"""

import sys
import os
from datetime import datetime

# Đảm bảo import được module app.*
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
sys.path.insert(0, PROJECT_ROOT)

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from app.core.database import SessionLocal, engine, Base
import app.models
from app.models.restaurant import (
    Restaurant,
    RestaurantAmenity,
    RestaurantMenu,
    MenuItem,
    RestaurantImage,
)

RESTAURANTS_DATA = [
    # =========================================================================
    # KHU VỰC 1: QUẬN 1 (15 QUÁN)
    # =========================================================================
    {
        "name": "Pizza 4P's Bến Thành",
        "description": "Thương hiệu pizza phô mai tươi thủ công nướng lò củi nổi tiếng bậc nhất Sài Gòn, không gian sang trọng và ấm cúng.",
        "address": "8 Thủ Khoa Huân, Phường Bến Thành, Quận 1, TP. Hồ Chí Minh",
        "phone_number": "02836220500",
        "cuisine_type": "Món Âu",
        "latitude": 10.772500,
        "longitude": 106.698000,
        "min_price": 150000.0,
        "max_price": 450000.0,
        "open_hours": "10:00 - 23:00",
        "avg_rating": 4.8,
        "total_reviews": 850,
        "amenities": {
            "has_parking": True,
            "has_private_room": True,
            "has_outdoor": False,
            "pet_friendly": False,
            "vegetarian_support": True,
        },
        "menus": [
            {
                "name": "Pizza Lò Củi",
                "description": "Các loại pizza phô mai Burrata và sốt đặc trưng nướng bằng lò củi cồn",
                "items": [
                    {"name": "Pizza 4 Loại Phô Mai (4 Cheese Pizza)", "description": "Kết hợp phô mai Mozzarella, Gorgonzola, Ricotta, Parmesan kèm mật ong hữu cơ", "price": 280000.0, "image_url": "https://images.unsplash.com/photo-1513104890138-7c749659a591?w=800"},
                    {"name": "Pizza Burrata Thịt Nguội Parma Ham", "description": "Bánh pizza giòn xốp phủ phô mai Burrata tươi nguyên quả và thịt nguội Ý cao cấp", "price": 340000.0, "image_url": "https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?w=800"},
                    {"name": "Pizza Hải Sản Sốt Cà Chua Cay", "description": "Tôm sú, mực tươi, nghêu và ớt chuông đỏ sốt cà chua San Marzano", "price": 290000.0, "image_url": "https://images.unsplash.com/photo-1574071318508-1cdbab80d002?w=800"},
                ]
            },
            {
                "name": "Mì Ý & Món Khai Vị",
                "description": "Mì Pasta tự làm tươi trong ngày",
                "items": [
                    {"name": "Mì Ý Sốt Cua Cà Chua Cay", "description": "Mì sợi dẹt Fettuccine nấu với thịt cua tươi Cà Mau và phô mai Ricotta", "price": 245000.0, "image_url": "https://images.unsplash.com/photo-1621996346565-e3d5d6281724?w=800"},
                    {"name": "Salad Phô Mai Cam & Trái Cây Tươi", "description": "Rau Rocket, dâu tây, cam vàng và phô mai tươi nhà làm", "price": 145000.0, "image_url": "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=800"},
                ]
            },
            {
                "name": "Đồ Uống & Tráng Miệng",
                "description": "Tráng miệng làm thủ công",
                "items": [
                    {"name": "Bánh Tiramisu Truyền Thống", "description": "Hương vị cà phê nồng nàn và phô mai Mascarpone béo mịn", "price": 95000.0, "image_url": "https://images.unsplash.com/photo-1571877227200-a0d98ea607e9?w=800"},
                    {"name": "Nước Ép Bưởi Hồng Ép Lạnh", "description": "100% bưởi hồng tươi nguyên chất không thêm đường", "price": 65000.0, "image_url": "https://images.unsplash.com/photo-1613478223719-2ab802602423?w=800"},
                ]
            }
        ],
        "images": [
            {"image_url": "https://images.unsplash.com/photo-1513104890138-7c749659a591?w=800", "caption": "Không gian bếp mở và lò củi hiện đại tại trung tâm nhà hàng", "is_cover": True},
            {"image_url": "https://images.unsplash.com/photo-1513104890138-7c749659a591?w=800", "caption": "Bánh Pizza phô mai Burrata trứ danh", "is_cover": False},
            {"image_url": "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=800", "caption": "Khu vực bàn ăn gia đình và hẹn hò ấm cúng", "is_cover": False},
        ]
    },
    {
        "name": "Quán Bụi - Authentic Vietnamese Cuisine",
        "description": "Địa chỉ ẩm thực Việt Nam hoài cổ với các món ăn gia đình ba miền đậm đà, không gian Indochine tinh tế giữa lòng Quận 1.",
        "address": "19 Ngô Văn Năm, Phường Bến Nghé, Quận 1, TP. Hồ Chí Minh",
        "phone_number": "02838291299",
        "cuisine_type": "Món Việt",
        "latitude": 10.781200,
        "longitude": 106.705600,
        "min_price": 90000.0,
        "max_price": 320000.0,
        "open_hours": "07:30 - 23:00",
        "avg_rating": 4.6,
        "total_reviews": 620,
        "amenities": {
            "has_parking": True,
            "has_private_room": True,
            "has_outdoor": True,
            "pet_friendly": False,
            "vegetarian_support": True,
        },
        "menus": [
            {
                "name": "Món Cơm Gia Đình",
                "description": "Các món kho, canh, xào đậm đà hương vị mâm cơm mẹ nấu",
                "items": [
                    {"name": "Thịt Kho Tàu Trứng Vịt", "description": "Thịt ba chỉ rút sườn kho nước dừa xiêm béo mềm kèm trứng vịt", "price": 165000.0, "image_url": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=800"},
                    {"name": "Cá Chẽm Kho Tộ Tiêu Xanh", "description": "Cá chẽm tươi kho tộ đất đượm vị tiêu đen Phú Quốc", "price": 195000.0, "image_url": "https://images.unsplash.com/photo-1519708227418-c8fd9a32b7a2?w=800"},
                    {"name": "Canh Chua Cá Bông Lau", "description": "Vị chua thanh mát từ me dốt, bạc hà, đậu bắp và cá bông lau tươi", "price": 185000.0, "image_url": "https://images.unsplash.com/photo-1547592180-85f173990554?w=800"},
                ]
            },
            {
                "name": "Món Cuốn & Khai Vị",
                "description": "Thanh mát, nhẹ nhàng trước bữa ăn",
                "items": [
                    {"name": "Gỏi Cuốn Tôm Thịt (4 cuộn)", "description": "Tôm tươi, thịt ba rọi luộc, bún tươi và rau thơm cuốn bánh tráng phơi sương", "price": 115000.0, "image_url": "https://images.unsplash.com/photo-1559847844-5315695dadae?w=800"},
                    {"name": "Chả Giò Quán Bụi", "description": "Chả giò chiên giòn rụm nhân tôm thịt cua nấm mèo", "price": 125000.0, "image_url": "https://images.unsplash.com/photo-1541544741938-0af808871cc0?w=800"},
                ]
            }
        ],
        "images": [
            {"image_url": "https://images.unsplash.com/photo-1552566626-52f8b828add9?w=800", "caption": "Không gian phong cách Indochine truyền thống sang trọng", "is_cover": True},
            {"image_url": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=800", "caption": "Mâm cơm gia đình Việt đầy đủ sắc hương vị", "is_cover": False},
        ]
    },
    {
        "name": "Dim Tu Tac - Saigon Centre",
        "description": "Thiên đường ẩm thực Quảng Đông hiện đại, nổi danh với các món Dimsum chế biến công phu, vịt quay Bắc Kinh da giòn.",
        "address": "Tầng 5 Saigon Centre, 65 Lê Lợi, Phường Bến Nghé, Quận 1, TP. Hồ Chí Minh",
        "phone_number": "02838266668",
        "cuisine_type": "Món Hoa",
        "latitude": 10.773800,
        "longitude": 106.701100,
        "min_price": 120000.0,
        "max_price": 600000.0,
        "open_hours": "10:30 - 22:00",
        "avg_rating": 4.7,
        "total_reviews": 780,
        "amenities": {
            "has_parking": True,
            "has_private_room": True,
            "has_outdoor": False,
            "pet_friendly": False,
            "vegetarian_support": True,
        },
        "menus": [
            {
                "name": "Dimsum Xửng Hấp Thủ Công",
                "description": "Dimsum hấp nóng hổi tại bàn, vỏ mỏng nhân đầy đặn",
                "items": [
                    {"name": "Há Cảo Tôm Tươi Hấp", "description": "Vỏ bánh trong suốt thấy rõ tôm sú tươi giòn sần sật", "price": 98000.0, "image_url": "https://images.unsplash.com/photo-1563245372-f21724e3856d?w=800"},
                    {"name": "Xíu Mại Tôm Thịt Gạch Cua", "description": "Thịt heo nạc dăm, tôm tươi phủ gạch cua béo ngậy bên trên", "price": 95000.0, "image_url": "https://images.unsplash.com/photo-1541696432-82c6da8ce7bf?w=800"},
                    {"name": "Bánh Bao Kim Sa Trứng Muối", "description": "Nhân trứng muối tan chảy thơm lừng mùi bơ sữa", "price": 85000.0, "image_url": "https://images.unsplash.com/photo-1541696490-8744a5dc0228?w=800"},
                ]
            },
            {
                "name": "Món Quay & Nướng Quảng Đông",
                "description": "Bí quyết tẩm ướp gia truyền hàng chục năm",
                "items": [
                    {"name": "Vịt Quay Bắc Kinh (Nửa con)", "description": "Da vịt giòn rụm cuốn bánh tráng kèm dưa leo hành hoa, thịt xào mì", "price": 480000.0, "image_url": "https://images.unsplash.com/photo-1518492104633-130d0cc84637?w=800"},
                    {"name": "Xá Xíu Mật Ong Đút Lò", "description": "Thịt nạc vai heo ướp mật ong rừng nướng xém cạnh mềm ngọt", "price": 260000.0, "image_url": "https://images.unsplash.com/photo-1544025162-d76694265947?w=800"},
                ]
            }
        ],
        "images": [
            {"image_url": "https://images.unsplash.com/photo-1550966871-3ed3cdb5ed0c?w=800", "caption": "Không gian nhà hàng Dim Tu Tac đẳng cấp tại Saigon Centre", "is_cover": True},
            {"image_url": "https://images.unsplash.com/photo-1563245372-f21724e3856d?w=800", "caption": "Xửng há cảo tôm tươi hấp khói nghi ngút", "is_cover": False},
        ]
    },
    {
        "name": "Cơm Tấm Thuận Kiều - Tôn Thất Tùng",
        "description": "Thương hiệu cơm tấm Sài Gòn lâu đời với miếng sườn nướng mật ong thơm lừng và chả trứng hấp mềm mịn đặc trưng.",
        "address": "46 Tôn Thất Tùng, Phường Bến Thành, Quận 1, TP. Hồ Chí Minh",
        "phone_number": "02839250935",
        "cuisine_type": "Món Việt",
        "latitude": 10.770100,
        "longitude": 106.691500,
        "min_price": 55000.0,
        "max_price": 140000.0,
        "open_hours": "06:00 - 21:30",
        "avg_rating": 4.4,
        "total_reviews": 530,
        "amenities": {
            "has_parking": True,
            "has_private_room": False,
            "has_outdoor": False,
            "pet_friendly": False,
            "vegetarian_support": False,
        },
        "menus": [
            {
                "name": "Cơm Tấm Đĩa Đặc Biệt",
                "description": "Hạt cơm tấm thơm dẻo chan mỡ hành tóp mỡ giòn rụm",
                "items": [
                    {"name": "Cơm Tấm Sườn Cốt Lết Nướng", "description": "Miếng sườn ướp gia vị đậm đà nướng than hoa vàng ươm", "price": 75000.0, "image_url": "https://images.unsplash.com/photo-1559847844-5315695dadae?w=800"},
                    {"name": "Cơm Tấm Sườn Bì Chả Trứng Ốp La", "description": "Combo đầy đủ nhất gồm sườn nướng, bì heo trộn thính, chả trứng và trứng ốp la", "price": 110000.0, "image_url": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=800"},
                    {"name": "Cơm Tấm Sườn Non Cọng", "description": "Sườn non nướng thơm béo ngậy kèm dưa chua củ cải cà rốt", "price": 95000.0, "image_url": "https://images.unsplash.com/photo-1544025162-d76694265947?w=800"},
                ]
            },
            {
                "name": "Canh & Nước Giải Khát",
                "description": "Canh nóng húp kèm cơm tấm",
                "items": [
                    {"name": "Canh Khổ Qua Nhồi Thịt", "description": "Khổ qua hầm thịt nạc xay mộc nhĩ thanh mát giải nhiệt", "price": 35000.0, "image_url": "https://images.unsplash.com/photo-1547592180-85f173990554?w=800"},
                    {"name": "Trà Đá Sâm Dứa Hạt É", "description": "Thơm mát vị lá dứa giải nhiệt ngày hè", "price": 15000.0, "image_url": "https://images.unsplash.com/photo-1513558161293-cdaf765ed2fd?w=800"},
                ]
            }
        ],
        "images": [
            {"image_url": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=800", "caption": "Không gian quán sạch sẽ, phục vụ nhanh chóng thân thiện", "is_cover": True},
            {"image_url": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=800", "caption": "Đĩa cơm tấm sườn bì chả ốp la trứ danh Sài Gòn", "is_cover": False},
        ]
    },
    {
        "name": "Sushi Tei - Đông Du",
        "description": "Nhà hàng Nhật Bản chuẩn mực với nguồn nguyên liệu hải sản tươi sống nhập khẩu trực tiếp từ chợ cá Toyosu Nhật Bản.",
        "address": "20 Đông Du, Phường Bến Nghé, Quận 1, TP. Hồ Chí Minh",
        "phone_number": "02862841188",
        "cuisine_type": "Món Nhật",
        "latitude": 10.776800,
        "longitude": 106.704200,
        "min_price": 150000.0,
        "max_price": 700000.0,
        "open_hours": "11:00 - 22:30",
        "avg_rating": 4.7,
        "total_reviews": 460,
        "amenities": {
            "has_parking": True,
            "has_private_room": True,
            "has_outdoor": False,
            "pet_friendly": False,
            "vegetarian_support": True,
        },
        "menus": [
            {
                "name": "Sashimi Tươi Sống",
                "description": "Cắt lát tươi ngon giữ trọn vẹn vị ngọt biển cả",
                "items": [
                    {"name": "Sashimi Cá Hồi Na Uy (Salmon Sashimi)", "description": "5 lát cá hồi vân mỡ đều đặn, béo ngậy ngọt thịt", "price": 185000.0, "image_url": "https://images.unsplash.com/photo-1579871494447-9811cf80d66c?w=800"},
                    {"name": "Thuyền Sashimi Thượng Hạng 5 Loại", "description": "Cá hồi, cá ngừ, bạch tuộc, sò điệp Nhật và tôm ngọt Amaebi", "price": 550000.0, "image_url": "https://images.unsplash.com/photo-1617196034796-73dfa7b1fd56?w=800"},
                ]
            },
            {
                "name": "Sushi & Cuốn Đặc Biệt",
                "description": "Cơm giấm dẻo hạt Akita kết hợp sốt đặc trưng",
                "items": [
                    {"name": "Sushi Lươn Nhật Nướng Unagi", "description": "Lươn Nhật nướng sốt Kabayaki đậm đà béo ngọt", "price": 165000.0, "image_url": "https://images.unsplash.com/photo-1611143669185-af224c5e3252?w=800"},
                    {"name": "Maki Cá Hồi Nướng Phô Mai", "description": "Cuốn cá hồi khò lửa tái béo ngậy với sốt phô mai trứng cá chuồn", "price": 195000.0, "image_url": "https://images.unsplash.com/photo-1563245372-f21724e3856d?w=800"},
                ]
            }
        ],
        "images": [
            {"image_url": "https://images.unsplash.com/photo-1579871494447-9811cf80d66c?w=800", "caption": "Set Sashimi tươi sống chuẩn phong cách ẩm thực xứ Phù Tang", "is_cover": True},
            {"image_url": "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=800", "caption": "Quầy Sushi Bar nơi thực khách chiêm ngưỡng đầu bếp biểu diễn", "is_cover": False},
        ]
    },
    {
        "name": "El Gaucho Argentinian Steakhouse",
        "description": "Nhà hàng bít tết phong cách Argentina sang trọng hàng đầu TP.HCM, thịt bò Black Angus và Wagyu nhập khẩu nướng than củi mộc.",
        "address": "74 Hai Bà Trưng, Phường Bến Nghé, Quận 1, TP. Hồ Chí Minh",
        "phone_number": "02838258500",
        "cuisine_type": "Món Âu",
        "latitude": 10.777200,
        "longitude": 106.703500,
        "min_price": 500000.0,
        "max_price": 2500000.0,
        "open_hours": "11:00 - 23:30",
        "avg_rating": 4.9,
        "total_reviews": 920,
        "amenities": {
            "has_parking": True,
            "has_private_room": True,
            "has_outdoor": True,
            "pet_friendly": False,
            "vegetarian_support": False,
        },
        "menus": [
            {
                "name": "Thịt Bò Thượng Hạng Nướng Than",
                "description": "Nướng than hoa theo độ chín yêu cầu của thực khách",
                "items": [
                    {"name": "Bò Ribeye Black Angus 300g", "description": "Phần nạc lưng bò Mỹ với vân mỡ cẩm thạch mềm mọng nước", "price": 890000.0, "image_url": "https://images.unsplash.com/photo-1544025162-d76694265947?w=800"},
                    {"name": "Bò Thăn Nội Tenderloin Wagyu 250g", "description": "Thịt mềm tan trong miệng ăn kèm sốt nấm Truffle quý hiếm", "price": 1450000.0, "image_url": "https://images.unsplash.com/photo-1558030006-450675393462?w=800"},
                ]
            },
            {
                "name": "Rượu Vang & Món Ăn Kèm",
                "description": "Kết hợp hoàn hảo cùng Steak",
                "items": [
                    {"name": "Khoai Tây Nghiền Bơ Nấm Truffle", "description": "Khoai tây vàng mịn thơm lừng mùi bơ Pháp và dầu nấm Truffle", "price": 160000.0, "image_url": "https://images.unsplash.com/photo-1518013034458-30b0ee243591?w=800"},
                    {"name": "Măng Tây Xanh Áp Chảo Bơ Tỏi", "description": "Măng tây giòn ngọt thơm dịu tỏi nướng", "price": 150000.0, "image_url": "https://images.unsplash.com/photo-1540420773420-3366772f4999?w=800"},
                ]
            }
        ],
        "images": [
            {"image_url": "https://images.unsplash.com/photo-1544025162-d76694265947?w=800", "caption": "Miếng bít tết bò Wagyu chín vừa mọng nước chuẩn 5 sao", "is_cover": True},
            {"image_url": "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=800", "caption": "Không gian đèn vàng quý phái đậm chất Nam Mỹ", "is_cover": False},
        ]
    },
    {
        "name": "Bếp Mẹ Ỉn - Vietnamese Street Food",
        "description": "Quán ăn ẩm thực đường phố Việt Nam đạt chứng nhận Michelin Bib Gourmand, nổi tiếng với bánh xèo tôm nhảy và cơm chiên trái dừa.",
        "address": "136 Lê Thánh Tôn, Phường Bến Thành, Quận 1, TP. Hồ Chí Minh",
        "phone_number": "02838244666",
        "cuisine_type": "Món Việt",
        "latitude": 10.772800,
        "longitude": 106.699100,
        "min_price": 70000.0,
        "max_price": 250000.0,
        "open_hours": "10:30 - 22:30",
        "avg_rating": 4.6,
        "total_reviews": 710,
        "amenities": {
            "has_parking": False,
            "has_private_room": False,
            "has_outdoor": False,
            "pet_friendly": False,
            "vegetarian_support": True,
        },
        "menus": [
            {
                "name": "Đặc Sản Bếp Mẹ Ỉn",
                "description": "Các món ăn dân dã sáng tạo đạt chuẩn Michelin",
                "items": [
                    {"name": "Bánh Xèo Tôm Thịt Chảo Nhỏ", "description": "Bánh xèo giòn rụm cuốn cải bẹ xanh chấm nước mắm chua ngọt", "price": 95000.0, "image_url": "https://images.unsplash.com/photo-1559847844-5315695dadae?w=800"},
                    {"name": "Cơm Chiên Trái Dừa Hải Sản", "description": "Cơm chiên hạt ngọc thơm phức bọc trong trái dừa xiêm tươi", "price": 145000.0, "image_url": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=800"},
                    {"name": "Trứng Non Cháy Tỏi", "description": "Trứng gà non vàng ươm xào bơ tỏi thơm ngào ngạt", "price": 125000.0, "image_url": "https://images.unsplash.com/photo-1541544741938-0af808871cc0?w=800"},
                ]
            }
        ],
        "images": [
            {"image_url": "https://images.unsplash.com/photo-1559847844-5315695dadae?w=800", "caption": "Không gian hoài niệm vẽ tranh tường Sài Gòn xưa", "is_cover": True},
            {"image_url": "https://images.unsplash.com/photo-1559847844-5315695dadae?w=800", "caption": "Mẹt bánh xèo giòn rụm rau rừng tươi sạch", "is_cover": False},
        ]
    },
    {
        "name": "TukTuk Thai Bistro - Lý Tự Trọng",
        "description": "Bistro ẩm thực Thái Lan sành điệu giữa trung tâm Sài Gòn với các món Tom Yum, pad Thái và gỏi đu đủ chua cay đúng điệu Bangkok.",
        "address": "38 Lý Tự Trọng, Phường Bến Nghé, Quận 1, TP. Hồ Chí Minh",
        "phone_number": "02838251676",
        "cuisine_type": "Món Thái",
        "latitude": 10.777000,
        "longitude": 106.700500,
        "min_price": 95000.0,
        "max_price": 350000.0,
        "open_hours": "10:00 - 22:00",
        "avg_rating": 4.5,
        "total_reviews": 540,
        "amenities": {
            "has_parking": True,
            "has_private_room": False,
            "has_outdoor": True,
            "pet_friendly": False,
            "vegetarian_support": True,
        },
        "menus": [
            {
                "name": "Món Cay & Nước Dùng Thái",
                "description": "Hương vị nồng nàn thảo mộc sả ớt lá chanh Thái",
                "items": [
                    {"name": "Súp Tom Yum Cốt Dừa Hải Sản", "description": "Tôm càng xanh, nấm rơm, sả, riềng trong nước súp chua cay cốt dừa", "price": 195000.0, "image_url": "https://images.unsplash.com/photo-1559314809-0d155014e29e?w=800"},
                    {"name": "Gỏi Đu Đủ Ba Khía Cay Nồng (Som Tum)", "description": "Đu đủ giã cối đất cùng đậu phộng, tôm khô và chanh ớt", "price": 125000.0, "image_url": "https://images.unsplash.com/photo-1540420773420-3366772f4999?w=800"},
                ]
            },
            {
                "name": "Mì & Cơm Chiên",
                "description": "Các món ăn quen thuộc đường phố Thái Lan",
                "items": [
                    {"name": "Pad Thai Tôm Sú", "description": "Hủ tiếu xào sốt me chua ngọt ăn kèm giá hẹ và đậu hũ chiên", "price": 165000.0, "image_url": "https://images.unsplash.com/photo-1559847844-5315695dadae?w=800"},
                    {"name": "Xôi Xoài Nước Cốt Dừa", "description": "Xôi nếp dẻo thơm ăn cùng xoài cát chín vàng ngọt lịm", "price": 85000.0, "image_url": "https://images.unsplash.com/photo-1571877227200-a0d98ea607e9?w=800"},
                ]
            }
        ],
        "images": [
            {"image_url": "https://images.unsplash.com/photo-1559314809-0d155014e29e?w=800", "caption": "Thố súp Tom Yum đỏ au nóng hổi đậm chất Thái Lan", "is_cover": True},
            {"image_url": "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=800", "caption": "Không gian Bistro hiện đại, phá cách", "is_cover": False},
        ]
    },
    {
        "name": "Phở Quỳnh - Phạm Ngũ Lão",
        "description": "Quán phở bò gia truyền hoạt động 24/7 tại khu phố Tây Bùi Viện, nước dùng hầm xương tủy bò 18 tiếng ngọt lịm tự nhiên.",
        "address": "323 Phạm Ngũ Lão, Phường Phạm Ngũ Lão, Quận 1, TP. Hồ Chí Minh",
        "phone_number": "02838368515",
        "cuisine_type": "Món Việt",
        "latitude": 10.767500,
        "longitude": 106.691200,
        "min_price": 65000.0,
        "max_price": 110000.0,
        "open_hours": "00:00 - 23:59 (Mở cả ngày)",
        "avg_rating": 4.5,
        "total_reviews": 690,
        "amenities": {
            "has_parking": True,
            "has_private_room": False,
            "has_outdoor": True,
            "pet_friendly": False,
            "vegetarian_support": False,
        },
        "menus": [
            {
                "name": "Các Món Phở Bò",
                "description": "Phở bò truyền thống bánh phở tươi dẻo thơm",
                "items": [
                    {"name": "Phở Bò Tái Nạm Gầu", "description": "Thịt bò tái mềm, nạm giòn thơm và gầu béo ngậy ngập trong nước dùng trong vắt", "price": 85000.0, "image_url": "https://images.unsplash.com/photo-1582878826629-29b7ad1cdc43?w=800"},
                    {"name": "Phở Đặc Biệt (Tái, Nạm, Gầu, Gân, Bò Viên)", "description": "Tô phở thập cẩm đầy đặn bồi bổ năng lượng", "price": 105000.0, "image_url": "https://images.unsplash.com/photo-1582878826629-29b7ad1cdc43?w=800"},
                    {"name": "Chén Trứng Chần Nước Béo", "description": "Trứng gà ta lòng đào ăn kèm hành lá và nước béo", "price": 15000.0, "image_url": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=800"},
                ]
            }
        ],
        "images": [
            {"image_url": "https://images.unsplash.com/photo-1582878826629-29b7ad1cdc43?w=800", "caption": "Tô phở bò nóng hổi nghi ngút khói thơm mùi hồi quế", "is_cover": True},
            {"image_url": "https://images.unsplash.com/photo-1555396273-367ea4eb4db5?w=800", "caption": "Mặt tiền quán phở nhộn nhịp tại phố Tây", "is_cover": False},
        ]
    },
    {
        "name": "Gyu-Shige Ngưu Phồn - Hàm Nghi",
        "description": "Hệ thống nướng Yakiniku trứ danh đến từ Nhật Bản, phục vụ thịt bò hảo hạng nướng trên bếp than hoa không khói.",
        "address": "119 Hàm Nghi, Phường Bến Nghé, Quận 1, TP. Hồ Chí Minh",
        "phone_number": "02838218958",
        "cuisine_type": "Lẩu Nướng",
        "latitude": 10.771800,
        "longitude": 106.702900,
        "min_price": 200000.0,
        "max_price": 650000.0,
        "open_hours": "10:30 - 23:00",
        "avg_rating": 4.6,
        "total_reviews": 480,
        "amenities": {
            "has_parking": True,
            "has_private_room": True,
            "has_outdoor": False,
            "pet_friendly": False,
            "vegetarian_support": False,
        },
        "menus": [
            {
                "name": "Thịt Nướng Yakiniku",
                "description": "Tẩm ướp sốt Tare gia truyền Nhật Bản",
                "items": [
                    {"name": "Dẻ Sườn Bò Mỹ Ướp Sốt Tare", "description": "Thịt dẻ sườn mềm thơm có độ giòn nhẹ nướng than hồng", "price": 210000.0, "image_url": "https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=800"},
                    {"name": "Lưỡi Bò Nướng Muối Hành", "description": "Lưỡi bò thái mỏng giòn sần sật nướng muối tiêu chanh Nhật", "price": 195000.0, "image_url": "https://images.unsplash.com/photo-1544025162-d76694265947?w=800"},
                ]
            }
        ],
        "images": [
            {"image_url": "https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=800", "caption": "Bếp than nướng Yakiniku rực hồng tỏa hương thơm phức", "is_cover": True},
        ]
    },
    {
        "name": "Secret Garden Restaurant - Rooftop Pasteur",
        "description": "Khu vườn ẩm thực bí mật trên tầng thượng chung cư cổ Pasteur, mang đến trải nghiệm ăn uống mộc mạc trong vườn cây xanh mát.",
        "address": "158 Pasteur, Phường Bến Nghé, Quận 1, TP. Hồ Chí Minh",
        "phone_number": "0909904621",
        "cuisine_type": "Món Việt",
        "latitude": 10.777800,
        "longitude": 106.698900,
        "min_price": 80000.0,
        "max_price": 280000.0,
        "open_hours": "11:00 - 22:00",
        "avg_rating": 4.5,
        "total_reviews": 810,
        "amenities": {
            "has_parking": True,
            "has_private_room": False,
            "has_outdoor": True,
            "pet_friendly": True,
            "vegetarian_support": True,
        },
        "menus": [
            {
                "name": "Đặc Sản Miền Tây Mộc Mạc",
                "description": "Món ăn chân quê dân dã",
                "items": [
                    {"name": "Bông Bí Xào Tỏi", "description": "Bông bí ngô ngọt giòn hái tại vườn xào tỏi đập dập", "price": 85000.0, "image_url": "https://images.unsplash.com/photo-1540420773420-3366772f4999?w=800"},
                    {"name": "Sườn Non Nướng Muối Ớt", "description": "Sườn non cây ướp ớt hiểm cay nồng thơm lừng", "price": 165000.0, "image_url": "https://images.unsplash.com/photo-1544025162-d76694265947?w=800"},
                ]
            }
        ],
        "images": [
            {"image_url": "https://images.unsplash.com/photo-1537047902294-62a40c20a6ae?w=800", "caption": "Khu vườn sân thượng ngập tràn cây xanh và ánh đèn lãng mạn", "is_cover": True},
        ]
    },
    {
        "name": "Hum Lounge & Restaurant - Thi Sách",
        "description": "Nhà hàng chay mỹ vị cao cấp hàng đầu Việt Nam, tôn vinh ẩm thực thuần thực vật tươi ngon trong không gian thiền tịnh tĩnh tại.",
        "address": "2 Thi Sách, Phường Bến Nghé, Quận 1, TP. Hồ Chí Minh",
        "phone_number": "02838238999",
        "cuisine_type": "Món Chay",
        "latitude": 10.778500,
        "longitude": 106.705000,
        "min_price": 120000.0,
        "max_price": 500000.0,
        "open_hours": "10:00 - 22:00",
        "avg_rating": 4.9,
        "total_reviews": 670,
        "amenities": {
            "has_parking": True,
            "has_private_room": True,
            "has_outdoor": True,
            "pet_friendly": False,
            "vegetarian_support": True,
        },
        "menus": [
            {
                "name": "Món Chay Dưỡng Sinh",
                "description": "Nguyên liệu rau củ hữu cơ tươi sạch theo mùa",
                "items": [
                    {"name": "Cơm Gạo Lứt Hạt Sen Lá Sen", "description": "Gạo lứt đỏ dẻo bùi bọc trong lá sen hấp cùng hạt sen tươi", "price": 155000.0, "image_url": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=800"},
                    {"name": "Súp Nấm Tùng Nhung Hạt Dẻ", "description": "Nấm quý bổ dưỡng hầm cùng hạt dẻ thơm bùi thanh đạm", "price": 135000.0, "image_url": "https://images.unsplash.com/photo-1547592180-85f173990554?w=800"},
                ]
            }
        ],
        "images": [
            {"image_url": "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=800", "caption": "Không gian thiền tịnh an yên giữa phố thị tấp nập", "is_cover": True},
        ]
    },
    {
        "name": "Bánh Mì Huỳnh Hoa - Lê Thị Riêng",
        "description": "Ổ bánh mì pate thịt nguội nổi tiếng bậc nhất Sài Gòn với biệt danh 'bánh mì ô môi', đầy ắp 5-6 loại chả lụa pate béo ngậy.",
        "address": "26 Lê Thị Riêng, Phường Bến Thành, Quận 1, TP. Hồ Chí Minh",
        "phone_number": "02839250885",
        "cuisine_type": "Món Việt",
        "latitude": 10.771200,
        "longitude": 106.692300,
        "min_price": 45000.0,
        "max_price": 75000.0,
        "open_hours": "06:00 - 22:00",
        "avg_rating": 4.4,
        "total_reviews": 1150,
        "amenities": {
            "has_parking": False,
            "has_private_room": False,
            "has_outdoor": False,
            "pet_friendly": False,
            "vegetarian_support": False,
        },
        "menus": [
            {
                "name": "Bánh Mì Đặc Biệt",
                "description": "Bánh mì giòn rụm nóng hổi nhân ngập tràn",
                "items": [
                    {"name": "Bánh Mì Thập Cẩm Đặc Biệt", "description": "Pate gan thơm lừng, bơ trứng vàng béo, giò thủ, chả lụa, jambon và chà bông", "price": 68000.0, "image_url": "https://images.unsplash.com/photo-1559847844-5315695dadae?w=800"},
                ]
            }
        ],
        "images": [
            {"image_url": "https://images.unsplash.com/photo-1509440159596-0249088772ff?w=800", "caption": "Ổ bánh mì đầy đặn trứ danh khiến bao thực khách mê mẩn", "is_cover": True},
        ]
    },
    {
        "name": "Hải Sản Rạn Biển - Nguyễn Thái Bình",
        "description": "Hệ thống nhà hàng hải sản tươi sống cao cấp với bể hải sản quy mô lớn, chế biến tại chỗ các loại cua hoàng đế, tôm hùm, cá mú.",
        "address": "45 Nguyễn Thái Bình, Phường Nguyễn Thái Bình, Quận 1, TP. Hồ Chí Minh",
        "phone_number": "02838210387",
        "cuisine_type": "Hải Sản",
        "latitude": 10.770800,
        "longitude": 106.700800,
        "min_price": 180000.0,
        "max_price": 1200000.0,
        "open_hours": "10:00 - 23:00",
        "avg_rating": 4.6,
        "total_reviews": 510,
        "amenities": {
            "has_parking": True,
            "has_private_room": True,
            "has_outdoor": False,
            "pet_friendly": False,
            "vegetarian_support": False,
        },
        "menus": [
            {
                "name": "Hải Sản Bắt Tại Bể",
                "description": "Tươi sống 100% cân ký chế biến theo yêu cầu",
                "items": [
                    {"name": "Cua Cà Mau Sốt Trứng Muối", "description": "Cua thịt chắc nịch phủ sốt trứng muối béo ngậy thơm lừng", "price": 380000.0, "image_url": "https://images.unsplash.com/photo-1534422298391-e4f8c172dddb?w=800"},
                    {"name": "Tôm Sú Hấp Nước Dừa", "description": "Tôm sú biển hấp dừa xiêm giữ nguyên độ ngọt giòn tươi ngon", "price": 280000.0, "image_url": "https://images.unsplash.com/photo-1565680018434-b513d5e5fd47?w=800"},
                ]
            }
        ],
        "images": [
            {"image_url": "https://images.unsplash.com/photo-1534422298391-e4f8c172dddb?w=800", "caption": "Đĩa cua sốt trứng muối vàng ươm hấp dẫn", "is_cover": True},
        ]
    },
    {
        "name": "Lẩu Gà Lá É Tao Ngộ - Nguyễn Thái Bình",
        "description": "Đặc sản lẩu gà lá é nổi tiếng Đà Lạt nay có mặt tại Quận 1, nước dùng ngọt thanh từ măng le tươi và vị cay nồng the the của lá é.",
        "address": "79 Nguyễn Thái Bình, Phường Nguyễn Thái Bình, Quận 1, TP. Hồ Chí Minh",
        "phone_number": "0977221345",
        "cuisine_type": "Lẩu Nướng",
        "latitude": 10.769800,
        "longitude": 106.699500,
        "min_price": 80000.0,
        "max_price": 220000.0,
        "open_hours": "09:30 - 23:00",
        "avg_rating": 4.5,
        "total_reviews": 410,
        "amenities": {
            "has_parking": True,
            "has_private_room": False,
            "has_outdoor": True,
            "pet_friendly": True,
            "vegetarian_support": False,
        },
        "menus": [
            {
                "name": "Lẩu Gà Đặc Sản",
                "description": "Gà ta thả đồi thịt dai ngọt",
                "items": [
                    {"name": "Lẩu Gà Lá É Nồi Nhỏ (2 người)", "description": "Nửa con gà ta, nấm sò, măng chua và rổ lá é tươi thơm phức", "price": 200000.0, "image_url": "https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=800"},
                    {"name": "Lẩu Gà Lá É Nồi Lớn (4 người)", "description": "Nguyên con gà ta kèm đĩa bún tươi và nấm tươi", "price": 320000.0, "image_url": "https://images.unsplash.com/photo-1547592180-85f173990554?w=800"},
                ]
            }
        ],
        "images": [
            {"image_url": "https://images.unsplash.com/photo-1547592180-85f173990554?w=800", "caption": "Nồi lẩu gà lá é sôi sùng sục ấm áp ngày mưa", "is_cover": True},
        ]
    },

    # =========================================================================
    # KHU VỰC 2: QUẬN 3 (10 QUÁN)
    # =========================================================================
    {
        "name": "Phở Hòa Pasteur",
        "description": "Quán phở biểu tượng hơn 50 năm của Sài Gòn trên con đường Pasteur, gắn liền với ký ức ẩm thực của nhiều thế hệ người dân TP.HCM.",
        "address": "260C Pasteur, Phường Võ Thị Sáu, Quận 3, TP. Hồ Chí Minh",
        "phone_number": "02838297943",
        "cuisine_type": "Món Việt",
        "latitude": 10.787100,
        "longitude": 106.688200,
        "min_price": 75000.0,
        "max_price": 120000.0,
        "open_hours": "06:00 - 22:30",
        "avg_rating": 4.6,
        "total_reviews": 1120,
        "amenities": {
            "has_parking": True,
            "has_private_room": False,
            "has_outdoor": False,
            "pet_friendly": False,
            "vegetarian_support": False,
        },
        "menus": [
            {
                "name": "Phở Bò Truyền Thống",
                "description": "Ăn kèm đĩa rau thơm, ngò gai, giá đỗ và quẩy giòn",
                "items": [
                    {"name": "Phở Tái Lăn Áp Chảo", "description": "Thịt bò xào lăn tỏi lửa lớn dậy mùi thơm quyến rũ", "price": 95000.0, "image_url": "https://images.unsplash.com/photo-1582878826629-29b7ad1cdc43?w=800"},
                    {"name": "Phở Thập Cẩm Hòa Pasteur", "description": "Tô phở lớn đầy ắp thịt bò tái, nạm, gân, bò viên và giò heo", "price": 115000.0, "image_url": "https://images.unsplash.com/photo-1582878826629-29b7ad1cdc43?w=800"},
                ]
            }
        ],
        "images": [
            {"image_url": "https://images.unsplash.com/photo-1503764654157-72d979d9af2f?w=800", "caption": "Tô phở Hòa Pasteur thơm nức mũi nước dùng trong trẻo", "is_cover": True},
        ]
    },
    {
        "name": "Cơm Niêu Sài Gòn - Tú Xương",
        "description": "Nhà hàng cơm niêu nổi tiếng với nghệ thuật tung hứng 'cơm đập' độc đáo và các món ăn đậm đà phong vị làng quê Bắc - Trung - Nam.",
        "address": "27 Tú Xương, Phường Võ Thị Sáu, Quận 3, TP. Hồ Chí Minh",
        "phone_number": "02839326344",
        "cuisine_type": "Món Việt",
        "latitude": 10.782000,
        "longitude": 106.684500,
        "min_price": 110000.0,
        "max_price": 400000.0,
        "open_hours": "10:00 - 22:00",
        "avg_rating": 4.6,
        "total_reviews": 750,
        "amenities": {
            "has_parking": True,
            "has_private_room": True,
            "has_outdoor": True,
            "pet_friendly": False,
            "vegetarian_support": True,
        },
        "menus": [
            {
                "name": "Cơm Niêu & Cơm Đập",
                "description": "Nấu trong niêu đất tạo lớp cháy vàng giòn rụm",
                "items": [
                    {"name": "Cơm Đập Cháy Hai Mặt", "description": "Niêu cơm đập vỡ lấy trọn mảng cơm cháy giòn rụm chan mỡ hành", "price": 65000.0, "image_url": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=800"},
                    {"name": "Cá Khoai Kho Tộ Đậm Đà", "description": "Cá béo ngọt kho kẹo sền sệt chấm cơm cháy giòn tan", "price": 185000.0, "image_url": "https://images.unsplash.com/photo-1519708227418-c8fd9a32b7a2?w=800"},
                ]
            }
        ],
        "images": [
            {"image_url": "https://images.unsplash.com/photo-1555396273-367ea4eb4db5?w=800", "caption": "Không gian sân vườn biệt thự cổ lãng mạn tại Tú Xương", "is_cover": True},
        ]
    },
    {
        "name": "Bánh Xèo Ăn Là Ghiền - Tú Xương",
        "description": "Quán bánh xèo miền Tây khổng lồ với vỏ bánh mỏng tanh vàng giòn, nhân tôm thịt nấm củ hũ dừa và rổ rau rừng Tây Ninh tươi sạch.",
        "address": "11A Tú Xương, Phường Võ Thị Sáu, Quận 3, TP. Hồ Chí Minh",
        "phone_number": "02839301969",
        "cuisine_type": "Món Việt",
        "latitude": 10.780200,
        "longitude": 106.686000,
        "min_price": 65000.0,
        "max_price": 180000.0,
        "open_hours": "09:00 - 22:00",
        "avg_rating": 4.4,
        "total_reviews": 430,
        "amenities": {
            "has_parking": True,
            "has_private_room": False,
            "has_outdoor": True,
            "pet_friendly": False,
            "vegetarian_support": True,
        },
        "menus": [
            {
                "name": "Bánh Xèo Vàng Giòn",
                "description": "Đổ chảo gang thủ công",
                "items": [
                    {"name": "Bánh Xèo Tôm Thịt Củ Hũ Dừa", "description": "Củ hũ dừa ngọt thanh giòn ngọt kết hợp tôm đất và thịt ba chỉ", "price": 95000.0, "image_url": "https://images.unsplash.com/photo-1559847844-5315695dadae?w=800"},
                    {"name": "Bánh Khọt Tôm Nước Cốt Dừa (8 cái)", "description": "Bánh khọt tôm tươi vàng giòn chan nước cốt dừa béo mặn", "price": 85000.0, "image_url": "https://images.unsplash.com/photo-1541544741938-0af808871cc0?w=800"},
                ]
            }
        ],
        "images": [
            {"image_url": "https://images.unsplash.com/photo-1541544741938-0af808871cc0?w=800", "caption": "Chiếc bánh xèo vàng ươm tràn ngập tôm thịt", "is_cover": True},
        ]
    },
    {
        "name": "Ẩm Thực Quê Nhà - Phạm Ngọc Thạch",
        "description": "Khu ẩm thực dân dã quy mô lớn rợp bóng tre trúc, hội tụ hơn 200 món ăn ba miền đặc sắc trong không gian làng quê Việt.",
        "address": "28 Phạm Ngọc Thạch, Phường Võ Thị Sáu, Quận 3, TP. Hồ Chí Minh",
        "phone_number": "0938226166",
        "cuisine_type": "Món Việt",
        "latitude": 10.784500,
        "longitude": 106.694200,
        "min_price": 100000.0,
        "max_price": 380000.0,
        "open_hours": "10:00 - 23:30",
        "avg_rating": 4.5,
        "total_reviews": 690,
        "amenities": {
            "has_parking": True,
            "has_private_room": True,
            "has_outdoor": True,
            "pet_friendly": False,
            "vegetarian_support": True,
        },
        "menus": [
            {
                "name": "Món Nhậu & Đồng Quê",
                "description": "Hương vị nồng ấm sum họp bạn bè",
                "items": [
                    {"name": "Gà Ta Hấp Mắm Nhĩ", "description": "Thịt gà ta thả vườn giòn da đẫm vị nước mắm nhĩ thơm lừng", "price": 280000.0, "image_url": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=800"},
                    {"name": "Cơm Cháy Chà Bông Mỡ Hành", "description": "Món ăn chơi giòn bùi ngập tràn ruốc thịt", "price": 95000.0, "image_url": "https://images.unsplash.com/photo-1541544741938-0af808871cc0?w=800"},
                ]
            }
        ],
        "images": [
            {"image_url": "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=800", "caption": "Không gian sân vườn tre xanh mộc mạc thoáng mát", "is_cover": True},
        ]
    },
    {
        "name": "Manwah Taiwanese Hotpot - Cao Thắng",
        "description": "Lẩu Đài Loan buffet thượng hạng với nước lẩu Mala cay nồng, lẩu collagen ngọt dưỡng và thịt bò Mỹ nhúng tươi ngon.",
        "address": "19 Cao Thắng, Phường 2, Quận 3, TP. Hồ Chí Minh",
        "phone_number": "02873007981",
        "cuisine_type": "Lẩu Nướng",
        "latitude": 10.769500,
        "longitude": 106.683000,
        "min_price": 299000.0,
        "max_price": 499000.0,
        "open_hours": "10:00 - 22:30",
        "avg_rating": 4.7,
        "total_reviews": 640,
        "amenities": {
            "has_parking": True,
            "has_private_room": True,
            "has_outdoor": False,
            "pet_friendly": False,
            "vegetarian_support": True,
        },
        "menus": [
            {
                "name": "Buffet Lẩu Xứ Đài",
                "description": "Thưởng thức không giới hạn thịt bò thượng hạng và hải sản",
                "items": [
                    {"name": "Suất Buffet Lẩu Premium", "description": "Thịt gầu bò hoa, ba chỉ bò Mỹ, há cảo Đài Loan và quầy kem đồ tráng miệng", "price": 439000.0, "image_url": "https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=800"},
                ]
            }
        ],
        "images": [
            {"image_url": "https://images.unsplash.com/photo-1569718212165-3a8278d5f624?w=800", "caption": "Nồi lẩu uyên ương 2 ngăn hương vị Đài Loan đặc sắc", "is_cover": True},
        ]
    },
    {
        "name": "Nhà Hàng Chay Pi Bistro - Võ Văn Tần",
        "description": "Quán chay mang phong cách nghệ thuật ấm áp, kết hợp hài hòa nguyên liệu bản địa và kỹ thuật ẩm thực Á Đông thanh nhẹ.",
        "address": "19 Võ Văn Tần, Phường Võ Thị Sáu, Quận 3, TP. Hồ Chí Minh",
        "phone_number": "0916414133",
        "cuisine_type": "Món Chay",
        "latitude": 10.778800,
        "longitude": 106.692200,
        "min_price": 85000.0,
        "max_price": 280000.0,
        "open_hours": "10:00 - 21:30",
        "avg_rating": 4.8,
        "total_reviews": 520,
        "amenities": {
            "has_parking": True,
            "has_private_room": False,
            "has_outdoor": True,
            "pet_friendly": True,
            "vegetarian_support": True,
        },
        "menus": [
            {
                "name": "Món Chay Nghệ Thuật",
                "description": "Hương vị thiên nhiên mộc mạc",
                "items": [
                    {"name": "Đậu Hũ Non Sốt Nấm Rừng", "description": "Đậu hũ tự làm mịn màng sốt nấm hương và dầu mè thơm", "price": 115000.0, "image_url": "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=800"},
                    {"name": "Gỏi Bưởi Tân Triều Hạt Điều", "description": "Tép bưởi hồng mọng nước trộn hạt điều rang giòn rụm", "price": 125000.0, "image_url": "https://images.unsplash.com/photo-1540420773420-3366772f4999?w=800"},
                ]
            }
        ],
        "images": [
            {"image_url": "https://images.unsplash.com/photo-1540420773420-3366772f4999?w=800", "caption": "Món ăn thuần chay bài trí tinh tế và bắt mắt", "is_cover": True},
        ]
    },
    {
        "name": "Hải Sản Biển Đông - Trần Quốc Toản",
        "description": "Nhà hàng hải sản tươi sống lâu năm tại Quận 3, nổi bật với thực đơn cua ghẹ Nha Trang, tôm hùm baby và cá mú đỏ biển sâu.",
        "address": "71 Trần Quốc Toản, Phường Võ Thị Sáu, Quận 3, TP. Hồ Chí Minh",
        "phone_number": "02838206888",
        "cuisine_type": "Hải Sản",
        "latitude": 10.788500,
        "longitude": 106.686500,
        "min_price": 150000.0,
        "max_price": 950000.0,
        "open_hours": "09:30 - 23:00",
        "avg_rating": 4.5,
        "total_reviews": 470,
        "amenities": {
            "has_parking": True,
            "has_private_room": True,
            "has_outdoor": False,
            "pet_friendly": False,
            "vegetarian_support": False,
        },
        "menus": [
            {
                "name": "Đặc Sản Biển Tươi Sống",
                "description": "Chế biến nướng mỡ hành, hấp bia hoặc xào sốt me",
                "items": [
                    {"name": "Mực Trứng Hấp Gừng", "description": "Mực trứng tươi béo ngậy ngọt lịm chấm muối ớt xanh", "price": 220000.0, "image_url": "https://images.unsplash.com/photo-1534422298391-e4f8c172dddb?w=800"},
                    {"name": "Hàu Nướng Phô Mai Béo Ngậy (4 con)", "description": "Hàu sữa béo núc ních phủ lớp sốt phô mai kéo sợi", "price": 140000.0, "image_url": "https://images.unsplash.com/photo-1565680018434-b513d5e5fd47?w=800"},
                ]
            }
        ],
        "images": [
            {"image_url": "https://images.unsplash.com/photo-1565680018434-b513d5e5fd47?w=800", "caption": "Hải sản tươi sống bắt tại bể chế biến theo phong vị Sài Gòn", "is_cover": True},
        ]
    },
    {
        "name": "Lẩu Dê Trương Định",
        "description": "Quán lẩu dê gia truyền nổi tiếng Sài Gòn, thịt dê đồi Ninh Bình tươi ngon không hề hôi, nước lẩu hầm thuốc bắc thơm nồng.",
        "address": "105 Trương Định, Phường Võ Thị Sáu, Quận 3, TP. Hồ Chí Minh",
        "phone_number": "02839304296",
        "cuisine_type": "Món Việt",
        "latitude": 10.781100,
        "longitude": 106.687500,
        "min_price": 120000.0,
        "max_price": 350000.0,
        "open_hours": "10:30 - 23:00",
        "avg_rating": 4.4,
        "total_reviews": 560,
        "amenities": {
            "has_parking": True,
            "has_private_room": False,
            "has_outdoor": True,
            "pet_friendly": False,
            "vegetarian_support": False,
        },
        "menus": [
            {
                "name": "Lẩu & Nướng Dê Núi",
                "description": "Đặc sản bồi bổ khí huyết thơm ngon",
                "items": [
                    {"name": "Lẩu Dựng Dê Thuốc Bắc", "description": "Dựng dê giòn sần sật ninh cùng củ sen, táo tàu, kỷ tử và nấm đông cô", "price": 260000.0, "image_url": "https://images.unsplash.com/photo-1547592180-85f173990554?w=800"},
                    {"name": "Dê Nướng Mọi Chấm Chao", "description": "Thịt đùi dê tơ ướp sả ớt nướng than hồng chấm chao sa tế", "price": 190000.0, "image_url": "https://images.unsplash.com/photo-1544025162-d76694265947?w=800"},
                ]
            }
        ],
        "images": [
            {"image_url": "https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=800", "caption": "Nồi lẩu dê thuốc bắc thơm lừng ngút khói", "is_cover": True},
        ]
    },
    {
        "name": "San Fu Lou - Ngô Thời Nhiệm",
        "description": "Ngôi nhà ẩm thực Quảng Đông hiện đại với mô hình bếp mở trực quan, phục vụ các món mì kéo sợi tươi và dimsum hấp dẫn.",
        "address": "24 Ngô Thời Nhiệm, Phường Võ Thị Sáu, Quận 3, TP. Hồ Chí Minh",
        "phone_number": "02839302888",
        "cuisine_type": "Món Hoa",
        "latitude": 10.780500,
        "longitude": 106.690800,
        "min_price": 100000.0,
        "max_price": 450000.0,
        "open_hours": "07:00 - 22:00",
        "avg_rating": 4.6,
        "total_reviews": 610,
        "amenities": {
            "has_parking": True,
            "has_private_room": True,
            "has_outdoor": True,
            "pet_friendly": False,
            "vegetarian_support": True,
        },
        "menus": [
            {
                "name": "Mì Kéo & Dimsum",
                "description": "Sợi mì tươi kéo bằng tay mềm dai",
                "items": [
                    {"name": "Mì Hoành Thánh Tôm Thịt Xá Xíu", "description": "Nước dùng xương hầm thanh ngọt kèm hoành thánh tôm nguyên con", "price": 115000.0, "image_url": "https://images.unsplash.com/photo-1582878826629-29b7ad1cdc43?w=800"},
                    {"name": "Chân Gà Hấp Tàu Xì", "description": "Chân gà rút xương mềm rục thấm đượm gia vị tàu xì thơm nồng", "price": 85000.0, "image_url": "https://images.unsplash.com/photo-1541696432-82c6da8ce7bf?w=800"},
                ]
            }
        ],
        "images": [
            {"image_url": "https://images.unsplash.com/photo-1563245372-f21724e3856d?w=800", "caption": "Không gian ẩm thực Quảng Đông sang trọng phong cách San Fu Lou", "is_cover": True},
        ]
    },
    {
        "name": "Gyu-Kaku BBQ - Nguyễn Thị Minh Khai",
        "description": "Thương hiệu nướng Yakiniku số 1 Nhật Bản, thỏa mãn đam mê ẩm thực nướng than hoa với các loại sốt nướng đậm đà chuẩn vị Tokyo.",
        "address": "254 Nguyễn Thị Minh Khai, Phường Võ Thị Sáu, Quận 3, TP. Hồ Chí Minh",
        "phone_number": "02862907481",
        "cuisine_type": "Lẩu Nướng",
        "latitude": 10.776000,
        "longitude": 106.688800,
        "min_price": 220000.0,
        "max_price": 600000.0,
        "open_hours": "10:30 - 22:00",
        "avg_rating": 4.6,
        "total_reviews": 510,
        "amenities": {
            "has_parking": True,
            "has_private_room": True,
            "has_outdoor": False,
            "pet_friendly": False,
            "vegetarian_support": False,
        },
        "menus": [
            {
                "name": "Bò Nướng Yakiniku",
                "description": "Thịt bò nướng than hoa mềm mọng nước",
                "items": [
                    {"name": "Ba Chỉ Bò Mỹ Sốt Miso Cay", "description": "Từng lát ba chỉ mỏng ướp tương miso nướng xèo xèo thơm ngát", "price": 145000.0, "image_url": "https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=800"},
                ]
            }
        ],
        "images": [
            {"image_url": "https://images.unsplash.com/photo-1558030006-450675393462?w=800", "caption": "Bàn tiệc nướng Nhật Bản đầy đặn sắc màu", "is_cover": True},
        ]
    },

    # =========================================================================
    # KHU VỰC 3: QUẬN BÌNH THẠNH (13 QUÁN)
    # =========================================================================
    {
        "name": "Bò Tơ Quán Mộc - Hoàng Hoa Thám",
        "description": "Không gian phố xưa Hà Nội thập niên 80 giữa lòng Bình Thạnh, nổi danh với bò tơ non mềm ngọt thịt cuốn bánh tráng rau rừng.",
        "address": "43 Hoàng Hoa Thám, Phường 6, Quận Bình Thạnh, TP. Hồ Chí Minh",
        "phone_number": "0946221188",
        "cuisine_type": "Món Việt",
        "latitude": 10.806200,
        "longitude": 106.694800,
        "min_price": 90000.0,
        "max_price": 320000.0,
        "open_hours": "10:00 - 23:00",
        "avg_rating": 4.7,
        "total_reviews": 680,
        "amenities": {
            "has_parking": True,
            "has_private_room": True,
            "has_outdoor": True,
            "pet_friendly": False,
            "vegetarian_support": False,
        },
        "menus": [
            {
                "name": "Đặc Sản Bò Tơ Cuốn",
                "description": "Bò non sữa mềm ngọt tự nhiên",
                "items": [
                    {"name": "Bò Tơ Cuốn Bánh Tráng Rau Rừng", "description": "Thịt bắp bò tơ hấp mềm cuộn rau rừng chấm mắm nêm đậm đà", "price": 195000.0, "image_url": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=800"},
                    {"name": "Bò Tơ Nướng Tảng Sốt Trứng Muối", "description": "Thịt bò nướng nguyên tảng giữ trọn vị ngọt chấm sốt trứng muối béo", "price": 245000.0, "image_url": "https://images.unsplash.com/photo-1544025162-d76694265947?w=800"},
                    {"name": "Lẩu Đuôi Bò Nấm Thảo Mộc", "description": "Nước lẩu thơm ngọt thanh từ củ sen và đuôi bò ninh nhừ", "price": 285000.0, "image_url": "https://images.unsplash.com/photo-1547592180-85f173990554?w=800"},
                ]
            }
        ],
        "images": [
            {"image_url": "https://images.unsplash.com/photo-1529193591184-b1d58069ecdd?w=800", "caption": "Không gian hoài niệm Hà Nội phố xưa ấm cúng", "is_cover": True},
            {"image_url": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=800", "caption": "Mẹt bò tơ cuốn bánh tráng rau rừng tươi ngon", "is_cover": False},
        ]
    },
    {
        "name": "Gà Nướng Ò Ó O - D2 (Nguyễn Gia Trí)",
        "description": "Thiên đường gà nướng với hơn 10 vị sốt độc quyền sáng tạo như sốt ớt cay Địa Trung Hải, sốt tiêu rừng Tây Bắc, xôi chiên giòn.",
        "address": "83 Nguyễn Gia Trí, Phường 25, Quận Bình Thạnh, TP. Hồ Chí Minh",
        "phone_number": "1900636009",
        "cuisine_type": "Món Việt",
        "latitude": 10.803500,
        "longitude": 106.714500,
        "min_price": 60000.0,
        "max_price": 220000.0,
        "open_hours": "10:30 - 22:00",
        "avg_rating": 4.5,
        "total_reviews": 590,
        "amenities": {
            "has_parking": True,
            "has_private_room": False,
            "has_outdoor": False,
            "pet_friendly": False,
            "vegetarian_support": False,
        },
        "menus": [
            {
                "name": "Gà Nướng Đủ Vị Sốt",
                "description": "Gà nướng lu than thơm vàng da giòn thịt mọng nước",
                "items": [
                    {"name": "Gà Nướng Tiêu Rừng Tây Bắc (Nguyên con)", "description": "Vị cay the the thơm nồng đặc trưng của hạt dổi và mắc khén", "price": 195000.0, "image_url": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=800"},
                    {"name": "Gà Nướng Sốt Ớt Cay Địa Trung Hải", "description": "Sốt ớt đỏ cay nồng kích thích vị giác chấm muối ớt chanh", "price": 195000.0, "image_url": "https://images.unsplash.com/photo-1544025162-d76694265947?w=800"},
                    {"name": "Xôi Chiên Phồng Dẻo Giòn", "description": "Xôi nếp chiên phồng ruộm giòn ngoài mềm trong", "price": 35000.0, "image_url": "https://images.unsplash.com/photo-1541544741938-0af808871cc0?w=800"},
                ]
            }
        ],
        "images": [
            {"image_url": "https://images.unsplash.com/photo-1518492104633-130d0cc84637?w=800", "caption": "Con gà nướng vàng ươm thơm phức gia vị đặc chế", "is_cover": True},
        ]
    },
    {
        "name": "Cháo Vịt Thanh Đa - Gốc Nhà Lá",
        "description": "Thương hiệu cháo gỏi vịt trứ danh vùng bán đảo Thanh Đa hơn 30 năm, thịt vịt cỏ ít mỡ chắc thịt, gỏi bắp cải trộn hành phi giòn rụm.",
        "address": "118 Bình Quới, Phường 27, Quận Bình Thạnh, TP. Hồ Chí Minh",
        "phone_number": "02838986656",
        "cuisine_type": "Món Việt",
        "latitude": 10.824200,
        "longitude": 106.726500,
        "min_price": 50000.0,
        "max_price": 180000.0,
        "open_hours": "07:00 - 23:00",
        "avg_rating": 4.5,
        "total_reviews": 840,
        "amenities": {
            "has_parking": True,
            "has_private_room": False,
            "has_outdoor": True,
            "pet_friendly": True,
            "vegetarian_support": False,
        },
        "menus": [
            {
                "name": "Cháo & Gỏi Vịt",
                "description": "Thịt vịt ngọt thịt không mùi hôi",
                "items": [
                    {"name": "Đĩa Gỏi Vịt Thanh Đa (Phần 2 người)", "description": "Thịt vịt chặt miếng đều tay rắc đậu phộng rang giòn chấm mắm gừng", "price": 140000.0, "image_url": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=800"},
                    {"name": "Tô Cháo Huyết Nóng Hổi", "description": "Cháo nấu gạo rang thơm sánh mịn cùng huyết vịt béo mềm", "price": 25000.0, "image_url": "https://images.unsplash.com/photo-1547592180-85f173990554?w=800"},
                ]
            }
        ],
        "images": [
            {"image_url": "https://images.unsplash.com/photo-1504754524776-8f4f37790ca0?w=800", "caption": "Đĩa gỏi vịt đầy đặn kèm chén nước mắm gừng sánh đặc", "is_cover": True},
        ]
    },
    {
        "name": "Vườn Chay Garden Restaurant - Lê Quang Định",
        "description": "Không gian ẩm thực chay xanh mát như khu vườn nhiệt đới, thực đơn phong phú hơn 100 món chay thanh đạm bồi bổ sức khỏe.",
        "address": "428 Lê Quang Định, Phường 11, Quận Bình Thạnh, TP. Hồ Chí Minh",
        "phone_number": "02836200778",
        "cuisine_type": "Món Chay",
        "latitude": 10.817000,
        "longitude": 106.692500,
        "min_price": 60000.0,
        "max_price": 240000.0,
        "open_hours": "09:00 - 21:30",
        "avg_rating": 4.6,
        "total_reviews": 430,
        "amenities": {
            "has_parking": True,
            "has_private_room": True,
            "has_outdoor": True,
            "pet_friendly": False,
            "vegetarian_support": True,
        },
        "menus": [
            {
                "name": "Món Chay Thanh Tịnh",
                "description": "Chế biến từ nấm và rau củ tươi hữu cơ",
                "items": [
                    {"name": "Lẩu Nấm Thập Cẩm Chay", "description": "Nấm đông cô, nấm đùi gà, nấm linh chi trong nước lẩu rau củ ngọt tự nhiên", "price": 195000.0, "image_url": "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=800"},
                    {"name": "Chả Giò Nấm Hạt Sen", "description": "Vỏ bánh rế giòn tan cuộn khoai môn và hạt sen bùi béo", "price": 85000.0, "image_url": "https://images.unsplash.com/photo-1541544741938-0af808871cc0?w=800"},
                ]
            }
        ],
        "images": [
            {"image_url": "https://images.unsplash.com/photo-1543353071-873f17a7a088?w=800", "caption": "Khu vườn sân vườn xanh mát của Vườn Chay Garden", "is_cover": True},
        ]
    },
    {
        "name": "Hải Sản Gió Biển - Bờ Sông Thanh Đa",
        "description": "Nhà hàng hải sản ven sông Sài Gòn lộng gió, điểm hẹn lý tưởng để thưởng thức bia mát lạnh và hải sản tươi rói lúc hoàng hôn.",
        "address": "101 Bình Quới, Cư xá Thanh Đa, Phường 27, Quận Bình Thạnh, TP. Hồ Chí Minh",
        "phone_number": "02835561122",
        "cuisine_type": "Hải Sản",
        "latitude": 10.825000,
        "longitude": 106.728000,
        "min_price": 120000.0,
        "max_price": 450000.0,
        "open_hours": "10:00 - 23:00",
        "avg_rating": 4.4,
        "total_reviews": 380,
        "amenities": {
            "has_parking": True,
            "has_private_room": True,
            "has_outdoor": True,
            "pet_friendly": True,
            "vegetarian_support": False,
        },
        "menus": [
            {
                "name": "Hải Sản Ven Sông",
                "description": "Thưởng thức cùng view sông Sài Gòn thoáng mát",
                "items": [
                    {"name": "Tôm Càng Xanh Nướng Muối Ớt", "description": "Tôm càng sông gạch son béo ngậy nướng muối ớt cay xè", "price": 260000.0, "image_url": "https://images.unsplash.com/photo-1534422298391-e4f8c172dddb?w=800"},
                    {"name": "Nghêu Hấp Sả Thơm Lừng", "description": "Nghêu biển ngọt nước hấp sả ớt nóng hổi", "price": 95000.0, "image_url": "https://images.unsplash.com/photo-1565680018434-b513d5e5fd47?w=800"},
                ]
            }
        ],
        "images": [
            {"image_url": "https://images.unsplash.com/photo-1519708227418-c8fd9a32b7a2?w=800", "caption": "Bàn tiệc ven sông ngắm hoàng hôn buông trên sông Sài Gòn", "is_cover": True},
        ]
    },
    {
        "name": "Quán Nướng Khói Quê - Điện Biên Phủ",
        "description": "Quán nướng bình dân đông đúc nổi tiếng với các món nướng ngói và nướng than hoa ướp sa tế cay nồng dành cho giới trẻ.",
        "address": "592 Điện Biên Phủ, Phường 22, Quận Bình Thạnh, TP. Hồ Chí Minh",
        "phone_number": "0908776655",
        "cuisine_type": "Lẩu Nướng",
        "latitude": 10.798500,
        "longitude": 106.718000,
        "min_price": 60000.0,
        "max_price": 200000.0,
        "open_hours": "15:30 - 23:30",
        "avg_rating": 4.3,
        "total_reviews": 490,
        "amenities": {
            "has_parking": True,
            "has_private_room": False,
            "has_outdoor": True,
            "pet_friendly": True,
            "vegetarian_support": False,
        },
        "menus": [
            {
                "name": "Nướng Ngói Độc Đáo",
                "description": "Nướng trên phiến ngói đất nung không khét dầu",
                "items": [
                    {"name": "Bò Cuộn Nấm Kim Châm Nướng Ngói", "description": "Bò Mỹ cuộn nấm kim châm giòn ngọt sốt tiêu đen", "price": 95000.0, "image_url": "https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=800"},
                    {"name": "Bạch Tuộc Sa Tế Nướng Giòn", "description": "Bạch tuộc nướng sần sật cay cay đã miệng", "price": 105000.0, "image_url": "https://images.unsplash.com/photo-1534422298391-e4f8c172dddb?w=800"},
                ]
            }
        ],
        "images": [
            {"image_url": "https://images.unsplash.com/photo-1529692236671-f1f6cf9683ba?w=800", "caption": "Món nướng ngói bốc khói nghi ngút thơm nức mũi", "is_cover": True},
        ]
    },
    {
        "name": "Bún Bò Huế Út Hưng - Bạch Đằng",
        "description": "Quán bún bò Huế lâu năm tại Bình Thạnh với nước dùng đậm đà mùi mắm ruốc Huế, sả tươi và miếng bắp bò hoa giòn ngọt.",
        "address": "113 Bạch Đằng, Phường 15, Quận Bình Thạnh, TP. Hồ Chí Minh",
        "phone_number": "02838401234",
        "cuisine_type": "Món Việt",
        "latitude": 10.801000,
        "longitude": 106.705000,
        "min_price": 45000.0,
        "max_price": 85000.0,
        "open_hours": "06:00 - 21:00",
        "avg_rating": 4.5,
        "total_reviews": 520,
        "amenities": {
            "has_parking": True,
            "has_private_room": False,
            "has_outdoor": False,
            "pet_friendly": False,
            "vegetarian_support": False,
        },
        "menus": [
            {
                "name": "Bún Bò Xứ Huế",
                "description": "Hương vị chuẩn cố đô cay the sa tế",
                "items": [
                    {"name": "Bún Bò Giò Nạc Chả Cua", "description": "Tô bún bò đầy đặn khoanh giò nạc, chả cua Huế và bò tái", "price": 65000.0, "image_url": "https://images.unsplash.com/photo-1582878826629-29b7ad1cdc43?w=800"},
                ]
            }
        ],
        "images": [
            {"image_url": "https://images.unsplash.com/photo-1555126634-323283e090fa?w=800", "caption": "Tô bún bò Huế thơm ngát mắm ruốc và màu dầu điều bắt mắt", "is_cover": True},
        ]
    },
    {
        "name": "Sumo Yakiniku - Landmark 81",
        "description": "Nhà hàng buffet nướng lẩu Nhật Bản cao cấp tại tòa nhà chọc trời Landmark 81, thưởng thức thịt bò Wagyu và hải sản không giới hạn.",
        "address": "Tầng B1 Landmark 81, 720A Điện Biên Phủ, Phường 22, Quận Bình Thạnh, TP. Hồ Chí Minh",
        "phone_number": "02873007393",
        "cuisine_type": "Lẩu Nướng",
        "latitude": 10.795000,
        "longitude": 106.721800,
        "min_price": 350000.0,
        "max_price": 650000.0,
        "open_hours": "10:30 - 22:00",
        "avg_rating": 4.7,
        "total_reviews": 670,
        "amenities": {
            "has_parking": True,
            "has_private_room": True,
            "has_outdoor": False,
            "pet_friendly": False,
            "vegetarian_support": False,
        },
        "menus": [
            {
                "name": "Buffet Nướng Sumo",
                "description": "Menu nướng thượng hạng Nhật Bản",
                "items": [
                    {"name": "Buffet Nướng Sumo Otoku", "description": "Thịt bò nướng sốt thảo mộc, sashimi cá hồi và các món nhắm izakaya", "price": 469000.0, "image_url": "https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=800"},
                ]
            }
        ],
        "images": [
            {"image_url": "https://images.unsplash.com/photo-1514933651103-005eec06c04b?w=800", "caption": "Không gian sang trọng tại tòa tháp Landmark 81", "is_cover": True},
        ]
    },
    {
        "name": "Kichi Kichi Lẩu Băng Chuyền - Pearl Plaza",
        "description": "Mô hình lẩu băng chuyền hiện đại chuyển động không ngừng với gần 100 món nhúng lẩu tươi ngon từ bò Mỹ đến hải sản.",
        "address": "Tầng 4 Pearl Plaza, 561A Điện Biên Phủ, Phường 25, Quận Bình Thạnh, TP. Hồ Chí Minh",
        "phone_number": "02873007994",
        "cuisine_type": "Lẩu Nướng",
        "latitude": 10.799800,
        "longitude": 106.717200,
        "min_price": 239000.0,
        "max_price": 329000.0,
        "open_hours": "10:00 - 22:00",
        "avg_rating": 4.5,
        "total_reviews": 510,
        "amenities": {
            "has_parking": True,
            "has_private_room": False,
            "has_outdoor": False,
            "pet_friendly": False,
            "vegetarian_support": True,
        },
        "menus": [
            {
                "name": "Buffet Lẩu Băng Chuyền",
                "description": "Lựa chọn 1 trong 4 vị nước lẩu đặc sắc",
                "items": [
                    {"name": "Suất Buffet Lẩu Không Giới Hạn", "description": "Tự do gắp bò Mỹ, mực nút, tôm thẻ, cá hồi và rau nấm tươi trên băng chuyền", "price": 279000.0, "image_url": "https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=800"},
                ]
            }
        ],
        "images": [
            {"image_url": "https://images.unsplash.com/photo-1553621042-f6e147245754?w=800", "caption": "Băng chuyền lẩu nhộn nhịp ngập tràn món nhúng tươi rói", "is_cover": True},
        ]
    },
    {
        "name": "Quán Ốc Sinh Viên - D2 (Nguyễn Gia Trí)",
        "description": "Tụ điểm ăn ốc giá học sinh sinh viên náo nhiệt bậc nhất Bình Thạnh, nổi tiếng với các món ốc móng tay xào rau muống, ốc hương sốt trứng muối.",
        "address": "69/18 Đường D2 (Nguyễn Gia Trí), Phường 25, Quận Bình Thạnh, TP. Hồ Chí Minh",
        "phone_number": "0934112233",
        "cuisine_type": "Hải Sản",
        "latitude": 10.804000,
        "longitude": 106.715500,
        "min_price": 40000.0,
        "max_price": 120000.0,
        "open_hours": "15:00 - 23:30",
        "avg_rating": 4.4,
        "total_reviews": 610,
        "amenities": {
            "has_parking": True,
            "has_private_room": False,
            "has_outdoor": True,
            "pet_friendly": True,
            "vegetarian_support": False,
        },
        "menus": [
            {
                "name": "Các Món Ốc & Sò",
                "description": "Nước sốt bánh mì chấm ăn kèm tuyệt đỉnh",
                "items": [
                    {"name": "Ốc Hương Xào Trứng Muối Kèm Bánh Mì", "description": "Ốc hương giòn sần sật ngập trong sốt trứng muối béo ngậy", "price": 85000.0, "image_url": "https://images.unsplash.com/photo-1534422298391-e4f8c172dddb?w=800"},
                    {"name": "Sò Điệp Nướng Mỡ Hành Đậu Phộng", "description": "Sò điệp béo ngọt nướng mỡ hành thơm nức mũi", "price": 60000.0, "image_url": "https://images.unsplash.com/photo-1565680018434-b513d5e5fd47?w=800"},
                ]
            }
        ],
        "images": [
            {"image_url": "https://images.unsplash.com/photo-1559339352-11d035aa65de?w=800", "caption": "Đĩa ốc hương xào bơ tỏi thơm ngậy màu vàng ươm", "is_cover": True},
        ]
    },
    {
        "name": "Namsan Korean BBQ - Ung Văn Khiêm",
        "description": "Quán nướng phong cách Hàn Quốc đường phố với thịt ba chỉ heo nướng kim chi, rượu Soju và các món panchan không giới hạn.",
        "address": "45 Ung Văn Khiêm, Phường 25, Quận Bình Thạnh, TP. Hồ Chí Minh",
        "phone_number": "02835123456",
        "cuisine_type": "Món Hàn",
        "latitude": 10.808000,
        "longitude": 106.719500,
        "min_price": 120000.0,
        "max_price": 320000.0,
        "open_hours": "11:00 - 22:30",
        "avg_rating": 4.5,
        "total_reviews": 420,
        "amenities": {
            "has_parking": True,
            "has_private_room": False,
            "has_outdoor": False,
            "pet_friendly": False,
            "vegetarian_support": False,
        },
        "menus": [
            {
                "name": "Thịt Nướng Xứ Hàn",
                "description": "Cuốn rau xà lách chấm sốt Ssamjang chuẩn vị",
                "items": [
                    {"name": "Ba Chỉ Heo Nướng Kim Chi Tươi", "description": "Thịt heo tươi thái dày nướng giòn rụm cuốn lá kim", "price": 165000.0, "image_url": "https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=800"},
                    {"name": "Cơm Trộn Thố Đá Hàn Quốc (Bibimbap)", "description": "Cơm trộn thịt bò băm, rau củ và trứng lòng đào sốt ớt Gochujang", "price": 95000.0, "image_url": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=800"},
                ]
            }
        ],
        "images": [
            {"image_url": "https://images.unsplash.com/photo-1590301157890-4815ed356275?w=800", "caption": "Bàn thịt nướng Hàn Quốc ngập tràn các món panchan", "is_cover": True},
        ]
    },
    {
        "name": "Lẩu Dê Đồng Kỵ - Nơ Trang Long",
        "description": "Quán nhậu đặc sản dê ré nổi tiếng Bình Thạnh, thịt dê tươi làm trong ngày, các món dê xào lăn, dê hấp tía tô và vú dê nướng chao.",
        "address": "128 Nơ Trang Long, Phường 14, Quận Bình Thạnh, TP. Hồ Chí Minh",
        "phone_number": "02835510988",
        "cuisine_type": "Món Việt",
        "latitude": 10.809500,
        "longitude": 106.698000,
        "min_price": 100000.0,
        "max_price": 280000.0,
        "open_hours": "10:00 - 23:00",
        "avg_rating": 4.4,
        "total_reviews": 360,
        "amenities": {
            "has_parking": True,
            "has_private_room": False,
            "has_outdoor": True,
            "pet_friendly": False,
            "vegetarian_support": False,
        },
        "menus": [
            {
                "name": "Đặc Sản Dê Tươi",
                "description": "Các món nhậu lai rai đậm vị",
                "items": [
                    {"name": "Vú Dê Nướng Chao Giòn Béo", "description": "Vú dê ướp chao nướng than hoa giòn sần sật", "price": 175000.0, "image_url": "https://images.unsplash.com/photo-1544025162-d76694265947?w=800"},
                    {"name": "Dê Hấp Lá Tía Tô", "description": "Thịt dê ngọt thanh cuốn bánh tráng chấm tương gừng", "price": 165000.0, "image_url": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=800"},
                ]
            }
        ],
        "images": [
            {"image_url": "https://images.unsplash.com/photo-1541696432-82c6da8ce7bf?w=800", "caption": "Đĩa vú dê nướng vàng ươm ăn cùng đậu bắp nướng", "is_cover": True},
        ]
    },
    {
        "name": "The Coffee House - D2 (Nguyễn Gia Trí)",
        "description": "Điểm hẹn cà phê hiện đại với không gian rộng rãi 3 tầng lầu, phục vụ cà phê phin Việt Nam, trà đào cam sả và bánh ngọt tươi mỗi ngày.",
        "address": "64 Nguyễn Gia Trí, Phường 25, Quận Bình Thạnh, TP. Hồ Chí Minh",
        "phone_number": "18006936",
        "cuisine_type": "Cà Phê & Bánh",
        "latitude": 10.802800,
        "longitude": 106.713800,
        "min_price": 35000.0,
        "max_price": 85000.0,
        "open_hours": "07:00 - 22:30",
        "avg_rating": 4.6,
        "total_reviews": 790,
        "amenities": {
            "has_parking": True,
            "has_private_room": False,
            "has_outdoor": True,
            "pet_friendly": True,
            "vegetarian_support": True,
        },
        "menus": [
            {
                "name": "Cà Phê & Trà Trái Cây",
                "description": "Pha chế theo công thức riêng của The Coffee House",
                "items": [
                    {"name": "Trà Đào Cam Sả Trứ Danh", "description": "Hương vị sả thanh mát kết hợp cam vàng và miếng đào giòn ngọt", "price": 55000.0, "image_url": "https://images.unsplash.com/photo-1513558161293-cdaf765ed2fd?w=800"},
                    {"name": "Cà Phê Sữa Đá Đậm Đà", "description": "Cà phê Robusta Đắk Lắk pha phin truyền thống thơm nồng", "price": 39000.0, "image_url": "https://images.unsplash.com/photo-1501339847302-ac426a4a7cbb?w=800"},
                ]
            }
        ],
        "images": [
            {"image_url": "https://images.unsplash.com/photo-1501339847302-ac426a4a7cbb?w=800", "caption": "Không gian quán cà phê hiện đại tràn ngập ánh sáng tự nhiên", "is_cover": True},
        ]
    },

    # =========================================================================
    # KHU VỰC 4: TP. THỦ ĐỨC (12 QUÁN)
    # =========================================================================
    {
        "name": "The Deck Saigon - Bờ Sông Thảo Điền",
        "description": "Nhà hàng phong cách Pan-Asian bên bờ sông Sài Gòn sang trọng bậc nhất Thảo Điền, ngắm hoàng hôn lộng lẫy cùng cocktail tinh tế.",
        "address": "38 Nguyễn Ư Dĩ, Phường Thảo Điền, TP. Thủ Đức, TP. Hồ Chí Minh",
        "phone_number": "02837446632",
        "cuisine_type": "Món Âu",
        "latitude": 10.807500,
        "longitude": 106.735000,
        "min_price": 250000.0,
        "max_price": 1500000.0,
        "open_hours": "08:00 - 23:30",
        "avg_rating": 4.8,
        "total_reviews": 980,
        "amenities": {
            "has_parking": True,
            "has_private_room": True,
            "has_outdoor": True,
            "pet_friendly": True,
            "vegetarian_support": True,
        },
        "menus": [
            {
                "name": "Món Chính Pan-Asian Thượng Hạng",
                "description": "Kết hợp ẩm thực Á - Âu hiện đại",
                "items": [
                    {"name": "Cá Hồi Na Uy Áp Chảo Sốt Miso", "description": "Cá hồi giòn da thịt ngọt mềm ăn kèm măng tây và khoai nghiền", "price": 380000.0, "image_url": "https://images.unsplash.com/photo-1519708227418-c8fd9a32b7a2?w=800"},
                    {"name": "Bò Wagyu Nướng Sốt Teriyaki Nấm", "description": "Thịt bò Wagyu mềm thơm kết hợp sốt nấm đậm đà", "price": 680000.0, "image_url": "https://images.unsplash.com/photo-1544025162-d76694265947?w=800"},
                ]
            }
        ],
        "images": [
            {"image_url": "https://images.unsplash.com/photo-1559329007-40df8a9345d8?w=800", "caption": "Sàn gỗ ngoài trời sát bờ sông Sài Gòn lãng mạn như tranh vẽ", "is_cover": True},
        ]
    },
    {
        "name": "Bụi Garden - Thảo Điền",
        "description": "Khu vườn ẩm thực Việt giữa lòng Thảo Điền với hồ sen, hàng chuối và các món ăn quê nhà ba miền ấm áp nghĩa tình.",
        "address": "55 Ngô Quang Huy, Phường Thảo Điền, TP. Thủ Đức, TP. Hồ Chí Minh",
        "phone_number": "02838989088",
        "cuisine_type": "Món Việt",
        "latitude": 10.804500,
        "longitude": 106.738000,
        "min_price": 90000.0,
        "max_price": 350000.0,
        "open_hours": "08:00 - 23:00",
        "avg_rating": 4.6,
        "total_reviews": 570,
        "amenities": {
            "has_parking": True,
            "has_private_room": True,
            "has_outdoor": True,
            "pet_friendly": True,
            "vegetarian_support": True,
        },
        "menus": [
            {
                "name": "Mâm Cơm Quê",
                "description": "Hương vị cơm nhà thanh nhã",
                "items": [
                    {"name": "Thịt Heo Kho Trứng Nước Dừa", "description": "Thịt kho mềm rục béo ngọt nước dừa tươi Bến Tre", "price": 175000.0, "image_url": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=800"},
                    {"name": "Đậu Rồng Xào Thịt Bò", "description": "Đậu rồng giòn ngọt xào thịt bò phi tỏi thơm phức", "price": 135000.0, "image_url": "https://images.unsplash.com/photo-1540420773420-3366772f4999?w=800"},
                ]
            }
        ],
        "images": [
            {"image_url": "https://images.unsplash.com/photo-1551218808-94e220e084d2?w=800", "caption": "Khuôn viên vườn nhà mát rượi tại Thảo Điền", "is_cover": True},
        ]
    },
    {
        "name": "Hải Sản Sepia - Khổng Tử",
        "description": "Thiên đường hải sản lớn bậc nhất TP. Thủ Đức với khuôn viên hơn 4000m2, hồ hải sản đa dạng tôm cua ghẹ ốc tươi rói bơi lội.",
        "address": "01 Khổng Tử, Phường Bình Thọ, TP. Thủ Đức, TP. Hồ Chí Minh",
        "phone_number": "0981100100",
        "cuisine_type": "Hải Sản",
        "latitude": 10.846500,
        "longitude": 106.771200,
        "min_price": 120000.0,
        "max_price": 850000.0,
        "open_hours": "09:30 - 23:00",
        "avg_rating": 4.6,
        "total_reviews": 690,
        "amenities": {
            "has_parking": True,
            "has_private_room": True,
            "has_outdoor": True,
            "pet_friendly": False,
            "vegetarian_support": False,
        },
        "menus": [
            {
                "name": "Hải Sản Tươi Sống Sepia",
                "description": "Cân ký chế biến tại chỗ",
                "items": [
                    {"name": "Cua Huỳnh Đế Hấp Gừng Hành", "description": "Thịt cua thơm lừng dai ngọt chấm muối tiêu chanh", "price": 450000.0, "image_url": "https://images.unsplash.com/photo-1534422298391-e4f8c172dddb?w=800"},
                    {"name": "Tôm Hùm Baby Nướng Phô Mai", "description": "Tôm hùm baby thịt chắc nạc phủ phô mai Mozzarella đút lò", "price": 380000.0, "image_url": "https://images.unsplash.com/photo-1565680018434-b513d5e5fd47?w=800"},
                ]
            }
        ],
        "images": [
            {"image_url": "https://images.unsplash.com/photo-1615141982883-c7ad0e69fd62?w=800", "caption": "Bể hải sản khổng lồ đa dạng sinh vật biển tươi sống", "is_cover": True},
        ]
    },
    {
        "name": "Lẩu Dê Năm Ri - Võ Văn Ngân",
        "description": "Thương hiệu lẩu dê gia truyền hơn 30 năm tại Thủ Đức, thịt dê tươi chấm chao bùi béo kết hợp tía tô và nước lẩu ngọt đậm đà.",
        "address": "204 Võ Văn Ngân, Phường Bình Thọ, TP. Thủ Đức, TP. Hồ Chí Minh",
        "phone_number": "02838965678",
        "cuisine_type": "Món Việt",
        "latitude": 10.849500,
        "longitude": 106.768000,
        "min_price": 90000.0,
        "max_price": 280000.0,
        "open_hours": "10:00 - 23:00",
        "avg_rating": 4.5,
        "total_reviews": 530,
        "amenities": {
            "has_parking": True,
            "has_private_room": False,
            "has_outdoor": True,
            "pet_friendly": False,
            "vegetarian_support": False,
        },
        "menus": [
            {
                "name": "Món Dê Đặc Sản",
                "description": "Nước lẩu hầm xương dê ngọt lịm",
                "items": [
                    {"name": "Lẩu Thịt Dê Đùi Tươi (Nồi vừa)", "description": "Thịt đùi dê cắt miếng dày, đậu hũ ky, khoai môn và mì trứng", "price": 220000.0, "image_url": "https://images.unsplash.com/photo-1547592180-85f173990554?w=800"},
                    {"name": "Dê Tái Chanh Cuốn Rau Rừng", "description": "Thịt dê bóp thấu chanh chua ngọt rắc mè thơm", "price": 160000.0, "image_url": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=800"},
                ]
            }
        ],
        "images": [
            {"image_url": "https://images.unsplash.com/photo-1534939561126-855b8675edd7?w=800", "caption": "Nồi lẩu dê sôi sùng sục cùng đĩa thịt dê tươi rói", "is_cover": True},
        ]
    },
    {
        "name": "Nhà Hàng Gió & Nước - Làng Đại Học",
        "description": "Không gian sinh thái hồ sen thoáng đãng tại Làng Đại học Quốc gia, chuyên phục vụ các món cá sông, gà đồi và lẩu dân dã giá cả sinh viên.",
        "address": "Khu Đô thị ĐHQG-HCM, Phường Linh Trung, TP. Thủ Đức, TP. Hồ Chí Minh",
        "phone_number": "0903334455",
        "cuisine_type": "Món Việt",
        "latitude": 10.871000,
        "longitude": 106.782000,
        "min_price": 50000.0,
        "max_price": 180000.0,
        "open_hours": "09:00 - 22:30",
        "avg_rating": 4.4,
        "total_reviews": 460,
        "amenities": {
            "has_parking": True,
            "has_private_room": True,
            "has_outdoor": True,
            "pet_friendly": True,
            "vegetarian_support": True,
        },
        "menus": [
            {
                "name": "Món Đồng Quê & Sân Vườn",
                "description": "Giá cả hợp lý cho sinh viên và nhóm bạn",
                "items": [
                    {"name": "Cá Lóc Nướng Trui Rơm Cuốn Bánh Tráng", "description": "Cá lóc đồng nướng rơm nguyên con ngọt lịm chấm mắm nêm", "price": 140000.0, "image_url": "https://images.unsplash.com/photo-1519708227418-c8fd9a32b7a2?w=800"},
                    {"name": "Gà Đồi Nướng Muối Ớt Kèm Xôi Cháy", "description": "Thịt gà chắc ngọt thơm mùi khói nướng", "price": 195000.0, "image_url": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=800"},
                ]
            }
        ],
        "images": [
            {"image_url": "https://images.unsplash.com/photo-1414235077428-338989a2e8c0?w=800", "caption": "Nhà chòi ven hồ sen thoáng mát yên bình", "is_cover": True},
        ]
    },
    {
        "name": "Gyu-Kaku BBQ - Vincom Thảo Điền",
        "description": "Trải nghiệm nướng Yakiniku Nhật Bản tiêu chuẩn quốc tế ngay tại trung tâm thương mại Vincom Mega Mall Thảo Điền.",
        "address": "Tầng 5 Vincom Mega Mall, 161 Xa Lộ Hà Nội, Phường Thảo Điền, TP. Thủ Đức, TP. Hồ Chí Minh",
        "phone_number": "02837446688",
        "cuisine_type": "Lẩu Nướng",
        "latitude": 10.802000,
        "longitude": 106.741000,
        "min_price": 220000.0,
        "max_price": 550000.0,
        "open_hours": "10:30 - 22:00",
        "avg_rating": 4.6,
        "total_reviews": 410,
        "amenities": {
            "has_parking": True,
            "has_private_room": True,
            "has_outdoor": False,
            "pet_friendly": False,
            "vegetarian_support": False,
        },
        "menus": [
            {
                "name": "Thịt Nướng Nhật Bản",
                "description": "Nướng than hoa không khói",
                "items": [
                    {"name": "Thịt Dẻ Sườn Bò Mỹ Nướng Sốt Tỏi", "description": "Miếng dẻ sườn ướp đậm sốt tỏi cay thơm giòn", "price": 185000.0, "image_url": "https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=800"},
                ]
            }
        ],
        "images": [
            {"image_url": "https://images.unsplash.com/photo-1611143669185-af224c5e3252?w=800", "caption": "Set nướng thịt bò nhập khẩu hảo hạng tại Gyu-Kaku", "is_cover": True},
        ]
    },
    {
        "name": "Nấm Lẩu Dân Gian - Thảo Điền",
        "description": "Nhà hàng lẩu nấm thanh tao với hơn 20 loại nấm quý tự nhiên bồi dưỡng cơ thể, không gian sân vườn xanh mát tĩnh lặng.",
        "address": "14 Quốc Hương, Phường Thảo Điền, TP. Thủ Đức, TP. Hồ Chí Minh",
        "phone_number": "02835191234",
        "cuisine_type": "Món Chay",
        "latitude": 10.801500,
        "longitude": 106.732500,
        "min_price": 120000.0,
        "max_price": 380000.0,
        "open_hours": "10:00 - 22:00",
        "avg_rating": 4.7,
        "total_reviews": 380,
        "amenities": {
            "has_parking": True,
            "has_private_room": True,
            "has_outdoor": True,
            "pet_friendly": True,
            "vegetarian_support": True,
        },
        "menus": [
            {
                "name": "Lẩu Nấm Thiên Nhiên",
                "description": "Nước dùng thanh tịnh hầm từ rễ cây và nấm quý",
                "items": [
                    {"name": "Set Lẩu Nấm Dưỡng Sinh Hoàng Kim", "description": "Nấm tùng nhung, nấm gan bò, nấm kê tùng và mì nấm tự làm", "price": 280000.0, "image_url": "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=800"},
                ]
            }
        ],
        "images": [
            {"image_url": "https://images.unsplash.com/photo-1498837167922-ddd27525d352?w=800", "caption": "Thớt nấm tươi rực rỡ sắc màu bổ dưỡng cho sức khỏe", "is_cover": True},
        ]
    },
    {
        "name": "Ẩm Thực Đồng Quê - Tô Ngọc Vân",
        "description": "Quán ăn gia đình đậm chất miền Tây Nam Bộ tại trung tâm Thủ Đức, đặc sản cá tai tượng chiên xù và lẩu mắm đậm đà.",
        "address": "123 Tô Ngọc Vân, Phường Linh Tây, TP. Thủ Đức, TP. Hồ Chí Minh",
        "phone_number": "02838971122",
        "cuisine_type": "Món Việt",
        "latitude": 10.858000,
        "longitude": 106.757000,
        "min_price": 70000.0,
        "max_price": 250000.0,
        "open_hours": "09:30 - 22:30",
        "avg_rating": 4.4,
        "total_reviews": 410,
        "amenities": {
            "has_parking": True,
            "has_private_room": True,
            "has_outdoor": True,
            "pet_friendly": False,
            "vegetarian_support": False,
        },
        "menus": [
            {
                "name": "Đặc Sản Miền Tây",
                "description": "Món ăn sông nước dân dã",
                "items": [
                    {"name": "Cá Tai Tượng Chiên Xù", "description": "Cá chiên xù vảy giòn rụm cuốn bánh tráng chấm mắm nêm chua cay", "price": 185000.0, "image_url": "https://images.unsplash.com/photo-1519708227418-c8fd9a32b7a2?w=800"},
                    {"name": "Lẩu Mắm Miền Tây Đậm Vị", "description": "Lẩu mắm cá linh cá sặc thơm nồng ăn cùng 10 loại rau đồng nội", "price": 250000.0, "image_url": "https://images.unsplash.com/photo-1547592180-85f173990554?w=800"},
                ]
            }
        ],
        "images": [
            {"image_url": "https://images.unsplash.com/photo-1476224203421-9ac39bcb3327?w=800", "caption": "Con cá tai tượng chiên xù vảy vàng óng ả", "is_cover": True},
        ]
    },
    {
        "name": "Quán Nhậu 136 - Đặng Văn Bi",
        "description": "Tụ điểm gặp gỡ bạn bè bia hơi và mồi nhậu bình dân nổi tiếng đường Đặng Văn Bi với các món bò sốt hàu, sụn gà hoàng kim giòn rụm.",
        "address": "136 Đặng Văn Bi, Phường Trường Thọ, TP. Thủ Đức, TP. Hồ Chí Minh",
        "phone_number": "0909554433",
        "cuisine_type": "Món Việt",
        "latitude": 10.838500,
        "longitude": 106.762000,
        "min_price": 50000.0,
        "max_price": 180000.0,
        "open_hours": "16:00 - 02:00",
        "avg_rating": 4.3,
        "total_reviews": 390,
        "amenities": {
            "has_parking": True,
            "has_private_room": False,
            "has_outdoor": True,
            "pet_friendly": True,
            "vegetarian_support": False,
        },
        "menus": [
            {
                "name": "Mồi Nhậu Lai Rai",
                "description": "Các món xào nướng thơm cay bắt vị",
                "items": [
                    {"name": "Chảo Bò Sốt Hàu Phô Mai Cay", "description": "Thịt bò Mỹ, hàu tươi, nấm kim châm ngập trong sốt cay kéo sợi phô mai", "price": 149000.0, "image_url": "https://images.unsplash.com/photo-1544025162-d76694265947?w=800"},
                    {"name": "Sụn Gà Chiên Nước Mắm", "description": "Sụn gà giòn sần sật bọc nước mắm tỏi ớt thơm lừng", "price": 85000.0, "image_url": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=800"},
                ]
            }
        ],
        "images": [
            {"image_url": "https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?w=800", "caption": "Chảo bò sốt hàu phô mai sôi xèo xèo hấp dẫn", "is_cover": True},
        ]
    },
    {
        "name": "Hủ Tiếu Mực Ông Già Cali - Thảo Điền",
        "description": "Thương hiệu hủ tiếu mực nổi danh đất Sài Gòn, mực tươi chong đèn dày cùi giòn ngọt sần sật, nước súp hầm mực khô thanh vị tự nhiên.",
        "address": "30 Trần Ngọc Diện, Phường Thảo Điền, TP. Thủ Đức, TP. Hồ Chí Minh",
        "phone_number": "0903099955",
        "cuisine_type": "Món Việt",
        "latitude": 10.805500,
        "longitude": 106.736500,
        "min_price": 55000.0,
        "max_price": 95000.0,
        "open_hours": "06:30 - 22:00",
        "avg_rating": 4.5,
        "total_reviews": 460,
        "amenities": {
            "has_parking": True,
            "has_private_room": False,
            "has_outdoor": True,
            "pet_friendly": False,
            "vegetarian_support": False,
        },
        "menus": [
            {
                "name": "Hủ Tiếu Mực Nước & Khô",
                "description": "Mực trứng và mực nang tươi giòn",
                "items": [
                    {"name": "Hủ Tiếu Mực Tươi Đặc Biệt", "description": "Mực tươi nguyên con, thịt viên bọc trứng cút và tôm sú tươi", "price": 79000.0, "image_url": "https://images.unsplash.com/photo-1582878826629-29b7ad1cdc43?w=800"},
                    {"name": "Hủ Tiếu Khô Sốt Tương Cay", "description": "Sợi hủ tiếu dai trộn sốt tương đen gia truyền kèm chén súp mực riêng", "price": 79000.0, "image_url": "https://images.unsplash.com/photo-1559847844-5315695dadae?w=800"},
                ]
            }
        ],
        "images": [
            {"image_url": "https://images.unsplash.com/photo-1617196034796-73dfa7b1fd56?w=800", "caption": "Tô hủ tiếu mực ngập tràn mực tươi và hành phi thơm lừng", "is_cover": True},
        ]
    },
    {
        "name": "Bia Tuyết - Nguyễn Duy Trinh",
        "description": "Quán hải sản và bia tuyết mát lạnh nổi tiếng tại khu vực Bình Trưng Tây, không gian sân thượng thoáng đãng view ngắm đường phố về đêm.",
        "address": "285 Nguyễn Duy Trinh, Phường Bình Trưng Tây, TP. Thủ Đức, TP. Hồ Chí Minh",
        "phone_number": "0937665544",
        "cuisine_type": "Hải Sản",
        "latitude": 10.789000,
        "longitude": 106.762500,
        "min_price": 80000.0,
        "max_price": 280000.0,
        "open_hours": "15:00 - 23:30",
        "avg_rating": 4.4,
        "total_reviews": 320,
        "amenities": {
            "has_parking": True,
            "has_private_room": False,
            "has_outdoor": True,
            "pet_friendly": True,
            "vegetarian_support": False,
        },
        "menus": [
            {
                "name": "Món Nhậu Hải Sản",
                "description": "Thưởng thức cùng bia ướp tuyết mát lạnh",
                "items": [
                    {"name": "Bạch Tuộc Nướng Muối Ớt Xanh", "description": "Bạch tuộc nướng than hoa giòn dai đẫm sốt muối ớt xanh", "price": 135000.0, "image_url": "https://images.unsplash.com/photo-1534422298391-e4f8c172dddb?w=800"},
                    {"name": "Lẩu Cá Bớp Nấu Măng Chua", "description": "Cá bớp biển tươi cắt khúc béo ngọt nấu măng chua cay nồng", "price": 210000.0, "image_url": "https://images.unsplash.com/photo-1547592180-85f173990554?w=800"},
                ]
            }
        ],
        "images": [
            {"image_url": "https://images.unsplash.com/photo-1574071318508-1cdbab80d002?w=800", "caption": "Đĩa bạch tuộc nướng muối ớt cay xè lai rai cùng bia lạnh", "is_cover": True},
        ]
    },
    {
        "name": "Quán Nướng Yummy Yummy - Hoàng Diệu 2",
        "description": "Tụ điểm buffet nướng lẩu sinh viên nhộn nhịp bậc nhất Thủ Đức trên phố ẩm thực Hoàng Diệu 2, thực đơn đa dạng hơn 50 món nướng tự chọn.",
        "address": "78 Hoàng Diệu 2, Phường Linh Trung, TP. Thủ Đức, TP. Hồ Chí Minh",
        "phone_number": "0988771122",
        "cuisine_type": "Lẩu Nướng",
        "latitude": 10.853000,
        "longitude": 106.772500,
        "min_price": 139000.0,
        "max_price": 219000.0,
        "open_hours": "16:00 - 23:00",
        "avg_rating": 4.3,
        "total_reviews": 580,
        "amenities": {
            "has_parking": True,
            "has_private_room": False,
            "has_outdoor": True,
            "pet_friendly": True,
            "vegetarian_support": False,
        },
        "menus": [
            {
                "name": "Buffet Nướng Sinh Viên",
                "description": "Ăn thả ga thịt nướng và tráng miệng",
                "items": [
                    {"name": "Vé Buffet Nướng Thả Ga", "description": "Tự chọn ba chỉ bò, dồi sụn, tôm nướng, hàu nướng mỡ hành và quầy tráng miệng", "price": 169000.0, "image_url": "https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=800"},
                ]
            }
        ],
        "images": [
            {"image_url": "https://images.unsplash.com/photo-1621996346565-e3d5d6281724?w=800", "caption": "Không gian quán nướng nhộn nhịp đông vui vào mỗi buổi tối", "is_cover": True},
        ]
    },
    # =========================================================================
    # MỞ RỘNG TOÀN KHU VỰC TP.HCM (60 QUÁN: GÒ VẤP, PHÚ NHUẬN, TÂN BÌNH, TÂN PHÚ, Q4, Q5, Q6, Q7, Q8, Q10, Q11, Q12, BÌNH TÂN, BÌNH CHÁNH, NHÀ BÈ, HÓC MÔN)
    # =========================================================================
    {'name': 'GoGi House - Quang Trung Gò Vấp', 'description': 'Thịt nướng Hàn Quốc chuẩn vị Seoul tại trung tâm Gò Vấp, không gian rộng rãi cho gia đình và nhóm bạn.', 'address': '189 Quang Trung, Phường 10, Quận Gò Vấp, TP. Hồ Chí Minh', 'phone_number': '02873007381', 'cuisine_type': 'Lẩu Nướng', 'latitude': 10.8295, 'longitude': 106.6728, 'min_price': 199000.0, 'max_price': 389000.0, 'open_hours': '10:00 - 22:00', 'avg_rating': 4.7, 'total_reviews': 540, 'amenities': {'has_parking': True, 'has_private_room': True, 'has_outdoor': False, 'pet_friendly': False, 'vegetarian_support': False}, 'menus': [{'name': 'Món Đặc Trưng', 'description': 'Các món nổi bật nhất tại GoGi House - Quang Trung Gò Vấp', 'items': [{'name': 'Dẻ Sườn Bò Mỹ Sốt Galbi', 'description': 'Món bán chạy hàng đầu tại GoGi House - Quang Trung Gò Vấp', 'price': 219000.0, 'image_url': 'https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=800&q=80&auto=format&fit=crop&sig=51'}, {'name': 'Ba Chỉ Bò Mỹ Cuộn Nấm', 'description': 'Hương vị đặc sắc được thực khách yêu thích', 'price': 169000.0, 'image_url': 'https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=800&q=80&auto=format&fit=crop&sig=51'}]}], 'images': [{'image_url': 'https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=800&q=80&auto=format&fit=crop&sig=51', 'caption': 'Không gian và món ngon tại GoGi House - Quang Trung Gò Vấp', 'is_cover': True}]},
    {'name': 'Lẩu Nấm Ashima - Phan Văn Trị', 'description': 'Lẩu nấm thiên nhiên thanh ngọt với hơn 20 loại nấm quý bổ dưỡng, có phòng riêng sang trọng.', 'address': '366 Phan Văn Trị, Phường 5, Quận Gò Vấp, TP. Hồ Chí Minh', 'phone_number': '02873007312', 'cuisine_type': 'Lẩu Nướng', 'latitude': 10.8214, 'longitude': 106.6915, 'min_price': 250000.0, 'max_price': 480000.0, 'open_hours': '10:30 - 22:00', 'avg_rating': 4.8, 'total_reviews': 410, 'amenities': {'has_parking': True, 'has_private_room': True, 'has_outdoor': True, 'pet_friendly': False, 'vegetarian_support': True}, 'menus': [{'name': 'Món Đặc Trưng', 'description': 'Các món nổi bật nhất tại Lẩu Nấm Ashima - Phan Văn Trị', 'items': [{'name': 'Set Lẩu Nấm Thiên Nhiên', 'description': 'Món bán chạy hàng đầu tại Lẩu Nấm Ashima - Phan Văn Trị', 'price': 340000.0, 'image_url': 'https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=800&q=80&auto=format&fit=crop&sig=52'}, {'name': 'Nấm Tùng Nhung Tươi', 'description': 'Hương vị đặc sắc được thực khách yêu thích', 'price': 155000.0, 'image_url': 'https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=800&q=80&auto=format&fit=crop&sig=52'}]}], 'images': [{'image_url': 'https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=800&q=80&auto=format&fit=crop&sig=52', 'caption': 'Không gian và món ngon tại Lẩu Nấm Ashima - Phan Văn Trị', 'is_cover': True}]},
    {'name': 'Hải Sản Biển Đông - Lê Văn Thọ', 'description': 'Hải sản tươi sống bắt tại bể, giá bình dân phục vụ các món nướng, hấp, rang me đậm vị.', 'address': '412 Lê Văn Thọ, Phường 11, Quận Gò Vấp, TP. Hồ Chí Minh', 'phone_number': '02839961234', 'cuisine_type': 'Hải Sản', 'latitude': 10.8415, 'longitude': 106.6598, 'min_price': 150000.0, 'max_price': 450000.0, 'open_hours': '10:00 - 23:00', 'avg_rating': 4.5, 'total_reviews': 320, 'amenities': {'has_parking': True, 'has_private_room': True, 'has_outdoor': True, 'pet_friendly': False, 'vegetarian_support': False}, 'menus': [{'name': 'Món Đặc Trưng', 'description': 'Các món nổi bật nhất tại Hải Sản Biển Đông - Lê Văn Thọ', 'items': [{'name': 'Cua Cà Mau Rang Me', 'description': 'Món bán chạy hàng đầu tại Hải Sản Biển Đông - Lê Văn Thọ', 'price': 320000.0, 'image_url': 'https://images.unsplash.com/photo-1567620905732-2d1ec7ab7445?w=800'}, {'name': 'Tôm Sú Nướng Muối Ớt', 'description': 'Hương vị đặc sắc được thực khách yêu thích', 'price': 240000.0, 'image_url': 'https://images.unsplash.com/photo-1567620905732-2d1ec7ab7445?w=800'}]}], 'images': [{'image_url': 'https://images.unsplash.com/photo-1567620905732-2d1ec7ab7445?w=800', 'caption': 'Không gian và món ngon tại Hải Sản Biển Đông - Lê Văn Thọ', 'is_cover': True}]},
    {'name': 'Cơm Tấm Cali - Thống Nhất', 'description': 'Cơm tấm sườn nướng cháy cạnh sạch sẽ, máy lạnh mát mẻ trên trục đường Thống Nhất.', 'address': '245 Thống Nhất, Phường 16, Quận Gò Vấp, TP. Hồ Chí Minh', 'phone_number': '02838945566', 'cuisine_type': 'Cơm tấm', 'latitude': 10.8386, 'longitude': 106.665, 'min_price': 55000.0, 'max_price': 115000.0, 'open_hours': '07:00 - 21:30', 'avg_rating': 4.4, 'total_reviews': 290, 'amenities': {'has_parking': True, 'has_private_room': False, 'has_outdoor': False, 'pet_friendly': False, 'vegetarian_support': False}, 'menus': [{'name': 'Món Đặc Trưng', 'description': 'Các món nổi bật nhất tại Cơm Tấm Cali - Thống Nhất', 'items': [{'name': 'Cơm Tấm Sườn Bì Chả', 'description': 'Món bán chạy hàng đầu tại Cơm Tấm Cali - Thống Nhất', 'price': 79000.0, 'image_url': 'https://images.unsplash.com/photo-1565958011703-44f9829ba187?w=800'}, {'name': 'Cơm Tấm Sườn Non Nướng', 'description': 'Hương vị đặc sắc được thực khách yêu thích', 'price': 95000.0, 'image_url': 'https://images.unsplash.com/photo-1565958011703-44f9829ba187?w=800'}]}], 'images': [{'image_url': 'https://images.unsplash.com/photo-1565958011703-44f9829ba187?w=800', 'caption': 'Không gian và món ngon tại Cơm Tấm Cali - Thống Nhất', 'is_cover': True}]},
    {'name': 'Quán Chay Tâm An - Nguyễn Oanh', 'description': 'Không gian chay thanh tịnh, thực đơn cơm chay và lẩu nấm giá hợp lý cho mọi lứa tuổi.', 'address': '158 Nguyễn Oanh, Phường 17, Quận Gò Vấp, TP. Hồ Chí Minh', 'phone_number': '0908112244', 'cuisine_type': 'Món Chay', 'latitude': 10.8342, 'longitude': 106.6789, 'min_price': 45000.0, 'max_price': 140000.0, 'open_hours': '07:00 - 21:00', 'avg_rating': 4.6, 'total_reviews': 260, 'amenities': {'has_parking': True, 'has_private_room': False, 'has_outdoor': True, 'pet_friendly': False, 'vegetarian_support': True}, 'menus': [{'name': 'Món Đặc Trưng', 'description': 'Các món nổi bật nhất tại Quán Chay Tâm An - Nguyễn Oanh', 'items': [{'name': 'Lẩu Thái Chay Nấm Rừng', 'description': 'Món bán chạy hàng đầu tại Quán Chay Tâm An - Nguyễn Oanh', 'price': 135000.0, 'image_url': 'https://images.unsplash.com/photo-1482049016688-2d3e1b311543?w=800'}, {'name': 'Cơm Chiên Lá É Chay', 'description': 'Hương vị đặc sắc được thực khách yêu thích', 'price': 55000.0, 'image_url': 'https://images.unsplash.com/photo-1482049016688-2d3e1b311543?w=800'}]}], 'images': [{'image_url': 'https://images.unsplash.com/photo-1482049016688-2d3e1b311543?w=800', 'caption': 'Không gian và món ngon tại Quán Chay Tâm An - Nguyễn Oanh', 'is_cover': True}]},
    {'name': 'Cà Phê Country House - Phan Văn Trị', 'description': 'Quán cà phê sân vườn phong cách đồng quê châu Âu rộng lớn nổi tiếng bậc nhất Gò Vấp.', 'address': '18C Phan Văn Trị, Phường 10, Quận Gò Vấp, TP. Hồ Chí Minh', 'phone_number': '02838942255', 'cuisine_type': 'Cà Phê & Bánh', 'latitude': 10.831, 'longitude': 106.679, 'min_price': 45000.0, 'max_price': 95000.0, 'open_hours': '07:00 - 23:00', 'avg_rating': 4.6, 'total_reviews': 890, 'amenities': {'has_parking': True, 'has_private_room': False, 'has_outdoor': True, 'pet_friendly': True, 'vegetarian_support': True}, 'menus': [{'name': 'Món Đặc Trưng', 'description': 'Các món nổi bật nhất tại Cà Phê Country House - Phan Văn Trị', 'items': [{'name': 'Trà Vải Hoa Hồng', 'description': 'Món bán chạy hàng đầu tại Cà Phê Country House - Phan Văn Trị', 'price': 62000.0, 'image_url': 'https://images.unsplash.com/photo-1484723091739-30a097e8f929?w=800'}, {'name': 'Cà Phê Kem Muối', 'description': 'Hương vị đặc sắc được thực khách yêu thích', 'price': 55000.0, 'image_url': 'https://images.unsplash.com/photo-1484723091739-30a097e8f929?w=800'}]}], 'images': [{'image_url': 'https://images.unsplash.com/photo-1484723091739-30a097e8f929?w=800', 'caption': 'Không gian và món ngon tại Cà Phê Country House - Phan Văn Trị', 'is_cover': True}]},
    {'name': 'Bò Né 3 Ngon - Phan Xích Long', 'description': 'Chảo bò né nóng hổi xèo xèo cùng pate, trứng ốp la và bánh mì giòn rụm trên phố ẩm thực Phan Xích Long.', 'address': '142 Phan Xích Long, Phường 2, Quận Phú Nhuận, TP. Hồ Chí Minh', 'phone_number': '02835171122', 'cuisine_type': 'Món Việt', 'latitude': 10.7995, 'longitude': 106.6885, 'min_price': 50000.0, 'max_price': 120000.0, 'open_hours': '07:00 - 22:00', 'avg_rating': 4.5, 'total_reviews': 480, 'amenities': {'has_parking': True, 'has_private_room': False, 'has_outdoor': False, 'pet_friendly': False, 'vegetarian_support': False}, 'menus': [{'name': 'Món Đặc Trưng', 'description': 'Các món nổi bật nhất tại Bò Né 3 Ngon - Phan Xích Long', 'items': [{'name': 'Bò Né Đặc Biệt Full Topping', 'description': 'Món bán chạy hàng đầu tại Bò Né 3 Ngon - Phan Xích Long', 'price': 85000.0, 'image_url': 'https://images.unsplash.com/photo-1473093295043-cdd812d0e601?w=800'}, {'name': 'Bò Lúc Lắc Khoai Tây', 'description': 'Hương vị đặc sắc được thực khách yêu thích', 'price': 95000.0, 'image_url': 'https://images.unsplash.com/photo-1473093295043-cdd812d0e601?w=800'}]}], 'images': [{'image_url': 'https://images.unsplash.com/photo-1473093295043-cdd812d0e601?w=800', 'caption': 'Không gian và món ngon tại Bò Né 3 Ngon - Phan Xích Long', 'is_cover': True}]},
    {'name': 'Sushi Kei - Phan Xích Long', 'description': 'Nhà hàng Nhật Bản với sashimi cá hồi tươi sống và các set cơm lươn nướng đậm đà.', 'address': '210 Phan Xích Long, Phường 2, Quận Phú Nhuận, TP. Hồ Chí Minh', 'phone_number': '02873001188', 'cuisine_type': 'Món Nhật', 'latitude': 10.8008, 'longitude': 106.6892, 'min_price': 150000.0, 'max_price': 450000.0, 'open_hours': '10:30 - 22:00', 'avg_rating': 4.7, 'total_reviews': 510, 'amenities': {'has_parking': True, 'has_private_room': True, 'has_outdoor': False, 'pet_friendly': False, 'vegetarian_support': True}, 'menus': [{'name': 'Món Đặc Trưng', 'description': 'Các món nổi bật nhất tại Sushi Kei - Phan Xích Long', 'items': [{'name': 'Sashimi Cá Hồi Tươi', 'description': 'Món bán chạy hàng đầu tại Sushi Kei - Phan Xích Long', 'price': 175000.0, 'image_url': 'https://images.unsplash.com/photo-1490645935967-10de6ba17061?w=800'}, {'name': 'Cơm Lươn Nhật Nướng', 'description': 'Hương vị đặc sắc được thực khách yêu thích', 'price': 195000.0, 'image_url': 'https://images.unsplash.com/photo-1490645935967-10de6ba17061?w=800'}]}], 'images': [{'image_url': 'https://images.unsplash.com/photo-1490645935967-10de6ba17061?w=800', 'caption': 'Không gian và món ngon tại Sushi Kei - Phan Xích Long', 'is_cover': True}]},
    {'name': 'Chay Bồ Đề Ngọc Xanh - Huỳnh Văn Bánh', 'description': 'Ẩm thực chay thực dưỡng tinh tế, không bột ngọt, phục vụ lẩu nấm và các món cuốn thanh đạm.', 'address': '195 Huỳnh Văn Bánh, Phường 12, Quận Phú Nhuận, TP. Hồ Chí Minh', 'phone_number': '02838445566', 'cuisine_type': 'Món Chay', 'latitude': 10.7945, 'longitude': 106.6752, 'min_price': 55000.0, 'max_price': 180000.0, 'open_hours': '08:00 - 21:30', 'avg_rating': 4.7, 'total_reviews': 340, 'amenities': {'has_parking': True, 'has_private_room': True, 'has_outdoor': True, 'pet_friendly': False, 'vegetarian_support': True}, 'menus': [{'name': 'Món Đặc Trưng', 'description': 'Các món nổi bật nhất tại Chay Bồ Đề Ngọc Xanh - Huỳnh Văn Bánh', 'items': [{'name': 'Gỏi Ngó Sen Chay', 'description': 'Món bán chạy hàng đầu tại Chay Bồ Đề Ngọc Xanh - Huỳnh Văn Bánh', 'price': 75000.0, 'image_url': 'https://images.unsplash.com/photo-1493770348161-369560ae357d?w=800'}, {'name': 'Lẩu Nấm Trường Thọ', 'description': 'Hương vị đặc sắc được thực khách yêu thích', 'price': 175000.0, 'image_url': 'https://images.unsplash.com/photo-1493770348161-369560ae357d?w=800'}]}], 'images': [{'image_url': 'https://images.unsplash.com/photo-1493770348161-369560ae357d?w=800', 'caption': 'Không gian và món ngon tại Chay Bồ Đề Ngọc Xanh - Huỳnh Văn Bánh', 'is_cover': True}]},
    {'name': 'Phở Phú Vương - Lê Văn Sỹ', 'description': 'Tô phở bò nước dùng đậm vị miền Nam, thịt bò tái nạm gầu mềm ngọt nổi tiếng khu Lê Văn Sỹ.', 'address': '339 Lê Văn Sỹ, Phường 1, Quận Tân Bình', 'phone_number': '02838443322', 'cuisine_type': 'Món Việt', 'latitude': 10.7928, 'longitude': 106.6695, 'min_price': 65000.0, 'max_price': 105000.0, 'open_hours': '06:00 - 22:30', 'avg_rating': 4.6, 'total_reviews': 720, 'amenities': {'has_parking': True, 'has_private_room': False, 'has_outdoor': False, 'pet_friendly': False, 'vegetarian_support': False}, 'menus': [{'name': 'Món Đặc Trưng', 'description': 'Các món nổi bật nhất tại Phở Phú Vương - Lê Văn Sỹ', 'items': [{'name': 'Phở Tái Nạm Gầu', 'description': 'Món bán chạy hàng đầu tại Phở Phú Vương - Lê Văn Sỹ', 'price': 80000.0, 'image_url': 'https://images.unsplash.com/photo-1499028344343-cd173ffc68a9?w=800'}, {'name': 'Phở Đặc Biệt Tô Lớn', 'description': 'Hương vị đặc sắc được thực khách yêu thích', 'price': 100000.0, 'image_url': 'https://images.unsplash.com/photo-1499028344343-cd173ffc68a9?w=800'}]}], 'images': [{'image_url': 'https://images.unsplash.com/photo-1499028344343-cd173ffc68a9?w=800', 'caption': 'Không gian và món ngon tại Phở Phú Vương - Lê Văn Sỹ', 'is_cover': True}]},
    {'name': 'KPub Korean BBQ - Phan Xích Long', 'description': 'Nướng thùng phuy đường phố Hàn Quốc với quầy panchan và sốt phô mai béo ngậy.', 'address': '134 Phan Xích Long, Phường 7, Quận Phú Nhuận, TP. Hồ Chí Minh', 'phone_number': '02873009911', 'cuisine_type': 'Món Hàn', 'latitude': 10.7988, 'longitude': 106.6878, 'min_price': 229000.0, 'max_price': 399000.0, 'open_hours': '10:00 - 22:30', 'avg_rating': 4.6, 'total_reviews': 430, 'amenities': {'has_parking': True, 'has_private_room': False, 'has_outdoor': True, 'pet_friendly': False, 'vegetarian_support': False}, 'menus': [{'name': 'Món Đặc Trưng', 'description': 'Các món nổi bật nhất tại KPub Korean BBQ - Phan Xích Long', 'items': [{'name': 'Buffet Nướng Thùng Phuy', 'description': 'Món bán chạy hàng đầu tại KPub Korean BBQ - Phan Xích Long', 'price': 299000.0, 'image_url': 'https://images.unsplash.com/photo-1506354666786-959d6d497f1a?w=800'}, {'name': 'Sườn Bò Hoàng Đế', 'description': 'Hương vị đặc sắc được thực khách yêu thích', 'price': 249000.0, 'image_url': 'https://images.unsplash.com/photo-1506354666786-959d6d497f1a?w=800'}]}], 'images': [{'image_url': 'https://images.unsplash.com/photo-1506354666786-959d6d497f1a?w=800', 'caption': 'Không gian và món ngon tại KPub Korean BBQ - Phan Xích Long', 'is_cover': True}]},
    {'name': 'Cơm Tấm Ba Ghiền - Đặng Văn Ngữ', 'description': 'Quán cơm tấm đạt Michelin Bib Gourmand với miếng sườn cốt lết khổng lồ nướng than thơm phức.', 'address': '84 Đặng Văn Ngữ, Phường 10, Quận Phú Nhuận, TP. Hồ Chí Minh', 'phone_number': '02838461073', 'cuisine_type': 'Cơm tấm', 'latitude': 10.7958, 'longitude': 106.6672, 'min_price': 65000.0, 'max_price': 125000.0, 'open_hours': '07:30 - 21:30', 'avg_rating': 4.7, 'total_reviews': 1320, 'amenities': {'has_parking': True, 'has_private_room': False, 'has_outdoor': False, 'pet_friendly': False, 'vegetarian_support': False}, 'menus': [{'name': 'Món Đặc Trưng', 'description': 'Các món nổi bật nhất tại Cơm Tấm Ba Ghiền - Đặng Văn Ngữ', 'items': [{'name': 'Cơm Tấm Sườn Khổng Lồ', 'description': 'Món bán chạy hàng đầu tại Cơm Tấm Ba Ghiền - Đặng Văn Ngữ', 'price': 85000.0, 'image_url': 'https://images.unsplash.com/photo-1511690656952-34342bb7c2f2?w=800'}, {'name': 'Cơm Tấm Sườn Bì Chả Ốp La', 'description': 'Hương vị đặc sắc được thực khách yêu thích', 'price': 115000.0, 'image_url': 'https://images.unsplash.com/photo-1511690656952-34342bb7c2f2?w=800'}]}], 'images': [{'image_url': 'https://images.unsplash.com/photo-1511690656952-34342bb7c2f2?w=800', 'caption': 'Không gian và món ngon tại Cơm Tấm Ba Ghiền - Đặng Văn Ngữ', 'is_cover': True}]},
    {'name': 'Bánh Canh Trảng Bàng Hoàng Minh - Cộng Hòa', 'description': 'Đặc sản bánh canh giò heo và bánh tráng phơi sương cuốn thịt luộc rau rừng Tây Ninh.', 'address': '324 Cộng Hòa, Phường 13, Quận Tân Bình, TP. Hồ Chí Minh', 'phone_number': '02838101122', 'cuisine_type': 'Món Việt', 'latitude': 10.8022, 'longitude': 106.6478, 'min_price': 60000.0, 'max_price': 160000.0, 'open_hours': '07:00 - 22:00', 'avg_rating': 4.5, 'total_reviews': 490, 'amenities': {'has_parking': True, 'has_private_room': False, 'has_outdoor': False, 'pet_friendly': False, 'vegetarian_support': False}, 'menus': [{'name': 'Món Đặc Trưng', 'description': 'Các món nổi bật nhất tại Bánh Canh Trảng Bàng Hoàng Minh - Cộng Hòa', 'items': [{'name': 'Bánh Canh Giò Heo', 'description': 'Món bán chạy hàng đầu tại Bánh Canh Trảng Bàng Hoàng Minh - Cộng Hòa', 'price': 68000.0, 'image_url': 'https://images.unsplash.com/photo-1525351484163-7529414344d8?w=800'}, {'name': 'Bánh Tráng Cuốn Thịt Luộc', 'description': 'Hương vị đặc sắc được thực khách yêu thích', 'price': 135000.0, 'image_url': 'https://images.unsplash.com/photo-1525351484163-7529414344d8?w=800'}]}], 'images': [{'image_url': 'https://images.unsplash.com/photo-1525351484163-7529414344d8?w=800', 'caption': 'Không gian và món ngon tại Bánh Canh Trảng Bàng Hoàng Minh - Cộng Hòa', 'is_cover': True}]},
    {'name': 'Lẩu Bò Sài Gòn Vivu - Trường Chinh', 'description': 'Lẩu bò hầm sả thơm lừng với nạm, gân, đuôi bò mềm rục chấm chao sa tế cực bắt vị.', 'address': '415 Trường Chinh, Phường 14, Quận Tân Bình, TP. Hồ Chí Minh', 'phone_number': '02838492233', 'cuisine_type': 'Lẩu Nướng', 'latitude': 10.8055, 'longitude': 106.6395, 'min_price': 120000.0, 'max_price': 280000.0, 'open_hours': '10:30 - 22:30', 'avg_rating': 4.5, 'total_reviews': 370, 'amenities': {'has_parking': True, 'has_private_room': False, 'has_outdoor': True, 'pet_friendly': False, 'vegetarian_support': False}, 'menus': [{'name': 'Món Đặc Trưng', 'description': 'Các món nổi bật nhất tại Lẩu Bò Sài Gòn Vivu - Trường Chinh', 'items': [{'name': 'Lẩu Bò Thập Cẩm Nồi Lớn', 'description': 'Món bán chạy hàng đầu tại Lẩu Bò Sài Gòn Vivu - Trường Chinh', 'price': 260000.0, 'image_url': 'https://images.unsplash.com/photo-1528735602780-2552fd46c7af?w=800'}, {'name': 'Bò Nướng Ngói Sa Tế', 'description': 'Hương vị đặc sắc được thực khách yêu thích', 'price': 145000.0, 'image_url': 'https://images.unsplash.com/photo-1528735602780-2552fd46c7af?w=800'}]}], 'images': [{'image_url': 'https://images.unsplash.com/photo-1528735602780-2552fd46c7af?w=800', 'caption': 'Không gian và món ngon tại Lẩu Bò Sài Gòn Vivu - Trường Chinh', 'is_cover': True}]},
    {'name': 'Hải Sản Phố Biển - Bàu Cát', 'description': 'Hải sản tươi sống khu Bàu Cát với không gian sân vườn thoáng mát và phòng VIP tiếp khách.', 'address': '68 Đồng Đen, Phường 14, Quận Tân Bình, TP. Hồ Chí Minh', 'phone_number': '0909887766', 'cuisine_type': 'Hải Sản', 'latitude': 10.794, 'longitude': 106.6412, 'min_price': 140000.0, 'max_price': 480000.0, 'open_hours': '10:00 - 23:00', 'avg_rating': 4.5, 'total_reviews': 310, 'amenities': {'has_parking': True, 'has_private_room': True, 'has_outdoor': True, 'pet_friendly': False, 'vegetarian_support': False}, 'menus': [{'name': 'Món Đặc Trưng', 'description': 'Các món nổi bật nhất tại Hải Sản Phố Biển - Bàu Cát', 'items': [{'name': 'Tôm Càng Nướng Phô Mai', 'description': 'Món bán chạy hàng đầu tại Hải Sản Phố Biển - Bàu Cát', 'price': 290000.0, 'image_url': 'https://images.unsplash.com/photo-1532550907401-a500c9a57435?w=800'}, {'name': 'Mực Một Nắng Nướng Muối Ớt', 'description': 'Hương vị đặc sắc được thực khách yêu thích', 'price': 220000.0, 'image_url': 'https://images.unsplash.com/photo-1532550907401-a500c9a57435?w=800'}]}], 'images': [{'image_url': 'https://images.unsplash.com/photo-1532550907401-a500c9a57435?w=800', 'caption': 'Không gian và món ngon tại Hải Sản Phố Biển - Bàu Cát', 'is_cover': True}]},
    {'name': 'Highlands Coffee - Cộng Hòa Plaza', 'description': 'Không gian cà phê làm việc, gặp gỡ đối tác rộng rãi gần sân bay Tân Sơn Nhất.', 'address': '19 Cộng Hòa, Phường 12, Quận Tân Bình, TP. Hồ Chí Minh', 'phone_number': '19001755', 'cuisine_type': 'Cà Phê & Bánh', 'latitude': 10.8012, 'longitude': 106.652, 'min_price': 35000.0, 'max_price': 75000.0, 'open_hours': '07:00 - 22:30', 'avg_rating': 4.4, 'total_reviews': 620, 'amenities': {'has_parking': True, 'has_private_room': False, 'has_outdoor': True, 'pet_friendly': False, 'vegetarian_support': True}, 'menus': [{'name': 'Món Đặc Trưng', 'description': 'Các món nổi bật nhất tại Highlands Coffee - Cộng Hòa Plaza', 'items': [{'name': 'Phin Sữa Đá', 'description': 'Món bán chạy hàng đầu tại Highlands Coffee - Cộng Hòa Plaza', 'price': 39000.0, 'image_url': 'https://images.unsplash.com/photo-1539136788836-5699e78bfc75?w=800'}, {'name': 'Trà Sen Vàng', 'description': 'Hương vị đặc sắc được thực khách yêu thích', 'price': 55000.0, 'image_url': 'https://images.unsplash.com/photo-1539136788836-5699e78bfc75?w=800'}]}], 'images': [{'image_url': 'https://images.unsplash.com/photo-1539136788836-5699e78bfc75?w=800', 'caption': 'Không gian và món ngon tại Highlands Coffee - Cộng Hòa Plaza', 'is_cover': True}]},
    {'name': 'King BBQ Buffet - Aeon Mall Tân Phú', 'description': 'Buffet nướng Hàn Quốc hơn 50 món thịt bò Mỹ tẩm sốt King độc quyền tại Aeon Mall Tân Phú.', 'address': 'Tầng 3 Aeon Mall Celadon, 30 Bờ Bao Tân Thắng, Quận Tân Phú, TP. Hồ Chí Minh', 'phone_number': '1900234546', 'cuisine_type': 'Lẩu Nướng', 'latitude': 10.8015, 'longitude': 106.6175, 'min_price': 259000.0, 'max_price': 399000.0, 'open_hours': '10:00 - 22:00', 'avg_rating': 4.6, 'total_reviews': 680, 'amenities': {'has_parking': True, 'has_private_room': True, 'has_outdoor': False, 'pet_friendly': False, 'vegetarian_support': False}, 'menus': [{'name': 'Món Đặc Trưng', 'description': 'Các món nổi bật nhất tại King BBQ Buffet - Aeon Mall Tân Phú', 'items': [{'name': 'Buffet Nướng King BBQ', 'description': 'Món bán chạy hàng đầu tại King BBQ Buffet - Aeon Mall Tân Phú', 'price': 329000.0, 'image_url': 'https://images.unsplash.com/photo-1540189549336-e6e99c3679fe?w=800'}, {'name': 'Cổ Bò Mỹ Sốt King', 'description': 'Hương vị đặc sắc được thực khách yêu thích', 'price': 189000.0, 'image_url': 'https://images.unsplash.com/photo-1540189549336-e6e99c3679fe?w=800'}]}], 'images': [{'image_url': 'https://images.unsplash.com/photo-1540189549336-e6e99c3679fe?w=800', 'caption': 'Không gian và món ngon tại King BBQ Buffet - Aeon Mall Tân Phú', 'is_cover': True}]},
    {'name': 'Chay Sen Vàng - Lũy Bán Bích', 'description': 'Quán chay bình dân sạch sẽ với thực đơn bún riêu chay, hủ tiếu chay và lẩu nấm thơm ngon.', 'address': '512 Lũy Bán Bích, Phường Hòa Thạnh, Quận Tân Phú, TP. Hồ Chí Minh', 'phone_number': '0903123789', 'cuisine_type': 'Món Chay', 'latitude': 10.7812, 'longitude': 106.6345, 'min_price': 40000.0, 'max_price': 120000.0, 'open_hours': '07:00 - 21:00', 'avg_rating': 4.5, 'total_reviews': 210, 'amenities': {'has_parking': True, 'has_private_room': False, 'has_outdoor': False, 'pet_friendly': False, 'vegetarian_support': True}, 'menus': [{'name': 'Món Đặc Trưng', 'description': 'Các món nổi bật nhất tại Chay Sen Vàng - Lũy Bán Bích', 'items': [{'name': 'Bún Riêu Chay', 'description': 'Món bán chạy hàng đầu tại Chay Sen Vàng - Lũy Bán Bích', 'price': 45000.0, 'image_url': 'https://images.unsplash.com/photo-1543339308-43e59d6b73a6?w=800'}, {'name': 'Lẩu Nấm Chay Thập Cẩm', 'description': 'Hương vị đặc sắc được thực khách yêu thích', 'price': 120000.0, 'image_url': 'https://images.unsplash.com/photo-1543339308-43e59d6b73a6?w=800'}]}], 'images': [{'image_url': 'https://images.unsplash.com/photo-1543339308-43e59d6b73a6?w=800', 'caption': 'Không gian và món ngon tại Chay Sen Vàng - Lũy Bán Bích', 'is_cover': True}]},
    {'name': 'Ốc Nhớ Sài Gòn - Tân Kỳ Tân Quý', 'description': 'Quán ốc đêm đông khách nổi tiếng Tân Phú với sốt trứng muối, sốt bơ cay béo ngậy.', 'address': '218 Tân Kỳ Tân Quý, Phường Sơn Kỳ, Quận Tân Phú, TP. Hồ Chí Minh', 'phone_number': '0938556677', 'cuisine_type': 'Hải Sản', 'latitude': 10.8045, 'longitude': 106.625, 'min_price': 50000.0, 'max_price': 180000.0, 'open_hours': '16:00 - 23:30', 'avg_rating': 4.5, 'total_reviews': 440, 'amenities': {'has_parking': True, 'has_private_room': False, 'has_outdoor': True, 'pet_friendly': True, 'vegetarian_support': False}, 'menus': [{'name': 'Món Đặc Trưng', 'description': 'Các món nổi bật nhất tại Ốc Nhớ Sài Gòn - Tân Kỳ Tân Quý', 'items': [{'name': 'Ốc Hương Sốt Trứng Muối', 'description': 'Món bán chạy hàng đầu tại Ốc Nhớ Sài Gòn - Tân Kỳ Tân Quý', 'price': 95000.0, 'image_url': 'https://images.unsplash.com/photo-1547592166-23ac45744acd?w=800'}, {'name': 'Sò Huyết Xào Me', 'description': 'Hương vị đặc sắc được thực khách yêu thích', 'price': 75000.0, 'image_url': 'https://images.unsplash.com/photo-1547592166-23ac45744acd?w=800'}]}], 'images': [{'image_url': 'https://images.unsplash.com/photo-1547592166-23ac45744acd?w=800', 'caption': 'Không gian và món ngon tại Ốc Nhớ Sài Gòn - Tân Kỳ Tân Quý', 'is_cover': True}]},
    {'name': 'Bún Đậu Mắm Tôm A Chảnh - Tân Sơn Nhì', 'description': 'Mẹt bún đậu tá lả đầy đặn chả cốm Hà Nội, nem chua rán, thịt chân giò luộc chấm mắm tôm đánh bông.', 'address': '145 Tân Sơn Nhì, Phường Tân Sơn Nhì, Quận Tân Phú, TP. Hồ Chí Minh', 'phone_number': '0902445566', 'cuisine_type': 'Món Việt', 'latitude': 10.7935, 'longitude': 106.6318, 'min_price': 45000.0, 'max_price': 95000.0, 'open_hours': '10:00 - 22:00', 'avg_rating': 4.4, 'total_reviews': 330, 'amenities': {'has_parking': True, 'has_private_room': False, 'has_outdoor': False, 'pet_friendly': False, 'vegetarian_support': False}, 'menus': [{'name': 'Món Đặc Trưng', 'description': 'Các món nổi bật nhất tại Bún Đậu Mắm Tôm A Chảnh - Tân Sơn Nhì', 'items': [{'name': 'Mẹt Bún Đậu Tá Lả', 'description': 'Món bán chạy hàng đầu tại Bún Đậu Mắm Tôm A Chảnh - Tân Sơn Nhì', 'price': 69000.0, 'image_url': 'https://images.unsplash.com/photo-1551024709-8f23befc6f87?w=800'}, {'name': 'Chả Cốm Chiên Giòn', 'description': 'Hương vị đặc sắc được thực khách yêu thích', 'price': 35000.0, 'image_url': 'https://images.unsplash.com/photo-1551024709-8f23befc6f87?w=800'}]}], 'images': [{'image_url': 'https://images.unsplash.com/photo-1551024709-8f23befc6f87?w=800', 'caption': 'Không gian và món ngon tại Bún Đậu Mắm Tôm A Chảnh - Tân Sơn Nhì', 'is_cover': True}]},
    {'name': 'Ốc Oanh - Vĩnh Khánh', 'description': 'Quán ốc biểu tượng của phố ẩm thực Vĩnh Khánh Quận 4, nổi tiếng với càng ghẹ rang muối ớt và ốc hương.', 'address': '534 Vĩnh Khánh, Phường 8, Quận 4, TP. Hồ Chí Minh', 'phone_number': '0909334455', 'cuisine_type': 'Hải Sản', 'latitude': 10.7615, 'longitude': 106.7032, 'min_price': 80000.0, 'max_price': 280000.0, 'open_hours': '15:00 - 00:00', 'avg_rating': 4.6, 'total_reviews': 1180, 'amenities': {'has_parking': True, 'has_private_room': False, 'has_outdoor': True, 'pet_friendly': True, 'vegetarian_support': False}, 'menus': [{'name': 'Món Đặc Trưng', 'description': 'Các món nổi bật nhất tại Ốc Oanh - Vĩnh Khánh', 'items': [{'name': 'Càng Ghẹ Rang Muối Ớt', 'description': 'Món bán chạy hàng đầu tại Ốc Oanh - Vĩnh Khánh', 'price': 160000.0, 'image_url': 'https://images.unsplash.com/photo-1551782450-a2132b4ba21d?w=800'}, {'name': 'Ốc Hương Nướng Mọi', 'description': 'Hương vị đặc sắc được thực khách yêu thích', 'price': 110000.0, 'image_url': 'https://images.unsplash.com/photo-1551782450-a2132b4ba21d?w=800'}]}], 'images': [{'image_url': 'https://images.unsplash.com/photo-1551782450-a2132b4ba21d?w=800', 'caption': 'Không gian và món ngon tại Ốc Oanh - Vĩnh Khánh', 'is_cover': True}]},
    {'name': 'Sushi Ko - Vĩnh Khánh', 'description': 'Sushi bình dân chất lượng cao nổi tiếng khắp Sài Gòn, cá hồi tươi cắt lát dày.', 'address': '122/37 Vĩnh Khánh, Phường 10, Quận 4, TP. Hồ Chí Minh', 'phone_number': '0908667788', 'cuisine_type': 'Món Nhật', 'latitude': 10.7602, 'longitude': 106.7048, 'min_price': 60000.0, 'max_price': 180000.0, 'open_hours': '16:00 - 22:30', 'avg_rating': 4.5, 'total_reviews': 590, 'amenities': {'has_parking': True, 'has_private_room': False, 'has_outdoor': True, 'pet_friendly': False, 'vegetarian_support': False}, 'menus': [{'name': 'Món Đặc Trưng', 'description': 'Các món nổi bật nhất tại Sushi Ko - Vĩnh Khánh', 'items': [{'name': 'Sashimi Cá Hồi (8 lát)', 'description': 'Món bán chạy hàng đầu tại Sushi Ko - Vĩnh Khánh', 'price': 115000.0, 'image_url': 'https://images.unsplash.com/photo-1555949258-eb67b1ef0ceb?w=800'}, {'name': 'Sushi Lươn Nhật', 'description': 'Hương vị đặc sắc được thực khách yêu thích', 'price': 85000.0, 'image_url': 'https://images.unsplash.com/photo-1555949258-eb67b1ef0ceb?w=800'}]}], 'images': [{'image_url': 'https://images.unsplash.com/photo-1555949258-eb67b1ef0ceb?w=800', 'caption': 'Không gian và món ngon tại Sushi Ko - Vĩnh Khánh', 'is_cover': True}]},
    {'name': 'Cơm Tấm Bãi Rác - Lê Văn Linh', 'description': 'Quán cơm tấm đêm huyền thoại Quận 4 với đủ loại đồ ăn kèm từ sườn nướng đến mực nhồi thịt.', 'address': '73 Lê Văn Linh, Phường 12, Quận 4, TP. Hồ Chí Minh', 'phone_number': '0903998877', 'cuisine_type': 'Cơm tấm', 'latitude': 10.7642, 'longitude': 106.7055, 'min_price': 70000.0, 'max_price': 130000.0, 'open_hours': '17:00 - 01:00', 'avg_rating': 4.4, 'total_reviews': 640, 'amenities': {'has_parking': False, 'has_private_room': False, 'has_outdoor': True, 'pet_friendly': False, 'vegetarian_support': False}, 'menus': [{'name': 'Món Đặc Trưng', 'description': 'Các món nổi bật nhất tại Cơm Tấm Bãi Rác - Lê Văn Linh', 'items': [{'name': 'Cơm Tấm Sườn Trứng Mực Nhồi', 'description': 'Món bán chạy hàng đầu tại Cơm Tấm Bãi Rác - Lê Văn Linh', 'price': 110000.0, 'image_url': 'https://images.unsplash.com/photo-1560717845-968823efbee1?w=800'}, {'name': 'Cơm Tấm Sườn Bì Chả', 'description': 'Hương vị đặc sắc được thực khách yêu thích', 'price': 85000.0, 'image_url': 'https://images.unsplash.com/photo-1560717845-968823efbee1?w=800'}]}], 'images': [{'image_url': 'https://images.unsplash.com/photo-1560717845-968823efbee1?w=800', 'caption': 'Không gian và món ngon tại Cơm Tấm Bãi Rác - Lê Văn Linh', 'is_cover': True}]},
    {'name': 'Elisa Floating Restaurant - Bến Nhà Rồng', 'description': 'Nhà hàng tàu nổi 5 sao trên sông Sài Gòn với thực đơn Âu - Á cao cấp và view thành phố về đêm.', 'address': '5 Nguyễn Tất Thành, Phường 12, Quận 4, TP. Hồ Chí Minh', 'phone_number': '02838299999', 'cuisine_type': 'Món Âu', 'latitude': 10.7685, 'longitude': 106.7072, 'min_price': 350000.0, 'max_price': 1500000.0, 'open_hours': '10:00 - 23:00', 'avg_rating': 4.7, 'total_reviews': 760, 'amenities': {'has_parking': True, 'has_private_room': True, 'has_outdoor': True, 'pet_friendly': False, 'vegetarian_support': True}, 'menus': [{'name': 'Món Đặc Trưng', 'description': 'Các món nổi bật nhất tại Elisa Floating Restaurant - Bến Nhà Rồng', 'items': [{'name': 'Bò Úc Nướng Sốt Tiêu Đen', 'description': 'Món bán chạy hàng đầu tại Elisa Floating Restaurant - Bến Nhà Rồng', 'price': 480000.0, 'image_url': 'https://images.unsplash.com/photo-1562967914-608f82629710?w=800'}, {'name': 'Tôm Hùm Nướng Bơ Tỏi', 'description': 'Hương vị đặc sắc được thực khách yêu thích', 'price': 890000.0, 'image_url': 'https://images.unsplash.com/photo-1562967914-608f82629710?w=800'}]}], 'images': [{'image_url': 'https://images.unsplash.com/photo-1562967914-608f82629710?w=800', 'caption': 'Không gian và món ngon tại Elisa Floating Restaurant - Bến Nhà Rồng', 'is_cover': True}]},
    {'name': 'Dimsum Baoz - Nguyễn Tri Phương', 'description': 'Nhà hàng Dimsum Hồng Kông nức tiếng Quận 5 với há cảo, bánh bao kim sa và vịt quay giòn da.', 'address': '88 Nguyễn Tri Phương, Phường 7, Quận 5, TP. Hồ Chí Minh', 'phone_number': '02839231480', 'cuisine_type': 'Món Hoa', 'latitude': 10.7575, 'longitude': 106.669, 'min_price': 120000.0, 'max_price': 420000.0, 'open_hours': '06:30 - 22:30', 'avg_rating': 4.7, 'total_reviews': 1250, 'amenities': {'has_parking': True, 'has_private_room': True, 'has_outdoor': False, 'pet_friendly': False, 'vegetarian_support': True}, 'menus': [{'name': 'Món Đặc Trưng', 'description': 'Các món nổi bật nhất tại Dimsum Baoz - Nguyễn Tri Phương', 'items': [{'name': 'Há Cảo Tôm Tươi Baoz', 'description': 'Món bán chạy hàng đầu tại Dimsum Baoz - Nguyễn Tri Phương', 'price': 78000.0, 'image_url': 'https://images.unsplash.com/photo-1563379926898-05f4575a45d8?w=800'}, {'name': 'Vịt Quay Hồng Kông', 'description': 'Hương vị đặc sắc được thực khách yêu thích', 'price': 320000.0, 'image_url': 'https://images.unsplash.com/photo-1563379926898-05f4575a45d8?w=800'}]}], 'images': [{'image_url': 'https://images.unsplash.com/photo-1563379926898-05f4575a45d8?w=800', 'caption': 'Không gian và món ngon tại Dimsum Baoz - Nguyễn Tri Phương', 'is_cover': True}]},
    {'name': 'Lẩu Cá Dân Ích - Châu Văn Liêm', 'description': 'Lẩu cá cù lao đốt than truyền thống của người Hoa hơn 40 năm tuổi, nước lẩu ngọt thanh đậm đà.', 'address': '99 Châu Văn Liêm, Phường 14, Quận 5, TP. Hồ Chí Minh', 'phone_number': '02838551887', 'cuisine_type': 'Món Hoa', 'latitude': 10.7525, 'longitude': 106.6598, 'min_price': 120000.0, 'max_price': 320000.0, 'open_hours': '16:00 - 22:00', 'avg_rating': 4.6, 'total_reviews': 870, 'amenities': {'has_parking': True, 'has_private_room': False, 'has_outdoor': False, 'pet_friendly': False, 'vegetarian_support': False}, 'menus': [{'name': 'Món Đặc Trưng', 'description': 'Các món nổi bật nhất tại Lẩu Cá Dân Ích - Châu Văn Liêm', 'items': [{'name': 'Lẩu Cá Cù Lao Thập Cẩm', 'description': 'Món bán chạy hàng đầu tại Lẩu Cá Dân Ích - Châu Văn Liêm', 'price': 290000.0, 'image_url': 'https://images.unsplash.com/photo-1564834724105-918b73d1b9e0?w=800'}, {'name': 'Chả Giò Tôm Cua', 'description': 'Hương vị đặc sắc được thực khách yêu thích', 'price': 95000.0, 'image_url': 'https://images.unsplash.com/photo-1564834724105-918b73d1b9e0?w=800'}]}], 'images': [{'image_url': 'https://images.unsplash.com/photo-1564834724105-918b73d1b9e0?w=800', 'caption': 'Không gian và món ngon tại Lẩu Cá Dân Ích - Châu Văn Liêm', 'is_cover': True}]},
    {'name': 'Cơm Gà Đông Nguyên - Châu Văn Liêm', 'description': 'Thương hiệu cơm gà Hải Nam lâu đời từ năm 1945 tại Chợ Lớn, gà ta luộc da vàng giòn thịt ngọt.', 'address': '801 Nguyễn Trãi, Phường 14, Quận 5, TP. Hồ Chí Minh', 'phone_number': '02838557678', 'cuisine_type': 'Món Hoa', 'latitude': 10.7532, 'longitude': 106.6612, 'min_price': 85000.0, 'max_price': 220000.0, 'open_hours': '09:00 - 20:30', 'avg_rating': 4.6, 'total_reviews': 940, 'amenities': {'has_parking': True, 'has_private_room': False, 'has_outdoor': False, 'pet_friendly': False, 'vegetarian_support': False}, 'menus': [{'name': 'Món Đặc Trưng', 'description': 'Các món nổi bật nhất tại Cơm Gà Đông Nguyên - Châu Văn Liêm', 'items': [{'name': 'Cơm Gà Luộc Chặt Đĩa', 'description': 'Món bán chạy hàng đầu tại Cơm Gà Đông Nguyên - Châu Văn Liêm', 'price': 135000.0, 'image_url': 'https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=800'}, {'name': 'Canh Tiềm Thuốc Bắc', 'description': 'Hương vị đặc sắc được thực khách yêu thích', 'price': 85000.0, 'image_url': 'https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=800'}]}], 'images': [{'image_url': 'https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=800', 'caption': 'Không gian và món ngon tại Cơm Gà Đông Nguyên - Châu Văn Liêm', 'is_cover': True}]},
    {'name': 'Chè Hà Ký - Châu Văn Liêm', 'description': 'Tiệm chè người Hoa nổi tiếng với hơn 30 món chè dưỡng nhan: quy linh cao, chè mè đen, hột gà trà.', 'address': '138 Châu Văn Liêm, Phường 11, Quận 5, TP. Hồ Chí Minh', 'phone_number': '02838567039', 'cuisine_type': 'Cà Phê & Bánh', 'latitude': 10.7538, 'longitude': 106.6592, 'min_price': 30000.0, 'max_price': 65000.0, 'open_hours': '10:00 - 22:30', 'avg_rating': 4.6, 'total_reviews': 810, 'amenities': {'has_parking': False, 'has_private_room': False, 'has_outdoor': False, 'pet_friendly': False, 'vegetarian_support': True}, 'menus': [{'name': 'Món Đặc Trưng', 'description': 'Các món nổi bật nhất tại Chè Hà Ký - Châu Văn Liêm', 'items': [{'name': 'Chè Mè Đen Hạnh Nhân', 'description': 'Món bán chạy hàng đầu tại Chè Hà Ký - Châu Văn Liêm', 'price': 38000.0, 'image_url': 'https://images.unsplash.com/photo-1572802419224-296b0aeee0d9?w=800'}, {'name': 'Quy Linh Cao Mật Ong', 'description': 'Hương vị đặc sắc được thực khách yêu thích', 'price': 42000.0, 'image_url': 'https://images.unsplash.com/photo-1572802419224-296b0aeee0d9?w=800'}]}], 'images': [{'image_url': 'https://images.unsplash.com/photo-1572802419224-296b0aeee0d9?w=800', 'caption': 'Không gian và món ngon tại Chè Hà Ký - Châu Văn Liêm', 'is_cover': True}]},
    {'name': 'Chay Giác Ngộ - Nguyễn Chí Thanh', 'description': 'Nhà hàng chay thanh lịch tại Quận 5 phục vụ các món chay phong cách Hoa - Việt tinh tế.', 'address': '213A Hùng Vương, Phường 9, Quận 5, TP. Hồ Chí Minh', 'phone_number': '02838332211', 'cuisine_type': 'Món Chay', 'latitude': 10.7585, 'longitude': 106.6685, 'min_price': 45000.0, 'max_price': 150000.0, 'open_hours': '08:00 - 21:00', 'avg_rating': 4.6, 'total_reviews': 310, 'amenities': {'has_parking': True, 'has_private_room': True, 'has_outdoor': False, 'pet_friendly': False, 'vegetarian_support': True}, 'menus': [{'name': 'Món Đặc Trưng', 'description': 'Các món nổi bật nhất tại Chay Giác Ngộ - Nguyễn Chí Thanh', 'items': [{'name': 'Mì Xào Giòn Chay', 'description': 'Món bán chạy hàng đầu tại Chay Giác Ngộ - Nguyễn Chí Thanh', 'price': 75000.0, 'image_url': 'https://images.unsplash.com/photo-1576867757603-05b134ebc379?w=800'}, {'name': 'Lẩu Thái Chay', 'description': 'Hương vị đặc sắc được thực khách yêu thích', 'price': 145000.0, 'image_url': 'https://images.unsplash.com/photo-1576867757603-05b134ebc379?w=800'}]}], 'images': [{'image_url': 'https://images.unsplash.com/photo-1576867757603-05b134ebc379?w=800', 'caption': 'Không gian và món ngon tại Chay Giác Ngộ - Nguyễn Chí Thanh', 'is_cover': True}]},
    {'name': 'Hủ Tiếu Hồ - Hậu Giang', 'description': 'Đặc sản hủ tiếu hồ Campuchia hiếm có tại Quận 6 với bánh hủ tiếu bản vuông ăn kèm phá lấu và cải chua.', 'address': '185 Hậu Giang, Phường 5, Quận 6, TP. Hồ Chí Minh', 'phone_number': '0908223344', 'cuisine_type': 'Món Việt', 'latitude': 10.7485, 'longitude': 106.6412, 'min_price': 45000.0, 'max_price': 80000.0, 'open_hours': '06:30 - 21:30', 'avg_rating': 4.5, 'total_reviews': 340, 'amenities': {'has_parking': True, 'has_private_room': False, 'has_outdoor': False, 'pet_friendly': False, 'vegetarian_support': False}, 'menus': [{'name': 'Món Đặc Trưng', 'description': 'Các món nổi bật nhất tại Hủ Tiếu Hồ - Hậu Giang', 'items': [{'name': 'Hủ Tiếu Hồ Phá Lấu', 'description': 'Món bán chạy hàng đầu tại Hủ Tiếu Hồ - Hậu Giang', 'price': 58000.0, 'image_url': 'https://images.unsplash.com/photo-1585032226651-759b368d7246?w=800'}, {'name': 'Hủ Tiếu Hồ Khô Đặc Biệt', 'description': 'Hương vị đặc sắc được thực khách yêu thích', 'price': 68000.0, 'image_url': 'https://images.unsplash.com/photo-1585032226651-759b368d7246?w=800'}]}], 'images': [{'image_url': 'https://images.unsplash.com/photo-1585032226651-759b368d7246?w=800', 'caption': 'Không gian và món ngon tại Hủ Tiếu Hồ - Hậu Giang', 'is_cover': True}]},
    {'name': 'Lẩu Bò Khu Bình Phú', 'description': 'Quán lẩu bò sân vườn thoáng mát khu dân cư Bình Phú, thịt bò tươi ngon và bãi đậu ô tô rộng.', 'address': '45 Đường Số 10, Phường 10, Quận 6, TP. Hồ Chí Minh', 'phone_number': '0937112299', 'cuisine_type': 'Lẩu Nướng', 'latitude': 10.7425, 'longitude': 106.6295, 'min_price': 100000.0, 'max_price': 260000.0, 'open_hours': '15:00 - 23:00', 'avg_rating': 4.5, 'total_reviews': 290, 'amenities': {'has_parking': True, 'has_private_room': False, 'has_outdoor': True, 'pet_friendly': True, 'vegetarian_support': False}, 'menus': [{'name': 'Món Đặc Trưng', 'description': 'Các món nổi bật nhất tại Lẩu Bò Khu Bình Phú', 'items': [{'name': 'Lẩu Đuôi Bò Khoai Môn', 'description': 'Món bán chạy hàng đầu tại Lẩu Bò Khu Bình Phú', 'price': 240000.0, 'image_url': 'https://images.unsplash.com/photo-1588166524941-3bf61a9c41db?w=800'}, {'name': 'Bò Nướng Lụi Sả', 'description': 'Hương vị đặc sắc được thực khách yêu thích', 'price': 135000.0, 'image_url': 'https://images.unsplash.com/photo-1588166524941-3bf61a9c41db?w=800'}]}], 'images': [{'image_url': 'https://images.unsplash.com/photo-1588166524941-3bf61a9c41db?w=800', 'caption': 'Không gian và món ngon tại Lẩu Bò Khu Bình Phú', 'is_cover': True}]},
    {'name': 'Dimsum Tân Nguyên Thái - Bình Tây', 'description': 'Tiệm điểm tâm sáng chuẩn vị người Hoa khu Chợ Bình Tây, bánh cuốn tôm và xíu mại hấp nóng hổi.', 'address': '102 Bình Tây, Phường 1, Quận 6, TP. Hồ Chí Minh', 'phone_number': '02838541234', 'cuisine_type': 'Món Hoa', 'latitude': 10.7492, 'longitude': 106.651, 'min_price': 60000.0, 'max_price': 180000.0, 'open_hours': '06:00 - 13:00', 'avg_rating': 4.5, 'total_reviews': 410, 'amenities': {'has_parking': True, 'has_private_room': False, 'has_outdoor': False, 'pet_friendly': False, 'vegetarian_support': False}, 'menus': [{'name': 'Món Đặc Trưng', 'description': 'Các món nổi bật nhất tại Dimsum Tân Nguyên Thái - Bình Tây', 'items': [{'name': 'Xíu Mại Tôm Thịt', 'description': 'Món bán chạy hàng đầu tại Dimsum Tân Nguyên Thái - Bình Tây', 'price': 55000.0, 'image_url': 'https://images.unsplash.com/photo-1598515214211-89d3c73ae83b?w=800'}, {'name': 'Bánh Cuốn Xá Xíu', 'description': 'Hương vị đặc sắc được thực khách yêu thích', 'price': 52000.0, 'image_url': 'https://images.unsplash.com/photo-1598515214211-89d3c73ae83b?w=800'}]}], 'images': [{'image_url': 'https://images.unsplash.com/photo-1598515214211-89d3c73ae83b?w=800', 'caption': 'Không gian và món ngon tại Dimsum Tân Nguyên Thái - Bình Tây', 'is_cover': True}]},
    {'name': "Pizza 4P's Phú Mỹ Hưng", 'description': 'Không gian hiện đại, rộng rãi tại Phú Mỹ Hưng với pizza phô mai tươi Burrata nướng lò củi trứ danh.', 'address': 'MD2 Nguyễn Văn Linh, Phường Tân Phú, Quận 7, TP. Hồ Chí Minh', 'phone_number': '02836220501', 'cuisine_type': 'Món Âu', 'latitude': 10.7285, 'longitude': 106.7185, 'min_price': 180000.0, 'max_price': 480000.0, 'open_hours': '10:00 - 23:00', 'avg_rating': 4.8, 'total_reviews': 920, 'amenities': {'has_parking': True, 'has_private_room': True, 'has_outdoor': True, 'pet_friendly': False, 'vegetarian_support': True}, 'menus': [{'name': 'Món Đặc Trưng', 'description': "Các món nổi bật nhất tại Pizza 4P's Phú Mỹ Hưng", 'items': [{'name': 'Pizza 4 Cheese', 'description': "Món bán chạy hàng đầu tại Pizza 4P's Phú Mỹ Hưng", 'price': 280000.0, 'image_url': 'https://images.unsplash.com/photo-1600891964599-f61ba0e24092?w=800'}, {'name': 'Mì Ý Cua Cà Chua', 'description': 'Hương vị đặc sắc được thực khách yêu thích', 'price': 245000.0, 'image_url': 'https://images.unsplash.com/photo-1600891964599-f61ba0e24092?w=800'}]}], 'images': [{'image_url': 'https://images.unsplash.com/photo-1600891964599-f61ba0e24092?w=800', 'caption': "Không gian và món ngon tại Pizza 4P's Phú Mỹ Hưng", 'is_cover': True}]},
    {'name': "D'Maris Buffet - Lotte Mart Quận 7", 'description': 'Nhà hàng buffet quốc tế cao cấp hơn 200 món Á - Âu, hải sản, sushi và quầy bánh ngọt khổng lồ.', 'address': 'Tầng 3 Lotte Mart, 469 Nguyễn Hữu Thọ, Quận 7, TP. Hồ Chí Minh', 'phone_number': '19000010', 'cuisine_type': 'Hải Sản', 'latitude': 10.7412, 'longitude': 106.7018, 'min_price': 450000.0, 'max_price': 620000.0, 'open_hours': '11:00 - 22:00', 'avg_rating': 4.7, 'total_reviews': 1050, 'amenities': {'has_parking': True, 'has_private_room': True, 'has_outdoor': False, 'pet_friendly': False, 'vegetarian_support': True}, 'menus': [{'name': 'Món Đặc Trưng', 'description': "Các món nổi bật nhất tại D'Maris Buffet - Lotte Mart Quận 7", 'items': [{'name': 'Vé Buffet Hải Sản Cao Cấp', 'description': "Món bán chạy hàng đầu tại D'Maris Buffet - Lotte Mart Quận 7", 'price': 540000.0, 'image_url': 'https://images.unsplash.com/photo-1603133872878-684f208fb84b?w=800'}, {'name': 'Sashimi & Hải Sản Không Giới Hạn', 'description': 'Hương vị đặc sắc được thực khách yêu thích', 'price': 540000.0, 'image_url': 'https://images.unsplash.com/photo-1603133872878-684f208fb84b?w=800'}]}], 'images': [{'image_url': 'https://images.unsplash.com/photo-1603133872878-684f208fb84b?w=800', 'caption': "Không gian và món ngon tại D'Maris Buffet - Lotte Mart Quận 7", 'is_cover': True}]},
    {'name': 'Marduk Korean BBQ - Phú Mỹ Hưng', 'description': 'Quán nướng Hàn Quốc chuẩn vị của người Hàn tại khu phố Hàn Phú Mỹ Hưng, thịt heo ủ lạnh mềm ngọt.', 'address': '56 Hưng Gia 2, Phường Tân Phong, Quận 7, TP. Hồ Chí Minh', 'phone_number': '02854101234', 'cuisine_type': 'Món Hàn', 'latitude': 10.7315, 'longitude': 106.7072, 'min_price': 200000.0, 'max_price': 550000.0, 'open_hours': '11:00 - 23:00', 'avg_rating': 4.7, 'total_reviews': 460, 'amenities': {'has_parking': True, 'has_private_room': True, 'has_outdoor': False, 'pet_friendly': False, 'vegetarian_support': False}, 'menus': [{'name': 'Món Đặc Trưng', 'description': 'Các món nổi bật nhất tại Marduk Korean BBQ - Phú Mỹ Hưng', 'items': [{'name': 'Ba Chỉ Heo Ủ Lạnh Nướng', 'description': 'Món bán chạy hàng đầu tại Marduk Korean BBQ - Phú Mỹ Hưng', 'price': 260000.0, 'image_url': 'https://images.unsplash.com/photo-1604908176997-125f25cc6f3d?w=800'}, {'name': 'Canh Kim Chi Thịt Heo', 'description': 'Hương vị đặc sắc được thực khách yêu thích', 'price': 150000.0, 'image_url': 'https://images.unsplash.com/photo-1604908176997-125f25cc6f3d?w=800'}]}], 'images': [{'image_url': 'https://images.unsplash.com/photo-1604908176997-125f25cc6f3d?w=800', 'caption': 'Không gian và món ngon tại Marduk Korean BBQ - Phú Mỹ Hưng', 'is_cover': True}]},
    {'name': 'Chay Garden - Nguyễn Thị Thập', 'description': 'Nhà hàng chay sân vườn xanh mát tại Quận 7, thích hợp cho bữa cơm gia đình cuối tuần.', 'address': '128 Nguyễn Thị Thập, Phường Bình Thuận, Quận 7, TP. Hồ Chí Minh', 'phone_number': '02837751122', 'cuisine_type': 'Món Chay', 'latitude': 10.7385, 'longitude': 106.7195, 'min_price': 75000.0, 'max_price': 240000.0, 'open_hours': '09:00 - 21:30', 'avg_rating': 4.7, 'total_reviews': 380, 'amenities': {'has_parking': True, 'has_private_room': True, 'has_outdoor': True, 'pet_friendly': True, 'vegetarian_support': True}, 'menus': [{'name': 'Món Đặc Trưng', 'description': 'Các món nổi bật nhất tại Chay Garden - Nguyễn Thị Thập', 'items': [{'name': 'Gỏi Bưởi Chay', 'description': 'Món bán chạy hàng đầu tại Chay Garden - Nguyễn Thị Thập', 'price': 95000.0, 'image_url': 'https://images.unsplash.com/photo-1606787366850-de6330128bfc?w=800'}, {'name': 'Lẩu Nấm Hoa Chuối', 'description': 'Hương vị đặc sắc được thực khách yêu thích', 'price': 210000.0, 'image_url': 'https://images.unsplash.com/photo-1606787366850-de6330128bfc?w=800'}]}], 'images': [{'image_url': 'https://images.unsplash.com/photo-1606787366850-de6330128bfc?w=800', 'caption': 'Không gian và món ngon tại Chay Garden - Nguyễn Thị Thập', 'is_cover': True}]},
    {'name': 'Phở Phú Gia - Sky Garden', 'description': 'Phở Bắc chuẩn vị Hà Nội tại khu Phú Mỹ Hưng, nước dùng trong vắt thơm mùi gừng nướng và hành hoa.', 'address': 'R1-42 Sky Garden 2, Phường Tân Phong, Quận 7, TP. Hồ Chí Minh', 'phone_number': '0908775533', 'cuisine_type': 'Món Việt', 'latitude': 10.7295, 'longitude': 106.7042, 'min_price': 65000.0, 'max_price': 110000.0, 'open_hours': '06:30 - 21:30', 'avg_rating': 4.6, 'total_reviews': 420, 'amenities': {'has_parking': True, 'has_private_room': False, 'has_outdoor': False, 'pet_friendly': False, 'vegetarian_support': False}, 'menus': [{'name': 'Món Đặc Trưng', 'description': 'Các món nổi bật nhất tại Phở Phú Gia - Sky Garden', 'items': [{'name': 'Phở Tái Lăn Hà Nội', 'description': 'Món bán chạy hàng đầu tại Phở Phú Gia - Sky Garden', 'price': 85000.0, 'image_url': 'https://images.unsplash.com/photo-1612929633738-8fe44f7ec841?w=800'}, {'name': 'Phở Chín Nạm', 'description': 'Hương vị đặc sắc được thực khách yêu thích', 'price': 75000.0, 'image_url': 'https://images.unsplash.com/photo-1612929633738-8fe44f7ec841?w=800'}]}], 'images': [{'image_url': 'https://images.unsplash.com/photo-1612929633738-8fe44f7ec841?w=800', 'caption': 'Không gian và món ngon tại Phở Phú Gia - Sky Garden', 'is_cover': True}]},
    {'name': 'The Coffee Bean & Tea Leaf - Crescent Mall', 'description': 'Quán cà phê view hồ Bán Nguyệt thoáng đãng, phục vụ cà phê rang xay và bánh ngọt cao cấp.', 'address': 'Tầng trệt Crescent Mall, 101 Tôn Dật Tiên, Quận 7, TP. Hồ Chí Minh', 'phone_number': '02854137788', 'cuisine_type': 'Cà Phê & Bánh', 'latitude': 10.729, 'longitude': 106.7198, 'min_price': 55000.0, 'max_price': 130000.0, 'open_hours': '07:30 - 22:30', 'avg_rating': 4.5, 'total_reviews': 510, 'amenities': {'has_parking': True, 'has_private_room': False, 'has_outdoor': True, 'pet_friendly': True, 'vegetarian_support': True}, 'menus': [{'name': 'Món Đặc Trưng', 'description': 'Các món nổi bật nhất tại The Coffee Bean & Tea Leaf - Crescent Mall', 'items': [{'name': 'Ice Blended Mocha', 'description': 'Món bán chạy hàng đầu tại The Coffee Bean & Tea Leaf - Crescent Mall', 'price': 89000.0, 'image_url': 'https://images.unsplash.com/photo-1626082927389-6cd097cdc6ec?w=800'}, {'name': 'Bánh Cheesecake Dâu', 'description': 'Hương vị đặc sắc được thực khách yêu thích', 'price': 75000.0, 'image_url': 'https://images.unsplash.com/photo-1626082927389-6cd097cdc6ec?w=800'}]}], 'images': [{'image_url': 'https://images.unsplash.com/photo-1626082927389-6cd097cdc6ec?w=800', 'caption': 'Không gian và món ngon tại The Coffee Bean & Tea Leaf - Crescent Mall', 'is_cover': True}]},
    {'name': 'Ốc Tuyết - Dương Bá Trạc', 'description': 'Quán ốc bình dân nổi tiếng Quận 8, ốc tươi chế biến đa dạng sốt bơ tỏi, phô mai, rang muối.', 'address': '456 Dương Bá Trạc, Phường 1, Quận 8, TP. Hồ Chí Minh', 'phone_number': '0909443322', 'cuisine_type': 'Hải Sản', 'latitude': 10.7458, 'longitude': 106.6885, 'min_price': 50000.0, 'max_price': 180000.0, 'open_hours': '16:00 - 23:30', 'avg_rating': 4.5, 'total_reviews': 420, 'amenities': {'has_parking': True, 'has_private_room': False, 'has_outdoor': True, 'pet_friendly': True, 'vegetarian_support': False}, 'menus': [{'name': 'Món Đặc Trưng', 'description': 'Các món nổi bật nhất tại Ốc Tuyết - Dương Bá Trạc', 'items': [{'name': 'Ốc Móng Tay Xào Rau Muống', 'description': 'Món bán chạy hàng đầu tại Ốc Tuyết - Dương Bá Trạc', 'price': 65000.0, 'image_url': 'https://images.unsplash.com/photo-1515003197210-e0cd71810b5f?w=800'}, {'name': 'Hàu Nướng Phô Mai', 'description': 'Hương vị đặc sắc được thực khách yêu thích', 'price': 70000.0, 'image_url': 'https://images.unsplash.com/photo-1515003197210-e0cd71810b5f?w=800'}]}], 'images': [{'image_url': 'https://images.unsplash.com/photo-1515003197210-e0cd71810b5f?w=800', 'caption': 'Không gian và món ngon tại Ốc Tuyết - Dương Bá Trạc', 'is_cover': True}]},
    {'name': 'Lẩu Dê 404 - Phạm Hùng', 'description': 'Lẩu dê thuốc bắc và vú dê nướng chao đậm vị, không gian rộng rãi có bãi đậu ô tô.', 'address': '218 Phạm Hùng, Phường 5, Quận 8, TP. Hồ Chí Minh', 'phone_number': '02838509988', 'cuisine_type': 'Lẩu Nướng', 'latitude': 10.7392, 'longitude': 106.6758, 'min_price': 120000.0, 'max_price': 320000.0, 'open_hours': '10:00 - 23:00', 'avg_rating': 4.4, 'total_reviews': 380, 'amenities': {'has_parking': True, 'has_private_room': True, 'has_outdoor': True, 'pet_friendly': False, 'vegetarian_support': False}, 'menus': [{'name': 'Món Đặc Trưng', 'description': 'Các món nổi bật nhất tại Lẩu Dê 404 - Phạm Hùng', 'items': [{'name': 'Lẩu Dê Thuốc Bắc', 'description': 'Món bán chạy hàng đầu tại Lẩu Dê 404 - Phạm Hùng', 'price': 250000.0, 'image_url': 'https://images.unsplash.com/photo-1529042410759-befb1204b468?w=800'}, {'name': 'Vú Dê Nướng Chao', 'description': 'Hương vị đặc sắc được thực khách yêu thích', 'price': 165000.0, 'image_url': 'https://images.unsplash.com/photo-1529042410759-befb1204b468?w=800'}]}], 'images': [{'image_url': 'https://images.unsplash.com/photo-1529042410759-befb1204b468?w=800', 'caption': 'Không gian và món ngon tại Lẩu Dê 404 - Phạm Hùng', 'is_cover': True}]},
    {'name': 'Cơm Tấm Tài - Tạ Quang Bửu', 'description': 'Cơm tấm sườn nướng mật ong mềm thấm vị, nước mắm kẹo chuẩn vị Sài Gòn.', 'address': '812 Tạ Quang Bửu, Phường 5, Quận 8, TP. Hồ Chí Minh', 'phone_number': '0903665544', 'cuisine_type': 'Cơm tấm', 'latitude': 10.7365, 'longitude': 106.6682, 'min_price': 45000.0, 'max_price': 85000.0, 'open_hours': '06:30 - 21:00', 'avg_rating': 4.5, 'total_reviews': 270, 'amenities': {'has_parking': True, 'has_private_room': False, 'has_outdoor': False, 'pet_friendly': False, 'vegetarian_support': False}, 'menus': [{'name': 'Món Đặc Trưng', 'description': 'Các món nổi bật nhất tại Cơm Tấm Tài - Tạ Quang Bửu', 'items': [{'name': 'Cơm Tấm Sườn Bì Chả', 'description': 'Món bán chạy hàng đầu tại Cơm Tấm Tài - Tạ Quang Bửu', 'price': 62000.0, 'image_url': 'https://images.unsplash.com/photo-1534422298391-e4f8c172dddb?w=800&q=80&auto=format&fit=crop&sig=91'}, {'name': 'Cơm Tấm Đùi Gà Nướng', 'description': 'Hương vị đặc sắc được thực khách yêu thích', 'price': 65000.0, 'image_url': 'https://images.unsplash.com/photo-1534422298391-e4f8c172dddb?w=800&q=80&auto=format&fit=crop&sig=91'}]}], 'images': [{'image_url': 'https://images.unsplash.com/photo-1534422298391-e4f8c172dddb?w=800&q=80&auto=format&fit=crop&sig=91', 'caption': 'Không gian và món ngon tại Cơm Tấm Tài - Tạ Quang Bửu', 'is_cover': True}]},
    {'name': 'Haidilao Hotpot - Vạn Hạnh Mall', 'description': 'Thương hiệu lẩu Tứ Xuyên dịch vụ 5 sao tại Vạn Hạnh Mall, nổi tiếng với múa mì và lẩu 4 ngăn.', 'address': 'Tầng 6 Vạn Hạnh Mall, 11 Sư Vạn Hạnh, Quận 10, TP. Hồ Chí Minh', 'phone_number': '02838621188', 'cuisine_type': 'Lẩu Nướng', 'latitude': 10.7705, 'longitude': 106.67, 'min_price': 300000.0, 'max_price': 650000.0, 'open_hours': '10:00 - 01:00', 'avg_rating': 4.8, 'total_reviews': 1450, 'amenities': {'has_parking': True, 'has_private_room': True, 'has_outdoor': False, 'pet_friendly': False, 'vegetarian_support': True}, 'menus': [{'name': 'Món Đặc Trưng', 'description': 'Các món nổi bật nhất tại Haidilao Hotpot - Vạn Hạnh Mall', 'items': [{'name': 'Nồi Lẩu 4 Ngăn (Cà Chua - Mala)', 'description': 'Món bán chạy hàng đầu tại Haidilao Hotpot - Vạn Hạnh Mall', 'price': 280000.0, 'image_url': 'https://images.unsplash.com/photo-1546069901-d5bfd2cbfb1f?w=800'}, {'name': 'Thịt Bò Haidilao Thượng Hạng', 'description': 'Hương vị đặc sắc được thực khách yêu thích', 'price': 220000.0, 'image_url': 'https://images.unsplash.com/photo-1546069901-d5bfd2cbfb1f?w=800'}]}], 'images': [{'image_url': 'https://images.unsplash.com/photo-1546069901-d5bfd2cbfb1f?w=800', 'caption': 'Không gian và món ngon tại Haidilao Hotpot - Vạn Hạnh Mall', 'is_cover': True}]},
    {'name': 'Cơm Niêu Thiên Lý - Sư Vạn Hạnh', 'description': 'Cơm niêu cháy giòn rụm ăn kèm cá kho tộ, thịt kho tiêu và canh cua rau đay chuẩn vị nhà làm.', 'address': '134 Sư Vạn Hạnh, Phường 12, Quận 10, TP. Hồ Chí Minh', 'phone_number': '0978785500', 'cuisine_type': 'Món Việt', 'latitude': 10.7718, 'longitude': 106.6695, 'min_price': 85000.0, 'max_price': 220000.0, 'open_hours': '10:00 - 21:30', 'avg_rating': 4.6, 'total_reviews': 610, 'amenities': {'has_parking': True, 'has_private_room': False, 'has_outdoor': False, 'pet_friendly': False, 'vegetarian_support': True}, 'menus': [{'name': 'Món Đặc Trưng', 'description': 'Các món nổi bật nhất tại Cơm Niêu Thiên Lý - Sư Vạn Hạnh', 'items': [{'name': 'Cơm Niêu Cháy Giòn', 'description': 'Món bán chạy hàng đầu tại Cơm Niêu Thiên Lý - Sư Vạn Hạnh', 'price': 28000.0, 'image_url': 'https://images.unsplash.com/photo-1550547660-d9450f859349?w=800'}, {'name': 'Cá Bống Kho Tộ', 'description': 'Hương vị đặc sắc được thực khách yêu thích', 'price': 95000.0, 'image_url': 'https://images.unsplash.com/photo-1550547660-d9450f859349?w=800'}]}], 'images': [{'image_url': 'https://images.unsplash.com/photo-1550547660-d9450f859349?w=800', 'caption': 'Không gian và món ngon tại Cơm Niêu Thiên Lý - Sư Vạn Hạnh', 'is_cover': True}]},
    {'name': 'Bún Thái Hải Sản Cô Ba - Tô Hiến Thành', 'description': 'Bún Thái hải sản chua cay đậm đà đầy ắp tôm, mực, bò tái và chả cá.', 'address': '245 Tô Hiến Thành, Phường 13, Quận 10, TP. Hồ Chí Minh', 'phone_number': '0909113355', 'cuisine_type': 'Món Thái', 'latitude': 10.7782, 'longitude': 106.6652, 'min_price': 55000.0, 'max_price': 110000.0, 'open_hours': '09:00 - 22:00', 'avg_rating': 4.5, 'total_reviews': 430, 'amenities': {'has_parking': True, 'has_private_room': False, 'has_outdoor': False, 'pet_friendly': False, 'vegetarian_support': False}, 'menus': [{'name': 'Món Đặc Trưng', 'description': 'Các món nổi bật nhất tại Bún Thái Hải Sản Cô Ba - Tô Hiến Thành', 'items': [{'name': 'Bún Thái Hải Sản Đặc Biệt', 'description': 'Món bán chạy hàng đầu tại Bún Thái Hải Sản Cô Ba - Tô Hiến Thành', 'price': 75000.0, 'image_url': 'https://images.unsplash.com/photo-1555126634-323283e090fa?w=800&q=80&auto=format&fit=crop&sig=94'}, {'name': 'Lẩu Thái Tom Yum Mini', 'description': 'Hương vị đặc sắc được thực khách yêu thích', 'price': 110000.0, 'image_url': 'https://images.unsplash.com/photo-1555126634-323283e090fa?w=800&q=80&auto=format&fit=crop&sig=94'}]}], 'images': [{'image_url': 'https://images.unsplash.com/photo-1555126634-323283e090fa?w=800&q=80&auto=format&fit=crop&sig=94', 'caption': 'Không gian và món ngon tại Bún Thái Hải Sản Cô Ba - Tô Hiến Thành', 'is_cover': True}]},
    {'name': 'Chay Thiền Ý - Ba Tháng Hai', 'description': 'Buffet chay và gọi món đa dạng hơn 40 món thanh đạm, không gian ấm cúng ngay trung tâm Quận 10.', 'address': '368 Đường 3/2, Phường 12, Quận 10, TP. Hồ Chí Minh', 'phone_number': '02838654433', 'cuisine_type': 'Món Chay', 'latitude': 10.772, 'longitude': 106.6735, 'min_price': 50000.0, 'max_price': 160000.0, 'open_hours': '08:00 - 21:30', 'avg_rating': 4.6, 'total_reviews': 350, 'amenities': {'has_parking': True, 'has_private_room': True, 'has_outdoor': False, 'pet_friendly': False, 'vegetarian_support': True}, 'menus': [{'name': 'Món Đặc Trưng', 'description': 'Các món nổi bật nhất tại Chay Thiền Ý - Ba Tháng Hai', 'items': [{'name': 'Buffet Chay Thanh Tịnh', 'description': 'Món bán chạy hàng đầu tại Chay Thiền Ý - Ba Tháng Hai', 'price': 139000.0, 'image_url': 'https://images.unsplash.com/photo-1559847844-d721426d6edc?w=800'}, {'name': 'Cơm Sen Chay', 'description': 'Hương vị đặc sắc được thực khách yêu thích', 'price': 65000.0, 'image_url': 'https://images.unsplash.com/photo-1559847844-d721426d6edc?w=800'}]}], 'images': [{'image_url': 'https://images.unsplash.com/photo-1559847844-d721426d6edc?w=800', 'caption': 'Không gian và món ngon tại Chay Thiền Ý - Ba Tháng Hai', 'is_cover': True}]},
    {'name': 'Ốc Quang Anh - Tô Hiến Thành', 'description': 'Quán ốc lâu năm siêu đông khách tại Quận 10, nổi tiếng với nghêu hấp sả và sò điệp nướng mỡ hành.', 'address': '189 Tô Hiến Thành, Phường 13, Quận 10, TP. Hồ Chí Minh', 'phone_number': '0903778899', 'cuisine_type': 'Hải Sản', 'latitude': 10.7775, 'longitude': 106.6665, 'min_price': 60000.0, 'max_price': 220000.0, 'open_hours': '13:00 - 23:00', 'avg_rating': 4.5, 'total_reviews': 780, 'amenities': {'has_parking': True, 'has_private_room': False, 'has_outdoor': True, 'pet_friendly': False, 'vegetarian_support': False}, 'menus': [{'name': 'Món Đặc Trưng', 'description': 'Các món nổi bật nhất tại Ốc Quang Anh - Tô Hiến Thành', 'items': [{'name': 'Nghêu Hấp Thái Cay', 'description': 'Món bán chạy hàng đầu tại Ốc Quang Anh - Tô Hiến Thành', 'price': 65000.0, 'image_url': 'https://images.unsplash.com/photo-1565299585323-38d6b0865b47?w=800'}, {'name': 'Ốc Len Xào Dừa', 'description': 'Hương vị đặc sắc được thực khách yêu thích', 'price': 85000.0, 'image_url': 'https://images.unsplash.com/photo-1565299585323-38d6b0865b47?w=800'}]}], 'images': [{'image_url': 'https://images.unsplash.com/photo-1565299585323-38d6b0865b47?w=800', 'caption': 'Không gian và món ngon tại Ốc Quang Anh - Tô Hiến Thành', 'is_cover': True}]},
    {'name': 'Sủi Cảo Thiên Thiên - Hà Tôn Quyền', 'description': 'Phố sủi cảo Hà Tôn Quyền trứ danh Quận 11, viên sủi cảo nhân tôm tươi nguyên con giòn ngọt.', 'address': '197 Hà Tôn Quyền, Phường 4, Quận 11, TP. Hồ Chí Minh', 'phone_number': '02838552233', 'cuisine_type': 'Món Hoa', 'latitude': 10.7595, 'longitude': 106.6562, 'min_price': 55000.0, 'max_price': 130000.0, 'open_hours': '13:00 - 23:30', 'avg_rating': 4.6, 'total_reviews': 980, 'amenities': {'has_parking': True, 'has_private_room': False, 'has_outdoor': True, 'pet_friendly': False, 'vegetarian_support': False}, 'menus': [{'name': 'Món Đặc Trưng', 'description': 'Các món nổi bật nhất tại Sủi Cảo Thiên Thiên - Hà Tôn Quyền', 'items': [{'name': 'Sủi Cảo Thập Cẩm Nước', 'description': 'Món bán chạy hàng đầu tại Sủi Cảo Thiên Thiên - Hà Tôn Quyền', 'price': 68000.0, 'image_url': 'https://images.unsplash.com/photo-1565299507177-b0ac66763828?w=800'}, {'name': 'Sủi Cảo Chiên Giòn', 'description': 'Hương vị đặc sắc được thực khách yêu thích', 'price': 72000.0, 'image_url': 'https://images.unsplash.com/photo-1565299507177-b0ac66763828?w=800'}]}], 'images': [{'image_url': 'https://images.unsplash.com/photo-1565299507177-b0ac66763828?w=800', 'caption': 'Không gian và món ngon tại Sủi Cảo Thiên Thiên - Hà Tôn Quyền', 'is_cover': True}]},
    {'name': 'Lẩu Cá Kèo Rau Đắng - Lê Đại Hành', 'description': 'Lẩu cá kèo lá giang chua thanh ăn kèm rau đắng, bông điên điển chuẩn miền Tây Nam Bộ.', 'address': '112 Lê Đại Hành, Phường 7, Quận 11, TP. Hồ Chí Minh', 'phone_number': '0908334466', 'cuisine_type': 'Món Việt', 'latitude': 10.7618, 'longitude': 106.6585, 'min_price': 90000.0, 'max_price': 250000.0, 'open_hours': '10:00 - 22:30', 'avg_rating': 4.5, 'total_reviews': 340, 'amenities': {'has_parking': True, 'has_private_room': False, 'has_outdoor': True, 'pet_friendly': False, 'vegetarian_support': False}, 'menus': [{'name': 'Món Đặc Trưng', 'description': 'Các món nổi bật nhất tại Lẩu Cá Kèo Rau Đắng - Lê Đại Hành', 'items': [{'name': 'Lẩu Cá Kèo Lá Giang', 'description': 'Món bán chạy hàng đầu tại Lẩu Cá Kèo Rau Đắng - Lê Đại Hành', 'price': 210000.0, 'image_url': 'https://images.unsplash.com/photo-1571091718767-18b5b1457add?w=800'}, {'name': 'Cá Kèo Nướng Muối Ớt', 'description': 'Hương vị đặc sắc được thực khách yêu thích', 'price': 110000.0, 'image_url': 'https://images.unsplash.com/photo-1571091718767-18b5b1457add?w=800'}]}], 'images': [{'image_url': 'https://images.unsplash.com/photo-1571091718767-18b5b1457add?w=800', 'caption': 'Không gian và món ngon tại Lẩu Cá Kèo Rau Đắng - Lê Đại Hành', 'is_cover': True}]},
    {'name': 'Cơm Tấm Hồng Calmette - Lạc Long Quân', 'description': 'Cơm tấm sườn nướng than hoa thơm nức mũi, chả trứng muối béo ngậy.', 'address': '256 Lạc Long Quân, Phường 10, Quận 11, TP. Hồ Chí Minh', 'phone_number': '0909221133', 'cuisine_type': 'Cơm tấm', 'latitude': 10.7665, 'longitude': 106.6458, 'min_price': 50000.0, 'max_price': 95000.0, 'open_hours': '07:00 - 21:00', 'avg_rating': 4.4, 'total_reviews': 260, 'amenities': {'has_parking': True, 'has_private_room': False, 'has_outdoor': False, 'pet_friendly': False, 'vegetarian_support': False}, 'menus': [{'name': 'Món Đặc Trưng', 'description': 'Các món nổi bật nhất tại Cơm Tấm Hồng Calmette - Lạc Long Quân', 'items': [{'name': 'Cơm Tấm Sườn Chả Trứng Muối', 'description': 'Món bán chạy hàng đầu tại Cơm Tấm Hồng Calmette - Lạc Long Quân', 'price': 72000.0, 'image_url': 'https://images.unsplash.com/photo-1574484284002-952d92456975?w=800'}, {'name': 'Canh Rong Biển Thịt Bằm', 'description': 'Hương vị đặc sắc được thực khách yêu thích', 'price': 25000.0, 'image_url': 'https://images.unsplash.com/photo-1574484284002-952d92456975?w=800'}]}], 'images': [{'image_url': 'https://images.unsplash.com/photo-1574484284002-952d92456975?w=800', 'caption': 'Không gian và món ngon tại Cơm Tấm Hồng Calmette - Lạc Long Quân', 'is_cover': True}]},
    {'name': 'Lẩu Bò Tơ Tây Ninh - Nguyễn Ảnh Thủ', 'description': 'Bò tơ Củ Chi tươi ngon chế biến tại chỗ, không gian sân vườn cực rộng có bãi đậu ô tô miễn phí.', 'address': '312 Nguyễn Ảnh Thủ, Phường Hiệp Thành, Quận 12, TP. Hồ Chí Minh', 'phone_number': '0908554422', 'cuisine_type': 'Món Việt', 'latitude': 10.8695, 'longitude': 106.6345, 'min_price': 100000.0, 'max_price': 280000.0, 'open_hours': '10:00 - 23:00', 'avg_rating': 4.5, 'total_reviews': 390, 'amenities': {'has_parking': True, 'has_private_room': True, 'has_outdoor': True, 'pet_friendly': True, 'vegetarian_support': False}, 'menus': [{'name': 'Món Đặc Trưng', 'description': 'Các món nổi bật nhất tại Lẩu Bò Tơ Tây Ninh - Nguyễn Ảnh Thủ', 'items': [{'name': 'Bò Tơ Luộc Cuốn Bánh Tráng', 'description': 'Món bán chạy hàng đầu tại Lẩu Bò Tơ Tây Ninh - Nguyễn Ảnh Thủ', 'price': 185000.0, 'image_url': 'https://images.unsplash.com/photo-1579584425555-c3ce17fd4351?w=800'}, {'name': 'Lẩu Xí Quách Bò Tơ', 'description': 'Hương vị đặc sắc được thực khách yêu thích', 'price': 240000.0, 'image_url': 'https://images.unsplash.com/photo-1579584425555-c3ce17fd4351?w=800'}]}], 'images': [{'image_url': 'https://images.unsplash.com/photo-1579584425555-c3ce17fd4351?w=800', 'caption': 'Không gian và món ngon tại Lẩu Bò Tơ Tây Ninh - Nguyễn Ảnh Thủ', 'is_cover': True}]},
    {'name': 'Gogi House - Phan Văn Hớn', 'description': 'Thịt nướng Hàn Quốc không khói tiện lợi cho cư dân khu vực Quận 12 và Hóc Môn.', 'address': '88 Phan Văn Hớn, Phường Tân Thới Nhất, Quận 12, TP. Hồ Chí Minh', 'phone_number': '02873007399', 'cuisine_type': 'Lẩu Nướng', 'latitude': 10.8315, 'longitude': 106.6185, 'min_price': 199000.0, 'max_price': 389000.0, 'open_hours': '10:00 - 22:00', 'avg_rating': 4.6, 'total_reviews': 310, 'amenities': {'has_parking': True, 'has_private_room': True, 'has_outdoor': False, 'pet_friendly': False, 'vegetarian_support': False}, 'menus': [{'name': 'Món Đặc Trưng', 'description': 'Các món nổi bật nhất tại Gogi House - Phan Văn Hớn', 'items': [{'name': 'Combo Nướng Gia Đình', 'description': 'Món bán chạy hàng đầu tại Gogi House - Phan Văn Hớn', 'price': 369000.0, 'image_url': 'https://images.unsplash.com/photo-1580476262798-bddd9f4b7369?w=800'}, {'name': 'Mì Lạnh Hàn Quốc', 'description': 'Hương vị đặc sắc được thực khách yêu thích', 'price': 99000.0, 'image_url': 'https://images.unsplash.com/photo-1580476262798-bddd9f4b7369?w=800'}]}], 'images': [{'image_url': 'https://images.unsplash.com/photo-1580476262798-bddd9f4b7369?w=800', 'caption': 'Không gian và món ngon tại Gogi House - Phan Văn Hớn', 'is_cover': True}]},
    {'name': 'Quán Chay Liên Hoa - Lê Văn Khương', 'description': 'Thực đơn chay phong phú, giá bình dân, phục vụ cơm trưa và lẩu chay thanh đạm.', 'address': '145 Lê Văn Khương, Phường Thới An, Quận 12, TP. Hồ Chí Minh', 'phone_number': '0937889900', 'cuisine_type': 'Món Chay', 'latitude': 10.872, 'longitude': 106.6485, 'min_price': 35000.0, 'max_price': 110000.0, 'open_hours': '07:00 - 21:00', 'avg_rating': 4.6, 'total_reviews': 220, 'amenities': {'has_parking': True, 'has_private_room': False, 'has_outdoor': True, 'pet_friendly': False, 'vegetarian_support': True}, 'menus': [{'name': 'Món Đặc Trưng', 'description': 'Các món nổi bật nhất tại Quán Chay Liên Hoa - Lê Văn Khương', 'items': [{'name': 'Lẩu Nấm Chay Liên Hoa', 'description': 'Món bán chạy hàng đầu tại Quán Chay Liên Hoa - Lê Văn Khương', 'price': 110000.0, 'image_url': 'https://images.unsplash.com/photo-1589302168068-964664d93dc0?w=800'}, {'name': 'Hủ Tiếu Chay Nam Vang', 'description': 'Hương vị đặc sắc được thực khách yêu thích', 'price': 42000.0, 'image_url': 'https://images.unsplash.com/photo-1589302168068-964664d93dc0?w=800'}]}], 'images': [{'image_url': 'https://images.unsplash.com/photo-1589302168068-964664d93dc0?w=800', 'caption': 'Không gian và món ngon tại Quán Chay Liên Hoa - Lê Văn Khương', 'is_cover': True}]},
    {'name': 'Kichi Kichi - Aeon Mall Bình Tân', 'description': 'Lẩu băng chuyền Nhật Bản hiện đại tại Aeon Mall Bình Tân với hơn 80 món nhúng tươi ngon.', 'address': 'Tầng 3 Aeon Mall Bình Tân, 1 Đường Số 17A, Quận Bình Tân, TP. Hồ Chí Minh', 'phone_number': '02873007988', 'cuisine_type': 'Lẩu Nướng', 'latitude': 10.7428, 'longitude': 106.6122, 'min_price': 239000.0, 'max_price': 329000.0, 'open_hours': '10:00 - 22:00', 'avg_rating': 4.6, 'total_reviews': 580, 'amenities': {'has_parking': True, 'has_private_room': False, 'has_outdoor': False, 'pet_friendly': False, 'vegetarian_support': True}, 'menus': [{'name': 'Món Đặc Trưng', 'description': 'Các món nổi bật nhất tại Kichi Kichi - Aeon Mall Bình Tân', 'items': [{'name': 'Buffet Lẩu Băng Chuyền', 'description': 'Món bán chạy hàng đầu tại Kichi Kichi - Aeon Mall Bình Tân', 'price': 279000.0, 'image_url': 'https://images.unsplash.com/photo-1594007654729-407eedc4be65?w=800'}, {'name': 'Nước Lẩu Tom Yum & Nấm', 'description': 'Hương vị đặc sắc được thực khách yêu thích', 'price': 0.0, 'image_url': 'https://images.unsplash.com/photo-1594007654729-407eedc4be65?w=800'}]}], 'images': [{'image_url': 'https://images.unsplash.com/photo-1594007654729-407eedc4be65?w=800', 'caption': 'Không gian và món ngon tại Kichi Kichi - Aeon Mall Bình Tân', 'is_cover': True}]},
    {'name': 'Hải Sản Hoàng Gia - Tên Lửa', 'description': 'Nhà hàng hải sản cao cấp trục đường Tên Lửa, có nhiều phòng VIP tiếp khách và bãi đậu xe rộng.', 'address': '168 Tên Lửa, Phường Bình Trị Đông B, Quận Bình Tân, TP. Hồ Chí Minh', 'phone_number': '02837528899', 'cuisine_type': 'Hải Sản', 'latitude': 10.7475, 'longitude': 106.6148, 'min_price': 180000.0, 'max_price': 850000.0, 'open_hours': '10:00 - 23:00', 'avg_rating': 4.6, 'total_reviews': 440, 'amenities': {'has_parking': True, 'has_private_room': True, 'has_outdoor': True, 'pet_friendly': False, 'vegetarian_support': False}, 'menus': [{'name': 'Món Đặc Trưng', 'description': 'Các món nổi bật nhất tại Hải Sản Hoàng Gia - Tên Lửa', 'items': [{'name': 'Cua Hoàng Đế Hấp', 'description': 'Món bán chạy hàng đầu tại Hải Sản Hoàng Gia - Tên Lửa', 'price': 750000.0, 'image_url': 'https://images.unsplash.com/photo-1604382354936-07c5d9983bd3?w=800'}, {'name': 'Tôm Sú Rang Muối Hồng Kông', 'description': 'Hương vị đặc sắc được thực khách yêu thích', 'price': 290000.0, 'image_url': 'https://images.unsplash.com/photo-1604382354936-07c5d9983bd3?w=800'}]}], 'images': [{'image_url': 'https://images.unsplash.com/photo-1604382354936-07c5d9983bd3?w=800', 'caption': 'Không gian và món ngon tại Hải Sản Hoàng Gia - Tên Lửa', 'is_cover': True}]},
    {'name': 'Bò Nướng Ngói Gia Bảo - Tên Lửa', 'description': 'Nướng ngói thơm lừng không khói, giá sinh viên và không gian vỉa hè thoáng mát.', 'address': '245 Tên Lửa, Phường Bình Trị Đông B, Quận Bình Tân, TP. Hồ Chí Minh', 'phone_number': '0909664422', 'cuisine_type': 'Lẩu Nướng', 'latitude': 10.751, 'longitude': 106.6135, 'min_price': 80000.0, 'max_price': 220000.0, 'open_hours': '16:00 - 23:30', 'avg_rating': 4.5, 'total_reviews': 360, 'amenities': {'has_parking': True, 'has_private_room': False, 'has_outdoor': True, 'pet_friendly': True, 'vegetarian_support': False}, 'menus': [{'name': 'Món Đặc Trưng', 'description': 'Các món nổi bật nhất tại Bò Nướng Ngói Gia Bảo - Tên Lửa', 'items': [{'name': 'Bò Tảng Nướng Ngói', 'description': 'Món bán chạy hàng đầu tại Bò Nướng Ngói Gia Bảo - Tên Lửa', 'price': 135000.0, 'image_url': 'https://images.unsplash.com/photo-1608039755401-742074f0548d?w=800'}, {'name': 'Bạch Tuộc Nướng Sa Tế', 'description': 'Hương vị đặc sắc được thực khách yêu thích', 'price': 115000.0, 'image_url': 'https://images.unsplash.com/photo-1608039755401-742074f0548d?w=800'}]}], 'images': [{'image_url': 'https://images.unsplash.com/photo-1608039755401-742074f0548d?w=800', 'caption': 'Không gian và món ngon tại Bò Nướng Ngói Gia Bảo - Tên Lửa', 'is_cover': True}]},
    {'name': 'Phở Lệ - Kinh Dương Vương', 'description': 'Thương hiệu Phở Lệ danh tiếng Sài Gòn với nước dùng béo ngọt đậm đà và bò viên giòn sần sật.', 'address': '303 Kinh Dương Vương, Phường An Lạc, Quận Bình Tân, TP. Hồ Chí Minh', 'phone_number': '02838751122', 'cuisine_type': 'Món Việt', 'latitude': 10.741, 'longitude': 106.6175, 'min_price': 70000.0, 'max_price': 115000.0, 'open_hours': '06:00 - 22:00', 'avg_rating': 4.6, 'total_reviews': 510, 'amenities': {'has_parking': True, 'has_private_room': False, 'has_outdoor': False, 'pet_friendly': False, 'vegetarian_support': False}, 'menus': [{'name': 'Món Đặc Trưng', 'description': 'Các món nổi bật nhất tại Phở Lệ - Kinh Dương Vương', 'items': [{'name': 'Phở Tái Bò Viên', 'description': 'Món bán chạy hàng đầu tại Phở Lệ - Kinh Dương Vương', 'price': 85000.0, 'image_url': 'https://images.unsplash.com/photo-1617093727343-374698b1b08d?w=800'}, {'name': 'Phở Thập Cẩm Đặc Biệt', 'description': 'Hương vị đặc sắc được thực khách yêu thích', 'price': 105000.0, 'image_url': 'https://images.unsplash.com/photo-1617093727343-374698b1b08d?w=800'}]}], 'images': [{'image_url': 'https://images.unsplash.com/photo-1617093727343-374698b1b08d?w=800', 'caption': 'Không gian và món ngon tại Phở Lệ - Kinh Dương Vương', 'is_cover': True}]},
    {'name': 'Ẩm Thực Sinh Thái Bình Xuyên - Bình Chánh', 'description': 'Khu ẩm thực sinh thái sân vườn ven hồ cực lớn ở Bình Chánh, nổi tiếng với gà nướng lu và hải sản.', 'address': 'C3/18 Phạm Hùng, Xã Bình Hưng, Huyện Bình Chánh, TP. Hồ Chí Minh', 'phone_number': '02854316316', 'cuisine_type': 'Món Việt', 'latitude': 10.7255, 'longitude': 106.6785, 'min_price': 120000.0, 'max_price': 420000.0, 'open_hours': '09:00 - 23:00', 'avg_rating': 4.6, 'total_reviews': 1120, 'amenities': {'has_parking': True, 'has_private_room': True, 'has_outdoor': True, 'pet_friendly': True, 'vegetarian_support': True}, 'menus': [{'name': 'Món Đặc Trưng', 'description': 'Các món nổi bật nhất tại Ẩm Thực Sinh Thái Bình Xuyên - Bình Chánh', 'items': [{'name': 'Gà Nướng Lu Xôi Cháy', 'description': 'Món bán chạy hàng đầu tại Ẩm Thực Sinh Thái Bình Xuyên - Bình Chánh', 'price': 280000.0, 'image_url': 'https://images.unsplash.com/photo-1623428187969-5da2dcea5ebf?w=800'}, {'name': 'Cá Tai Tượng Chiên Xù', 'description': 'Hương vị đặc sắc được thực khách yêu thích', 'price': 220000.0, 'image_url': 'https://images.unsplash.com/photo-1623428187969-5da2dcea5ebf?w=800'}]}], 'images': [{'image_url': 'https://images.unsplash.com/photo-1623428187969-5da2dcea5ebf?w=800', 'caption': 'Không gian và món ngon tại Ẩm Thực Sinh Thái Bình Xuyên - Bình Chánh', 'is_cover': True}]},
    {'name': 'Lẩu Mắm Bà Dú - Trung Sơn Bình Chánh', 'description': 'Lẩu mắm miền Tây chuẩn vị với hơn 15 loại rau đồng nội tươi rói tại khu Trung Sơn.', 'address': '92 Đường 9A, KDC Trung Sơn, Huyện Bình Chánh, TP. Hồ Chí Minh', 'phone_number': '02854318899', 'cuisine_type': 'Món Việt', 'latitude': 10.7335, 'longitude': 106.6895, 'min_price': 95000.0, 'max_price': 260000.0, 'open_hours': '10:00 - 22:00', 'avg_rating': 4.6, 'total_reviews': 540, 'amenities': {'has_parking': True, 'has_private_room': True, 'has_outdoor': False, 'pet_friendly': False, 'vegetarian_support': False}, 'menus': [{'name': 'Món Đặc Trưng', 'description': 'Các món nổi bật nhất tại Lẩu Mắm Bà Dú - Trung Sơn Bình Chánh', 'items': [{'name': 'Lẩu Mắm Thập Cẩm Miền Tây', 'description': 'Món bán chạy hàng đầu tại Lẩu Mắm Bà Dú - Trung Sơn Bình Chánh', 'price': 245000.0, 'image_url': 'https://images.unsplash.com/photo-1626804475297-41608ea09aeb?w=800'}, {'name': 'Cá Kèo Kho Tộ', 'description': 'Hương vị đặc sắc được thực khách yêu thích', 'price': 115000.0, 'image_url': 'https://images.unsplash.com/photo-1626804475297-41608ea09aeb?w=800'}]}], 'images': [{'image_url': 'https://images.unsplash.com/photo-1626804475297-41608ea09aeb?w=800', 'caption': 'Không gian và món ngon tại Lẩu Mắm Bà Dú - Trung Sơn Bình Chánh', 'is_cover': True}]},
    {'name': 'Nhà Hàng Sân Vườn Phú Xuân - Nhà Bè', 'description': 'Không gian chòi lá ven sông thoáng mát tại Nhà Bè, chuyên tôm càng xanh và cá sông tươi sống.', 'address': '1850 Huỳnh Tấn Phát, Thị trấn Nhà Bè, Huyện Nhà Bè, TP. Hồ Chí Minh', 'phone_number': '0908991122', 'cuisine_type': 'Hải Sản', 'latitude': 10.6953, 'longitude': 106.7312, 'min_price': 110000.0, 'max_price': 380000.0, 'open_hours': '09:30 - 23:00', 'avg_rating': 4.5, 'total_reviews': 310, 'amenities': {'has_parking': True, 'has_private_room': True, 'has_outdoor': True, 'pet_friendly': True, 'vegetarian_support': False}, 'menus': [{'name': 'Món Đặc Trưng', 'description': 'Các món nổi bật nhất tại Nhà Hàng Sân Vườn Phú Xuân - Nhà Bè', 'items': [{'name': 'Tôm Càng Xanh Nướng Mọi', 'description': 'Món bán chạy hàng đầu tại Nhà Hàng Sân Vườn Phú Xuân - Nhà Bè', 'price': 290000.0, 'image_url': 'https://images.unsplash.com/photo-1509722747041-616f39b57569?w=800'}, {'name': 'Lẩu Cá Ngát Nấu Chua', 'description': 'Hương vị đặc sắc được thực khách yêu thích', 'price': 210000.0, 'image_url': 'https://images.unsplash.com/photo-1509722747041-616f39b57569?w=800'}]}], 'images': [{'image_url': 'https://images.unsplash.com/photo-1509722747041-616f39b57569?w=800', 'caption': 'Không gian và món ngon tại Nhà Hàng Sân Vườn Phú Xuân - Nhà Bè', 'is_cover': True}]},
    {'name': 'Bò Tơ Xuân Đào - Hóc Môn', 'description': 'Đặc sản bò tơ Củ Chi - Hóc Môn nổi tiếng nhiều năm, thịt mềm ngọt và không gian sân vườn rộng rãi.', 'address': '215 Quốc Lộ 22, Xã Tân Xuân, Huyện Hóc Môn, TP. Hồ Chí Minh', 'phone_number': '02838912233', 'cuisine_type': 'Món Việt', 'latitude': 10.8839, 'longitude': 106.5912, 'min_price': 90000.0, 'max_price': 280000.0, 'open_hours': '09:00 - 22:30', 'avg_rating': 4.6, 'total_reviews': 620, 'amenities': {'has_parking': True, 'has_private_room': True, 'has_outdoor': True, 'pet_friendly': True, 'vegetarian_support': False}, 'menus': [{'name': 'Món Đặc Trưng', 'description': 'Các món nổi bật nhất tại Bò Tơ Xuân Đào - Hóc Môn', 'items': [{'name': 'Bò Tơ Hấp Gừng Cuốn Rau Rừng', 'description': 'Món bán chạy hàng đầu tại Bò Tơ Xuân Đào - Hóc Môn', 'price': 190000.0, 'image_url': 'https://images.unsplash.com/photo-1512058564366-18510be2db19?w=800'}, {'name': 'Thăn Bò Tơ Nướng Y', 'description': 'Hương vị đặc sắc được thực khách yêu thích', 'price': 210000.0, 'image_url': 'https://images.unsplash.com/photo-1512058564366-18510be2db19?w=800'}]}], 'images': [{'image_url': 'https://images.unsplash.com/photo-1512058564366-18510be2db19?w=800', 'caption': 'Không gian và món ngon tại Bò Tơ Xuân Đào - Hóc Môn', 'is_cover': True}]}
]


def escape_sql(val):
    """Helper escape ký tự đơn để xuất file SQL an toàn."""
    if val is None:
        return "NULL"
    if isinstance(val, (int, float)):
        return str(val)
    if isinstance(val, bool):
        return "1" if val else "0"
    val_str = str(val).replace("'", "''")
    return f"'{val_str}'"


def run_seed():
    print("=" * 70)
    print("   BẮT ĐẦU SEED DỮ LIỆU 110 QUÁN ĂN TOÀN KHU VỰC TP.HCM (ĐẦY ĐỦ CÁC QUẬN HUYỆN)")
    print("=" * 70)

    # 1. Đảm bảo cấu trúc các bảng đã được tạo
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    # Dọn dẹp dữ liệu quán cũ nếu có để tránh trùng lặp
    existing_count = db.query(Restaurant).count()
    if existing_count > 0:
        print(f"-> Phát hiện {existing_count} quán ăn đã có sẵn trong CSDL. Đang tiến hành làm mới...")
        db.query(MenuItem).delete()
        db.query(RestaurantMenu).delete()
        db.query(RestaurantAmenity).delete()
        db.query(RestaurantImage).delete()
        db.query(Restaurant).delete()
        db.commit()

    sql_statements = [
        "-- ====================================================================",
        "-- SMART DINING - SEED DỮ LIỆU 50 NHÀ HÀNG TẠI TP. HỒ CHÍ MINH",
        "-- Khu vực: Quận 1, Quận 3, Bình Thạnh, TP. Thủ Đức",
        f"-- Ngày tạo: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "-- ====================================================================",
        "",
        "SET FOREIGN_KEY_CHECKS = 0;",
        "TRUNCATE TABLE menu_items;",
        "TRUNCATE TABLE restaurant_menus;",
        "TRUNCATE TABLE restaurant_amenities;",
        "TRUNCATE TABLE restaurant_images;",
        "TRUNCATE TABLE restaurants;",
        "SET FOREIGN_KEY_CHECKS = 1;",
        "",
    ]

    restaurant_counter = 0
    menu_counter = 0
    item_counter = 0
    image_counter = 0

    for idx, r_data in enumerate(RESTAURANTS_DATA, start=1):
        restaurant_counter += 1
        # 1. Tạo bản ghi Restaurant
        res = Restaurant(
            name=r_data["name"],
            description=r_data["description"],
            address=r_data["address"],
            phone_number=r_data["phone_number"],
            cuisine_type=r_data["cuisine_type"],
            latitude=r_data["latitude"],
            longitude=r_data["longitude"],
            min_price=r_data["min_price"],
            max_price=r_data["max_price"],
            open_hours=r_data["open_hours"],
            avg_rating=r_data["avg_rating"],
            total_reviews=r_data["total_reviews"],
            status="active",
        )
        db.add(res)
        db.flush()  # Lấy res.id

        sql_statements.append(
            f"INSERT INTO restaurants (id, name, description, address, phone_number, cuisine_type, latitude, longitude, min_price, max_price, open_hours, avg_rating, total_reviews, status, created_at, updated_at) "
            f"VALUES ({res.id}, {escape_sql(res.name)}, {escape_sql(res.description)}, {escape_sql(res.address)}, {escape_sql(res.phone_number)}, {escape_sql(res.cuisine_type)}, {res.latitude}, {res.longitude}, {res.min_price}, {res.max_price}, {escape_sql(res.open_hours)}, {res.avg_rating}, {res.total_reviews}, 'active', NOW(), NOW());"
        )

        # 2. Tạo bản ghi RestaurantAmenity
        amenity_data = r_data.get("amenities", {})
        amenity = RestaurantAmenity(
            restaurant_id=res.id,
            has_parking=amenity_data.get("has_parking", True),
            has_private_room=amenity_data.get("has_private_room", False),
            has_outdoor=amenity_data.get("has_outdoor", False),
            pet_friendly=amenity_data.get("pet_friendly", False),
            vegetarian_support=amenity_data.get("vegetarian_support", False),
        )
        db.add(amenity)
        db.flush()

        sql_statements.append(
            f"INSERT INTO restaurant_amenities (id, restaurant_id, has_parking, has_private_room, has_outdoor, pet_friendly, vegetarian_support, created_at, updated_at) "
            f"VALUES ({amenity.id}, {res.id}, {escape_sql(amenity.has_parking)}, {escape_sql(amenity.has_private_room)}, {escape_sql(amenity.has_outdoor)}, {escape_sql(amenity.pet_friendly)}, {escape_sql(amenity.vegetarian_support)}, NOW(), NOW());"
        )

        # 3. Tạo danh mục Menu và các món ăn MenuItem
        for menu_order, m_data in enumerate(r_data.get("menus", []), start=1):
            menu_counter += 1
            menu = RestaurantMenu(
                restaurant_id=res.id,
                name=m_data["name"],
                description=m_data.get("description", ""),
                display_order=menu_order,
            )
            db.add(menu)
            db.flush()

            sql_statements.append(
                f"INSERT INTO restaurant_menus (id, restaurant_id, name, description, display_order, created_at) "
                f"VALUES ({menu.id}, {res.id}, {escape_sql(menu.name)}, {escape_sql(menu.description)}, {menu.display_order}, NOW());"
            )

            for item in m_data.get("items", []):
                item_counter += 1
                menu_item = MenuItem(
                    menu_id=menu.id,
                    name=item["name"],
                    description=item.get("description", ""),
                    price=item["price"],
                    image_url=item.get("image_url", ""),
                    is_available=True,
                )
                db.add(menu_item)
                db.flush()

                sql_statements.append(
                    f"INSERT INTO menu_items (id, menu_id, name, description, price, image_url, is_available, created_at) "
                    f"VALUES ({menu_item.id}, {menu.id}, {escape_sql(menu_item.name)}, {escape_sql(menu_item.description)}, {menu_item.price}, {escape_sql(menu_item.image_url)}, 1, NOW());"
                )

        # 4. Tạo thư viện hình ảnh RestaurantImage
        for img_order, img_data in enumerate(r_data.get("images", []), start=1):
            image_counter += 1
            res_image = RestaurantImage(
                restaurant_id=res.id,
                image_url=img_data["image_url"],
                caption=img_data.get("caption", res.name),
                is_cover=img_data.get("is_cover", False),
                display_order=img_order,
            )
            db.add(res_image)
            db.flush()

            sql_statements.append(
                f"INSERT INTO restaurant_images (id, restaurant_id, image_url, caption, is_cover, display_order, created_at) "
                f"VALUES ({res_image.id}, {res.id}, {escape_sql(res_image.image_url)}, {escape_sql(res_image.caption)}, {escape_sql(res_image.is_cover)}, {res_image.display_order}, NOW());"
            )

        print(f"[{restaurant_counter:03d}/110] Đã nạp quán: {res.name} ({r_data['cuisine_type']} - {r_data['address'][:35]}...)")

    db.commit()
    db.close()

    # Xuất file SQL thuần để cả nhóm có thể import trực tiếp vào MySQL / phpMyAdmin
    sql_file_path = os.path.join(CURRENT_DIR, "seed_restaurants.sql")
    with open(sql_file_path, "w", encoding="utf-8") as f:
        f.write("\n".join(sql_statements))

    # Đồng bộ sang database/init_db.sql
    init_sql_path = os.path.join(CURRENT_DIR, "init_db.sql")
    with open(init_sql_path, "w", encoding="utf-8") as f:
        f.write("\n".join(sql_statements))

    print("\n" + "=" * 70)
    print(f"-> THÀNH CÔNG! Đã seed đầy đủ vào Database:")
    print(f"   + {restaurant_counter} Quán ăn / Nhà hàng (Restaurants)")
    print(f"   + {restaurant_counter} Bộ tiện ích (RestaurantAmenities)")
    print(f"   + {menu_counter} Danh mục thực đơn (RestaurantMenus)")
    print(f"   + {item_counter} Món ăn chi tiết (MenuItems)")
    print(f"   + {image_counter} Hình ảnh chất lượng cao (RestaurantImages)")
    print(f"-> Đã xuất file SQL thuần tại:")
    print(f"   + {sql_file_path}")
    print(f"   + {init_sql_path}")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    run_seed()
