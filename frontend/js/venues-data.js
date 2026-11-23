// Dữ liệu 50 nhà hàng TP.HCM khởi tạo từ CSDL seed
const SEED_VENUES = [
{
    "id": 1,
    "name": "Pizza 4P's Bến Thành",
    "address": "8 Thủ Khoa Huân, Phường Bến Thành, Quận 1, TP. Hồ Chí Minh",
    "lat": 10.7725,
    "lng": 106.698,
    "category": "western",
    "cuisineLabel": "Món Âu",
    "priceMin": 150000,
    "priceMax": 450000,
    "rating": 4.8,
    "reviews": 850,
    "parking": true,
    "private_room": true,
    "vegetarian": true,
    "openHours": "10:00 - 23:00",
    "image": "https://images.unsplash.com/photo-1555396273-367ea4eb4db5?w=800",
    "menu": [
      {
        "name": "Pizza 4 Loại Phô Mai (4 Cheese Pizza)",
        "price": 280000.0
      },
      {
        "name": "Pizza Burrata Thịt Nguội Parma Ham",
        "price": 340000.0
      },
      {
        "name": "Pizza Hải Sản Sốt Cà Chua Cay",
        "price": 290000.0
      },
      {
        "name": "Mì Ý Sốt Cua Cà Chua Cay",
        "price": 245000.0
      },
      {
        "name": "Salad Phô Mai Cam & Trái Cây Tươi",
        "price": 145000.0
      },
      {
        "name": "Bánh Tiramisu Truyền Thống",
        "price": 95000.0
      },
      {
        "name": "Nước Ép Bưởi Hồng Ép Lạnh",
        "price": 65000.0
      }
    ],
    "district": "Quận 1",
    "has_parking": true,
    "has_private_room": true,
    "has_outdoor": false,
    "outdoor": false,
    "pet_friendly": false,
    "has_pet_friendly": false,
    "vegetarian_support": true,
    "menus": [
      {
        "name": "Pizza Lò Củi",
        "description": "Các loại pizza phô mai Burrata và sốt đặc trưng nướng bằng lò củi cồn",
        "items": [
          {
            "name": "Pizza 4 Loại Phô Mai (4 Cheese Pizza)",
            "description": "Kết hợp phô mai Mozzarella, Gorgonzola, Ricotta, Parmesan kèm mật ong hữu cơ",
            "price": 280000.0,
            "image_url": "https://images.unsplash.com/photo-1513104890138-7c749659a591?w=800"
          },
          {
            "name": "Pizza Burrata Thịt Nguội Parma Ham",
            "description": "Bánh pizza giòn xốp phủ phô mai Burrata tươi nguyên quả và thịt nguội Ý cao cấp",
            "price": 340000.0,
            "image_url": "https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?w=800"
          },
          {
            "name": "Pizza Hải Sản Sốt Cà Chua Cay",
            "description": "Tôm sú, mực tươi, nghêu và ớt chuông đỏ sốt cà chua San Marzano",
            "price": 290000.0,
            "image_url": "https://images.unsplash.com/photo-1574071318508-1cdbab80d002?w=800"
          }
        ]
      },
      {
        "name": "Mì Ý & Món Khai Vị",
        "description": "Mì Pasta tự làm tươi trong ngày",
        "items": [
          {
            "name": "Mì Ý Sốt Cua Cà Chua Cay",
            "description": "Mì sợi dẹt Fettuccine nấu với thịt cua tươi Cà Mau và phô mai Ricotta",
            "price": 245000.0,
            "image_url": "https://images.unsplash.com/photo-1621996346565-e3d5d6281724?w=800"
          },
          {
            "name": "Salad Phô Mai Cam & Trái Cây Tươi",
            "description": "Rau Rocket, dâu tây, cam vàng và phô mai tươi nhà làm",
            "price": 145000.0,
            "image_url": "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=800"
          }
        ]
      },
      {
        "name": "Đồ Uống & Tráng Miệng",
        "description": "Tráng miệng làm thủ công",
        "items": [
          {
            "name": "Bánh Tiramisu Truyền Thống",
            "description": "Hương vị cà phê nồng nàn và phô mai Mascarpone béo mịn",
            "price": 95000.0,
            "image_url": "https://images.unsplash.com/photo-1571877227200-a0d98ea607e9?w=800"
          },
          {
            "name": "Nước Ép Bưởi Hồng Ép Lạnh",
            "description": "100% bưởi hồng tươi nguyên chất không thêm đường",
            "price": 65000.0,
            "image_url": "https://images.unsplash.com/photo-1613478223719-2ab802602423?w=800"
          }
        ]
      }
    ],
    "images": [
      {
        "image_url": "https://images.unsplash.com/photo-1555396273-367ea4eb4db5?w=800",
        "caption": "Không gian bếp mở và lò củi hiện đại tại trung tâm nhà hàng",
        "is_cover": true
      },
      {
        "image_url": "https://images.unsplash.com/photo-1513104890138-7c749659a591?w=800",
        "caption": "Bánh Pizza phô mai Burrata trứ danh",
        "is_cover": false
      },
      {
        "image_url": "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=800",
        "caption": "Khu vực bàn ăn gia đình và hẹn hò ấm cúng",
        "is_cover": false
      }
    ],
    "description": "Thương hiệu pizza phô mai tươi thủ công nướng lò củi nổi tiếng bậc nhất Sài Gòn, không gian sang trọng và ấm cúng.",
    "phone_number": "02836220500"
  },
  {
    "id": 2,
    "name": "Quán Bụi - Authentic Vietnamese Cuisine",
    "address": "19 Ngô Văn Năm, Phường Bến Nghé, Quận 1, TP. Hồ Chí Minh",
    "lat": 10.7812,
    "lng": 106.7056,
    "category": "vietnamese",
    "cuisineLabel": "Món Việt",
    "priceMin": 90000,
    "priceMax": 320000,
    "rating": 4.6,
    "reviews": 620,
    "parking": true,
    "private_room": true,
    "vegetarian": true,
    "openHours": "07:30 - 23:00",
    "image": "https://images.unsplash.com/photo-1552566626-52f8b828add9?w=800",
    "menu": [
      {
        "name": "Thịt Kho Tàu Trứng Vịt",
        "price": 165000.0
      },
      {
        "name": "Cá Chẽm Kho Tộ Tiêu Xanh",
        "price": 195000.0
      },
      {
        "name": "Canh Chua Cá Bông Lau",
        "price": 185000.0
      },
      {
        "name": "Gỏi Cuốn Tôm Thịt (4 cuộn)",
        "price": 115000.0
      },
      {
        "name": "Chả Giò Quán Bụi",
        "price": 125000.0
      }
    ],
    "district": "Quận 1",
    "has_parking": true,
    "has_private_room": true,
    "has_outdoor": true,
    "outdoor": true,
    "pet_friendly": false,
    "has_pet_friendly": false,
    "vegetarian_support": true,
    "menus": [
      {
        "name": "Món Cơm Gia Đình",
        "description": "Các món kho, canh, xào đậm đà hương vị mâm cơm mẹ nấu",
        "items": [
          {
            "name": "Thịt Kho Tàu Trứng Vịt",
            "description": "Thịt ba chỉ rút sườn kho nước dừa xiêm béo mềm kèm trứng vịt",
            "price": 165000.0,
            "image_url": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=800"
          },
          {
            "name": "Cá Chẽm Kho Tộ Tiêu Xanh",
            "description": "Cá chẽm tươi kho tộ đất đượm vị tiêu đen Phú Quốc",
            "price": 195000.0,
            "image_url": "https://images.unsplash.com/photo-1519708227418-c8fd9a32b7a2?w=800"
          },
          {
            "name": "Canh Chua Cá Bông Lau",
            "description": "Vị chua thanh mát từ me dốt, bạc hà, đậu bắp và cá bông lau tươi",
            "price": 185000.0,
            "image_url": "https://images.unsplash.com/photo-1547592180-85f173990554?w=800"
          }
        ]
      },
      {
        "name": "Món Cuốn & Khai Vị",
        "description": "Thanh mát, nhẹ nhàng trước bữa ăn",
        "items": [
          {
            "name": "Gỏi Cuốn Tôm Thịt (4 cuộn)",
            "description": "Tôm tươi, thịt ba rọi luộc, bún tươi và rau thơm cuốn bánh tráng phơi sương",
            "price": 115000.0,
            "image_url": "https://images.unsplash.com/photo-1559847844-5315695dadae?w=800"
          },
          {
            "name": "Chả Giò Quán Bụi",
            "description": "Chả giò chiên giòn rụm nhân tôm thịt cua nấm mèo",
            "price": 125000.0,
            "image_url": "https://images.unsplash.com/photo-1541544741938-0af808871cc0?w=800"
          }
        ]
      }
    ],
    "images": [
      {
        "image_url": "https://images.unsplash.com/photo-1552566626-52f8b828add9?w=800",
        "caption": "Không gian phong cách Indochine truyền thống sang trọng",
        "is_cover": true
      },
      {
        "image_url": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=800",
        "caption": "Mâm cơm gia đình Việt đầy đủ sắc hương vị",
        "is_cover": false
      }
    ],
    "description": "Địa chỉ ẩm thực Việt Nam hoài cổ với các món ăn gia đình ba miền đậm đà, không gian Indochine tinh tế giữa lòng Quận 1.",
    "phone_number": "02838291299"
  },
  {
    "id": 3,
    "name": "Dim Tu Tac - Saigon Centre",
    "address": "Tầng 5 Saigon Centre, 65 Lê Lợi, Phường Bến Nghé, Quận 1, TP. Hồ Chí Minh",
    "lat": 10.7738,
    "lng": 106.7011,
    "category": "other",
    "cuisineLabel": "Món Hoa",
    "priceMin": 120000,
    "priceMax": 600000,
    "rating": 4.7,
    "reviews": 780,
    "parking": true,
    "private_room": true,
    "vegetarian": true,
    "openHours": "10:30 - 22:00",
    "image": "https://images.unsplash.com/photo-1550966871-3ed3cdb5ed0c?w=800",
    "menu": [
      {
        "name": "Há Cảo Tôm Tươi Hấp",
        "price": 98000.0
      },
      {
        "name": "Xíu Mại Tôm Thịt Gạch Cua",
        "price": 95000.0
      },
      {
        "name": "Bánh Bao Kim Sa Trứng Muối",
        "price": 85000.0
      },
      {
        "name": "Vịt Quay Bắc Kinh (Nửa con)",
        "price": 480000.0
      },
      {
        "name": "Xá Xíu Mật Ong Đút Lò",
        "price": 260000.0
      }
    ],
    "district": "Quận 1",
    "has_parking": true,
    "has_private_room": true,
    "has_outdoor": false,
    "outdoor": false,
    "pet_friendly": false,
    "has_pet_friendly": false,
    "vegetarian_support": true,
    "menus": [
      {
        "name": "Dimsum Xửng Hấp Thủ Công",
        "description": "Dimsum hấp nóng hổi tại bàn, vỏ mỏng nhân đầy đặn",
        "items": [
          {
            "name": "Há Cảo Tôm Tươi Hấp",
            "description": "Vỏ bánh trong suốt thấy rõ tôm sú tươi giòn sần sật",
            "price": 98000.0,
            "image_url": "https://images.unsplash.com/photo-1563245372-f21724e3856d?w=800"
          },
          {
            "name": "Xíu Mại Tôm Thịt Gạch Cua",
            "description": "Thịt heo nạc dăm, tôm tươi phủ gạch cua béo ngậy bên trên",
            "price": 95000.0,
            "image_url": "https://images.unsplash.com/photo-1541696432-82c6da8ce7bf?w=800"
          },
          {
            "name": "Bánh Bao Kim Sa Trứng Muối",
            "description": "Nhân trứng muối tan chảy thơm lừng mùi bơ sữa",
            "price": 85000.0,
            "image_url": "https://images.unsplash.com/photo-1541696490-8744a5dc0228?w=800"
          }
        ]
      },
      {
        "name": "Món Quay & Nướng Quảng Đông",
        "description": "Bí quyết tẩm ướp gia truyền hàng chục năm",
        "items": [
          {
            "name": "Vịt Quay Bắc Kinh (Nửa con)",
            "description": "Da vịt giòn rụm cuốn bánh tráng kèm dưa leo hành hoa, thịt xào mì",
            "price": 480000.0,
            "image_url": "https://images.unsplash.com/photo-1518492104633-130d0cc84637?w=800"
          },
          {
            "name": "Xá Xíu Mật Ong Đút Lò",
            "description": "Thịt nạc vai heo ướp mật ong rừng nướng xém cạnh mềm ngọt",
            "price": 260000.0,
            "image_url": "https://images.unsplash.com/photo-1544025162-d76694265947?w=800"
          }
        ]
      }
    ],
    "images": [
      {
        "image_url": "https://images.unsplash.com/photo-1550966871-3ed3cdb5ed0c?w=800",
        "caption": "Không gian nhà hàng Dim Tu Tac đẳng cấp tại Saigon Centre",
        "is_cover": true
      },
      {
        "image_url": "https://images.unsplash.com/photo-1563245372-f21724e3856d?w=800",
        "caption": "Xửng há cảo tôm tươi hấp khói nghi ngút",
        "is_cover": false
      }
    ],
    "description": "Thiên đường ẩm thực Quảng Đông hiện đại, nổi danh với các món Dimsum chế biến công phu, vịt quay Bắc Kinh da giòn.",
    "phone_number": "02838266668"
  },
  {
    "id": 4,
    "name": "Cơm Tấm Thuận Kiều - Tôn Thất Tùng",
    "address": "46 Tôn Thất Tùng, Phường Bến Thành, Quận 1, TP. Hồ Chí Minh",
    "lat": 10.7701,
    "lng": 106.6915,
    "category": "vietnamese",
    "cuisineLabel": "Món Việt",
    "priceMin": 55000,
    "priceMax": 140000,
    "rating": 4.4,
    "reviews": 530,
    "parking": true,
    "private_room": false,
    "vegetarian": false,
    "openHours": "06:00 - 21:30",
    "image": "https://images.unsplash.com/photo-1555396273-367ea4eb4db5?w=800",
    "menu": [
      {
        "name": "Cơm Tấm Sườn Cốt Lết Nướng",
        "price": 75000.0
      },
      {
        "name": "Cơm Tấm Sườn Bì Chả Trứng Ốp La",
        "price": 110000.0
      },
      {
        "name": "Cơm Tấm Sườn Non Cọng",
        "price": 95000.0
      },
      {
        "name": "Canh Khổ Qua Nhồi Thịt",
        "price": 35000.0
      },
      {
        "name": "Trà Đá Sâm Dứa Hạt É",
        "price": 15000.0
      }
    ],
    "district": "Quận 1",
    "has_parking": true,
    "has_private_room": false,
    "has_outdoor": false,
    "outdoor": false,
    "pet_friendly": false,
    "has_pet_friendly": false,
    "vegetarian_support": false,
    "menus": [
      {
        "name": "Cơm Tấm Đĩa Đặc Biệt",
        "description": "Hạt cơm tấm thơm dẻo chan mỡ hành tóp mỡ giòn rụm",
        "items": [
          {
            "name": "Cơm Tấm Sườn Cốt Lết Nướng",
            "description": "Miếng sườn ướp gia vị đậm đà nướng than hoa vàng ươm",
            "price": 75000.0,
            "image_url": "https://images.unsplash.com/photo-1559847844-5315695dadae?w=800"
          },
          {
            "name": "Cơm Tấm Sườn Bì Chả Trứng Ốp La",
            "description": "Combo đầy đủ nhất gồm sườn nướng, bì heo trộn thính, chả trứng và trứng ốp la",
            "price": 110000.0,
            "image_url": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=800"
          },
          {
            "name": "Cơm Tấm Sườn Non Cọng",
            "description": "Sườn non nướng thơm béo ngậy kèm dưa chua củ cải cà rốt",
            "price": 95000.0,
            "image_url": "https://images.unsplash.com/photo-1544025162-d76694265947?w=800"
          }
        ]
      },
      {
        "name": "Canh & Nước Giải Khát",
        "description": "Canh nóng húp kèm cơm tấm",
        "items": [
          {
            "name": "Canh Khổ Qua Nhồi Thịt",
            "description": "Khổ qua hầm thịt nạc xay mộc nhĩ thanh mát giải nhiệt",
            "price": 35000.0,
            "image_url": "https://images.unsplash.com/photo-1547592180-85f173990554?w=800"
          },
          {
            "name": "Trà Đá Sâm Dứa Hạt É",
            "description": "Thơm mát vị lá dứa giải nhiệt ngày hè",
            "price": 15000.0,
            "image_url": "https://images.unsplash.com/photo-1513558161293-cdaf765ed2fd?w=800"
          }
        ]
      }
    ],
    "images": [
      {
        "image_url": "https://images.unsplash.com/photo-1555396273-367ea4eb4db5?w=800",
        "caption": "Không gian quán sạch sẽ, phục vụ nhanh chóng thân thiện",
        "is_cover": true
      },
      {
        "image_url": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=800",
        "caption": "Đĩa cơm tấm sườn bì chả ốp la trứ danh Sài Gòn",
        "is_cover": false
      }
    ],
    "description": "Thương hiệu cơm tấm Sài Gòn lâu đời với miếng sườn nướng mật ong thơm lừng và chả trứng hấp mềm mịn đặc trưng.",
    "phone_number": "02839250935"
  },
  {
    "id": 5,
    "name": "Sushi Tei - Đông Du",
    "address": "20 Đông Du, Phường Bến Nghé, Quận 1, TP. Hồ Chí Minh",
    "lat": 10.7768,
    "lng": 106.7042,
    "category": "japanese",
    "cuisineLabel": "Món Nhật",
    "priceMin": 150000,
    "priceMax": 700000,
    "rating": 4.7,
    "reviews": 460,
    "parking": true,
    "private_room": true,
    "vegetarian": true,
    "openHours": "11:00 - 22:30",
    "image": "https://images.unsplash.com/photo-1579871494447-9811cf80d66c?w=800",
    "menu": [
      {
        "name": "Sashimi Cá Hồi Na Uy (Salmon Sashimi)",
        "price": 185000.0
      },
      {
        "name": "Thuyền Sashimi Thượng Hạng 5 Loại",
        "price": 550000.0
      },
      {
        "name": "Sushi Lươn Nhật Nướng Unagi",
        "price": 165000.0
      },
      {
        "name": "Maki Cá Hồi Nướng Phô Mai",
        "price": 195000.0
      }
    ],
    "district": "Quận 1",
    "has_parking": true,
    "has_private_room": true,
    "has_outdoor": false,
    "outdoor": false,
    "pet_friendly": false,
    "has_pet_friendly": false,
    "vegetarian_support": true,
    "menus": [
      {
        "name": "Sashimi Tươi Sống",
        "description": "Cắt lát tươi ngon giữ trọn vẹn vị ngọt biển cả",
        "items": [
          {
            "name": "Sashimi Cá Hồi Na Uy (Salmon Sashimi)",
            "description": "5 lát cá hồi vân mỡ đều đặn, béo ngậy ngọt thịt",
            "price": 185000.0,
            "image_url": "https://images.unsplash.com/photo-1579871494447-9811cf80d66c?w=800"
          },
          {
            "name": "Thuyền Sashimi Thượng Hạng 5 Loại",
            "description": "Cá hồi, cá ngừ, bạch tuộc, sò điệp Nhật và tôm ngọt Amaebi",
            "price": 550000.0,
            "image_url": "https://images.unsplash.com/photo-1617196034796-73dfa7b1fd56?w=800"
          }
        ]
      },
      {
        "name": "Sushi & Cuốn Đặc Biệt",
        "description": "Cơm giấm dẻo hạt Akita kết hợp sốt đặc trưng",
        "items": [
          {
            "name": "Sushi Lươn Nhật Nướng Unagi",
            "description": "Lươn Nhật nướng sốt Kabayaki đậm đà béo ngọt",
            "price": 165000.0,
            "image_url": "https://images.unsplash.com/photo-1611143669185-af224c5e3252?w=800"
          },
          {
            "name": "Maki Cá Hồi Nướng Phô Mai",
            "description": "Cuốn cá hồi khò lửa tái béo ngậy với sốt phô mai trứng cá chuồn",
            "price": 195000.0,
            "image_url": "https://images.unsplash.com/photo-1563245372-f21724e3856d?w=800"
          }
        ]
      }
    ],
    "images": [
      {
        "image_url": "https://images.unsplash.com/photo-1579871494447-9811cf80d66c?w=800",
        "caption": "Set Sashimi tươi sống chuẩn phong cách ẩm thực xứ Phù Tang",
        "is_cover": true
      },
      {
        "image_url": "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=800",
        "caption": "Quầy Sushi Bar nơi thực khách chiêm ngưỡng đầu bếp biểu diễn",
        "is_cover": false
      }
    ],
    "description": "Nhà hàng Nhật Bản chuẩn mực với nguồn nguyên liệu hải sản tươi sống nhập khẩu trực tiếp từ chợ cá Toyosu Nhật Bản.",
    "phone_number": "02862841188"
  },
  {
    "id": 6,
    "name": "El Gaucho Argentinian Steakhouse",
    "address": "74 Hai Bà Trưng, Phường Bến Nghé, Quận 1, TP. Hồ Chí Minh",
    "lat": 10.7772,
    "lng": 106.7035,
    "category": "western",
    "cuisineLabel": "Món Âu",
    "priceMin": 500000,
    "priceMax": 2500000,
    "rating": 4.9,
    "reviews": 920,
    "parking": true,
    "private_room": true,
    "vegetarian": false,
    "openHours": "11:00 - 23:30",
    "image": "https://images.unsplash.com/photo-1544025162-d76694265947?w=800",
    "menu": [
      {
        "name": "Bò Ribeye Black Angus 300g",
        "price": 890000.0
      },
      {
        "name": "Bò Thăn Nội Tenderloin Wagyu 250g",
        "price": 1450000.0
      },
      {
        "name": "Khoai Tây Nghiền Bơ Nấm Truffle",
        "price": 160000.0
      },
      {
        "name": "Măng Tây Xanh Áp Chảo Bơ Tỏi",
        "price": 150000.0
      }
    ],
    "district": "Quận 1",
    "has_parking": true,
    "has_private_room": true,
    "has_outdoor": true,
    "outdoor": true,
    "pet_friendly": false,
    "has_pet_friendly": false,
    "vegetarian_support": false,
    "menus": [
      {
        "name": "Thịt Bò Thượng Hạng Nướng Than",
        "description": "Nướng than hoa theo độ chín yêu cầu của thực khách",
        "items": [
          {
            "name": "Bò Ribeye Black Angus 300g",
            "description": "Phần nạc lưng bò Mỹ với vân mỡ cẩm thạch mềm mọng nước",
            "price": 890000.0,
            "image_url": "https://images.unsplash.com/photo-1544025162-d76694265947?w=800"
          },
          {
            "name": "Bò Thăn Nội Tenderloin Wagyu 250g",
            "description": "Thịt mềm tan trong miệng ăn kèm sốt nấm Truffle quý hiếm",
            "price": 1450000.0,
            "image_url": "https://images.unsplash.com/photo-1558030006-450675393462?w=800"
          }
        ]
      },
      {
        "name": "Rượu Vang & Món Ăn Kèm",
        "description": "Kết hợp hoàn hảo cùng Steak",
        "items": [
          {
            "name": "Khoai Tây Nghiền Bơ Nấm Truffle",
            "description": "Khoai tây vàng mịn thơm lừng mùi bơ Pháp và dầu nấm Truffle",
            "price": 160000.0,
            "image_url": "https://images.unsplash.com/photo-1518013034458-30b0ee243591?w=800"
          },
          {
            "name": "Măng Tây Xanh Áp Chảo Bơ Tỏi",
            "description": "Măng tây giòn ngọt thơm dịu tỏi nướng",
            "price": 150000.0,
            "image_url": "https://images.unsplash.com/photo-1540420773420-3366772f4999?w=800"
          }
        ]
      }
    ],
    "images": [
      {
        "image_url": "https://images.unsplash.com/photo-1544025162-d76694265947?w=800",
        "caption": "Miếng bít tết bò Wagyu chín vừa mọng nước chuẩn 5 sao",
        "is_cover": true
      },
      {
        "image_url": "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=800",
        "caption": "Không gian đèn vàng quý phái đậm chất Nam Mỹ",
        "is_cover": false
      }
    ],
    "description": "Nhà hàng bít tết phong cách Argentina sang trọng hàng đầu TP.HCM, thịt bò Black Angus và Wagyu nhập khẩu nướng than củi mộc.",
    "phone_number": "02838258500"
  },
  {
    "id": 7,
    "name": "Bếp Mẹ Ỉn - Vietnamese Street Food",
    "address": "136 Lê Thánh Tôn, Phường Bến Thành, Quận 1, TP. Hồ Chí Minh",
    "lat": 10.7728,
    "lng": 106.6991,
    "category": "vietnamese",
    "cuisineLabel": "Món Việt",
    "priceMin": 70000,
    "priceMax": 250000,
    "rating": 4.6,
    "reviews": 710,
    "parking": false,
    "private_room": false,
    "vegetarian": true,
    "openHours": "10:30 - 22:30",
    "image": "https://images.unsplash.com/photo-1555396273-367ea4eb4db5?w=800",
    "menu": [
      {
        "name": "Bánh Xèo Tôm Thịt Chảo Nhỏ",
        "price": 95000.0
      },
      {
        "name": "Cơm Chiên Trái Dừa Hải Sản",
        "price": 145000.0
      },
      {
        "name": "Trứng Non Cháy Tỏi",
        "price": 125000.0
      }
    ],
    "district": "Quận 1",
    "has_parking": false,
    "has_private_room": false,
    "has_outdoor": false,
    "outdoor": false,
    "pet_friendly": false,
    "has_pet_friendly": false,
    "vegetarian_support": true,
    "menus": [
      {
        "name": "Đặc Sản Bếp Mẹ Ỉn",
        "description": "Các món ăn dân dã sáng tạo đạt chuẩn Michelin",
        "items": [
          {
            "name": "Bánh Xèo Tôm Thịt Chảo Nhỏ",
            "description": "Bánh xèo giòn rụm cuốn cải bẹ xanh chấm nước mắm chua ngọt",
            "price": 95000.0,
            "image_url": "https://images.unsplash.com/photo-1559847844-5315695dadae?w=800"
          },
          {
            "name": "Cơm Chiên Trái Dừa Hải Sản",
            "description": "Cơm chiên hạt ngọc thơm phức bọc trong trái dừa xiêm tươi",
            "price": 145000.0,
            "image_url": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=800"
          },
          {
            "name": "Trứng Non Cháy Tỏi",
            "description": "Trứng gà non vàng ươm xào bơ tỏi thơm ngào ngạt",
            "price": 125000.0,
            "image_url": "https://images.unsplash.com/photo-1541544741938-0af808871cc0?w=800"
          }
        ]
      }
    ],
    "images": [
      {
        "image_url": "https://images.unsplash.com/photo-1555396273-367ea4eb4db5?w=800",
        "caption": "Không gian hoài niệm vẽ tranh tường Sài Gòn xưa",
        "is_cover": true
      },
      {
        "image_url": "https://images.unsplash.com/photo-1559847844-5315695dadae?w=800",
        "caption": "Mẹt bánh xèo giòn rụm rau rừng tươi sạch",
        "is_cover": false
      }
    ],
    "description": "Quán ăn ẩm thực đường phố Việt Nam đạt chứng nhận Michelin Bib Gourmand, nổi tiếng với bánh xèo tôm nhảy và cơm chiên trái dừa.",
    "phone_number": "02838244666"
  },
  {
    "id": 8,
    "name": "TukTuk Thai Bistro - Lý Tự Trọng",
    "address": "38 Lý Tự Trọng, Phường Bến Nghé, Quận 1, TP. Hồ Chí Minh",
    "lat": 10.777,
    "lng": 106.7005,
    "category": "other",
    "cuisineLabel": "Món Thái",
    "priceMin": 95000,
    "priceMax": 350000,
    "rating": 4.5,
    "reviews": 540,
    "parking": true,
    "private_room": false,
    "vegetarian": true,
    "openHours": "10:00 - 22:00",
    "image": "https://images.unsplash.com/photo-1559314809-0d155014e29e?w=800",
    "menu": [
      {
        "name": "Súp Tom Yum Cốt Dừa Hải Sản",
        "price": 195000.0
      },
      {
        "name": "Gỏi Đu Đủ Ba Khía Cay Nồng (Som Tum)",
        "price": 125000.0
      },
      {
        "name": "Pad Thai Tôm Sú",
        "price": 165000.0
      },
      {
        "name": "Xôi Xoài Nước Cốt Dừa",
        "price": 85000.0
      }
    ],
    "district": "Quận 1",
    "has_parking": true,
    "has_private_room": false,
    "has_outdoor": true,
    "outdoor": true,
    "pet_friendly": false,
    "has_pet_friendly": false,
    "vegetarian_support": true,
    "menus": [
      {
        "name": "Món Cay & Nước Dùng Thái",
        "description": "Hương vị nồng nàn thảo mộc sả ớt lá chanh Thái",
        "items": [
          {
            "name": "Súp Tom Yum Cốt Dừa Hải Sản",
            "description": "Tôm càng xanh, nấm rơm, sả, riềng trong nước súp chua cay cốt dừa",
            "price": 195000.0,
            "image_url": "https://images.unsplash.com/photo-1559314809-0d155014e29e?w=800"
          },
          {
            "name": "Gỏi Đu Đủ Ba Khía Cay Nồng (Som Tum)",
            "description": "Đu đủ giã cối đất cùng đậu phộng, tôm khô và chanh ớt",
            "price": 125000.0,
            "image_url": "https://images.unsplash.com/photo-1540420773420-3366772f4999?w=800"
          }
        ]
      },
      {
        "name": "Mì & Cơm Chiên",
        "description": "Các món ăn quen thuộc đường phố Thái Lan",
        "items": [
          {
            "name": "Pad Thai Tôm Sú",
            "description": "Hủ tiếu xào sốt me chua ngọt ăn kèm giá hẹ và đậu hũ chiên",
            "price": 165000.0,
            "image_url": "https://images.unsplash.com/photo-1559847844-5315695dadae?w=800"
          },
          {
            "name": "Xôi Xoài Nước Cốt Dừa",
            "description": "Xôi nếp dẻo thơm ăn cùng xoài cát chín vàng ngọt lịm",
            "price": 85000.0,
            "image_url": "https://images.unsplash.com/photo-1571877227200-a0d98ea607e9?w=800"
          }
        ]
      }
    ],
    "images": [
      {
        "image_url": "https://images.unsplash.com/photo-1559314809-0d155014e29e?w=800",
        "caption": "Thố súp Tom Yum đỏ au nóng hổi đậm chất Thái Lan",
        "is_cover": true
      },
      {
        "image_url": "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=800",
        "caption": "Không gian Bistro hiện đại, phá cách",
        "is_cover": false
      }
    ],
    "description": "Bistro ẩm thực Thái Lan sành điệu giữa trung tâm Sài Gòn với các món Tom Yum, pad Thái và gỏi đu đủ chua cay đúng điệu Bangkok.",
    "phone_number": "02838251676"
  },
  {
    "id": 9,
    "name": "Phở Quỳnh - Phạm Ngũ Lão",
    "address": "323 Phạm Ngũ Lão, Phường Phạm Ngũ Lão, Quận 1, TP. Hồ Chí Minh",
    "lat": 10.7675,
    "lng": 106.6912,
    "category": "vietnamese",
    "cuisineLabel": "Món Việt",
    "priceMin": 65000,
    "priceMax": 110000,
    "rating": 4.5,
    "reviews": 690,
    "parking": true,
    "private_room": false,
    "vegetarian": false,
    "openHours": "00:00 - 23:59 (Mở cả ngày)",
    "image": "https://images.unsplash.com/photo-1582878826629-29b7ad1cdc43?w=800",
    "menu": [
      {
        "name": "Phở Bò Tái Nạm Gầu",
        "price": 85000.0
      },
      {
        "name": "Phở Đặc Biệt (Tái, Nạm, Gầu, Gân, Bò Viên)",
        "price": 105000.0
      },
      {
        "name": "Chén Trứng Chần Nước Béo",
        "price": 15000.0
      }
    ],
    "district": "Quận 1",
    "has_parking": true,
    "has_private_room": false,
    "has_outdoor": true,
    "outdoor": true,
    "pet_friendly": false,
    "has_pet_friendly": false,
    "vegetarian_support": false,
    "menus": [
      {
        "name": "Các Món Phở Bò",
        "description": "Phở bò truyền thống bánh phở tươi dẻo thơm",
        "items": [
          {
            "name": "Phở Bò Tái Nạm Gầu",
            "description": "Thịt bò tái mềm, nạm giòn thơm và gầu béo ngậy ngập trong nước dùng trong vắt",
            "price": 85000.0,
            "image_url": "https://images.unsplash.com/photo-1582878826629-29b7ad1cdc43?w=800"
          },
          {
            "name": "Phở Đặc Biệt (Tái, Nạm, Gầu, Gân, Bò Viên)",
            "description": "Tô phở thập cẩm đầy đặn bồi bổ năng lượng",
            "price": 105000.0,
            "image_url": "https://images.unsplash.com/photo-1582878826629-29b7ad1cdc43?w=800"
          },
          {
            "name": "Chén Trứng Chần Nước Béo",
            "description": "Trứng gà ta lòng đào ăn kèm hành lá và nước béo",
            "price": 15000.0,
            "image_url": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=800"
          }
        ]
      }
    ],
    "images": [
      {
        "image_url": "https://images.unsplash.com/photo-1582878826629-29b7ad1cdc43?w=800",
        "caption": "Tô phở bò nóng hổi nghi ngút khói thơm mùi hồi quế",
        "is_cover": true
      },
      {
        "image_url": "https://images.unsplash.com/photo-1555396273-367ea4eb4db5?w=800",
        "caption": "Mặt tiền quán phở nhộn nhịp tại phố Tây",
        "is_cover": false
      }
    ],
    "description": "Quán phở bò gia truyền hoạt động 24/7 tại khu phố Tây Bùi Viện, nước dùng hầm xương tủy bò 18 tiếng ngọt lịm tự nhiên.",
    "phone_number": "02838368515"
  },
  {
    "id": 10,
    "name": "Gyu-Shige Ngưu Phồn - Hàm Nghi",
    "address": "119 Hàm Nghi, Phường Bến Nghé, Quận 1, TP. Hồ Chí Minh",
    "lat": 10.7718,
    "lng": 106.7029,
    "category": "other",
    "cuisineLabel": "Lẩu Nướng",
    "priceMin": 200000,
    "priceMax": 650000,
    "rating": 4.6,
    "reviews": 480,
    "parking": true,
    "private_room": true,
    "vegetarian": false,
    "openHours": "10:30 - 23:00",
    "image": "https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=800",
    "menu": [
      {
        "name": "Dẻ Sườn Bò Mỹ Ướp Sốt Tare",
        "price": 210000.0
      },
      {
        "name": "Lưỡi Bò Nướng Muối Hành",
        "price": 195000.0
      }
    ],
    "district": "Quận 1",
    "has_parking": true,
    "has_private_room": true,
    "has_outdoor": false,
    "outdoor": false,
    "pet_friendly": false,
    "has_pet_friendly": false,
    "vegetarian_support": false,
    "menus": [
      {
        "name": "Thịt Nướng Yakiniku",
        "description": "Tẩm ướp sốt Tare gia truyền Nhật Bản",
        "items": [
          {
            "name": "Dẻ Sườn Bò Mỹ Ướp Sốt Tare",
            "description": "Thịt dẻ sườn mềm thơm có độ giòn nhẹ nướng than hồng",
            "price": 210000.0,
            "image_url": "https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=800"
          },
          {
            "name": "Lưỡi Bò Nướng Muối Hành",
            "description": "Lưỡi bò thái mỏng giòn sần sật nướng muối tiêu chanh Nhật",
            "price": 195000.0,
            "image_url": "https://images.unsplash.com/photo-1544025162-d76694265947?w=800"
          }
        ]
      }
    ],
    "images": [
      {
        "image_url": "https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=800",
        "caption": "Bếp than nướng Yakiniku rực hồng tỏa hương thơm phức",
        "is_cover": true
      }
    ],
    "description": "Hệ thống nướng Yakiniku trứ danh đến từ Nhật Bản, phục vụ thịt bò hảo hạng nướng trên bếp than hoa không khói.",
    "phone_number": "02838218958"
  },
  {
    "id": 11,
    "name": "Secret Garden Restaurant - Rooftop Pasteur",
    "address": "158 Pasteur, Phường Bến Nghé, Quận 1, TP. Hồ Chí Minh",
    "lat": 10.7778,
    "lng": 106.6989,
    "category": "vietnamese",
    "cuisineLabel": "Món Việt",
    "priceMin": 80000,
    "priceMax": 280000,
    "rating": 4.5,
    "reviews": 810,
    "parking": true,
    "private_room": false,
    "vegetarian": true,
    "openHours": "11:00 - 22:00",
    "image": "https://images.unsplash.com/photo-1537047902294-62a40c20a6ae?w=800",
    "menu": [
      {
        "name": "Bông Bí Xào Tỏi",
        "price": 85000.0
      },
      {
        "name": "Sườn Non Nướng Muối Ớt",
        "price": 165000.0
      }
    ],
    "district": "Quận 1",
    "has_parking": true,
    "has_private_room": false,
    "has_outdoor": true,
    "outdoor": true,
    "pet_friendly": true,
    "has_pet_friendly": true,
    "vegetarian_support": true,
    "menus": [
      {
        "name": "Đặc Sản Miền Tây Mộc Mạc",
        "description": "Món ăn chân quê dân dã",
        "items": [
          {
            "name": "Bông Bí Xào Tỏi",
            "description": "Bông bí ngô ngọt giòn hái tại vườn xào tỏi đập dập",
            "price": 85000.0,
            "image_url": "https://images.unsplash.com/photo-1540420773420-3366772f4999?w=800"
          },
          {
            "name": "Sườn Non Nướng Muối Ớt",
            "description": "Sườn non cây ướp ớt hiểm cay nồng thơm lừng",
            "price": 165000.0,
            "image_url": "https://images.unsplash.com/photo-1544025162-d76694265947?w=800"
          }
        ]
      }
    ],
    "images": [
      {
        "image_url": "https://images.unsplash.com/photo-1537047902294-62a40c20a6ae?w=800",
        "caption": "Khu vườn sân thượng ngập tràn cây xanh và ánh đèn lãng mạn",
        "is_cover": true
      }
    ],
    "description": "Khu vườn ẩm thực bí mật trên tầng thượng chung cư cổ Pasteur, mang đến trải nghiệm ăn uống mộc mạc trong vườn cây xanh mát.",
    "phone_number": "0909904621"
  },
  {
    "id": 12,
    "name": "Hum Lounge & Restaurant - Thi Sách",
    "address": "2 Thi Sách, Phường Bến Nghé, Quận 1, TP. Hồ Chí Minh",
    "lat": 10.7785,
    "lng": 106.705,
    "category": "vegetarian",
    "cuisineLabel": "Món Chay",
    "priceMin": 120000,
    "priceMax": 500000,
    "rating": 4.9,
    "reviews": 670,
    "parking": true,
    "private_room": true,
    "vegetarian": true,
    "openHours": "10:00 - 22:00",
    "image": "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=800",
    "menu": [
      {
        "name": "Cơm Gạo Lứt Hạt Sen Lá Sen",
        "price": 155000.0
      },
      {
        "name": "Súp Nấm Tùng Nhung Hạt Dẻ",
        "price": 135000.0
      }
    ],
    "district": "Quận 1",
    "has_parking": true,
    "has_private_room": true,
    "has_outdoor": true,
    "outdoor": true,
    "pet_friendly": false,
    "has_pet_friendly": false,
    "vegetarian_support": true,
    "menus": [
      {
        "name": "Món Chay Dưỡng Sinh",
        "description": "Nguyên liệu rau củ hữu cơ tươi sạch theo mùa",
        "items": [
          {
            "name": "Cơm Gạo Lứt Hạt Sen Lá Sen",
            "description": "Gạo lứt đỏ dẻo bùi bọc trong lá sen hấp cùng hạt sen tươi",
            "price": 155000.0,
            "image_url": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=800"
          },
          {
            "name": "Súp Nấm Tùng Nhung Hạt Dẻ",
            "description": "Nấm quý bổ dưỡng hầm cùng hạt dẻ thơm bùi thanh đạm",
            "price": 135000.0,
            "image_url": "https://images.unsplash.com/photo-1547592180-85f173990554?w=800"
          }
        ]
      }
    ],
    "images": [
      {
        "image_url": "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=800",
        "caption": "Không gian thiền tịnh an yên giữa phố thị tấp nập",
        "is_cover": true
      }
    ],
    "description": "Nhà hàng chay mỹ vị cao cấp hàng đầu Việt Nam, tôn vinh ẩm thực thuần thực vật tươi ngon trong không gian thiền tịnh tĩnh tại.",
    "phone_number": "02838238999"
  },
  {
    "id": 13,
    "name": "Bánh Mì Huỳnh Hoa - Lê Thị Riêng",
    "address": "26 Lê Thị Riêng, Phường Bến Thành, Quận 1, TP. Hồ Chí Minh",
    "lat": 10.7712,
    "lng": 106.6923,
    "category": "vietnamese",
    "cuisineLabel": "Món Việt",
    "priceMin": 45000,
    "priceMax": 75000,
    "rating": 4.4,
    "reviews": 1150,
    "parking": false,
    "private_room": false,
    "vegetarian": false,
    "openHours": "06:00 - 22:00",
    "image": "https://images.unsplash.com/photo-1559847844-5315695dadae?w=800",
    "menu": [
      {
        "name": "Bánh Mì Thập Cẩm Đặc Biệt",
        "price": 68000.0
      }
    ],
    "district": "Quận 1",
    "has_parking": false,
    "has_private_room": false,
    "has_outdoor": false,
    "outdoor": false,
    "pet_friendly": false,
    "has_pet_friendly": false,
    "vegetarian_support": false,
    "menus": [
      {
        "name": "Bánh Mì Đặc Biệt",
        "description": "Bánh mì giòn rụm nóng hổi nhân ngập tràn",
        "items": [
          {
            "name": "Bánh Mì Thập Cẩm Đặc Biệt",
            "description": "Pate gan thơm lừng, bơ trứng vàng béo, giò thủ, chả lụa, jambon và chà bông",
            "price": 68000.0,
            "image_url": "https://images.unsplash.com/photo-1559847844-5315695dadae?w=800"
          }
        ]
      }
    ],
    "images": [
      {
        "image_url": "https://images.unsplash.com/photo-1559847844-5315695dadae?w=800",
        "caption": "Ổ bánh mì đầy đặn trứ danh khiến bao thực khách mê mẩn",
        "is_cover": true
      }
    ],
    "description": "Ổ bánh mì pate thịt nguội nổi tiếng bậc nhất Sài Gòn với biệt danh 'bánh mì ô môi', đầy ắp 5-6 loại chả lụa pate béo ngậy.",
    "phone_number": "02839250885"
  },
  {
    "id": 14,
    "name": "Hải Sản Rạn Biển - Nguyễn Thái Bình",
    "address": "45 Nguyễn Thái Bình, Phường Nguyễn Thái Bình, Quận 1, TP. Hồ Chí Minh",
    "lat": 10.7708,
    "lng": 106.7008,
    "category": "other",
    "cuisineLabel": "Hải Sản",
    "priceMin": 180000,
    "priceMax": 1200000,
    "rating": 4.6,
    "reviews": 510,
    "parking": true,
    "private_room": true,
    "vegetarian": false,
    "openHours": "10:00 - 23:00",
    "image": "https://images.unsplash.com/photo-1534422298391-e4f8c172dddb?w=800",
    "menu": [
      {
        "name": "Cua Cà Mau Sốt Trứng Muối",
        "price": 380000.0
      },
      {
        "name": "Tôm Sú Hấp Nước Dừa",
        "price": 280000.0
      }
    ],
    "district": "Quận 1",
    "has_parking": true,
    "has_private_room": true,
    "has_outdoor": false,
    "outdoor": false,
    "pet_friendly": false,
    "has_pet_friendly": false,
    "vegetarian_support": false,
    "menus": [
      {
        "name": "Hải Sản Bắt Tại Bể",
        "description": "Tươi sống 100% cân ký chế biến theo yêu cầu",
        "items": [
          {
            "name": "Cua Cà Mau Sốt Trứng Muối",
            "description": "Cua thịt chắc nịch phủ sốt trứng muối béo ngậy thơm lừng",
            "price": 380000.0,
            "image_url": "https://images.unsplash.com/photo-1534422298391-e4f8c172dddb?w=800"
          },
          {
            "name": "Tôm Sú Hấp Nước Dừa",
            "description": "Tôm sú biển hấp dừa xiêm giữ nguyên độ ngọt giòn tươi ngon",
            "price": 280000.0,
            "image_url": "https://images.unsplash.com/photo-1565680018434-b513d5e5fd47?w=800"
          }
        ]
      }
    ],
    "images": [
      {
        "image_url": "https://images.unsplash.com/photo-1534422298391-e4f8c172dddb?w=800",
        "caption": "Đĩa cua sốt trứng muối vàng ươm hấp dẫn",
        "is_cover": true
      }
    ],
    "description": "Hệ thống nhà hàng hải sản tươi sống cao cấp với bể hải sản quy mô lớn, chế biến tại chỗ các loại cua hoàng đế, tôm hùm, cá mú.",
    "phone_number": "02838210387"
  },
  {
    "id": 15,
    "name": "Lẩu Gà Lá É Tao Ngộ - Nguyễn Thái Bình",
    "address": "79 Nguyễn Thái Bình, Phường Nguyễn Thái Bình, Quận 1, TP. Hồ Chí Minh",
    "lat": 10.7698,
    "lng": 106.6995,
    "category": "hotpot",
    "cuisineLabel": "Lẩu Nướng",
    "priceMin": 80000,
    "priceMax": 220000,
    "rating": 4.5,
    "reviews": 410,
    "parking": true,
    "private_room": false,
    "vegetarian": false,
    "openHours": "09:30 - 23:00",
    "image": "https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=800",
    "menu": [
      {
        "name": "Lẩu Gà Lá É Nồi Nhỏ (2 người)",
        "price": 200000.0
      },
      {
        "name": "Lẩu Gà Lá É Nồi Lớn (4 người)",
        "price": 320000.0
      }
    ],
    "district": "Quận 1",
    "has_parking": true,
    "has_private_room": false,
    "has_outdoor": true,
    "outdoor": true,
    "pet_friendly": true,
    "has_pet_friendly": true,
    "vegetarian_support": false,
    "menus": [
      {
        "name": "Lẩu Gà Đặc Sản",
        "description": "Gà ta thả đồi thịt dai ngọt",
        "items": [
          {
            "name": "Lẩu Gà Lá É Nồi Nhỏ (2 người)",
            "description": "Nửa con gà ta, nấm sò, măng chua và rổ lá é tươi thơm phức",
            "price": 200000.0,
            "image_url": "https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=800"
          },
          {
            "name": "Lẩu Gà Lá É Nồi Lớn (4 người)",
            "description": "Nguyên con gà ta kèm đĩa bún tươi và nấm tươi",
            "price": 320000.0,
            "image_url": "https://images.unsplash.com/photo-1547592180-85f173990554?w=800"
          }
        ]
      }
    ],
    "images": [
      {
        "image_url": "https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=800",
        "caption": "Nồi lẩu gà lá é sôi sùng sục ấm áp ngày mưa",
        "is_cover": true
      }
    ],
    "description": "Đặc sản lẩu gà lá é nổi tiếng Đà Lạt nay có mặt tại Quận 1, nước dùng ngọt thanh từ măng le tươi và vị cay nồng the the của lá é.",
    "phone_number": "0977221345"
  },
  {
    "id": 16,
    "name": "Phở Hòa Pasteur",
    "address": "260C Pasteur, Phường Võ Thị Sáu, Quận 3, TP. Hồ Chí Minh",
    "lat": 10.7871,
    "lng": 106.6882,
    "category": "vietnamese",
    "cuisineLabel": "Món Việt",
    "priceMin": 75000,
    "priceMax": 120000,
    "rating": 4.6,
    "reviews": 1120,
    "parking": true,
    "private_room": false,
    "vegetarian": false,
    "openHours": "06:00 - 22:30",
    "image": "https://images.unsplash.com/photo-1582878826629-29b7ad1cdc43?w=800",
    "menu": [
      {
        "name": "Phở Tái Lăn Áp Chảo",
        "price": 95000.0
      },
      {
        "name": "Phở Thập Cẩm Hòa Pasteur",
        "price": 115000.0
      }
    ],
    "district": "Quận 3",
    "has_parking": true,
    "has_private_room": false,
    "has_outdoor": false,
    "outdoor": false,
    "pet_friendly": false,
    "has_pet_friendly": false,
    "vegetarian_support": false,
    "menus": [
      {
        "name": "Phở Bò Truyền Thống",
        "description": "Ăn kèm đĩa rau thơm, ngò gai, giá đỗ và quẩy giòn",
        "items": [
          {
            "name": "Phở Tái Lăn Áp Chảo",
            "description": "Thịt bò xào lăn tỏi lửa lớn dậy mùi thơm quyến rũ",
            "price": 95000.0,
            "image_url": "https://images.unsplash.com/photo-1582878826629-29b7ad1cdc43?w=800"
          },
          {
            "name": "Phở Thập Cẩm Hòa Pasteur",
            "description": "Tô phở lớn đầy ắp thịt bò tái, nạm, gân, bò viên và giò heo",
            "price": 115000.0,
            "image_url": "https://images.unsplash.com/photo-1582878826629-29b7ad1cdc43?w=800"
          }
        ]
      }
    ],
    "images": [
      {
        "image_url": "https://images.unsplash.com/photo-1582878826629-29b7ad1cdc43?w=800",
        "caption": "Tô phở Hòa Pasteur thơm nức mũi nước dùng trong trẻo",
        "is_cover": true
      }
    ],
    "description": "Quán phở biểu tượng hơn 50 năm của Sài Gòn trên con đường Pasteur, gắn liền với ký ức ẩm thực của nhiều thế hệ người dân TP.HCM.",
    "phone_number": "02838297943"
  },
  {
    "id": 17,
    "name": "Cơm Niêu Sài Gòn - Tú Xương",
    "address": "27 Tú Xương, Phường Võ Thị Sáu, Quận 3, TP. Hồ Chí Minh",
    "lat": 10.782,
    "lng": 106.6845,
    "category": "vietnamese",
    "cuisineLabel": "Món Việt",
    "priceMin": 110000,
    "priceMax": 400000,
    "rating": 4.6,
    "reviews": 750,
    "parking": true,
    "private_room": true,
    "vegetarian": true,
    "openHours": "10:00 - 22:00",
    "image": "https://images.unsplash.com/photo-1555396273-367ea4eb4db5?w=800",
    "menu": [
      {
        "name": "Cơm Đập Cháy Hai Mặt",
        "price": 65000.0
      },
      {
        "name": "Cá Khoai Kho Tộ Đậm Đà",
        "price": 185000.0
      }
    ],
    "district": "Quận 3",
    "has_parking": true,
    "has_private_room": true,
    "has_outdoor": true,
    "outdoor": true,
    "pet_friendly": false,
    "has_pet_friendly": false,
    "vegetarian_support": true,
    "menus": [
      {
        "name": "Cơm Niêu & Cơm Đập",
        "description": "Nấu trong niêu đất tạo lớp cháy vàng giòn rụm",
        "items": [
          {
            "name": "Cơm Đập Cháy Hai Mặt",
            "description": "Niêu cơm đập vỡ lấy trọn mảng cơm cháy giòn rụm chan mỡ hành",
            "price": 65000.0,
            "image_url": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=800"
          },
          {
            "name": "Cá Khoai Kho Tộ Đậm Đà",
            "description": "Cá béo ngọt kho kẹo sền sệt chấm cơm cháy giòn tan",
            "price": 185000.0,
            "image_url": "https://images.unsplash.com/photo-1519708227418-c8fd9a32b7a2?w=800"
          }
        ]
      }
    ],
    "images": [
      {
        "image_url": "https://images.unsplash.com/photo-1555396273-367ea4eb4db5?w=800",
        "caption": "Không gian sân vườn biệt thự cổ lãng mạn tại Tú Xương",
        "is_cover": true
      }
    ],
    "description": "Nhà hàng cơm niêu nổi tiếng với nghệ thuật tung hứng 'cơm đập' độc đáo và các món ăn đậm đà phong vị làng quê Bắc - Trung - Nam.",
    "phone_number": "02839326344"
  },
  {
    "id": 18,
    "name": "Bánh Xèo Ăn Là Ghiền - Tú Xương",
    "address": "11A Tú Xương, Phường Võ Thị Sáu, Quận 3, TP. Hồ Chí Minh",
    "lat": 10.7802,
    "lng": 106.686,
    "category": "vietnamese",
    "cuisineLabel": "Món Việt",
    "priceMin": 65000,
    "priceMax": 180000,
    "rating": 4.4,
    "reviews": 430,
    "parking": true,
    "private_room": false,
    "vegetarian": true,
    "openHours": "09:00 - 22:00",
    "image": "https://images.unsplash.com/photo-1559847844-5315695dadae?w=800",
    "menu": [
      {
        "name": "Bánh Xèo Tôm Thịt Củ Hũ Dừa",
        "price": 95000.0
      },
      {
        "name": "Bánh Khọt Tôm Nước Cốt Dừa (8 cái)",
        "price": 85000.0
      }
    ],
    "district": "Quận 3",
    "has_parking": true,
    "has_private_room": false,
    "has_outdoor": true,
    "outdoor": true,
    "pet_friendly": false,
    "has_pet_friendly": false,
    "vegetarian_support": true,
    "menus": [
      {
        "name": "Bánh Xèo Vàng Giòn",
        "description": "Đổ chảo gang thủ công",
        "items": [
          {
            "name": "Bánh Xèo Tôm Thịt Củ Hũ Dừa",
            "description": "Củ hũ dừa ngọt thanh giòn ngọt kết hợp tôm đất và thịt ba chỉ",
            "price": 95000.0,
            "image_url": "https://images.unsplash.com/photo-1559847844-5315695dadae?w=800"
          },
          {
            "name": "Bánh Khọt Tôm Nước Cốt Dừa (8 cái)",
            "description": "Bánh khọt tôm tươi vàng giòn chan nước cốt dừa béo mặn",
            "price": 85000.0,
            "image_url": "https://images.unsplash.com/photo-1541544741938-0af808871cc0?w=800"
          }
        ]
      }
    ],
    "images": [
      {
        "image_url": "https://images.unsplash.com/photo-1559847844-5315695dadae?w=800",
        "caption": "Chiếc bánh xèo vàng ươm tràn ngập tôm thịt",
        "is_cover": true
      }
    ],
    "description": "Quán bánh xèo miền Tây khổng lồ với vỏ bánh mỏng tanh vàng giòn, nhân tôm thịt nấm củ hũ dừa và rổ rau rừng Tây Ninh tươi sạch.",
    "phone_number": "02839301969"
  },
  {
    "id": 19,
    "name": "Ẩm Thực Quê Nhà - Phạm Ngọc Thạch",
    "address": "28 Phạm Ngọc Thạch, Phường Võ Thị Sáu, Quận 3, TP. Hồ Chí Minh",
    "lat": 10.7845,
    "lng": 106.6942,
    "category": "vietnamese",
    "cuisineLabel": "Món Việt",
    "priceMin": 100000,
    "priceMax": 380000,
    "rating": 4.5,
    "reviews": 690,
    "parking": true,
    "private_room": true,
    "vegetarian": true,
    "openHours": "10:00 - 23:30",
    "image": "https://images.unsplash.com/photo-1537047902294-62a40c20a6ae?w=800",
    "menu": [
      {
        "name": "Gà Ta Hấp Mắm Nhĩ",
        "price": 280000.0
      },
      {
        "name": "Cơm Cháy Chà Bông Mỡ Hành",
        "price": 95000.0
      }
    ],
    "district": "Quận 3",
    "has_parking": true,
    "has_private_room": true,
    "has_outdoor": true,
    "outdoor": true,
    "pet_friendly": false,
    "has_pet_friendly": false,
    "vegetarian_support": true,
    "menus": [
      {
        "name": "Món Nhậu & Đồng Quê",
        "description": "Hương vị nồng ấm sum họp bạn bè",
        "items": [
          {
            "name": "Gà Ta Hấp Mắm Nhĩ",
            "description": "Thịt gà ta thả vườn giòn da đẫm vị nước mắm nhĩ thơm lừng",
            "price": 280000.0,
            "image_url": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=800"
          },
          {
            "name": "Cơm Cháy Chà Bông Mỡ Hành",
            "description": "Món ăn chơi giòn bùi ngập tràn ruốc thịt",
            "price": 95000.0,
            "image_url": "https://images.unsplash.com/photo-1541544741938-0af808871cc0?w=800"
          }
        ]
      }
    ],
    "images": [
      {
        "image_url": "https://images.unsplash.com/photo-1537047902294-62a40c20a6ae?w=800",
        "caption": "Không gian sân vườn tre xanh mộc mạc thoáng mát",
        "is_cover": true
      }
    ],
    "description": "Khu ẩm thực dân dã quy mô lớn rợp bóng tre trúc, hội tụ hơn 200 món ăn ba miền đặc sắc trong không gian làng quê Việt.",
    "phone_number": "0938226166"
  },
  {
    "id": 20,
    "name": "Manwah Taiwanese Hotpot - Cao Thắng",
    "address": "19 Cao Thắng, Phường 2, Quận 3, TP. Hồ Chí Minh",
    "lat": 10.7695,
    "lng": 106.683,
    "category": "hotpot",
    "cuisineLabel": "Lẩu Nướng",
    "priceMin": 299000,
    "priceMax": 499000,
    "rating": 4.7,
    "reviews": 640,
    "parking": true,
    "private_room": true,
    "vegetarian": true,
    "openHours": "10:00 - 22:30",
    "image": "https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=800",
    "menu": [
      {
        "name": "Suất Buffet Lẩu Premium",
        "price": 439000.0
      }
    ],
    "district": "Quận 3",
    "has_parking": true,
    "has_private_room": true,
    "has_outdoor": false,
    "outdoor": false,
    "pet_friendly": false,
    "has_pet_friendly": false,
    "vegetarian_support": true,
    "menus": [
      {
        "name": "Buffet Lẩu Xứ Đài",
        "description": "Thưởng thức không giới hạn thịt bò thượng hạng và hải sản",
        "items": [
          {
            "name": "Suất Buffet Lẩu Premium",
            "description": "Thịt gầu bò hoa, ba chỉ bò Mỹ, há cảo Đài Loan và quầy kem đồ tráng miệng",
            "price": 439000.0,
            "image_url": "https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=800"
          }
        ]
      }
    ],
    "images": [
      {
        "image_url": "https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=800",
        "caption": "Nồi lẩu uyên ương 2 ngăn hương vị Đài Loan đặc sắc",
        "is_cover": true
      }
    ],
    "description": "Lẩu Đài Loan buffet thượng hạng với nước lẩu Mala cay nồng, lẩu collagen ngọt dưỡng và thịt bò Mỹ nhúng tươi ngon.",
    "phone_number": "02873007981"
  },
  {
    "id": 21,
    "name": "Nhà Hàng Chay Pi Bistro - Võ Văn Tần",
    "address": "19 Võ Văn Tần, Phường Võ Thị Sáu, Quận 3, TP. Hồ Chí Minh",
    "lat": 10.7788,
    "lng": 106.6922,
    "category": "vegetarian",
    "cuisineLabel": "Món Chay",
    "priceMin": 85000,
    "priceMax": 280000,
    "rating": 4.8,
    "reviews": 520,
    "parking": true,
    "private_room": false,
    "vegetarian": true,
    "openHours": "10:00 - 21:30",
    "image": "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=800",
    "menu": [
      {
        "name": "Đậu Hũ Non Sốt Nấm Rừng",
        "price": 115000.0
      },
      {
        "name": "Gỏi Bưởi Tân Triều Hạt Điều",
        "price": 125000.0
      }
    ],
    "district": "Quận 3",
    "has_parking": true,
    "has_private_room": false,
    "has_outdoor": true,
    "outdoor": true,
    "pet_friendly": true,
    "has_pet_friendly": true,
    "vegetarian_support": true,
    "menus": [
      {
        "name": "Món Chay Nghệ Thuật",
        "description": "Hương vị thiên nhiên mộc mạc",
        "items": [
          {
            "name": "Đậu Hũ Non Sốt Nấm Rừng",
            "description": "Đậu hũ tự làm mịn màng sốt nấm hương và dầu mè thơm",
            "price": 115000.0,
            "image_url": "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=800"
          },
          {
            "name": "Gỏi Bưởi Tân Triều Hạt Điều",
            "description": "Tép bưởi hồng mọng nước trộn hạt điều rang giòn rụm",
            "price": 125000.0,
            "image_url": "https://images.unsplash.com/photo-1540420773420-3366772f4999?w=800"
          }
        ]
      }
    ],
    "images": [
      {
        "image_url": "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=800",
        "caption": "Món ăn thuần chay bài trí tinh tế và bắt mắt",
        "is_cover": true
      }
    ],
    "description": "Quán chay mang phong cách nghệ thuật ấm áp, kết hợp hài hòa nguyên liệu bản địa và kỹ thuật ẩm thực Á Đông thanh nhẹ.",
    "phone_number": "0916414133"
  },
  {
    "id": 22,
    "name": "Hải Sản Biển Đông - Trần Quốc Toản",
    "address": "71 Trần Quốc Toản, Phường Võ Thị Sáu, Quận 3, TP. Hồ Chí Minh",
    "lat": 10.7885,
    "lng": 106.6865,
    "category": "other",
    "cuisineLabel": "Hải Sản",
    "priceMin": 150000,
    "priceMax": 950000,
    "rating": 4.5,
    "reviews": 470,
    "parking": true,
    "private_room": true,
    "vegetarian": false,
    "openHours": "09:30 - 23:00",
    "image": "https://images.unsplash.com/photo-1534422298391-e4f8c172dddb?w=800",
    "menu": [
      {
        "name": "Mực Trứng Hấp Gừng",
        "price": 220000.0
      },
      {
        "name": "Hàu Nướng Phô Mai Béo Ngậy (4 con)",
        "price": 140000.0
      }
    ],
    "district": "Quận 3",
    "has_parking": true,
    "has_private_room": true,
    "has_outdoor": false,
    "outdoor": false,
    "pet_friendly": false,
    "has_pet_friendly": false,
    "vegetarian_support": false,
    "menus": [
      {
        "name": "Đặc Sản Biển Tươi Sống",
        "description": "Chế biến nướng mỡ hành, hấp bia hoặc xào sốt me",
        "items": [
          {
            "name": "Mực Trứng Hấp Gừng",
            "description": "Mực trứng tươi béo ngậy ngọt lịm chấm muối ớt xanh",
            "price": 220000.0,
            "image_url": "https://images.unsplash.com/photo-1534422298391-e4f8c172dddb?w=800"
          },
          {
            "name": "Hàu Nướng Phô Mai Béo Ngậy (4 con)",
            "description": "Hàu sữa béo núc ních phủ lớp sốt phô mai kéo sợi",
            "price": 140000.0,
            "image_url": "https://images.unsplash.com/photo-1565680018434-b513d5e5fd47?w=800"
          }
        ]
      }
    ],
    "images": [
      {
        "image_url": "https://images.unsplash.com/photo-1534422298391-e4f8c172dddb?w=800",
        "caption": "Hải sản tươi sống bắt tại bể chế biến theo phong vị Sài Gòn",
        "is_cover": true
      }
    ],
    "description": "Nhà hàng hải sản tươi sống lâu năm tại Quận 3, nổi bật với thực đơn cua ghẹ Nha Trang, tôm hùm baby và cá mú đỏ biển sâu.",
    "phone_number": "02838206888"
  },
  {
    "id": 23,
    "name": "Lẩu Dê Trương Định",
    "address": "105 Trương Định, Phường Võ Thị Sáu, Quận 3, TP. Hồ Chí Minh",
    "lat": 10.7811,
    "lng": 106.6875,
    "category": "hotpot",
    "cuisineLabel": "Món Việt",
    "priceMin": 120000,
    "priceMax": 350000,
    "rating": 4.4,
    "reviews": 560,
    "parking": true,
    "private_room": false,
    "vegetarian": false,
    "openHours": "10:30 - 23:00",
    "image": "https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=800",
    "menu": [
      {
        "name": "Lẩu Dựng Dê Thuốc Bắc",
        "price": 260000.0
      },
      {
        "name": "Dê Nướng Mọi Chấm Chao",
        "price": 190000.0
      }
    ],
    "district": "Quận 3",
    "has_parking": true,
    "has_private_room": false,
    "has_outdoor": true,
    "outdoor": true,
    "pet_friendly": false,
    "has_pet_friendly": false,
    "vegetarian_support": false,
    "menus": [
      {
        "name": "Lẩu & Nướng Dê Núi",
        "description": "Đặc sản bồi bổ khí huyết thơm ngon",
        "items": [
          {
            "name": "Lẩu Dựng Dê Thuốc Bắc",
            "description": "Dựng dê giòn sần sật ninh cùng củ sen, táo tàu, kỷ tử và nấm đông cô",
            "price": 260000.0,
            "image_url": "https://images.unsplash.com/photo-1547592180-85f173990554?w=800"
          },
          {
            "name": "Dê Nướng Mọi Chấm Chao",
            "description": "Thịt đùi dê tơ ướp sả ớt nướng than hồng chấm chao sa tế",
            "price": 190000.0,
            "image_url": "https://images.unsplash.com/photo-1544025162-d76694265947?w=800"
          }
        ]
      }
    ],
    "images": [
      {
        "image_url": "https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=800",
        "caption": "Nồi lẩu dê thuốc bắc thơm lừng ngút khói",
        "is_cover": true
      }
    ],
    "description": "Quán lẩu dê gia truyền nổi tiếng Sài Gòn, thịt dê đồi Ninh Bình tươi ngon không hề hôi, nước lẩu hầm thuốc bắc thơm nồng.",
    "phone_number": "02839304296"
  },
  {
    "id": 24,
    "name": "San Fu Lou - Ngô Thời Nhiệm",
    "address": "24 Ngô Thời Nhiệm, Phường Võ Thị Sáu, Quận 3, TP. Hồ Chí Minh",
    "lat": 10.7805,
    "lng": 106.6908,
    "category": "other",
    "cuisineLabel": "Món Hoa",
    "priceMin": 100000,
    "priceMax": 450000,
    "rating": 4.6,
    "reviews": 610,
    "parking": true,
    "private_room": true,
    "vegetarian": true,
    "openHours": "07:00 - 22:00",
    "image": "https://images.unsplash.com/photo-1550966871-3ed3cdb5ed0c?w=800",
    "menu": [
      {
        "name": "Mì Hoành Thánh Tôm Thịt Xá Xíu",
        "price": 115000.0
      },
      {
        "name": "Chân Gà Hấp Tàu Xì",
        "price": 85000.0
      }
    ],
    "district": "Quận 3",
    "has_parking": true,
    "has_private_room": true,
    "has_outdoor": true,
    "outdoor": true,
    "pet_friendly": false,
    "has_pet_friendly": false,
    "vegetarian_support": true,
    "menus": [
      {
        "name": "Mì Kéo & Dimsum",
        "description": "Sợi mì tươi kéo bằng tay mềm dai",
        "items": [
          {
            "name": "Mì Hoành Thánh Tôm Thịt Xá Xíu",
            "description": "Nước dùng xương hầm thanh ngọt kèm hoành thánh tôm nguyên con",
            "price": 115000.0,
            "image_url": "https://images.unsplash.com/photo-1582878826629-29b7ad1cdc43?w=800"
          },
          {
            "name": "Chân Gà Hấp Tàu Xì",
            "description": "Chân gà rút xương mềm rục thấm đượm gia vị tàu xì thơm nồng",
            "price": 85000.0,
            "image_url": "https://images.unsplash.com/photo-1541696432-82c6da8ce7bf?w=800"
          }
        ]
      }
    ],
    "images": [
      {
        "image_url": "https://images.unsplash.com/photo-1550966871-3ed3cdb5ed0c?w=800",
        "caption": "Không gian ẩm thực Quảng Đông sang trọng phong cách San Fu Lou",
        "is_cover": true
      }
    ],
    "description": "Ngôi nhà ẩm thực Quảng Đông hiện đại với mô hình bếp mở trực quan, phục vụ các món mì kéo sợi tươi và dimsum hấp dẫn.",
    "phone_number": "02839302888"
  },
  {
    "id": 25,
    "name": "Gyu-Kaku BBQ - Nguyễn Thị Minh Khai",
    "address": "254 Nguyễn Thị Minh Khai, Phường Võ Thị Sáu, Quận 3, TP. Hồ Chí Minh",
    "lat": 10.776,
    "lng": 106.6888,
    "category": "bbq",
    "cuisineLabel": "Lẩu Nướng",
    "priceMin": 220000,
    "priceMax": 600000,
    "rating": 4.6,
    "reviews": 510,
    "parking": true,
    "private_room": true,
    "vegetarian": false,
    "openHours": "10:30 - 22:00",
    "image": "https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=800",
    "menu": [
      {
        "name": "Ba Chỉ Bò Mỹ Sốt Miso Cay",
        "price": 145000.0
      }
    ],
    "district": "Quận 3",
    "has_parking": true,
    "has_private_room": true,
    "has_outdoor": false,
    "outdoor": false,
    "pet_friendly": false,
    "has_pet_friendly": false,
    "vegetarian_support": false,
    "menus": [
      {
        "name": "Bò Nướng Yakiniku",
        "description": "Thịt bò nướng than hoa mềm mọng nước",
        "items": [
          {
            "name": "Ba Chỉ Bò Mỹ Sốt Miso Cay",
            "description": "Từng lát ba chỉ mỏng ướp tương miso nướng xèo xèo thơm ngát",
            "price": 145000.0,
            "image_url": "https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=800"
          }
        ]
      }
    ],
    "images": [
      {
        "image_url": "https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=800",
        "caption": "Bàn tiệc nướng Nhật Bản đầy đặn sắc màu",
        "is_cover": true
      }
    ],
    "description": "Thương hiệu nướng Yakiniku số 1 Nhật Bản, thỏa mãn đam mê ẩm thực nướng than hoa với các loại sốt nướng đậm đà chuẩn vị Tokyo.",
    "phone_number": "02862907481"
  },
  {
    "id": 26,
    "name": "Bò Tơ Quán Mộc - Hoàng Hoa Thám",
    "address": "43 Hoàng Hoa Thám, Phường 6, Quận Bình Thạnh, TP. Hồ Chí Minh",
    "lat": 10.8062,
    "lng": 106.6948,
    "category": "vietnamese",
    "cuisineLabel": "Món Việt",
    "priceMin": 90000,
    "priceMax": 320000,
    "rating": 4.7,
    "reviews": 680,
    "parking": true,
    "private_room": true,
    "vegetarian": false,
    "openHours": "10:00 - 23:00",
    "image": "https://images.unsplash.com/photo-1555396273-367ea4eb4db5?w=800",
    "menu": [
      {
        "name": "Bò Tơ Cuốn Bánh Tráng Rau Rừng",
        "price": 195000.0
      },
      {
        "name": "Bò Tơ Nướng Tảng Sốt Trứng Muối",
        "price": 245000.0
      },
      {
        "name": "Lẩu Đuôi Bò Nấm Thảo Mộc",
        "price": 285000.0
      }
    ],
    "district": "Quận Bình Thạnh",
    "has_parking": true,
    "has_private_room": true,
    "has_outdoor": true,
    "outdoor": true,
    "pet_friendly": false,
    "has_pet_friendly": false,
    "vegetarian_support": false,
    "menus": [
      {
        "name": "Đặc Sản Bò Tơ Cuốn",
        "description": "Bò non sữa mềm ngọt tự nhiên",
        "items": [
          {
            "name": "Bò Tơ Cuốn Bánh Tráng Rau Rừng",
            "description": "Thịt bắp bò tơ hấp mềm cuộn rau rừng chấm mắm nêm đậm đà",
            "price": 195000.0,
            "image_url": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=800"
          },
          {
            "name": "Bò Tơ Nướng Tảng Sốt Trứng Muối",
            "description": "Thịt bò nướng nguyên tảng giữ trọn vị ngọt chấm sốt trứng muối béo",
            "price": 245000.0,
            "image_url": "https://images.unsplash.com/photo-1544025162-d76694265947?w=800"
          },
          {
            "name": "Lẩu Đuôi Bò Nấm Thảo Mộc",
            "description": "Nước lẩu thơm ngọt thanh từ củ sen và đuôi bò ninh nhừ",
            "price": 285000.0,
            "image_url": "https://images.unsplash.com/photo-1547592180-85f173990554?w=800"
          }
        ]
      }
    ],
    "images": [
      {
        "image_url": "https://images.unsplash.com/photo-1555396273-367ea4eb4db5?w=800",
        "caption": "Không gian hoài niệm Hà Nội phố xưa ấm cúng",
        "is_cover": true
      },
      {
        "image_url": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=800",
        "caption": "Mẹt bò tơ cuốn bánh tráng rau rừng tươi ngon",
        "is_cover": false
      }
    ],
    "description": "Không gian phố xưa Hà Nội thập niên 80 giữa lòng Bình Thạnh, nổi danh với bò tơ non mềm ngọt thịt cuốn bánh tráng rau rừng.",
    "phone_number": "0946221188"
  },
  {
    "id": 27,
    "name": "Gà Nướng Ò Ó O - D2 (Nguyễn Gia Trí)",
    "address": "83 Nguyễn Gia Trí, Phường 25, Quận Bình Thạnh, TP. Hồ Chí Minh",
    "lat": 10.8035,
    "lng": 106.7145,
    "category": "bbq",
    "cuisineLabel": "Món Việt",
    "priceMin": 60000,
    "priceMax": 220000,
    "rating": 4.5,
    "reviews": 590,
    "parking": true,
    "private_room": false,
    "vegetarian": false,
    "openHours": "10:30 - 22:00",
    "image": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=800",
    "menu": [
      {
        "name": "Gà Nướng Tiêu Rừng Tây Bắc (Nguyên con)",
        "price": 195000.0
      },
      {
        "name": "Gà Nướng Sốt Ớt Cay Địa Trung Hải",
        "price": 195000.0
      },
      {
        "name": "Xôi Chiên Phồng Dẻo Giòn",
        "price": 35000.0
      }
    ],
    "district": "Quận Bình Thạnh",
    "has_parking": true,
    "has_private_room": false,
    "has_outdoor": false,
    "outdoor": false,
    "pet_friendly": false,
    "has_pet_friendly": false,
    "vegetarian_support": false,
    "menus": [
      {
        "name": "Gà Nướng Đủ Vị Sốt",
        "description": "Gà nướng lu than thơm vàng da giòn thịt mọng nước",
        "items": [
          {
            "name": "Gà Nướng Tiêu Rừng Tây Bắc (Nguyên con)",
            "description": "Vị cay the the thơm nồng đặc trưng của hạt dổi và mắc khén",
            "price": 195000.0,
            "image_url": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=800"
          },
          {
            "name": "Gà Nướng Sốt Ớt Cay Địa Trung Hải",
            "description": "Sốt ớt đỏ cay nồng kích thích vị giác chấm muối ớt chanh",
            "price": 195000.0,
            "image_url": "https://images.unsplash.com/photo-1544025162-d76694265947?w=800"
          },
          {
            "name": "Xôi Chiên Phồng Dẻo Giòn",
            "description": "Xôi nếp chiên phồng ruộm giòn ngoài mềm trong",
            "price": 35000.0,
            "image_url": "https://images.unsplash.com/photo-1541544741938-0af808871cc0?w=800"
          }
        ]
      }
    ],
    "images": [
      {
        "image_url": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=800",
        "caption": "Con gà nướng vàng ươm thơm phức gia vị đặc chế",
        "is_cover": true
      }
    ],
    "description": "Thiên đường gà nướng với hơn 10 vị sốt độc quyền sáng tạo như sốt ớt cay Địa Trung Hải, sốt tiêu rừng Tây Bắc, xôi chiên giòn.",
    "phone_number": "1900636009"
  },
  {
    "id": 28,
    "name": "Cháo Vịt Thanh Đa - Gốc Nhà Lá",
    "address": "118 Bình Quới, Phường 27, Quận Bình Thạnh, TP. Hồ Chí Minh",
    "lat": 10.8242,
    "lng": 106.7265,
    "category": "vietnamese",
    "cuisineLabel": "Món Việt",
    "priceMin": 50000,
    "priceMax": 180000,
    "rating": 4.5,
    "reviews": 840,
    "parking": true,
    "private_room": false,
    "vegetarian": false,
    "openHours": "07:00 - 23:00",
    "image": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=800",
    "menu": [
      {
        "name": "Đĩa Gỏi Vịt Thanh Đa (Phần 2 người)",
        "price": 140000.0
      },
      {
        "name": "Tô Cháo Huyết Nóng Hổi",
        "price": 25000.0
      }
    ],
    "district": "Quận Bình Thạnh",
    "has_parking": true,
    "has_private_room": false,
    "has_outdoor": true,
    "outdoor": true,
    "pet_friendly": true,
    "has_pet_friendly": true,
    "vegetarian_support": false,
    "menus": [
      {
        "name": "Cháo & Gỏi Vịt",
        "description": "Thịt vịt ngọt thịt không mùi hôi",
        "items": [
          {
            "name": "Đĩa Gỏi Vịt Thanh Đa (Phần 2 người)",
            "description": "Thịt vịt chặt miếng đều tay rắc đậu phộng rang giòn chấm mắm gừng",
            "price": 140000.0,
            "image_url": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=800"
          },
          {
            "name": "Tô Cháo Huyết Nóng Hổi",
            "description": "Cháo nấu gạo rang thơm sánh mịn cùng huyết vịt béo mềm",
            "price": 25000.0,
            "image_url": "https://images.unsplash.com/photo-1547592180-85f173990554?w=800"
          }
        ]
      }
    ],
    "images": [
      {
        "image_url": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=800",
        "caption": "Đĩa gỏi vịt đầy đặn kèm chén nước mắm gừng sánh đặc",
        "is_cover": true
      }
    ],
    "description": "Thương hiệu cháo gỏi vịt trứ danh vùng bán đảo Thanh Đa hơn 30 năm, thịt vịt cỏ ít mỡ chắc thịt, gỏi bắp cải trộn hành phi giòn rụm.",
    "phone_number": "02838986656"
  },
  {
    "id": 29,
    "name": "Vườn Chay Garden Restaurant - Lê Quang Định",
    "address": "428 Lê Quang Định, Phường 11, Quận Bình Thạnh, TP. Hồ Chí Minh",
    "lat": 10.817,
    "lng": 106.6925,
    "category": "vegetarian",
    "cuisineLabel": "Món Chay",
    "priceMin": 60000,
    "priceMax": 240000,
    "rating": 4.6,
    "reviews": 430,
    "parking": true,
    "private_room": true,
    "vegetarian": true,
    "openHours": "09:00 - 21:30",
    "image": "https://images.unsplash.com/photo-1537047902294-62a40c20a6ae?w=800",
    "menu": [
      {
        "name": "Lẩu Nấm Thập Cẩm Chay",
        "price": 195000.0
      },
      {
        "name": "Chả Giò Nấm Hạt Sen",
        "price": 85000.0
      }
    ],
    "district": "Quận Bình Thạnh",
    "has_parking": true,
    "has_private_room": true,
    "has_outdoor": true,
    "outdoor": true,
    "pet_friendly": false,
    "has_pet_friendly": false,
    "vegetarian_support": true,
    "menus": [
      {
        "name": "Món Chay Thanh Tịnh",
        "description": "Chế biến từ nấm và rau củ tươi hữu cơ",
        "items": [
          {
            "name": "Lẩu Nấm Thập Cẩm Chay",
            "description": "Nấm đông cô, nấm đùi gà, nấm linh chi trong nước lẩu rau củ ngọt tự nhiên",
            "price": 195000.0,
            "image_url": "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=800"
          },
          {
            "name": "Chả Giò Nấm Hạt Sen",
            "description": "Vỏ bánh rế giòn tan cuộn khoai môn và hạt sen bùi béo",
            "price": 85000.0,
            "image_url": "https://images.unsplash.com/photo-1541544741938-0af808871cc0?w=800"
          }
        ]
      }
    ],
    "images": [
      {
        "image_url": "https://images.unsplash.com/photo-1537047902294-62a40c20a6ae?w=800",
        "caption": "Khu vườn sân vườn xanh mát của Vườn Chay Garden",
        "is_cover": true
      }
    ],
    "description": "Không gian ẩm thực chay xanh mát như khu vườn nhiệt đới, thực đơn phong phú hơn 100 món chay thanh đạm bồi bổ sức khỏe.",
    "phone_number": "02836200778"
  },
  {
    "id": 30,
    "name": "Hải Sản Gió Biển - Bờ Sông Thanh Đa",
    "address": "101 Bình Quới, Cư xá Thanh Đa, Phường 27, Quận Bình Thạnh, TP. Hồ Chí Minh",
    "lat": 10.825,
    "lng": 106.728,
    "category": "other",
    "cuisineLabel": "Hải Sản",
    "priceMin": 120000,
    "priceMax": 450000,
    "rating": 4.4,
    "reviews": 380,
    "parking": true,
    "private_room": true,
    "vegetarian": false,
    "openHours": "10:00 - 23:00",
    "image": "https://images.unsplash.com/photo-1537047902294-62a40c20a6ae?w=800",
    "menu": [
      {
        "name": "Tôm Càng Xanh Nướng Muối Ớt",
        "price": 260000.0
      },
      {
        "name": "Nghêu Hấp Sả Thơm Lừng",
        "price": 95000.0
      }
    ],
    "district": "Quận Bình Thạnh",
    "has_parking": true,
    "has_private_room": true,
    "has_outdoor": true,
    "outdoor": true,
    "pet_friendly": true,
    "has_pet_friendly": true,
    "vegetarian_support": false,
    "menus": [
      {
        "name": "Hải Sản Ven Sông",
        "description": "Thưởng thức cùng view sông Sài Gòn thoáng mát",
        "items": [
          {
            "name": "Tôm Càng Xanh Nướng Muối Ớt",
            "description": "Tôm càng sông gạch son béo ngậy nướng muối ớt cay xè",
            "price": 260000.0,
            "image_url": "https://images.unsplash.com/photo-1534422298391-e4f8c172dddb?w=800"
          },
          {
            "name": "Nghêu Hấp Sả Thơm Lừng",
            "description": "Nghêu biển ngọt nước hấp sả ớt nóng hổi",
            "price": 95000.0,
            "image_url": "https://images.unsplash.com/photo-1565680018434-b513d5e5fd47?w=800"
          }
        ]
      }
    ],
    "images": [
      {
        "image_url": "https://images.unsplash.com/photo-1537047902294-62a40c20a6ae?w=800",
        "caption": "Bàn tiệc ven sông ngắm hoàng hôn buông trên sông Sài Gòn",
        "is_cover": true
      }
    ],
    "description": "Nhà hàng hải sản ven sông Sài Gòn lộng gió, điểm hẹn lý tưởng để thưởng thức bia mát lạnh và hải sản tươi rói lúc hoàng hôn.",
    "phone_number": "02835561122"
  },
  {
    "id": 31,
    "name": "Quán Nướng Khói Quê - Điện Biên Phủ",
    "address": "592 Điện Biên Phủ, Phường 22, Quận Bình Thạnh, TP. Hồ Chí Minh",
    "lat": 10.7985,
    "lng": 106.718,
    "category": "bbq",
    "cuisineLabel": "Lẩu Nướng",
    "priceMin": 60000,
    "priceMax": 200000,
    "rating": 4.3,
    "reviews": 490,
    "parking": true,
    "private_room": false,
    "vegetarian": false,
    "openHours": "15:30 - 23:30",
    "image": "https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=800",
    "menu": [
      {
        "name": "Bò Cuộn Nấm Kim Châm Nướng Ngói",
        "price": 95000.0
      },
      {
        "name": "Bạch Tuộc Sa Tế Nướng Giòn",
        "price": 105000.0
      }
    ],
    "district": "Quận Bình Thạnh",
    "has_parking": true,
    "has_private_room": false,
    "has_outdoor": true,
    "outdoor": true,
    "pet_friendly": true,
    "has_pet_friendly": true,
    "vegetarian_support": false,
    "menus": [
      {
        "name": "Nướng Ngói Độc Đáo",
        "description": "Nướng trên phiến ngói đất nung không khét dầu",
        "items": [
          {
            "name": "Bò Cuộn Nấm Kim Châm Nướng Ngói",
            "description": "Bò Mỹ cuộn nấm kim châm giòn ngọt sốt tiêu đen",
            "price": 95000.0,
            "image_url": "https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=800"
          },
          {
            "name": "Bạch Tuộc Sa Tế Nướng Giòn",
            "description": "Bạch tuộc nướng sần sật cay cay đã miệng",
            "price": 105000.0,
            "image_url": "https://images.unsplash.com/photo-1534422298391-e4f8c172dddb?w=800"
          }
        ]
      }
    ],
    "images": [
      {
        "image_url": "https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=800",
        "caption": "Món nướng ngói bốc khói nghi ngút thơm nức mũi",
        "is_cover": true
      }
    ],
    "description": "Quán nướng bình dân đông đúc nổi tiếng với các món nướng ngói và nướng than hoa ướp sa tế cay nồng dành cho giới trẻ.",
    "phone_number": "0908776655"
  },
  {
    "id": 32,
    "name": "Bún Bò Huế Út Hưng - Bạch Đằng",
    "address": "113 Bạch Đằng, Phường 15, Quận Bình Thạnh, TP. Hồ Chí Minh",
    "lat": 10.801,
    "lng": 106.705,
    "category": "vietnamese",
    "cuisineLabel": "Món Việt",
    "priceMin": 45000,
    "priceMax": 85000,
    "rating": 4.5,
    "reviews": 520,
    "parking": true,
    "private_room": false,
    "vegetarian": false,
    "openHours": "06:00 - 21:00",
    "image": "https://images.unsplash.com/photo-1582878826629-29b7ad1cdc43?w=800",
    "menu": [
      {
        "name": "Bún Bò Giò Nạc Chả Cua",
        "price": 65000.0
      }
    ],
    "district": "Quận Bình Thạnh",
    "has_parking": true,
    "has_private_room": false,
    "has_outdoor": false,
    "outdoor": false,
    "pet_friendly": false,
    "has_pet_friendly": false,
    "vegetarian_support": false,
    "menus": [
      {
        "name": "Bún Bò Xứ Huế",
        "description": "Hương vị chuẩn cố đô cay the sa tế",
        "items": [
          {
            "name": "Bún Bò Giò Nạc Chả Cua",
            "description": "Tô bún bò đầy đặn khoanh giò nạc, chả cua Huế và bò tái",
            "price": 65000.0,
            "image_url": "https://images.unsplash.com/photo-1582878826629-29b7ad1cdc43?w=800"
          }
        ]
      }
    ],
    "images": [
      {
        "image_url": "https://images.unsplash.com/photo-1582878826629-29b7ad1cdc43?w=800",
        "caption": "Tô bún bò Huế thơm ngát mắm ruốc và màu dầu điều bắt mắt",
        "is_cover": true
      }
    ],
    "description": "Quán bún bò Huế lâu năm tại Bình Thạnh với nước dùng đậm đà mùi mắm ruốc Huế, sả tươi và miếng bắp bò hoa giòn ngọt.",
    "phone_number": "02838401234"
  },
  {
    "id": 33,
    "name": "Sumo Yakiniku - Landmark 81",
    "address": "Tầng B1 Landmark 81, 720A Điện Biên Phủ, Phường 22, Quận Bình Thạnh, TP. Hồ Chí Minh",
    "lat": 10.795,
    "lng": 106.7218,
    "category": "other",
    "cuisineLabel": "Lẩu Nướng",
    "priceMin": 350000,
    "priceMax": 650000,
    "rating": 4.7,
    "reviews": 670,
    "parking": true,
    "private_room": true,
    "vegetarian": false,
    "openHours": "10:30 - 22:00",
    "image": "https://images.unsplash.com/photo-1555396273-367ea4eb4db5?w=800",
    "menu": [
      {
        "name": "Buffet Nướng Sumo Otoku",
        "price": 469000.0
      }
    ],
    "district": "Quận Bình Thạnh",
    "has_parking": true,
    "has_private_room": true,
    "has_outdoor": false,
    "outdoor": false,
    "pet_friendly": false,
    "has_pet_friendly": false,
    "vegetarian_support": false,
    "menus": [
      {
        "name": "Buffet Nướng Sumo",
        "description": "Menu nướng thượng hạng Nhật Bản",
        "items": [
          {
            "name": "Buffet Nướng Sumo Otoku",
            "description": "Thịt bò nướng sốt thảo mộc, sashimi cá hồi và các món nhắm izakaya",
            "price": 469000.0,
            "image_url": "https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=800"
          }
        ]
      }
    ],
    "images": [
      {
        "image_url": "https://images.unsplash.com/photo-1555396273-367ea4eb4db5?w=800",
        "caption": "Không gian sang trọng tại tòa tháp Landmark 81",
        "is_cover": true
      }
    ],
    "description": "Nhà hàng buffet nướng lẩu Nhật Bản cao cấp tại tòa nhà chọc trời Landmark 81, thưởng thức thịt bò Wagyu và hải sản không giới hạn.",
    "phone_number": "02873007393"
  },
  {
    "id": 34,
    "name": "Kichi Kichi Lẩu Băng Chuyền - Pearl Plaza",
    "address": "Tầng 4 Pearl Plaza, 561A Điện Biên Phủ, Phường 25, Quận Bình Thạnh, TP. Hồ Chí Minh",
    "lat": 10.7998,
    "lng": 106.7172,
    "category": "hotpot",
    "cuisineLabel": "Lẩu Nướng",
    "priceMin": 239000,
    "priceMax": 329000,
    "rating": 4.5,
    "reviews": 510,
    "parking": true,
    "private_room": false,
    "vegetarian": true,
    "openHours": "10:00 - 22:00",
    "image": "https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=800",
    "menu": [
      {
        "name": "Suất Buffet Lẩu Không Giới Hạn",
        "price": 279000.0
      }
    ],
    "district": "Quận Bình Thạnh",
    "has_parking": true,
    "has_private_room": false,
    "has_outdoor": false,
    "outdoor": false,
    "pet_friendly": false,
    "has_pet_friendly": false,
    "vegetarian_support": true,
    "menus": [
      {
        "name": "Buffet Lẩu Băng Chuyền",
        "description": "Lựa chọn 1 trong 4 vị nước lẩu đặc sắc",
        "items": [
          {
            "name": "Suất Buffet Lẩu Không Giới Hạn",
            "description": "Tự do gắp bò Mỹ, mực nút, tôm thẻ, cá hồi và rau nấm tươi trên băng chuyền",
            "price": 279000.0,
            "image_url": "https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=800"
          }
        ]
      }
    ],
    "images": [
      {
        "image_url": "https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=800",
        "caption": "Băng chuyền lẩu nhộn nhịp ngập tràn món nhúng tươi rói",
        "is_cover": true
      }
    ],
    "description": "Mô hình lẩu băng chuyền hiện đại chuyển động không ngừng với gần 100 món nhúng lẩu tươi ngon từ bò Mỹ đến hải sản.",
    "phone_number": "02873007994"
  },
  {
    "id": 35,
    "name": "Quán Ốc Sinh Viên - D2 (Nguyễn Gia Trí)",
    "address": "69/18 Đường D2 (Nguyễn Gia Trí), Phường 25, Quận Bình Thạnh, TP. Hồ Chí Minh",
    "lat": 10.804,
    "lng": 106.7155,
    "category": "other",
    "cuisineLabel": "Hải Sản",
    "priceMin": 40000,
    "priceMax": 120000,
    "rating": 4.4,
    "reviews": 610,
    "parking": true,
    "private_room": false,
    "vegetarian": false,
    "openHours": "15:00 - 23:30",
    "image": "https://images.unsplash.com/photo-1534422298391-e4f8c172dddb?w=800",
    "menu": [
      {
        "name": "Ốc Hương Xào Trứng Muối Kèm Bánh Mì",
        "price": 85000.0
      },
      {
        "name": "Sò Điệp Nướng Mỡ Hành Đậu Phộng",
        "price": 60000.0
      }
    ],
    "district": "Quận Bình Thạnh",
    "has_parking": true,
    "has_private_room": false,
    "has_outdoor": true,
    "outdoor": true,
    "pet_friendly": true,
    "has_pet_friendly": true,
    "vegetarian_support": false,
    "menus": [
      {
        "name": "Các Món Ốc & Sò",
        "description": "Nước sốt bánh mì chấm ăn kèm tuyệt đỉnh",
        "items": [
          {
            "name": "Ốc Hương Xào Trứng Muối Kèm Bánh Mì",
            "description": "Ốc hương giòn sần sật ngập trong sốt trứng muối béo ngậy",
            "price": 85000.0,
            "image_url": "https://images.unsplash.com/photo-1534422298391-e4f8c172dddb?w=800"
          },
          {
            "name": "Sò Điệp Nướng Mỡ Hành Đậu Phộng",
            "description": "Sò điệp béo ngọt nướng mỡ hành thơm nức mũi",
            "price": 60000.0,
            "image_url": "https://images.unsplash.com/photo-1565680018434-b513d5e5fd47?w=800"
          }
        ]
      }
    ],
    "images": [
      {
        "image_url": "https://images.unsplash.com/photo-1534422298391-e4f8c172dddb?w=800",
        "caption": "Đĩa ốc hương xào bơ tỏi thơm ngậy màu vàng ươm",
        "is_cover": true
      }
    ],
    "description": "Tụ điểm ăn ốc giá học sinh sinh viên náo nhiệt bậc nhất Bình Thạnh, nổi tiếng với các món ốc móng tay xào rau muống, ốc hương sốt trứng muối.",
    "phone_number": "0934112233"
  },
  {
    "id": 36,
    "name": "Namsan Korean BBQ - Ung Văn Khiêm",
    "address": "45 Ung Văn Khiêm, Phường 25, Quận Bình Thạnh, TP. Hồ Chí Minh",
    "lat": 10.808,
    "lng": 106.7195,
    "category": "bbq",
    "cuisineLabel": "Món Hàn",
    "priceMin": 120000,
    "priceMax": 320000,
    "rating": 4.5,
    "reviews": 420,
    "parking": true,
    "private_room": false,
    "vegetarian": false,
    "openHours": "11:00 - 22:30",
    "image": "https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=800",
    "menu": [
      {
        "name": "Ba Chỉ Heo Nướng Kim Chi Tươi",
        "price": 165000.0
      },
      {
        "name": "Cơm Trộn Thố Đá Hàn Quốc (Bibimbap)",
        "price": 95000.0
      }
    ],
    "district": "Quận Bình Thạnh",
    "has_parking": true,
    "has_private_room": false,
    "has_outdoor": false,
    "outdoor": false,
    "pet_friendly": false,
    "has_pet_friendly": false,
    "vegetarian_support": false,
    "menus": [
      {
        "name": "Thịt Nướng Xứ Hàn",
        "description": "Cuốn rau xà lách chấm sốt Ssamjang chuẩn vị",
        "items": [
          {
            "name": "Ba Chỉ Heo Nướng Kim Chi Tươi",
            "description": "Thịt heo tươi thái dày nướng giòn rụm cuốn lá kim",
            "price": 165000.0,
            "image_url": "https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=800"
          },
          {
            "name": "Cơm Trộn Thố Đá Hàn Quốc (Bibimbap)",
            "description": "Cơm trộn thịt bò băm, rau củ và trứng lòng đào sốt ớt Gochujang",
            "price": 95000.0,
            "image_url": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=800"
          }
        ]
      }
    ],
    "images": [
      {
        "image_url": "https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=800",
        "caption": "Bàn thịt nướng Hàn Quốc ngập tràn các món panchan",
        "is_cover": true
      }
    ],
    "description": "Quán nướng phong cách Hàn Quốc đường phố với thịt ba chỉ heo nướng kim chi, rượu Soju và các món panchan không giới hạn.",
    "phone_number": "02835123456"
  },
  {
    "id": 37,
    "name": "Lẩu Dê Đồng Kỵ - Nơ Trang Long",
    "address": "128 Nơ Trang Long, Phường 14, Quận Bình Thạnh, TP. Hồ Chí Minh",
    "lat": 10.8095,
    "lng": 106.698,
    "category": "hotpot",
    "cuisineLabel": "Món Việt",
    "priceMin": 100000,
    "priceMax": 280000,
    "rating": 4.4,
    "reviews": 360,
    "parking": true,
    "private_room": false,
    "vegetarian": false,
    "openHours": "10:00 - 23:00",
    "image": "https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=800",
    "menu": [
      {
        "name": "Vú Dê Nướng Chao Giòn Béo",
        "price": 175000.0
      },
      {
        "name": "Dê Hấp Lá Tía Tô",
        "price": 165000.0
      }
    ],
    "district": "Quận Bình Thạnh",
    "has_parking": true,
    "has_private_room": false,
    "has_outdoor": true,
    "outdoor": true,
    "pet_friendly": false,
    "has_pet_friendly": false,
    "vegetarian_support": false,
    "menus": [
      {
        "name": "Đặc Sản Dê Tươi",
        "description": "Các món nhậu lai rai đậm vị",
        "items": [
          {
            "name": "Vú Dê Nướng Chao Giòn Béo",
            "description": "Vú dê ướp chao nướng than hoa giòn sần sật",
            "price": 175000.0,
            "image_url": "https://images.unsplash.com/photo-1544025162-d76694265947?w=800"
          },
          {
            "name": "Dê Hấp Lá Tía Tô",
            "description": "Thịt dê ngọt thanh cuốn bánh tráng chấm tương gừng",
            "price": 165000.0,
            "image_url": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=800"
          }
        ]
      }
    ],
    "images": [
      {
        "image_url": "https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=800",
        "caption": "Đĩa vú dê nướng vàng ươm ăn cùng đậu bắp nướng",
        "is_cover": true
      }
    ],
    "description": "Quán nhậu đặc sản dê ré nổi tiếng Bình Thạnh, thịt dê tươi làm trong ngày, các món dê xào lăn, dê hấp tía tô và vú dê nướng chao.",
    "phone_number": "02835510988"
  },
  {
    "id": 38,
    "name": "The Coffee House - D2 (Nguyễn Gia Trí)",
    "address": "64 Nguyễn Gia Trí, Phường 25, Quận Bình Thạnh, TP. Hồ Chí Minh",
    "lat": 10.8028,
    "lng": 106.7138,
    "category": "other",
    "cuisineLabel": "Cà Phê & Bánh",
    "priceMin": 35000,
    "priceMax": 85000,
    "rating": 4.6,
    "reviews": 790,
    "parking": true,
    "private_room": false,
    "vegetarian": true,
    "openHours": "07:00 - 22:30",
    "image": "https://images.unsplash.com/photo-1501339847302-ac426a4a7cbb?w=800",
    "menu": [
      {
        "name": "Trà Đào Cam Sả Trứ Danh",
        "price": 55000.0
      },
      {
        "name": "Cà Phê Sữa Đá Đậm Đà",
        "price": 39000.0
      }
    ],
    "district": "Quận Bình Thạnh",
    "has_parking": true,
    "has_private_room": false,
    "has_outdoor": true,
    "outdoor": true,
    "pet_friendly": true,
    "has_pet_friendly": true,
    "vegetarian_support": true,
    "menus": [
      {
        "name": "Cà Phê & Trà Trái Cây",
        "description": "Pha chế theo công thức riêng của The Coffee House",
        "items": [
          {
            "name": "Trà Đào Cam Sả Trứ Danh",
            "description": "Hương vị sả thanh mát kết hợp cam vàng và miếng đào giòn ngọt",
            "price": 55000.0,
            "image_url": "https://images.unsplash.com/photo-1513558161293-cdaf765ed2fd?w=800"
          },
          {
            "name": "Cà Phê Sữa Đá Đậm Đà",
            "description": "Cà phê Robusta Đắk Lắk pha phin truyền thống thơm nồng",
            "price": 39000.0,
            "image_url": "https://images.unsplash.com/photo-1501339847302-ac426a4a7cbb?w=800"
          }
        ]
      }
    ],
    "images": [
      {
        "image_url": "https://images.unsplash.com/photo-1501339847302-ac426a4a7cbb?w=800",
        "caption": "Không gian quán cà phê hiện đại tràn ngập ánh sáng tự nhiên",
        "is_cover": true
      }
    ],
    "description": "Điểm hẹn cà phê hiện đại với không gian rộng rãi 3 tầng lầu, phục vụ cà phê phin Việt Nam, trà đào cam sả và bánh ngọt tươi mỗi ngày.",
    "phone_number": "18006936"
  },
  {
    "id": 39,
    "name": "The Deck Saigon - Bờ Sông Thảo Điền",
    "address": "38 Nguyễn Ư Dĩ, Phường Thảo Điền, TP. Thủ Đức, TP. Hồ Chí Minh",
    "lat": 10.8075,
    "lng": 106.735,
    "category": "western",
    "cuisineLabel": "Món Âu",
    "priceMin": 250000,
    "priceMax": 1500000,
    "rating": 4.8,
    "reviews": 980,
    "parking": true,
    "private_room": true,
    "vegetarian": true,
    "openHours": "08:00 - 23:30",
    "image": "https://images.unsplash.com/photo-1537047902294-62a40c20a6ae?w=800",
    "menu": [
      {
        "name": "Cá Hồi Na Uy Áp Chảo Sốt Miso",
        "price": 380000.0
      },
      {
        "name": "Bò Wagyu Nướng Sốt Teriyaki Nấm",
        "price": 680000.0
      }
    ],
    "district": "TP. Thủ Đức",
    "has_parking": true,
    "has_private_room": true,
    "has_outdoor": true,
    "outdoor": true,
    "pet_friendly": true,
    "has_pet_friendly": true,
    "vegetarian_support": true,
    "menus": [
      {
        "name": "Món Chính Pan-Asian Thượng Hạng",
        "description": "Kết hợp ẩm thực Á - Âu hiện đại",
        "items": [
          {
            "name": "Cá Hồi Na Uy Áp Chảo Sốt Miso",
            "description": "Cá hồi giòn da thịt ngọt mềm ăn kèm măng tây và khoai nghiền",
            "price": 380000.0,
            "image_url": "https://images.unsplash.com/photo-1519708227418-c8fd9a32b7a2?w=800"
          },
          {
            "name": "Bò Wagyu Nướng Sốt Teriyaki Nấm",
            "description": "Thịt bò Wagyu mềm thơm kết hợp sốt nấm đậm đà",
            "price": 680000.0,
            "image_url": "https://images.unsplash.com/photo-1544025162-d76694265947?w=800"
          }
        ]
      }
    ],
    "images": [
      {
        "image_url": "https://images.unsplash.com/photo-1537047902294-62a40c20a6ae?w=800",
        "caption": "Sàn gỗ ngoài trời sát bờ sông Sài Gòn lãng mạn như tranh vẽ",
        "is_cover": true
      }
    ],
    "description": "Nhà hàng phong cách Pan-Asian bên bờ sông Sài Gòn sang trọng bậc nhất Thảo Điền, ngắm hoàng hôn lộng lẫy cùng cocktail tinh tế.",
    "phone_number": "02837446632"
  },
  {
    "id": 40,
    "name": "Bụi Garden - Thảo Điền",
    "address": "55 Ngô Quang Huy, Phường Thảo Điền, TP. Thủ Đức, TP. Hồ Chí Minh",
    "lat": 10.8045,
    "lng": 106.738,
    "category": "vietnamese",
    "cuisineLabel": "Món Việt",
    "priceMin": 90000,
    "priceMax": 350000,
    "rating": 4.6,
    "reviews": 570,
    "parking": true,
    "private_room": true,
    "vegetarian": true,
    "openHours": "08:00 - 23:00",
    "image": "https://images.unsplash.com/photo-1537047902294-62a40c20a6ae?w=800",
    "menu": [
      {
        "name": "Thịt Heo Kho Trứng Nước Dừa",
        "price": 175000.0
      },
      {
        "name": "Đậu Rồng Xào Thịt Bò",
        "price": 135000.0
      }
    ],
    "district": "TP. Thủ Đức",
    "has_parking": true,
    "has_private_room": true,
    "has_outdoor": true,
    "outdoor": true,
    "pet_friendly": true,
    "has_pet_friendly": true,
    "vegetarian_support": true,
    "menus": [
      {
        "name": "Mâm Cơm Quê",
        "description": "Hương vị cơm nhà thanh nhã",
        "items": [
          {
            "name": "Thịt Heo Kho Trứng Nước Dừa",
            "description": "Thịt kho mềm rục béo ngọt nước dừa tươi Bến Tre",
            "price": 175000.0,
            "image_url": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=800"
          },
          {
            "name": "Đậu Rồng Xào Thịt Bò",
            "description": "Đậu rồng giòn ngọt xào thịt bò phi tỏi thơm phức",
            "price": 135000.0,
            "image_url": "https://images.unsplash.com/photo-1540420773420-3366772f4999?w=800"
          }
        ]
      }
    ],
    "images": [
      {
        "image_url": "https://images.unsplash.com/photo-1537047902294-62a40c20a6ae?w=800",
        "caption": "Khuôn viên vườn nhà mát rượi tại Thảo Điền",
        "is_cover": true
      }
    ],
    "description": "Khu vườn ẩm thực Việt giữa lòng Thảo Điền với hồ sen, hàng chuối và các món ăn quê nhà ba miền ấm áp nghĩa tình.",
    "phone_number": "02838989088"
  },
  {
    "id": 41,
    "name": "Hải Sản Sepia - Khổng Tử",
    "address": "01 Khổng Tử, Phường Bình Thọ, TP. Thủ Đức, TP. Hồ Chí Minh",
    "lat": 10.8465,
    "lng": 106.7712,
    "category": "other",
    "cuisineLabel": "Hải Sản",
    "priceMin": 120000,
    "priceMax": 850000,
    "rating": 4.6,
    "reviews": 690,
    "parking": true,
    "private_room": true,
    "vegetarian": false,
    "openHours": "09:30 - 23:00",
    "image": "https://images.unsplash.com/photo-1534422298391-e4f8c172dddb?w=800",
    "menu": [
      {
        "name": "Cua Huỳnh Đế Hấp Gừng Hành",
        "price": 450000.0
      },
      {
        "name": "Tôm Hùm Baby Nướng Phô Mai",
        "price": 380000.0
      }
    ],
    "district": "TP. Thủ Đức",
    "has_parking": true,
    "has_private_room": true,
    "has_outdoor": true,
    "outdoor": true,
    "pet_friendly": false,
    "has_pet_friendly": false,
    "vegetarian_support": false,
    "menus": [
      {
        "name": "Hải Sản Tươi Sống Sepia",
        "description": "Cân ký chế biến tại chỗ",
        "items": [
          {
            "name": "Cua Huỳnh Đế Hấp Gừng Hành",
            "description": "Thịt cua thơm lừng dai ngọt chấm muối tiêu chanh",
            "price": 450000.0,
            "image_url": "https://images.unsplash.com/photo-1534422298391-e4f8c172dddb?w=800"
          },
          {
            "name": "Tôm Hùm Baby Nướng Phô Mai",
            "description": "Tôm hùm baby thịt chắc nạc phủ phô mai Mozzarella đút lò",
            "price": 380000.0,
            "image_url": "https://images.unsplash.com/photo-1565680018434-b513d5e5fd47?w=800"
          }
        ]
      }
    ],
    "images": [
      {
        "image_url": "https://images.unsplash.com/photo-1534422298391-e4f8c172dddb?w=800",
        "caption": "Bể hải sản khổng lồ đa dạng sinh vật biển tươi sống",
        "is_cover": true
      }
    ],
    "description": "Thiên đường hải sản lớn bậc nhất TP. Thủ Đức với khuôn viên hơn 4000m2, hồ hải sản đa dạng tôm cua ghẹ ốc tươi rói bơi lội.",
    "phone_number": "0981100100"
  },
  {
    "id": 42,
    "name": "Lẩu Dê Năm Ri - Võ Văn Ngân",
    "address": "204 Võ Văn Ngân, Phường Bình Thọ, TP. Thủ Đức, TP. Hồ Chí Minh",
    "lat": 10.8495,
    "lng": 106.768,
    "category": "hotpot",
    "cuisineLabel": "Món Việt",
    "priceMin": 90000,
    "priceMax": 280000,
    "rating": 4.5,
    "reviews": 530,
    "parking": true,
    "private_room": false,
    "vegetarian": false,
    "openHours": "10:00 - 23:00",
    "image": "https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=800",
    "menu": [
      {
        "name": "Lẩu Thịt Dê Đùi Tươi (Nồi vừa)",
        "price": 220000.0
      },
      {
        "name": "Dê Tái Chanh Cuốn Rau Rừng",
        "price": 160000.0
      }
    ],
    "district": "TP. Thủ Đức",
    "has_parking": true,
    "has_private_room": false,
    "has_outdoor": true,
    "outdoor": true,
    "pet_friendly": false,
    "has_pet_friendly": false,
    "vegetarian_support": false,
    "menus": [
      {
        "name": "Món Dê Đặc Sản",
        "description": "Nước lẩu hầm xương dê ngọt lịm",
        "items": [
          {
            "name": "Lẩu Thịt Dê Đùi Tươi (Nồi vừa)",
            "description": "Thịt đùi dê cắt miếng dày, đậu hũ ky, khoai môn và mì trứng",
            "price": 220000.0,
            "image_url": "https://images.unsplash.com/photo-1547592180-85f173990554?w=800"
          },
          {
            "name": "Dê Tái Chanh Cuốn Rau Rừng",
            "description": "Thịt dê bóp thấu chanh chua ngọt rắc mè thơm",
            "price": 160000.0,
            "image_url": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=800"
          }
        ]
      }
    ],
    "images": [
      {
        "image_url": "https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=800",
        "caption": "Nồi lẩu dê sôi sùng sục cùng đĩa thịt dê tươi rói",
        "is_cover": true
      }
    ],
    "description": "Thương hiệu lẩu dê gia truyền hơn 30 năm tại Thủ Đức, thịt dê tươi chấm chao bùi béo kết hợp tía tô và nước lẩu ngọt đậm đà.",
    "phone_number": "02838965678"
  },
  {
    "id": 43,
    "name": "Nhà Hàng Gió & Nước - Làng Đại Học",
    "address": "Khu Đô thị ĐHQG-HCM, Phường Linh Trung, TP. Thủ Đức, TP. Hồ Chí Minh",
    "lat": 10.871,
    "lng": 106.782,
    "category": "vietnamese",
    "cuisineLabel": "Món Việt",
    "priceMin": 50000,
    "priceMax": 180000,
    "rating": 4.4,
    "reviews": 460,
    "parking": true,
    "private_room": true,
    "vegetarian": true,
    "openHours": "09:00 - 22:30",
    "image": "https://images.unsplash.com/photo-1537047902294-62a40c20a6ae?w=800",
    "menu": [
      {
        "name": "Cá Lóc Nướng Trui Rơm Cuốn Bánh Tráng",
        "price": 140000.0
      },
      {
        "name": "Gà Đồi Nướng Muối Ớt Kèm Xôi Cháy",
        "price": 195000.0
      }
    ],
    "district": "TP. Thủ Đức",
    "has_parking": true,
    "has_private_room": true,
    "has_outdoor": true,
    "outdoor": true,
    "pet_friendly": true,
    "has_pet_friendly": true,
    "vegetarian_support": true,
    "menus": [
      {
        "name": "Món Đồng Quê & Sân Vườn",
        "description": "Giá cả hợp lý cho sinh viên và nhóm bạn",
        "items": [
          {
            "name": "Cá Lóc Nướng Trui Rơm Cuốn Bánh Tráng",
            "description": "Cá lóc đồng nướng rơm nguyên con ngọt lịm chấm mắm nêm",
            "price": 140000.0,
            "image_url": "https://images.unsplash.com/photo-1519708227418-c8fd9a32b7a2?w=800"
          },
          {
            "name": "Gà Đồi Nướng Muối Ớt Kèm Xôi Cháy",
            "description": "Thịt gà chắc ngọt thơm mùi khói nướng",
            "price": 195000.0,
            "image_url": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=800"
          }
        ]
      }
    ],
    "images": [
      {
        "image_url": "https://images.unsplash.com/photo-1537047902294-62a40c20a6ae?w=800",
        "caption": "Nhà chòi ven hồ sen thoáng mát yên bình",
        "is_cover": true
      }
    ],
    "description": "Không gian sinh thái hồ sen thoáng đãng tại Làng Đại học Quốc gia, chuyên phục vụ các món cá sông, gà đồi và lẩu dân dã giá cả sinh viên.",
    "phone_number": "0903334455"
  },
  {
    "id": 44,
    "name": "Gyu-Kaku BBQ - Vincom Thảo Điền",
    "address": "Tầng 5 Vincom Mega Mall, 161 Xa Lộ Hà Nội, Phường Thảo Điền, TP. Thủ Đức, TP. Hồ Chí Minh",
    "lat": 10.802,
    "lng": 106.741,
    "category": "bbq",
    "cuisineLabel": "Lẩu Nướng",
    "priceMin": 220000,
    "priceMax": 550000,
    "rating": 4.6,
    "reviews": 410,
    "parking": true,
    "private_room": true,
    "vegetarian": false,
    "openHours": "10:30 - 22:00",
    "image": "https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=800",
    "menu": [
      {
        "name": "Thịt Dẻ Sườn Bò Mỹ Nướng Sốt Tỏi",
        "price": 185000.0
      }
    ],
    "district": "TP. Thủ Đức",
    "has_parking": true,
    "has_private_room": true,
    "has_outdoor": false,
    "outdoor": false,
    "pet_friendly": false,
    "has_pet_friendly": false,
    "vegetarian_support": false,
    "menus": [
      {
        "name": "Thịt Nướng Nhật Bản",
        "description": "Nướng than hoa không khói",
        "items": [
          {
            "name": "Thịt Dẻ Sườn Bò Mỹ Nướng Sốt Tỏi",
            "description": "Miếng dẻ sườn ướp đậm sốt tỏi cay thơm giòn",
            "price": 185000.0,
            "image_url": "https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=800"
          }
        ]
      }
    ],
    "images": [
      {
        "image_url": "https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=800",
        "caption": "Set nướng thịt bò nhập khẩu hảo hạng tại Gyu-Kaku",
        "is_cover": true
      }
    ],
    "description": "Trải nghiệm nướng Yakiniku Nhật Bản tiêu chuẩn quốc tế ngay tại trung tâm thương mại Vincom Mega Mall Thảo Điền.",
    "phone_number": "02837446688"
  },
  {
    "id": 45,
    "name": "Nấm Lẩu Dân Gian - Thảo Điền",
    "address": "14 Quốc Hương, Phường Thảo Điền, TP. Thủ Đức, TP. Hồ Chí Minh",
    "lat": 10.8015,
    "lng": 106.7325,
    "category": "hotpot",
    "cuisineLabel": "Món Chay",
    "priceMin": 120000,
    "priceMax": 380000,
    "rating": 4.7,
    "reviews": 380,
    "parking": true,
    "private_room": true,
    "vegetarian": true,
    "openHours": "10:00 - 22:00",
    "image": "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=800",
    "menu": [
      {
        "name": "Set Lẩu Nấm Dưỡng Sinh Hoàng Kim",
        "price": 280000.0
      }
    ],
    "district": "TP. Thủ Đức",
    "has_parking": true,
    "has_private_room": true,
    "has_outdoor": true,
    "outdoor": true,
    "pet_friendly": true,
    "has_pet_friendly": true,
    "vegetarian_support": true,
    "menus": [
      {
        "name": "Lẩu Nấm Thiên Nhiên",
        "description": "Nước dùng thanh tịnh hầm từ rễ cây và nấm quý",
        "items": [
          {
            "name": "Set Lẩu Nấm Dưỡng Sinh Hoàng Kim",
            "description": "Nấm tùng nhung, nấm gan bò, nấm kê tùng và mì nấm tự làm",
            "price": 280000.0,
            "image_url": "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=800"
          }
        ]
      }
    ],
    "images": [
      {
        "image_url": "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=800",
        "caption": "Thớt nấm tươi rực rỡ sắc màu bổ dưỡng cho sức khỏe",
        "is_cover": true
      }
    ],
    "description": "Nhà hàng lẩu nấm thanh tao với hơn 20 loại nấm quý tự nhiên bồi dưỡng cơ thể, không gian sân vườn xanh mát tĩnh lặng.",
    "phone_number": "02835191234"
  },
  {
    "id": 46,
    "name": "Ẩm Thực Đồng Quê - Tô Ngọc Vân",
    "address": "123 Tô Ngọc Vân, Phường Linh Tây, TP. Thủ Đức, TP. Hồ Chí Minh",
    "lat": 10.858,
    "lng": 106.757,
    "category": "vietnamese",
    "cuisineLabel": "Món Việt",
    "priceMin": 70000,
    "priceMax": 250000,
    "rating": 4.4,
    "reviews": 410,
    "parking": true,
    "private_room": true,
    "vegetarian": false,
    "openHours": "09:30 - 22:30",
    "image": "https://images.unsplash.com/photo-1519708227418-c8fd9a32b7a2?w=800",
    "menu": [
      {
        "name": "Cá Tai Tượng Chiên Xù",
        "price": 185000.0
      },
      {
        "name": "Lẩu Mắm Miền Tây Đậm Vị",
        "price": 250000.0
      }
    ],
    "district": "TP. Thủ Đức",
    "has_parking": true,
    "has_private_room": true,
    "has_outdoor": true,
    "outdoor": true,
    "pet_friendly": false,
    "has_pet_friendly": false,
    "vegetarian_support": false,
    "menus": [
      {
        "name": "Đặc Sản Miền Tây",
        "description": "Món ăn sông nước dân dã",
        "items": [
          {
            "name": "Cá Tai Tượng Chiên Xù",
            "description": "Cá chiên xù vảy giòn rụm cuốn bánh tráng chấm mắm nêm chua cay",
            "price": 185000.0,
            "image_url": "https://images.unsplash.com/photo-1519708227418-c8fd9a32b7a2?w=800"
          },
          {
            "name": "Lẩu Mắm Miền Tây Đậm Vị",
            "description": "Lẩu mắm cá linh cá sặc thơm nồng ăn cùng 10 loại rau đồng nội",
            "price": 250000.0,
            "image_url": "https://images.unsplash.com/photo-1547592180-85f173990554?w=800"
          }
        ]
      }
    ],
    "images": [
      {
        "image_url": "https://images.unsplash.com/photo-1519708227418-c8fd9a32b7a2?w=800",
        "caption": "Con cá tai tượng chiên xù vảy vàng óng ả",
        "is_cover": true
      }
    ],
    "description": "Quán ăn gia đình đậm chất miền Tây Nam Bộ tại trung tâm Thủ Đức, đặc sản cá tai tượng chiên xù và lẩu mắm đậm đà.",
    "phone_number": "02838971122"
  },
  {
    "id": 47,
    "name": "Quán Nhậu 136 - Đặng Văn Bi",
    "address": "136 Đặng Văn Bi, Phường Trường Thọ, TP. Thủ Đức, TP. Hồ Chí Minh",
    "lat": 10.8385,
    "lng": 106.762,
    "category": "vietnamese",
    "cuisineLabel": "Món Việt",
    "priceMin": 50000,
    "priceMax": 180000,
    "rating": 4.3,
    "reviews": 390,
    "parking": true,
    "private_room": false,
    "vegetarian": false,
    "openHours": "16:00 - 02:00",
    "image": "https://images.unsplash.com/photo-1544025162-d76694265947?w=800",
    "menu": [
      {
        "name": "Chảo Bò Sốt Hàu Phô Mai Cay",
        "price": 149000.0
      },
      {
        "name": "Sụn Gà Chiên Nước Mắm",
        "price": 85000.0
      }
    ],
    "district": "TP. Thủ Đức",
    "has_parking": true,
    "has_private_room": false,
    "has_outdoor": true,
    "outdoor": true,
    "pet_friendly": true,
    "has_pet_friendly": true,
    "vegetarian_support": false,
    "menus": [
      {
        "name": "Mồi Nhậu Lai Rai",
        "description": "Các món xào nướng thơm cay bắt vị",
        "items": [
          {
            "name": "Chảo Bò Sốt Hàu Phô Mai Cay",
            "description": "Thịt bò Mỹ, hàu tươi, nấm kim châm ngập trong sốt cay kéo sợi phô mai",
            "price": 149000.0,
            "image_url": "https://images.unsplash.com/photo-1544025162-d76694265947?w=800"
          },
          {
            "name": "Sụn Gà Chiên Nước Mắm",
            "description": "Sụn gà giòn sần sật bọc nước mắm tỏi ớt thơm lừng",
            "price": 85000.0,
            "image_url": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=800"
          }
        ]
      }
    ],
    "images": [
      {
        "image_url": "https://images.unsplash.com/photo-1544025162-d76694265947?w=800",
        "caption": "Chảo bò sốt hàu phô mai sôi xèo xèo hấp dẫn",
        "is_cover": true
      }
    ],
    "description": "Tụ điểm gặp gỡ bạn bè bia hơi và mồi nhậu bình dân nổi tiếng đường Đặng Văn Bi với các món bò sốt hàu, sụn gà hoàng kim giòn rụm.",
    "phone_number": "0909554433"
  },
  {
    "id": 48,
    "name": "Hủ Tiếu Mực Ông Già Cali - Thảo Điền",
    "address": "30 Trần Ngọc Diện, Phường Thảo Điền, TP. Thủ Đức, TP. Hồ Chí Minh",
    "lat": 10.8055,
    "lng": 106.7365,
    "category": "vietnamese",
    "cuisineLabel": "Món Việt",
    "priceMin": 55000,
    "priceMax": 95000,
    "rating": 4.5,
    "reviews": 460,
    "parking": true,
    "private_room": false,
    "vegetarian": false,
    "openHours": "06:30 - 22:00",
    "image": "https://images.unsplash.com/photo-1582878826629-29b7ad1cdc43?w=800",
    "menu": [
      {
        "name": "Hủ Tiếu Mực Tươi Đặc Biệt",
        "price": 79000.0
      },
      {
        "name": "Hủ Tiếu Khô Sốt Tương Cay",
        "price": 79000.0
      }
    ],
    "district": "TP. Thủ Đức",
    "has_parking": true,
    "has_private_room": false,
    "has_outdoor": true,
    "outdoor": true,
    "pet_friendly": false,
    "has_pet_friendly": false,
    "vegetarian_support": false,
    "menus": [
      {
        "name": "Hủ Tiếu Mực Nước & Khô",
        "description": "Mực trứng và mực nang tươi giòn",
        "items": [
          {
            "name": "Hủ Tiếu Mực Tươi Đặc Biệt",
            "description": "Mực tươi nguyên con, thịt viên bọc trứng cút và tôm sú tươi",
            "price": 79000.0,
            "image_url": "https://images.unsplash.com/photo-1582878826629-29b7ad1cdc43?w=800"
          },
          {
            "name": "Hủ Tiếu Khô Sốt Tương Cay",
            "description": "Sợi hủ tiếu dai trộn sốt tương đen gia truyền kèm chén súp mực riêng",
            "price": 79000.0,
            "image_url": "https://images.unsplash.com/photo-1559847844-5315695dadae?w=800"
          }
        ]
      }
    ],
    "images": [
      {
        "image_url": "https://images.unsplash.com/photo-1582878826629-29b7ad1cdc43?w=800",
        "caption": "Tô hủ tiếu mực ngập tràn mực tươi và hành phi thơm lừng",
        "is_cover": true
      }
    ],
    "description": "Thương hiệu hủ tiếu mực nổi danh đất Sài Gòn, mực tươi chong đèn dày cùi giòn ngọt sần sật, nước súp hầm mực khô thanh vị tự nhiên.",
    "phone_number": "0903099955"
  },
  {
    "id": 49,
    "name": "Bia Tuyết - Nguyễn Duy Trinh",
    "address": "285 Nguyễn Duy Trinh, Phường Bình Trưng Tây, TP. Thủ Đức, TP. Hồ Chí Minh",
    "lat": 10.789,
    "lng": 106.7625,
    "category": "other",
    "cuisineLabel": "Hải Sản",
    "priceMin": 80000,
    "priceMax": 280000,
    "rating": 4.4,
    "reviews": 320,
    "parking": true,
    "private_room": false,
    "vegetarian": false,
    "openHours": "15:00 - 23:30",
    "image": "https://images.unsplash.com/photo-1534422298391-e4f8c172dddb?w=800",
    "menu": [
      {
        "name": "Bạch Tuộc Nướng Muối Ớt Xanh",
        "price": 135000.0
      },
      {
        "name": "Lẩu Cá Bớp Nấu Măng Chua",
        "price": 210000.0
      }
    ],
    "district": "TP. Thủ Đức",
    "has_parking": true,
    "has_private_room": false,
    "has_outdoor": true,
    "outdoor": true,
    "pet_friendly": true,
    "has_pet_friendly": true,
    "vegetarian_support": false,
    "menus": [
      {
        "name": "Món Nhậu Hải Sản",
        "description": "Thưởng thức cùng bia ướp tuyết mát lạnh",
        "items": [
          {
            "name": "Bạch Tuộc Nướng Muối Ớt Xanh",
            "description": "Bạch tuộc nướng than hoa giòn dai đẫm sốt muối ớt xanh",
            "price": 135000.0,
            "image_url": "https://images.unsplash.com/photo-1534422298391-e4f8c172dddb?w=800"
          },
          {
            "name": "Lẩu Cá Bớp Nấu Măng Chua",
            "description": "Cá bớp biển tươi cắt khúc béo ngọt nấu măng chua cay nồng",
            "price": 210000.0,
            "image_url": "https://images.unsplash.com/photo-1547592180-85f173990554?w=800"
          }
        ]
      }
    ],
    "images": [
      {
        "image_url": "https://images.unsplash.com/photo-1534422298391-e4f8c172dddb?w=800",
        "caption": "Đĩa bạch tuộc nướng muối ớt cay xè lai rai cùng bia lạnh",
        "is_cover": true
      }
    ],
    "description": "Quán hải sản và bia tuyết mát lạnh nổi tiếng tại khu vực Bình Trưng Tây, không gian sân thượng thoáng đãng view ngắm đường phố về đêm.",
    "phone_number": "0937665544"
  },
  {
    "id": 50,
    "name": "Quán Nướng Yummy Yummy - Hoàng Diệu 2",
    "address": "78 Hoàng Diệu 2, Phường Linh Trung, TP. Thủ Đức, TP. Hồ Chí Minh",
    "lat": 10.853,
    "lng": 106.7725,
    "category": "bbq",
    "cuisineLabel": "Lẩu Nướng",
    "priceMin": 139000,
    "priceMax": 219000,
    "rating": 4.3,
    "reviews": 580,
    "parking": true,
    "private_room": false,
    "vegetarian": false,
    "openHours": "16:00 - 23:00",
    "image": "https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=800",
    "menu": [
      {
        "name": "Vé Buffet Nướng Thả Ga",
        "price": 169000.0
      }
    ],
    "district": "TP. Thủ Đức",
    "has_parking": true,
    "has_private_room": false,
    "has_outdoor": true,
    "outdoor": true,
    "pet_friendly": true,
    "has_pet_friendly": true,
    "vegetarian_support": false,
    "menus": [
      {
        "name": "Buffet Nướng Sinh Viên",
        "description": "Ăn thả ga thịt nướng và tráng miệng",
        "items": [
          {
            "name": "Vé Buffet Nướng Thả Ga",
            "description": "Tự chọn ba chỉ bò, dồi sụn, tôm nướng, hàu nướng mỡ hành và quầy tráng miệng",
            "price": 169000.0,
            "image_url": "https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=800"
          }
        ]
      }
    ],
    "images": [
      {
        "image_url": "https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=800",
        "caption": "Không gian quán nướng nhộn nhịp đông vui vào mỗi buổi tối",
        "is_cover": true
      }
    ],
    "description": "Tụ điểm buffet nướng lẩu sinh viên nhộn nhịp bậc nhất Thủ Đức trên phố ẩm thực Hoàng Diệu 2, thực đơn đa dạng hơn 50 món nướng tự chọn.",
    "phone_number": "0988771122"
  }
];