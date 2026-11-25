// Dữ liệu 110 nhà hàng toàn khu vực TP.HCM (110 ảnh đại diện riêng biệt)
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
    "image": "https://images.unsplash.com/photo-1513104890138-7c749659a591?w=800",
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
        "image_url": "https://images.unsplash.com/photo-1513104890138-7c749659a591?w=800",
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
    "image": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=800",
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
        "image_url": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=800",
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
    "image": "https://images.unsplash.com/photo-1559847844-5315695dadae?w=800",
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
        "image_url": "https://images.unsplash.com/photo-1559847844-5315695dadae?w=800",
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
    "image": "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=800",
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
        "image_url": "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=800",
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
    "image": "https://images.unsplash.com/photo-1509440159596-0249088772ff?w=800",
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
        "image_url": "https://images.unsplash.com/photo-1509440159596-0249088772ff?w=800",
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
    "image": "https://images.unsplash.com/photo-1547592180-85f173990554?w=800",
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
        "image_url": "https://images.unsplash.com/photo-1547592180-85f173990554?w=800",
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
    "image": "https://images.unsplash.com/photo-1503764654157-72d979d9af2f?w=800",
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
        "image_url": "https://images.unsplash.com/photo-1503764654157-72d979d9af2f?w=800",
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
    "image": "https://images.unsplash.com/photo-1541544741938-0af808871cc0?w=800",
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
        "image_url": "https://images.unsplash.com/photo-1541544741938-0af808871cc0?w=800",
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
    "image": "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=800",
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
        "image_url": "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=800",
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
    "image": "https://images.unsplash.com/photo-1569718212165-3a8278d5f624?w=800",
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
        "image_url": "https://images.unsplash.com/photo-1569718212165-3a8278d5f624?w=800",
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
    "image": "https://images.unsplash.com/photo-1540420773420-3366772f4999?w=800",
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
        "image_url": "https://images.unsplash.com/photo-1540420773420-3366772f4999?w=800",
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
    "image": "https://images.unsplash.com/photo-1565680018434-b513d5e5fd47?w=800",
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
        "image_url": "https://images.unsplash.com/photo-1565680018434-b513d5e5fd47?w=800",
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
    "image": "https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=800",
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
        "image_url": "https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=800",
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
    "image": "https://images.unsplash.com/photo-1563245372-f21724e3856d?w=800",
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
        "image_url": "https://images.unsplash.com/photo-1563245372-f21724e3856d?w=800",
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
    "image": "https://images.unsplash.com/photo-1558030006-450675393462?w=800",
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
        "image_url": "https://images.unsplash.com/photo-1558030006-450675393462?w=800",
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
    "image": "https://images.unsplash.com/photo-1529193591184-b1d58069ecdd?w=800",
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
        "image_url": "https://images.unsplash.com/photo-1529193591184-b1d58069ecdd?w=800",
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
    "image": "https://images.unsplash.com/photo-1518492104633-130d0cc84637?w=800",
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
        "image_url": "https://images.unsplash.com/photo-1518492104633-130d0cc84637?w=800",
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
    "image": "https://images.unsplash.com/photo-1504754524776-8f4f37790ca0?w=800",
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
        "image_url": "https://images.unsplash.com/photo-1504754524776-8f4f37790ca0?w=800",
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
    "image": "https://images.unsplash.com/photo-1543353071-873f17a7a088?w=800",
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
        "image_url": "https://images.unsplash.com/photo-1543353071-873f17a7a088?w=800",
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
    "image": "https://images.unsplash.com/photo-1519708227418-c8fd9a32b7a2?w=800",
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
        "image_url": "https://images.unsplash.com/photo-1519708227418-c8fd9a32b7a2?w=800",
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
    "image": "https://images.unsplash.com/photo-1529692236671-f1f6cf9683ba?w=800",
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
        "image_url": "https://images.unsplash.com/photo-1529692236671-f1f6cf9683ba?w=800",
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
    "image": "https://images.unsplash.com/photo-1555126634-323283e090fa?w=800",
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
        "image_url": "https://images.unsplash.com/photo-1555126634-323283e090fa?w=800",
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
    "image": "https://images.unsplash.com/photo-1514933651103-005eec06c04b?w=800",
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
        "image_url": "https://images.unsplash.com/photo-1514933651103-005eec06c04b?w=800",
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
    "image": "https://images.unsplash.com/photo-1553621042-f6e147245754?w=800",
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
        "image_url": "https://images.unsplash.com/photo-1553621042-f6e147245754?w=800",
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
    "image": "https://images.unsplash.com/photo-1559339352-11d035aa65de?w=800",
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
        "image_url": "https://images.unsplash.com/photo-1559339352-11d035aa65de?w=800",
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
    "image": "https://images.unsplash.com/photo-1590301157890-4815ed356275?w=800",
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
        "image_url": "https://images.unsplash.com/photo-1590301157890-4815ed356275?w=800",
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
    "image": "https://images.unsplash.com/photo-1541696432-82c6da8ce7bf?w=800",
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
        "image_url": "https://images.unsplash.com/photo-1541696432-82c6da8ce7bf?w=800",
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
    "image": "https://images.unsplash.com/photo-1559329007-40df8a9345d8?w=800",
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
        "image_url": "https://images.unsplash.com/photo-1559329007-40df8a9345d8?w=800",
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
    "image": "https://images.unsplash.com/photo-1551218808-94e220e084d2?w=800",
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
        "image_url": "https://images.unsplash.com/photo-1551218808-94e220e084d2?w=800",
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
    "image": "https://images.unsplash.com/photo-1615141982883-c7ad0e69fd62?w=800",
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
        "image_url": "https://images.unsplash.com/photo-1615141982883-c7ad0e69fd62?w=800",
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
    "image": "https://images.unsplash.com/photo-1534939561126-855b8675edd7?w=800",
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
        "image_url": "https://images.unsplash.com/photo-1534939561126-855b8675edd7?w=800",
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
    "image": "https://images.unsplash.com/photo-1414235077428-338989a2e8c0?w=800",
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
        "image_url": "https://images.unsplash.com/photo-1414235077428-338989a2e8c0?w=800",
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
    "image": "https://images.unsplash.com/photo-1611143669185-af224c5e3252?w=800",
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
        "image_url": "https://images.unsplash.com/photo-1611143669185-af224c5e3252?w=800",
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
    "image": "https://images.unsplash.com/photo-1498837167922-ddd27525d352?w=800",
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
        "image_url": "https://images.unsplash.com/photo-1498837167922-ddd27525d352?w=800",
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
    "image": "https://images.unsplash.com/photo-1476224203421-9ac39bcb3327?w=800",
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
        "image_url": "https://images.unsplash.com/photo-1476224203421-9ac39bcb3327?w=800",
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
    "image": "https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?w=800",
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
        "image_url": "https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?w=800",
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
    "image": "https://images.unsplash.com/photo-1617196034796-73dfa7b1fd56?w=800",
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
        "image_url": "https://images.unsplash.com/photo-1617196034796-73dfa7b1fd56?w=800",
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
    "image": "https://images.unsplash.com/photo-1574071318508-1cdbab80d002?w=800",
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
        "image_url": "https://images.unsplash.com/photo-1574071318508-1cdbab80d002?w=800",
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
    "image": "https://images.unsplash.com/photo-1621996346565-e3d5d6281724?w=800",
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
        "image_url": "https://images.unsplash.com/photo-1621996346565-e3d5d6281724?w=800",
        "caption": "Không gian quán nướng nhộn nhịp đông vui vào mỗi buổi tối",
        "is_cover": true
      }
    ],
    "description": "Tụ điểm buffet nướng lẩu sinh viên nhộn nhịp bậc nhất Thủ Đức trên phố ẩm thực Hoàng Diệu 2, thực đơn đa dạng hơn 50 món nướng tự chọn.",
    "phone_number": "0988771122"
  },
  {
    "id": 51,
    "name": "GoGi House - Quang Trung Gò Vấp",
    "address": "189 Quang Trung, Phường 10, Quận Gò Vấp, TP. Hồ Chí Minh",
    "lat": 10.8295,
    "lng": 106.6728,
    "category": "bbq",
    "cuisineLabel": "Lẩu Nướng",
    "priceMin": 199000,
    "priceMax": 389000,
    "rating": 4.7,
    "reviews": 540,
    "parking": true,
    "private_room": true,
    "vegetarian": false,
    "openHours": "10:00 - 22:00",
    "image": "https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=800&q=80&auto=format&fit=crop&sig=51",
    "menu": [
      {
        "name": "Dẻ Sườn Bò Mỹ Sốt Galbi",
        "price": 219000.0
      },
      {
        "name": "Ba Chỉ Bò Mỹ Cuộn Nấm",
        "price": 169000.0
      }
    ],
    "district": "Quận Gò Vấp",
    "has_parking": true,
    "has_private_room": true,
    "has_outdoor": false,
    "outdoor": false,
    "pet_friendly": false,
    "has_pet_friendly": false,
    "vegetarian_support": false,
    "menus": [
      {
        "name": "Món Đặc Trưng",
        "description": "Các món nổi bật nhất tại GoGi House - Quang Trung Gò Vấp",
        "items": [
          {
            "name": "Dẻ Sườn Bò Mỹ Sốt Galbi",
            "description": "Món bán chạy hàng đầu tại GoGi House - Quang Trung Gò Vấp",
            "price": 219000.0,
            "image_url": "https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=800&q=80&auto=format&fit=crop&sig=51"
          },
          {
            "name": "Ba Chỉ Bò Mỹ Cuộn Nấm",
            "description": "Hương vị đặc sắc được thực khách yêu thích",
            "price": 169000.0,
            "image_url": "https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=800&q=80&auto=format&fit=crop&sig=51"
          }
        ]
      }
    ],
    "images": [
      {
        "image_url": "https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=800&q=80&auto=format&fit=crop&sig=51",
        "caption": "Không gian và món ngon tại GoGi House - Quang Trung Gò Vấp",
        "is_cover": true
      }
    ],
    "description": "Thịt nướng Hàn Quốc chuẩn vị Seoul tại trung tâm Gò Vấp, không gian rộng rãi cho gia đình và nhóm bạn.",
    "phone_number": "02873007381"
  },
  {
    "id": 52,
    "name": "Lẩu Nấm Ashima - Phan Văn Trị",
    "address": "366 Phan Văn Trị, Phường 5, Quận Gò Vấp, TP. Hồ Chí Minh",
    "lat": 10.8214,
    "lng": 106.6915,
    "category": "bbq",
    "cuisineLabel": "Lẩu Nướng",
    "priceMin": 250000,
    "priceMax": 480000,
    "rating": 4.8,
    "reviews": 410,
    "parking": true,
    "private_room": true,
    "vegetarian": true,
    "openHours": "10:30 - 22:00",
    "image": "https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=800&q=80&auto=format&fit=crop&sig=52",
    "menu": [
      {
        "name": "Set Lẩu Nấm Thiên Nhiên",
        "price": 340000.0
      },
      {
        "name": "Nấm Tùng Nhung Tươi",
        "price": 155000.0
      }
    ],
    "district": "Quận Gò Vấp",
    "has_parking": true,
    "has_private_room": true,
    "has_outdoor": true,
    "outdoor": true,
    "pet_friendly": false,
    "has_pet_friendly": false,
    "vegetarian_support": true,
    "menus": [
      {
        "name": "Món Đặc Trưng",
        "description": "Các món nổi bật nhất tại Lẩu Nấm Ashima - Phan Văn Trị",
        "items": [
          {
            "name": "Set Lẩu Nấm Thiên Nhiên",
            "description": "Món bán chạy hàng đầu tại Lẩu Nấm Ashima - Phan Văn Trị",
            "price": 340000.0,
            "image_url": "https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=800&q=80&auto=format&fit=crop&sig=52"
          },
          {
            "name": "Nấm Tùng Nhung Tươi",
            "description": "Hương vị đặc sắc được thực khách yêu thích",
            "price": 155000.0,
            "image_url": "https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=800&q=80&auto=format&fit=crop&sig=52"
          }
        ]
      }
    ],
    "images": [
      {
        "image_url": "https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=800&q=80&auto=format&fit=crop&sig=52",
        "caption": "Không gian và món ngon tại Lẩu Nấm Ashima - Phan Văn Trị",
        "is_cover": true
      }
    ],
    "description": "Lẩu nấm thiên nhiên thanh ngọt với hơn 20 loại nấm quý bổ dưỡng, có phòng riêng sang trọng.",
    "phone_number": "02873007312"
  },
  {
    "id": 53,
    "name": "Hải Sản Biển Đông - Lê Văn Thọ",
    "address": "412 Lê Văn Thọ, Phường 11, Quận Gò Vấp, TP. Hồ Chí Minh",
    "lat": 10.8415,
    "lng": 106.6598,
    "category": "other",
    "cuisineLabel": "Hải Sản",
    "priceMin": 150000,
    "priceMax": 450000,
    "rating": 4.5,
    "reviews": 320,
    "parking": true,
    "private_room": true,
    "vegetarian": false,
    "openHours": "10:00 - 23:00",
    "image": "https://images.unsplash.com/photo-1567620905732-2d1ec7ab7445?w=800",
    "menu": [
      {
        "name": "Cua Cà Mau Rang Me",
        "price": 320000.0
      },
      {
        "name": "Tôm Sú Nướng Muối Ớt",
        "price": 240000.0
      }
    ],
    "district": "Quận Gò Vấp",
    "has_parking": true,
    "has_private_room": true,
    "has_outdoor": true,
    "outdoor": true,
    "pet_friendly": false,
    "has_pet_friendly": false,
    "vegetarian_support": false,
    "menus": [
      {
        "name": "Món Đặc Trưng",
        "description": "Các món nổi bật nhất tại Hải Sản Biển Đông - Lê Văn Thọ",
        "items": [
          {
            "name": "Cua Cà Mau Rang Me",
            "description": "Món bán chạy hàng đầu tại Hải Sản Biển Đông - Lê Văn Thọ",
            "price": 320000.0,
            "image_url": "https://images.unsplash.com/photo-1567620905732-2d1ec7ab7445?w=800"
          },
          {
            "name": "Tôm Sú Nướng Muối Ớt",
            "description": "Hương vị đặc sắc được thực khách yêu thích",
            "price": 240000.0,
            "image_url": "https://images.unsplash.com/photo-1567620905732-2d1ec7ab7445?w=800"
          }
        ]
      }
    ],
    "images": [
      {
        "image_url": "https://images.unsplash.com/photo-1567620905732-2d1ec7ab7445?w=800",
        "caption": "Không gian và món ngon tại Hải Sản Biển Đông - Lê Văn Thọ",
        "is_cover": true
      }
    ],
    "description": "Hải sản tươi sống bắt tại bể, giá bình dân phục vụ các món nướng, hấp, rang me đậm vị.",
    "phone_number": "02839961234"
  },
  {
    "id": 54,
    "name": "Cơm Tấm Cali - Thống Nhất",
    "address": "245 Thống Nhất, Phường 16, Quận Gò Vấp, TP. Hồ Chí Minh",
    "lat": 10.8386,
    "lng": 106.665,
    "category": "vietnamese",
    "cuisineLabel": "Cơm tấm",
    "priceMin": 55000,
    "priceMax": 115000,
    "rating": 4.4,
    "reviews": 290,
    "parking": true,
    "private_room": false,
    "vegetarian": false,
    "openHours": "07:00 - 21:30",
    "image": "https://images.unsplash.com/photo-1565958011703-44f9829ba187?w=800",
    "menu": [
      {
        "name": "Cơm Tấm Sườn Bì Chả",
        "price": 79000.0
      },
      {
        "name": "Cơm Tấm Sườn Non Nướng",
        "price": 95000.0
      }
    ],
    "district": "Quận Gò Vấp",
    "has_parking": true,
    "has_private_room": false,
    "has_outdoor": false,
    "outdoor": false,
    "pet_friendly": false,
    "has_pet_friendly": false,
    "vegetarian_support": false,
    "menus": [
      {
        "name": "Món Đặc Trưng",
        "description": "Các món nổi bật nhất tại Cơm Tấm Cali - Thống Nhất",
        "items": [
          {
            "name": "Cơm Tấm Sườn Bì Chả",
            "description": "Món bán chạy hàng đầu tại Cơm Tấm Cali - Thống Nhất",
            "price": 79000.0,
            "image_url": "https://images.unsplash.com/photo-1565958011703-44f9829ba187?w=800"
          },
          {
            "name": "Cơm Tấm Sườn Non Nướng",
            "description": "Hương vị đặc sắc được thực khách yêu thích",
            "price": 95000.0,
            "image_url": "https://images.unsplash.com/photo-1565958011703-44f9829ba187?w=800"
          }
        ]
      }
    ],
    "images": [
      {
        "image_url": "https://images.unsplash.com/photo-1565958011703-44f9829ba187?w=800",
        "caption": "Không gian và món ngon tại Cơm Tấm Cali - Thống Nhất",
        "is_cover": true
      }
    ],
    "description": "Cơm tấm sườn nướng cháy cạnh sạch sẽ, máy lạnh mát mẻ trên trục đường Thống Nhất.",
    "phone_number": "02838945566"
  },
  {
    "id": 55,
    "name": "Quán Chay Tâm An - Nguyễn Oanh",
    "address": "158 Nguyễn Oanh, Phường 17, Quận Gò Vấp, TP. Hồ Chí Minh",
    "lat": 10.8342,
    "lng": 106.6789,
    "category": "vegetarian",
    "cuisineLabel": "Món Chay",
    "priceMin": 45000,
    "priceMax": 140000,
    "rating": 4.6,
    "reviews": 260,
    "parking": true,
    "private_room": false,
    "vegetarian": true,
    "openHours": "07:00 - 21:00",
    "image": "https://images.unsplash.com/photo-1482049016688-2d3e1b311543?w=800",
    "menu": [
      {
        "name": "Lẩu Thái Chay Nấm Rừng",
        "price": 135000.0
      },
      {
        "name": "Cơm Chiên Lá É Chay",
        "price": 55000.0
      }
    ],
    "district": "Quận Gò Vấp",
    "has_parking": true,
    "has_private_room": false,
    "has_outdoor": true,
    "outdoor": true,
    "pet_friendly": false,
    "has_pet_friendly": false,
    "vegetarian_support": true,
    "menus": [
      {
        "name": "Món Đặc Trưng",
        "description": "Các món nổi bật nhất tại Quán Chay Tâm An - Nguyễn Oanh",
        "items": [
          {
            "name": "Lẩu Thái Chay Nấm Rừng",
            "description": "Món bán chạy hàng đầu tại Quán Chay Tâm An - Nguyễn Oanh",
            "price": 135000.0,
            "image_url": "https://images.unsplash.com/photo-1482049016688-2d3e1b311543?w=800"
          },
          {
            "name": "Cơm Chiên Lá É Chay",
            "description": "Hương vị đặc sắc được thực khách yêu thích",
            "price": 55000.0,
            "image_url": "https://images.unsplash.com/photo-1482049016688-2d3e1b311543?w=800"
          }
        ]
      }
    ],
    "images": [
      {
        "image_url": "https://images.unsplash.com/photo-1482049016688-2d3e1b311543?w=800",
        "caption": "Không gian và món ngon tại Quán Chay Tâm An - Nguyễn Oanh",
        "is_cover": true
      }
    ],
    "description": "Không gian chay thanh tịnh, thực đơn cơm chay và lẩu nấm giá hợp lý cho mọi lứa tuổi.",
    "phone_number": "0908112244"
  },
  {
    "id": 56,
    "name": "Cà Phê Country House - Phan Văn Trị",
    "address": "18C Phan Văn Trị, Phường 10, Quận Gò Vấp, TP. Hồ Chí Minh",
    "lat": 10.831,
    "lng": 106.679,
    "category": "other",
    "cuisineLabel": "Cà Phê & Bánh",
    "priceMin": 45000,
    "priceMax": 95000,
    "rating": 4.6,
    "reviews": 890,
    "parking": true,
    "private_room": false,
    "vegetarian": true,
    "openHours": "07:00 - 23:00",
    "image": "https://images.unsplash.com/photo-1484723091739-30a097e8f929?w=800",
    "menu": [
      {
        "name": "Trà Vải Hoa Hồng",
        "price": 62000.0
      },
      {
        "name": "Cà Phê Kem Muối",
        "price": 55000.0
      }
    ],
    "district": "Quận Gò Vấp",
    "has_parking": true,
    "has_private_room": false,
    "has_outdoor": true,
    "outdoor": true,
    "pet_friendly": true,
    "has_pet_friendly": true,
    "vegetarian_support": true,
    "menus": [
      {
        "name": "Món Đặc Trưng",
        "description": "Các món nổi bật nhất tại Cà Phê Country House - Phan Văn Trị",
        "items": [
          {
            "name": "Trà Vải Hoa Hồng",
            "description": "Món bán chạy hàng đầu tại Cà Phê Country House - Phan Văn Trị",
            "price": 62000.0,
            "image_url": "https://images.unsplash.com/photo-1484723091739-30a097e8f929?w=800"
          },
          {
            "name": "Cà Phê Kem Muối",
            "description": "Hương vị đặc sắc được thực khách yêu thích",
            "price": 55000.0,
            "image_url": "https://images.unsplash.com/photo-1484723091739-30a097e8f929?w=800"
          }
        ]
      }
    ],
    "images": [
      {
        "image_url": "https://images.unsplash.com/photo-1484723091739-30a097e8f929?w=800",
        "caption": "Không gian và món ngon tại Cà Phê Country House - Phan Văn Trị",
        "is_cover": true
      }
    ],
    "description": "Quán cà phê sân vườn phong cách đồng quê châu Âu rộng lớn nổi tiếng bậc nhất Gò Vấp.",
    "phone_number": "02838942255"
  },
  {
    "id": 57,
    "name": "Bò Né 3 Ngon - Phan Xích Long",
    "address": "142 Phan Xích Long, Phường 2, Quận Phú Nhuận, TP. Hồ Chí Minh",
    "lat": 10.7995,
    "lng": 106.6885,
    "category": "vietnamese",
    "cuisineLabel": "Món Việt",
    "priceMin": 50000,
    "priceMax": 120000,
    "rating": 4.5,
    "reviews": 480,
    "parking": true,
    "private_room": false,
    "vegetarian": false,
    "openHours": "07:00 - 22:00",
    "image": "https://images.unsplash.com/photo-1473093295043-cdd812d0e601?w=800",
    "menu": [
      {
        "name": "Bò Né Đặc Biệt Full Topping",
        "price": 85000.0
      },
      {
        "name": "Bò Lúc Lắc Khoai Tây",
        "price": 95000.0
      }
    ],
    "district": "Quận Phú Nhuận",
    "has_parking": true,
    "has_private_room": false,
    "has_outdoor": false,
    "outdoor": false,
    "pet_friendly": false,
    "has_pet_friendly": false,
    "vegetarian_support": false,
    "menus": [
      {
        "name": "Món Đặc Trưng",
        "description": "Các món nổi bật nhất tại Bò Né 3 Ngon - Phan Xích Long",
        "items": [
          {
            "name": "Bò Né Đặc Biệt Full Topping",
            "description": "Món bán chạy hàng đầu tại Bò Né 3 Ngon - Phan Xích Long",
            "price": 85000.0,
            "image_url": "https://images.unsplash.com/photo-1473093295043-cdd812d0e601?w=800"
          },
          {
            "name": "Bò Lúc Lắc Khoai Tây",
            "description": "Hương vị đặc sắc được thực khách yêu thích",
            "price": 95000.0,
            "image_url": "https://images.unsplash.com/photo-1473093295043-cdd812d0e601?w=800"
          }
        ]
      }
    ],
    "images": [
      {
        "image_url": "https://images.unsplash.com/photo-1473093295043-cdd812d0e601?w=800",
        "caption": "Không gian và món ngon tại Bò Né 3 Ngon - Phan Xích Long",
        "is_cover": true
      }
    ],
    "description": "Chảo bò né nóng hổi xèo xèo cùng pate, trứng ốp la và bánh mì giòn rụm trên phố ẩm thực Phan Xích Long.",
    "phone_number": "02835171122"
  },
  {
    "id": 58,
    "name": "Sushi Kei - Phan Xích Long",
    "address": "210 Phan Xích Long, Phường 2, Quận Phú Nhuận, TP. Hồ Chí Minh",
    "lat": 10.8008,
    "lng": 106.6892,
    "category": "japanese",
    "cuisineLabel": "Món Nhật",
    "priceMin": 150000,
    "priceMax": 450000,
    "rating": 4.7,
    "reviews": 510,
    "parking": true,
    "private_room": true,
    "vegetarian": true,
    "openHours": "10:30 - 22:00",
    "image": "https://images.unsplash.com/photo-1490645935967-10de6ba17061?w=800",
    "menu": [
      {
        "name": "Sashimi Cá Hồi Tươi",
        "price": 175000.0
      },
      {
        "name": "Cơm Lươn Nhật Nướng",
        "price": 195000.0
      }
    ],
    "district": "Quận Phú Nhuận",
    "has_parking": true,
    "has_private_room": true,
    "has_outdoor": false,
    "outdoor": false,
    "pet_friendly": false,
    "has_pet_friendly": false,
    "vegetarian_support": true,
    "menus": [
      {
        "name": "Món Đặc Trưng",
        "description": "Các món nổi bật nhất tại Sushi Kei - Phan Xích Long",
        "items": [
          {
            "name": "Sashimi Cá Hồi Tươi",
            "description": "Món bán chạy hàng đầu tại Sushi Kei - Phan Xích Long",
            "price": 175000.0,
            "image_url": "https://images.unsplash.com/photo-1490645935967-10de6ba17061?w=800"
          },
          {
            "name": "Cơm Lươn Nhật Nướng",
            "description": "Hương vị đặc sắc được thực khách yêu thích",
            "price": 195000.0,
            "image_url": "https://images.unsplash.com/photo-1490645935967-10de6ba17061?w=800"
          }
        ]
      }
    ],
    "images": [
      {
        "image_url": "https://images.unsplash.com/photo-1490645935967-10de6ba17061?w=800",
        "caption": "Không gian và món ngon tại Sushi Kei - Phan Xích Long",
        "is_cover": true
      }
    ],
    "description": "Nhà hàng Nhật Bản với sashimi cá hồi tươi sống và các set cơm lươn nướng đậm đà.",
    "phone_number": "02873001188"
  },
  {
    "id": 59,
    "name": "Chay Bồ Đề Ngọc Xanh - Huỳnh Văn Bánh",
    "address": "195 Huỳnh Văn Bánh, Phường 12, Quận Phú Nhuận, TP. Hồ Chí Minh",
    "lat": 10.7945,
    "lng": 106.6752,
    "category": "vegetarian",
    "cuisineLabel": "Món Chay",
    "priceMin": 55000,
    "priceMax": 180000,
    "rating": 4.7,
    "reviews": 340,
    "parking": true,
    "private_room": true,
    "vegetarian": true,
    "openHours": "08:00 - 21:30",
    "image": "https://images.unsplash.com/photo-1493770348161-369560ae357d?w=800",
    "menu": [
      {
        "name": "Gỏi Ngó Sen Chay",
        "price": 75000.0
      },
      {
        "name": "Lẩu Nấm Trường Thọ",
        "price": 175000.0
      }
    ],
    "district": "Quận Phú Nhuận",
    "has_parking": true,
    "has_private_room": true,
    "has_outdoor": true,
    "outdoor": true,
    "pet_friendly": false,
    "has_pet_friendly": false,
    "vegetarian_support": true,
    "menus": [
      {
        "name": "Món Đặc Trưng",
        "description": "Các món nổi bật nhất tại Chay Bồ Đề Ngọc Xanh - Huỳnh Văn Bánh",
        "items": [
          {
            "name": "Gỏi Ngó Sen Chay",
            "description": "Món bán chạy hàng đầu tại Chay Bồ Đề Ngọc Xanh - Huỳnh Văn Bánh",
            "price": 75000.0,
            "image_url": "https://images.unsplash.com/photo-1493770348161-369560ae357d?w=800"
          },
          {
            "name": "Lẩu Nấm Trường Thọ",
            "description": "Hương vị đặc sắc được thực khách yêu thích",
            "price": 175000.0,
            "image_url": "https://images.unsplash.com/photo-1493770348161-369560ae357d?w=800"
          }
        ]
      }
    ],
    "images": [
      {
        "image_url": "https://images.unsplash.com/photo-1493770348161-369560ae357d?w=800",
        "caption": "Không gian và món ngon tại Chay Bồ Đề Ngọc Xanh - Huỳnh Văn Bánh",
        "is_cover": true
      }
    ],
    "description": "Ẩm thực chay thực dưỡng tinh tế, không bột ngọt, phục vụ lẩu nấm và các món cuốn thanh đạm.",
    "phone_number": "02838445566"
  },
  {
    "id": 60,
    "name": "Phở Phú Vương - Lê Văn Sỹ",
    "address": "339 Lê Văn Sỹ, Phường 1, Quận Tân Bình",
    "lat": 10.7928,
    "lng": 106.6695,
    "category": "vietnamese",
    "cuisineLabel": "Món Việt",
    "priceMin": 65000,
    "priceMax": 105000,
    "rating": 4.6,
    "reviews": 720,
    "parking": true,
    "private_room": false,
    "vegetarian": false,
    "openHours": "06:00 - 22:30",
    "image": "https://images.unsplash.com/photo-1499028344343-cd173ffc68a9?w=800",
    "menu": [
      {
        "name": "Phở Tái Nạm Gầu",
        "price": 80000.0
      },
      {
        "name": "Phở Đặc Biệt Tô Lớn",
        "price": 100000.0
      }
    ],
    "district": "Quận Phú Nhuận",
    "has_parking": true,
    "has_private_room": false,
    "has_outdoor": false,
    "outdoor": false,
    "pet_friendly": false,
    "has_pet_friendly": false,
    "vegetarian_support": false,
    "menus": [
      {
        "name": "Món Đặc Trưng",
        "description": "Các món nổi bật nhất tại Phở Phú Vương - Lê Văn Sỹ",
        "items": [
          {
            "name": "Phở Tái Nạm Gầu",
            "description": "Món bán chạy hàng đầu tại Phở Phú Vương - Lê Văn Sỹ",
            "price": 80000.0,
            "image_url": "https://images.unsplash.com/photo-1499028344343-cd173ffc68a9?w=800"
          },
          {
            "name": "Phở Đặc Biệt Tô Lớn",
            "description": "Hương vị đặc sắc được thực khách yêu thích",
            "price": 100000.0,
            "image_url": "https://images.unsplash.com/photo-1499028344343-cd173ffc68a9?w=800"
          }
        ]
      }
    ],
    "images": [
      {
        "image_url": "https://images.unsplash.com/photo-1499028344343-cd173ffc68a9?w=800",
        "caption": "Không gian và món ngon tại Phở Phú Vương - Lê Văn Sỹ",
        "is_cover": true
      }
    ],
    "description": "Tô phở bò nước dùng đậm vị miền Nam, thịt bò tái nạm gầu mềm ngọt nổi tiếng khu Lê Văn Sỹ.",
    "phone_number": "02838443322"
  },
  {
    "id": 61,
    "name": "KPub Korean BBQ - Phan Xích Long",
    "address": "134 Phan Xích Long, Phường 7, Quận Phú Nhuận, TP. Hồ Chí Minh",
    "lat": 10.7988,
    "lng": 106.6878,
    "category": "other",
    "cuisineLabel": "Món Hàn",
    "priceMin": 229000,
    "priceMax": 399000,
    "rating": 4.6,
    "reviews": 430,
    "parking": true,
    "private_room": false,
    "vegetarian": false,
    "openHours": "10:00 - 22:30",
    "image": "https://images.unsplash.com/photo-1506354666786-959d6d497f1a?w=800",
    "menu": [
      {
        "name": "Buffet Nướng Thùng Phuy",
        "price": 299000.0
      },
      {
        "name": "Sườn Bò Hoàng Đế",
        "price": 249000.0
      }
    ],
    "district": "Quận Phú Nhuận",
    "has_parking": true,
    "has_private_room": false,
    "has_outdoor": true,
    "outdoor": true,
    "pet_friendly": false,
    "has_pet_friendly": false,
    "vegetarian_support": false,
    "menus": [
      {
        "name": "Món Đặc Trưng",
        "description": "Các món nổi bật nhất tại KPub Korean BBQ - Phan Xích Long",
        "items": [
          {
            "name": "Buffet Nướng Thùng Phuy",
            "description": "Món bán chạy hàng đầu tại KPub Korean BBQ - Phan Xích Long",
            "price": 299000.0,
            "image_url": "https://images.unsplash.com/photo-1506354666786-959d6d497f1a?w=800"
          },
          {
            "name": "Sườn Bò Hoàng Đế",
            "description": "Hương vị đặc sắc được thực khách yêu thích",
            "price": 249000.0,
            "image_url": "https://images.unsplash.com/photo-1506354666786-959d6d497f1a?w=800"
          }
        ]
      }
    ],
    "images": [
      {
        "image_url": "https://images.unsplash.com/photo-1506354666786-959d6d497f1a?w=800",
        "caption": "Không gian và món ngon tại KPub Korean BBQ - Phan Xích Long",
        "is_cover": true
      }
    ],
    "description": "Nướng thùng phuy đường phố Hàn Quốc với quầy panchan và sốt phô mai béo ngậy.",
    "phone_number": "02873009911"
  },
  {
    "id": 62,
    "name": "Cơm Tấm Ba Ghiền - Đặng Văn Ngữ",
    "address": "84 Đặng Văn Ngữ, Phường 10, Quận Phú Nhuận, TP. Hồ Chí Minh",
    "lat": 10.7958,
    "lng": 106.6672,
    "category": "vietnamese",
    "cuisineLabel": "Cơm tấm",
    "priceMin": 65000,
    "priceMax": 125000,
    "rating": 4.7,
    "reviews": 1320,
    "parking": true,
    "private_room": false,
    "vegetarian": false,
    "openHours": "07:30 - 21:30",
    "image": "https://images.unsplash.com/photo-1511690656952-34342bb7c2f2?w=800",
    "menu": [
      {
        "name": "Cơm Tấm Sườn Khổng Lồ",
        "price": 85000.0
      },
      {
        "name": "Cơm Tấm Sườn Bì Chả Ốp La",
        "price": 115000.0
      }
    ],
    "district": "Quận Tân Bình",
    "has_parking": true,
    "has_private_room": false,
    "has_outdoor": false,
    "outdoor": false,
    "pet_friendly": false,
    "has_pet_friendly": false,
    "vegetarian_support": false,
    "menus": [
      {
        "name": "Món Đặc Trưng",
        "description": "Các món nổi bật nhất tại Cơm Tấm Ba Ghiền - Đặng Văn Ngữ",
        "items": [
          {
            "name": "Cơm Tấm Sườn Khổng Lồ",
            "description": "Món bán chạy hàng đầu tại Cơm Tấm Ba Ghiền - Đặng Văn Ngữ",
            "price": 85000.0,
            "image_url": "https://images.unsplash.com/photo-1511690656952-34342bb7c2f2?w=800"
          },
          {
            "name": "Cơm Tấm Sườn Bì Chả Ốp La",
            "description": "Hương vị đặc sắc được thực khách yêu thích",
            "price": 115000.0,
            "image_url": "https://images.unsplash.com/photo-1511690656952-34342bb7c2f2?w=800"
          }
        ]
      }
    ],
    "images": [
      {
        "image_url": "https://images.unsplash.com/photo-1511690656952-34342bb7c2f2?w=800",
        "caption": "Không gian và món ngon tại Cơm Tấm Ba Ghiền - Đặng Văn Ngữ",
        "is_cover": true
      }
    ],
    "description": "Quán cơm tấm đạt Michelin Bib Gourmand với miếng sườn cốt lết khổng lồ nướng than thơm phức.",
    "phone_number": "02838461073"
  },
  {
    "id": 63,
    "name": "Bánh Canh Trảng Bàng Hoàng Minh - Cộng Hòa",
    "address": "324 Cộng Hòa, Phường 13, Quận Tân Bình, TP. Hồ Chí Minh",
    "lat": 10.8022,
    "lng": 106.6478,
    "category": "vietnamese",
    "cuisineLabel": "Món Việt",
    "priceMin": 60000,
    "priceMax": 160000,
    "rating": 4.5,
    "reviews": 490,
    "parking": true,
    "private_room": false,
    "vegetarian": false,
    "openHours": "07:00 - 22:00",
    "image": "https://images.unsplash.com/photo-1525351484163-7529414344d8?w=800",
    "menu": [
      {
        "name": "Bánh Canh Giò Heo",
        "price": 68000.0
      },
      {
        "name": "Bánh Tráng Cuốn Thịt Luộc",
        "price": 135000.0
      }
    ],
    "district": "Quận Tân Bình",
    "has_parking": true,
    "has_private_room": false,
    "has_outdoor": false,
    "outdoor": false,
    "pet_friendly": false,
    "has_pet_friendly": false,
    "vegetarian_support": false,
    "menus": [
      {
        "name": "Món Đặc Trưng",
        "description": "Các món nổi bật nhất tại Bánh Canh Trảng Bàng Hoàng Minh - Cộng Hòa",
        "items": [
          {
            "name": "Bánh Canh Giò Heo",
            "description": "Món bán chạy hàng đầu tại Bánh Canh Trảng Bàng Hoàng Minh - Cộng Hòa",
            "price": 68000.0,
            "image_url": "https://images.unsplash.com/photo-1525351484163-7529414344d8?w=800"
          },
          {
            "name": "Bánh Tráng Cuốn Thịt Luộc",
            "description": "Hương vị đặc sắc được thực khách yêu thích",
            "price": 135000.0,
            "image_url": "https://images.unsplash.com/photo-1525351484163-7529414344d8?w=800"
          }
        ]
      }
    ],
    "images": [
      {
        "image_url": "https://images.unsplash.com/photo-1525351484163-7529414344d8?w=800",
        "caption": "Không gian và món ngon tại Bánh Canh Trảng Bàng Hoàng Minh - Cộng Hòa",
        "is_cover": true
      }
    ],
    "description": "Đặc sản bánh canh giò heo và bánh tráng phơi sương cuốn thịt luộc rau rừng Tây Ninh.",
    "phone_number": "02838101122"
  },
  {
    "id": 64,
    "name": "Lẩu Bò Sài Gòn Vivu - Trường Chinh",
    "address": "415 Trường Chinh, Phường 14, Quận Tân Bình, TP. Hồ Chí Minh",
    "lat": 10.8055,
    "lng": 106.6395,
    "category": "bbq",
    "cuisineLabel": "Lẩu Nướng",
    "priceMin": 120000,
    "priceMax": 280000,
    "rating": 4.5,
    "reviews": 370,
    "parking": true,
    "private_room": false,
    "vegetarian": false,
    "openHours": "10:30 - 22:30",
    "image": "https://images.unsplash.com/photo-1528735602780-2552fd46c7af?w=800",
    "menu": [
      {
        "name": "Lẩu Bò Thập Cẩm Nồi Lớn",
        "price": 260000.0
      },
      {
        "name": "Bò Nướng Ngói Sa Tế",
        "price": 145000.0
      }
    ],
    "district": "Quận Tân Bình",
    "has_parking": true,
    "has_private_room": false,
    "has_outdoor": true,
    "outdoor": true,
    "pet_friendly": false,
    "has_pet_friendly": false,
    "vegetarian_support": false,
    "menus": [
      {
        "name": "Món Đặc Trưng",
        "description": "Các món nổi bật nhất tại Lẩu Bò Sài Gòn Vivu - Trường Chinh",
        "items": [
          {
            "name": "Lẩu Bò Thập Cẩm Nồi Lớn",
            "description": "Món bán chạy hàng đầu tại Lẩu Bò Sài Gòn Vivu - Trường Chinh",
            "price": 260000.0,
            "image_url": "https://images.unsplash.com/photo-1528735602780-2552fd46c7af?w=800"
          },
          {
            "name": "Bò Nướng Ngói Sa Tế",
            "description": "Hương vị đặc sắc được thực khách yêu thích",
            "price": 145000.0,
            "image_url": "https://images.unsplash.com/photo-1528735602780-2552fd46c7af?w=800"
          }
        ]
      }
    ],
    "images": [
      {
        "image_url": "https://images.unsplash.com/photo-1528735602780-2552fd46c7af?w=800",
        "caption": "Không gian và món ngon tại Lẩu Bò Sài Gòn Vivu - Trường Chinh",
        "is_cover": true
      }
    ],
    "description": "Lẩu bò hầm sả thơm lừng với nạm, gân, đuôi bò mềm rục chấm chao sa tế cực bắt vị.",
    "phone_number": "02838492233"
  },
  {
    "id": 65,
    "name": "Hải Sản Phố Biển - Bàu Cát",
    "address": "68 Đồng Đen, Phường 14, Quận Tân Bình, TP. Hồ Chí Minh",
    "lat": 10.794,
    "lng": 106.6412,
    "category": "other",
    "cuisineLabel": "Hải Sản",
    "priceMin": 140000,
    "priceMax": 480000,
    "rating": 4.5,
    "reviews": 310,
    "parking": true,
    "private_room": true,
    "vegetarian": false,
    "openHours": "10:00 - 23:00",
    "image": "https://images.unsplash.com/photo-1532550907401-a500c9a57435?w=800",
    "menu": [
      {
        "name": "Tôm Càng Nướng Phô Mai",
        "price": 290000.0
      },
      {
        "name": "Mực Một Nắng Nướng Muối Ớt",
        "price": 220000.0
      }
    ],
    "district": "Quận Tân Bình",
    "has_parking": true,
    "has_private_room": true,
    "has_outdoor": true,
    "outdoor": true,
    "pet_friendly": false,
    "has_pet_friendly": false,
    "vegetarian_support": false,
    "menus": [
      {
        "name": "Món Đặc Trưng",
        "description": "Các món nổi bật nhất tại Hải Sản Phố Biển - Bàu Cát",
        "items": [
          {
            "name": "Tôm Càng Nướng Phô Mai",
            "description": "Món bán chạy hàng đầu tại Hải Sản Phố Biển - Bàu Cát",
            "price": 290000.0,
            "image_url": "https://images.unsplash.com/photo-1532550907401-a500c9a57435?w=800"
          },
          {
            "name": "Mực Một Nắng Nướng Muối Ớt",
            "description": "Hương vị đặc sắc được thực khách yêu thích",
            "price": 220000.0,
            "image_url": "https://images.unsplash.com/photo-1532550907401-a500c9a57435?w=800"
          }
        ]
      }
    ],
    "images": [
      {
        "image_url": "https://images.unsplash.com/photo-1532550907401-a500c9a57435?w=800",
        "caption": "Không gian và món ngon tại Hải Sản Phố Biển - Bàu Cát",
        "is_cover": true
      }
    ],
    "description": "Hải sản tươi sống khu Bàu Cát với không gian sân vườn thoáng mát và phòng VIP tiếp khách.",
    "phone_number": "0909887766"
  },
  {
    "id": 66,
    "name": "Highlands Coffee - Cộng Hòa Plaza",
    "address": "19 Cộng Hòa, Phường 12, Quận Tân Bình, TP. Hồ Chí Minh",
    "lat": 10.8012,
    "lng": 106.652,
    "category": "other",
    "cuisineLabel": "Cà Phê & Bánh",
    "priceMin": 35000,
    "priceMax": 75000,
    "rating": 4.4,
    "reviews": 620,
    "parking": true,
    "private_room": false,
    "vegetarian": true,
    "openHours": "07:00 - 22:30",
    "image": "https://images.unsplash.com/photo-1539136788836-5699e78bfc75?w=800",
    "menu": [
      {
        "name": "Phin Sữa Đá",
        "price": 39000.0
      },
      {
        "name": "Trà Sen Vàng",
        "price": 55000.0
      }
    ],
    "district": "Quận Tân Bình",
    "has_parking": true,
    "has_private_room": false,
    "has_outdoor": true,
    "outdoor": true,
    "pet_friendly": false,
    "has_pet_friendly": false,
    "vegetarian_support": true,
    "menus": [
      {
        "name": "Món Đặc Trưng",
        "description": "Các món nổi bật nhất tại Highlands Coffee - Cộng Hòa Plaza",
        "items": [
          {
            "name": "Phin Sữa Đá",
            "description": "Món bán chạy hàng đầu tại Highlands Coffee - Cộng Hòa Plaza",
            "price": 39000.0,
            "image_url": "https://images.unsplash.com/photo-1539136788836-5699e78bfc75?w=800"
          },
          {
            "name": "Trà Sen Vàng",
            "description": "Hương vị đặc sắc được thực khách yêu thích",
            "price": 55000.0,
            "image_url": "https://images.unsplash.com/photo-1539136788836-5699e78bfc75?w=800"
          }
        ]
      }
    ],
    "images": [
      {
        "image_url": "https://images.unsplash.com/photo-1539136788836-5699e78bfc75?w=800",
        "caption": "Không gian và món ngon tại Highlands Coffee - Cộng Hòa Plaza",
        "is_cover": true
      }
    ],
    "description": "Không gian cà phê làm việc, gặp gỡ đối tác rộng rãi gần sân bay Tân Sơn Nhất.",
    "phone_number": "19001755"
  },
  {
    "id": 67,
    "name": "King BBQ Buffet - Aeon Mall Tân Phú",
    "address": "Tầng 3 Aeon Mall Celadon, 30 Bờ Bao Tân Thắng, Quận Tân Phú, TP. Hồ Chí Minh",
    "lat": 10.8015,
    "lng": 106.6175,
    "category": "bbq",
    "cuisineLabel": "Lẩu Nướng",
    "priceMin": 259000,
    "priceMax": 399000,
    "rating": 4.6,
    "reviews": 680,
    "parking": true,
    "private_room": true,
    "vegetarian": false,
    "openHours": "10:00 - 22:00",
    "image": "https://images.unsplash.com/photo-1540189549336-e6e99c3679fe?w=800",
    "menu": [
      {
        "name": "Buffet Nướng King BBQ",
        "price": 329000.0
      },
      {
        "name": "Cổ Bò Mỹ Sốt King",
        "price": 189000.0
      }
    ],
    "district": "Quận Tân Phú",
    "has_parking": true,
    "has_private_room": true,
    "has_outdoor": false,
    "outdoor": false,
    "pet_friendly": false,
    "has_pet_friendly": false,
    "vegetarian_support": false,
    "menus": [
      {
        "name": "Món Đặc Trưng",
        "description": "Các món nổi bật nhất tại King BBQ Buffet - Aeon Mall Tân Phú",
        "items": [
          {
            "name": "Buffet Nướng King BBQ",
            "description": "Món bán chạy hàng đầu tại King BBQ Buffet - Aeon Mall Tân Phú",
            "price": 329000.0,
            "image_url": "https://images.unsplash.com/photo-1540189549336-e6e99c3679fe?w=800"
          },
          {
            "name": "Cổ Bò Mỹ Sốt King",
            "description": "Hương vị đặc sắc được thực khách yêu thích",
            "price": 189000.0,
            "image_url": "https://images.unsplash.com/photo-1540189549336-e6e99c3679fe?w=800"
          }
        ]
      }
    ],
    "images": [
      {
        "image_url": "https://images.unsplash.com/photo-1540189549336-e6e99c3679fe?w=800",
        "caption": "Không gian và món ngon tại King BBQ Buffet - Aeon Mall Tân Phú",
        "is_cover": true
      }
    ],
    "description": "Buffet nướng Hàn Quốc hơn 50 món thịt bò Mỹ tẩm sốt King độc quyền tại Aeon Mall Tân Phú.",
    "phone_number": "1900234546"
  },
  {
    "id": 68,
    "name": "Chay Sen Vàng - Lũy Bán Bích",
    "address": "512 Lũy Bán Bích, Phường Hòa Thạnh, Quận Tân Phú, TP. Hồ Chí Minh",
    "lat": 10.7812,
    "lng": 106.6345,
    "category": "vegetarian",
    "cuisineLabel": "Món Chay",
    "priceMin": 40000,
    "priceMax": 120000,
    "rating": 4.5,
    "reviews": 210,
    "parking": true,
    "private_room": false,
    "vegetarian": true,
    "openHours": "07:00 - 21:00",
    "image": "https://images.unsplash.com/photo-1543339308-43e59d6b73a6?w=800",
    "menu": [
      {
        "name": "Bún Riêu Chay",
        "price": 45000.0
      },
      {
        "name": "Lẩu Nấm Chay Thập Cẩm",
        "price": 120000.0
      }
    ],
    "district": "Quận Tân Phú",
    "has_parking": true,
    "has_private_room": false,
    "has_outdoor": false,
    "outdoor": false,
    "pet_friendly": false,
    "has_pet_friendly": false,
    "vegetarian_support": true,
    "menus": [
      {
        "name": "Món Đặc Trưng",
        "description": "Các món nổi bật nhất tại Chay Sen Vàng - Lũy Bán Bích",
        "items": [
          {
            "name": "Bún Riêu Chay",
            "description": "Món bán chạy hàng đầu tại Chay Sen Vàng - Lũy Bán Bích",
            "price": 45000.0,
            "image_url": "https://images.unsplash.com/photo-1543339308-43e59d6b73a6?w=800"
          },
          {
            "name": "Lẩu Nấm Chay Thập Cẩm",
            "description": "Hương vị đặc sắc được thực khách yêu thích",
            "price": 120000.0,
            "image_url": "https://images.unsplash.com/photo-1543339308-43e59d6b73a6?w=800"
          }
        ]
      }
    ],
    "images": [
      {
        "image_url": "https://images.unsplash.com/photo-1543339308-43e59d6b73a6?w=800",
        "caption": "Không gian và món ngon tại Chay Sen Vàng - Lũy Bán Bích",
        "is_cover": true
      }
    ],
    "description": "Quán chay bình dân sạch sẽ với thực đơn bún riêu chay, hủ tiếu chay và lẩu nấm thơm ngon.",
    "phone_number": "0903123789"
  },
  {
    "id": 69,
    "name": "Ốc Nhớ Sài Gòn - Tân Kỳ Tân Quý",
    "address": "218 Tân Kỳ Tân Quý, Phường Sơn Kỳ, Quận Tân Phú, TP. Hồ Chí Minh",
    "lat": 10.8045,
    "lng": 106.625,
    "category": "other",
    "cuisineLabel": "Hải Sản",
    "priceMin": 50000,
    "priceMax": 180000,
    "rating": 4.5,
    "reviews": 440,
    "parking": true,
    "private_room": false,
    "vegetarian": false,
    "openHours": "16:00 - 23:30",
    "image": "https://images.unsplash.com/photo-1547592166-23ac45744acd?w=800",
    "menu": [
      {
        "name": "Ốc Hương Sốt Trứng Muối",
        "price": 95000.0
      },
      {
        "name": "Sò Huyết Xào Me",
        "price": 75000.0
      }
    ],
    "district": "Quận Tân Phú",
    "has_parking": true,
    "has_private_room": false,
    "has_outdoor": true,
    "outdoor": true,
    "pet_friendly": true,
    "has_pet_friendly": true,
    "vegetarian_support": false,
    "menus": [
      {
        "name": "Món Đặc Trưng",
        "description": "Các món nổi bật nhất tại Ốc Nhớ Sài Gòn - Tân Kỳ Tân Quý",
        "items": [
          {
            "name": "Ốc Hương Sốt Trứng Muối",
            "description": "Món bán chạy hàng đầu tại Ốc Nhớ Sài Gòn - Tân Kỳ Tân Quý",
            "price": 95000.0,
            "image_url": "https://images.unsplash.com/photo-1547592166-23ac45744acd?w=800"
          },
          {
            "name": "Sò Huyết Xào Me",
            "description": "Hương vị đặc sắc được thực khách yêu thích",
            "price": 75000.0,
            "image_url": "https://images.unsplash.com/photo-1547592166-23ac45744acd?w=800"
          }
        ]
      }
    ],
    "images": [
      {
        "image_url": "https://images.unsplash.com/photo-1547592166-23ac45744acd?w=800",
        "caption": "Không gian và món ngon tại Ốc Nhớ Sài Gòn - Tân Kỳ Tân Quý",
        "is_cover": true
      }
    ],
    "description": "Quán ốc đêm đông khách nổi tiếng Tân Phú với sốt trứng muối, sốt bơ cay béo ngậy.",
    "phone_number": "0938556677"
  },
  {
    "id": 70,
    "name": "Bún Đậu Mắm Tôm A Chảnh - Tân Sơn Nhì",
    "address": "145 Tân Sơn Nhì, Phường Tân Sơn Nhì, Quận Tân Phú, TP. Hồ Chí Minh",
    "lat": 10.7935,
    "lng": 106.6318,
    "category": "vietnamese",
    "cuisineLabel": "Món Việt",
    "priceMin": 45000,
    "priceMax": 95000,
    "rating": 4.4,
    "reviews": 330,
    "parking": true,
    "private_room": false,
    "vegetarian": false,
    "openHours": "10:00 - 22:00",
    "image": "https://images.unsplash.com/photo-1551024709-8f23befc6f87?w=800",
    "menu": [
      {
        "name": "Mẹt Bún Đậu Tá Lả",
        "price": 69000.0
      },
      {
        "name": "Chả Cốm Chiên Giòn",
        "price": 35000.0
      }
    ],
    "district": "Quận Tân Phú",
    "has_parking": true,
    "has_private_room": false,
    "has_outdoor": false,
    "outdoor": false,
    "pet_friendly": false,
    "has_pet_friendly": false,
    "vegetarian_support": false,
    "menus": [
      {
        "name": "Món Đặc Trưng",
        "description": "Các món nổi bật nhất tại Bún Đậu Mắm Tôm A Chảnh - Tân Sơn Nhì",
        "items": [
          {
            "name": "Mẹt Bún Đậu Tá Lả",
            "description": "Món bán chạy hàng đầu tại Bún Đậu Mắm Tôm A Chảnh - Tân Sơn Nhì",
            "price": 69000.0,
            "image_url": "https://images.unsplash.com/photo-1551024709-8f23befc6f87?w=800"
          },
          {
            "name": "Chả Cốm Chiên Giòn",
            "description": "Hương vị đặc sắc được thực khách yêu thích",
            "price": 35000.0,
            "image_url": "https://images.unsplash.com/photo-1551024709-8f23befc6f87?w=800"
          }
        ]
      }
    ],
    "images": [
      {
        "image_url": "https://images.unsplash.com/photo-1551024709-8f23befc6f87?w=800",
        "caption": "Không gian và món ngon tại Bún Đậu Mắm Tôm A Chảnh - Tân Sơn Nhì",
        "is_cover": true
      }
    ],
    "description": "Mẹt bún đậu tá lả đầy đặn chả cốm Hà Nội, nem chua rán, thịt chân giò luộc chấm mắm tôm đánh bông.",
    "phone_number": "0902445566"
  },
  {
    "id": 71,
    "name": "Ốc Oanh - Vĩnh Khánh",
    "address": "534 Vĩnh Khánh, Phường 8, Quận 4, TP. Hồ Chí Minh",
    "lat": 10.7615,
    "lng": 106.7032,
    "category": "other",
    "cuisineLabel": "Hải Sản",
    "priceMin": 80000,
    "priceMax": 280000,
    "rating": 4.6,
    "reviews": 1180,
    "parking": true,
    "private_room": false,
    "vegetarian": false,
    "openHours": "15:00 - 00:00",
    "image": "https://images.unsplash.com/photo-1551782450-a2132b4ba21d?w=800",
    "menu": [
      {
        "name": "Càng Ghẹ Rang Muối Ớt",
        "price": 160000.0
      },
      {
        "name": "Ốc Hương Nướng Mọi",
        "price": 110000.0
      }
    ],
    "district": "Quận 4",
    "has_parking": true,
    "has_private_room": false,
    "has_outdoor": true,
    "outdoor": true,
    "pet_friendly": true,
    "has_pet_friendly": true,
    "vegetarian_support": false,
    "menus": [
      {
        "name": "Món Đặc Trưng",
        "description": "Các món nổi bật nhất tại Ốc Oanh - Vĩnh Khánh",
        "items": [
          {
            "name": "Càng Ghẹ Rang Muối Ớt",
            "description": "Món bán chạy hàng đầu tại Ốc Oanh - Vĩnh Khánh",
            "price": 160000.0,
            "image_url": "https://images.unsplash.com/photo-1551782450-a2132b4ba21d?w=800"
          },
          {
            "name": "Ốc Hương Nướng Mọi",
            "description": "Hương vị đặc sắc được thực khách yêu thích",
            "price": 110000.0,
            "image_url": "https://images.unsplash.com/photo-1551782450-a2132b4ba21d?w=800"
          }
        ]
      }
    ],
    "images": [
      {
        "image_url": "https://images.unsplash.com/photo-1551782450-a2132b4ba21d?w=800",
        "caption": "Không gian và món ngon tại Ốc Oanh - Vĩnh Khánh",
        "is_cover": true
      }
    ],
    "description": "Quán ốc biểu tượng của phố ẩm thực Vĩnh Khánh Quận 4, nổi tiếng với càng ghẹ rang muối ớt và ốc hương.",
    "phone_number": "0909334455"
  },
  {
    "id": 72,
    "name": "Sushi Ko - Vĩnh Khánh",
    "address": "122/37 Vĩnh Khánh, Phường 10, Quận 4, TP. Hồ Chí Minh",
    "lat": 10.7602,
    "lng": 106.7048,
    "category": "japanese",
    "cuisineLabel": "Món Nhật",
    "priceMin": 60000,
    "priceMax": 180000,
    "rating": 4.5,
    "reviews": 590,
    "parking": true,
    "private_room": false,
    "vegetarian": false,
    "openHours": "16:00 - 22:30",
    "image": "https://images.unsplash.com/photo-1555949258-eb67b1ef0ceb?w=800",
    "menu": [
      {
        "name": "Sashimi Cá Hồi (8 lát)",
        "price": 115000.0
      },
      {
        "name": "Sushi Lươn Nhật",
        "price": 85000.0
      }
    ],
    "district": "Quận 4",
    "has_parking": true,
    "has_private_room": false,
    "has_outdoor": true,
    "outdoor": true,
    "pet_friendly": false,
    "has_pet_friendly": false,
    "vegetarian_support": false,
    "menus": [
      {
        "name": "Món Đặc Trưng",
        "description": "Các món nổi bật nhất tại Sushi Ko - Vĩnh Khánh",
        "items": [
          {
            "name": "Sashimi Cá Hồi (8 lát)",
            "description": "Món bán chạy hàng đầu tại Sushi Ko - Vĩnh Khánh",
            "price": 115000.0,
            "image_url": "https://images.unsplash.com/photo-1555949258-eb67b1ef0ceb?w=800"
          },
          {
            "name": "Sushi Lươn Nhật",
            "description": "Hương vị đặc sắc được thực khách yêu thích",
            "price": 85000.0,
            "image_url": "https://images.unsplash.com/photo-1555949258-eb67b1ef0ceb?w=800"
          }
        ]
      }
    ],
    "images": [
      {
        "image_url": "https://images.unsplash.com/photo-1555949258-eb67b1ef0ceb?w=800",
        "caption": "Không gian và món ngon tại Sushi Ko - Vĩnh Khánh",
        "is_cover": true
      }
    ],
    "description": "Sushi bình dân chất lượng cao nổi tiếng khắp Sài Gòn, cá hồi tươi cắt lát dày.",
    "phone_number": "0908667788"
  },
  {
    "id": 73,
    "name": "Cơm Tấm Bãi Rác - Lê Văn Linh",
    "address": "73 Lê Văn Linh, Phường 12, Quận 4, TP. Hồ Chí Minh",
    "lat": 10.7642,
    "lng": 106.7055,
    "category": "vietnamese",
    "cuisineLabel": "Cơm tấm",
    "priceMin": 70000,
    "priceMax": 130000,
    "rating": 4.4,
    "reviews": 640,
    "parking": false,
    "private_room": false,
    "vegetarian": false,
    "openHours": "17:00 - 01:00",
    "image": "https://images.unsplash.com/photo-1560717845-968823efbee1?w=800",
    "menu": [
      {
        "name": "Cơm Tấm Sườn Trứng Mực Nhồi",
        "price": 110000.0
      },
      {
        "name": "Cơm Tấm Sườn Bì Chả",
        "price": 85000.0
      }
    ],
    "district": "Quận 4",
    "has_parking": false,
    "has_private_room": false,
    "has_outdoor": true,
    "outdoor": true,
    "pet_friendly": false,
    "has_pet_friendly": false,
    "vegetarian_support": false,
    "menus": [
      {
        "name": "Món Đặc Trưng",
        "description": "Các món nổi bật nhất tại Cơm Tấm Bãi Rác - Lê Văn Linh",
        "items": [
          {
            "name": "Cơm Tấm Sườn Trứng Mực Nhồi",
            "description": "Món bán chạy hàng đầu tại Cơm Tấm Bãi Rác - Lê Văn Linh",
            "price": 110000.0,
            "image_url": "https://images.unsplash.com/photo-1560717845-968823efbee1?w=800"
          },
          {
            "name": "Cơm Tấm Sườn Bì Chả",
            "description": "Hương vị đặc sắc được thực khách yêu thích",
            "price": 85000.0,
            "image_url": "https://images.unsplash.com/photo-1560717845-968823efbee1?w=800"
          }
        ]
      }
    ],
    "images": [
      {
        "image_url": "https://images.unsplash.com/photo-1560717845-968823efbee1?w=800",
        "caption": "Không gian và món ngon tại Cơm Tấm Bãi Rác - Lê Văn Linh",
        "is_cover": true
      }
    ],
    "description": "Quán cơm tấm đêm huyền thoại Quận 4 với đủ loại đồ ăn kèm từ sườn nướng đến mực nhồi thịt.",
    "phone_number": "0903998877"
  },
  {
    "id": 74,
    "name": "Elisa Floating Restaurant - Bến Nhà Rồng",
    "address": "5 Nguyễn Tất Thành, Phường 12, Quận 4, TP. Hồ Chí Minh",
    "lat": 10.7685,
    "lng": 106.7072,
    "category": "western",
    "cuisineLabel": "Món Âu",
    "priceMin": 350000,
    "priceMax": 1500000,
    "rating": 4.7,
    "reviews": 760,
    "parking": true,
    "private_room": true,
    "vegetarian": true,
    "openHours": "10:00 - 23:00",
    "image": "https://images.unsplash.com/photo-1562967914-608f82629710?w=800",
    "menu": [
      {
        "name": "Bò Úc Nướng Sốt Tiêu Đen",
        "price": 480000.0
      },
      {
        "name": "Tôm Hùm Nướng Bơ Tỏi",
        "price": 890000.0
      }
    ],
    "district": "Quận 4",
    "has_parking": true,
    "has_private_room": true,
    "has_outdoor": true,
    "outdoor": true,
    "pet_friendly": false,
    "has_pet_friendly": false,
    "vegetarian_support": true,
    "menus": [
      {
        "name": "Món Đặc Trưng",
        "description": "Các món nổi bật nhất tại Elisa Floating Restaurant - Bến Nhà Rồng",
        "items": [
          {
            "name": "Bò Úc Nướng Sốt Tiêu Đen",
            "description": "Món bán chạy hàng đầu tại Elisa Floating Restaurant - Bến Nhà Rồng",
            "price": 480000.0,
            "image_url": "https://images.unsplash.com/photo-1562967914-608f82629710?w=800"
          },
          {
            "name": "Tôm Hùm Nướng Bơ Tỏi",
            "description": "Hương vị đặc sắc được thực khách yêu thích",
            "price": 890000.0,
            "image_url": "https://images.unsplash.com/photo-1562967914-608f82629710?w=800"
          }
        ]
      }
    ],
    "images": [
      {
        "image_url": "https://images.unsplash.com/photo-1562967914-608f82629710?w=800",
        "caption": "Không gian và món ngon tại Elisa Floating Restaurant - Bến Nhà Rồng",
        "is_cover": true
      }
    ],
    "description": "Nhà hàng tàu nổi 5 sao trên sông Sài Gòn với thực đơn Âu - Á cao cấp và view thành phố về đêm.",
    "phone_number": "02838299999"
  },
  {
    "id": 75,
    "name": "Dimsum Baoz - Nguyễn Tri Phương",
    "address": "88 Nguyễn Tri Phương, Phường 7, Quận 5, TP. Hồ Chí Minh",
    "lat": 10.7575,
    "lng": 106.669,
    "category": "other",
    "cuisineLabel": "Món Hoa",
    "priceMin": 120000,
    "priceMax": 420000,
    "rating": 4.7,
    "reviews": 1250,
    "parking": true,
    "private_room": true,
    "vegetarian": true,
    "openHours": "06:30 - 22:30",
    "image": "https://images.unsplash.com/photo-1563379926898-05f4575a45d8?w=800",
    "menu": [
      {
        "name": "Há Cảo Tôm Tươi Baoz",
        "price": 78000.0
      },
      {
        "name": "Vịt Quay Hồng Kông",
        "price": 320000.0
      }
    ],
    "district": "Quận 5",
    "has_parking": true,
    "has_private_room": true,
    "has_outdoor": false,
    "outdoor": false,
    "pet_friendly": false,
    "has_pet_friendly": false,
    "vegetarian_support": true,
    "menus": [
      {
        "name": "Món Đặc Trưng",
        "description": "Các món nổi bật nhất tại Dimsum Baoz - Nguyễn Tri Phương",
        "items": [
          {
            "name": "Há Cảo Tôm Tươi Baoz",
            "description": "Món bán chạy hàng đầu tại Dimsum Baoz - Nguyễn Tri Phương",
            "price": 78000.0,
            "image_url": "https://images.unsplash.com/photo-1563379926898-05f4575a45d8?w=800"
          },
          {
            "name": "Vịt Quay Hồng Kông",
            "description": "Hương vị đặc sắc được thực khách yêu thích",
            "price": 320000.0,
            "image_url": "https://images.unsplash.com/photo-1563379926898-05f4575a45d8?w=800"
          }
        ]
      }
    ],
    "images": [
      {
        "image_url": "https://images.unsplash.com/photo-1563379926898-05f4575a45d8?w=800",
        "caption": "Không gian và món ngon tại Dimsum Baoz - Nguyễn Tri Phương",
        "is_cover": true
      }
    ],
    "description": "Nhà hàng Dimsum Hồng Kông nức tiếng Quận 5 với há cảo, bánh bao kim sa và vịt quay giòn da.",
    "phone_number": "02839231480"
  },
  {
    "id": 76,
    "name": "Lẩu Cá Dân Ích - Châu Văn Liêm",
    "address": "99 Châu Văn Liêm, Phường 14, Quận 5, TP. Hồ Chí Minh",
    "lat": 10.7525,
    "lng": 106.6598,
    "category": "other",
    "cuisineLabel": "Món Hoa",
    "priceMin": 120000,
    "priceMax": 320000,
    "rating": 4.6,
    "reviews": 870,
    "parking": true,
    "private_room": false,
    "vegetarian": false,
    "openHours": "16:00 - 22:00",
    "image": "https://images.unsplash.com/photo-1564834724105-918b73d1b9e0?w=800",
    "menu": [
      {
        "name": "Lẩu Cá Cù Lao Thập Cẩm",
        "price": 290000.0
      },
      {
        "name": "Chả Giò Tôm Cua",
        "price": 95000.0
      }
    ],
    "district": "Quận 5",
    "has_parking": true,
    "has_private_room": false,
    "has_outdoor": false,
    "outdoor": false,
    "pet_friendly": false,
    "has_pet_friendly": false,
    "vegetarian_support": false,
    "menus": [
      {
        "name": "Món Đặc Trưng",
        "description": "Các món nổi bật nhất tại Lẩu Cá Dân Ích - Châu Văn Liêm",
        "items": [
          {
            "name": "Lẩu Cá Cù Lao Thập Cẩm",
            "description": "Món bán chạy hàng đầu tại Lẩu Cá Dân Ích - Châu Văn Liêm",
            "price": 290000.0,
            "image_url": "https://images.unsplash.com/photo-1564834724105-918b73d1b9e0?w=800"
          },
          {
            "name": "Chả Giò Tôm Cua",
            "description": "Hương vị đặc sắc được thực khách yêu thích",
            "price": 95000.0,
            "image_url": "https://images.unsplash.com/photo-1564834724105-918b73d1b9e0?w=800"
          }
        ]
      }
    ],
    "images": [
      {
        "image_url": "https://images.unsplash.com/photo-1564834724105-918b73d1b9e0?w=800",
        "caption": "Không gian và món ngon tại Lẩu Cá Dân Ích - Châu Văn Liêm",
        "is_cover": true
      }
    ],
    "description": "Lẩu cá cù lao đốt than truyền thống của người Hoa hơn 40 năm tuổi, nước lẩu ngọt thanh đậm đà.",
    "phone_number": "02838551887"
  },
  {
    "id": 77,
    "name": "Cơm Gà Đông Nguyên - Châu Văn Liêm",
    "address": "801 Nguyễn Trãi, Phường 14, Quận 5, TP. Hồ Chí Minh",
    "lat": 10.7532,
    "lng": 106.6612,
    "category": "other",
    "cuisineLabel": "Món Hoa",
    "priceMin": 85000,
    "priceMax": 220000,
    "rating": 4.6,
    "reviews": 940,
    "parking": true,
    "private_room": false,
    "vegetarian": false,
    "openHours": "09:00 - 20:30",
    "image": "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=800",
    "menu": [
      {
        "name": "Cơm Gà Luộc Chặt Đĩa",
        "price": 135000.0
      },
      {
        "name": "Canh Tiềm Thuốc Bắc",
        "price": 85000.0
      }
    ],
    "district": "Quận 5",
    "has_parking": true,
    "has_private_room": false,
    "has_outdoor": false,
    "outdoor": false,
    "pet_friendly": false,
    "has_pet_friendly": false,
    "vegetarian_support": false,
    "menus": [
      {
        "name": "Món Đặc Trưng",
        "description": "Các món nổi bật nhất tại Cơm Gà Đông Nguyên - Châu Văn Liêm",
        "items": [
          {
            "name": "Cơm Gà Luộc Chặt Đĩa",
            "description": "Món bán chạy hàng đầu tại Cơm Gà Đông Nguyên - Châu Văn Liêm",
            "price": 135000.0,
            "image_url": "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=800"
          },
          {
            "name": "Canh Tiềm Thuốc Bắc",
            "description": "Hương vị đặc sắc được thực khách yêu thích",
            "price": 85000.0,
            "image_url": "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=800"
          }
        ]
      }
    ],
    "images": [
      {
        "image_url": "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=800",
        "caption": "Không gian và món ngon tại Cơm Gà Đông Nguyên - Châu Văn Liêm",
        "is_cover": true
      }
    ],
    "description": "Thương hiệu cơm gà Hải Nam lâu đời từ năm 1945 tại Chợ Lớn, gà ta luộc da vàng giòn thịt ngọt.",
    "phone_number": "02838557678"
  },
  {
    "id": 78,
    "name": "Chè Hà Ký - Châu Văn Liêm",
    "address": "138 Châu Văn Liêm, Phường 11, Quận 5, TP. Hồ Chí Minh",
    "lat": 10.7538,
    "lng": 106.6592,
    "category": "other",
    "cuisineLabel": "Cà Phê & Bánh",
    "priceMin": 30000,
    "priceMax": 65000,
    "rating": 4.6,
    "reviews": 810,
    "parking": false,
    "private_room": false,
    "vegetarian": true,
    "openHours": "10:00 - 22:30",
    "image": "https://images.unsplash.com/photo-1572802419224-296b0aeee0d9?w=800",
    "menu": [
      {
        "name": "Chè Mè Đen Hạnh Nhân",
        "price": 38000.0
      },
      {
        "name": "Quy Linh Cao Mật Ong",
        "price": 42000.0
      }
    ],
    "district": "Quận 5",
    "has_parking": false,
    "has_private_room": false,
    "has_outdoor": false,
    "outdoor": false,
    "pet_friendly": false,
    "has_pet_friendly": false,
    "vegetarian_support": true,
    "menus": [
      {
        "name": "Món Đặc Trưng",
        "description": "Các món nổi bật nhất tại Chè Hà Ký - Châu Văn Liêm",
        "items": [
          {
            "name": "Chè Mè Đen Hạnh Nhân",
            "description": "Món bán chạy hàng đầu tại Chè Hà Ký - Châu Văn Liêm",
            "price": 38000.0,
            "image_url": "https://images.unsplash.com/photo-1572802419224-296b0aeee0d9?w=800"
          },
          {
            "name": "Quy Linh Cao Mật Ong",
            "description": "Hương vị đặc sắc được thực khách yêu thích",
            "price": 42000.0,
            "image_url": "https://images.unsplash.com/photo-1572802419224-296b0aeee0d9?w=800"
          }
        ]
      }
    ],
    "images": [
      {
        "image_url": "https://images.unsplash.com/photo-1572802419224-296b0aeee0d9?w=800",
        "caption": "Không gian và món ngon tại Chè Hà Ký - Châu Văn Liêm",
        "is_cover": true
      }
    ],
    "description": "Tiệm chè người Hoa nổi tiếng với hơn 30 món chè dưỡng nhan: quy linh cao, chè mè đen, hột gà trà.",
    "phone_number": "02838567039"
  },
  {
    "id": 79,
    "name": "Chay Giác Ngộ - Nguyễn Chí Thanh",
    "address": "213A Hùng Vương, Phường 9, Quận 5, TP. Hồ Chí Minh",
    "lat": 10.7585,
    "lng": 106.6685,
    "category": "vegetarian",
    "cuisineLabel": "Món Chay",
    "priceMin": 45000,
    "priceMax": 150000,
    "rating": 4.6,
    "reviews": 310,
    "parking": true,
    "private_room": true,
    "vegetarian": true,
    "openHours": "08:00 - 21:00",
    "image": "https://images.unsplash.com/photo-1576867757603-05b134ebc379?w=800",
    "menu": [
      {
        "name": "Mì Xào Giòn Chay",
        "price": 75000.0
      },
      {
        "name": "Lẩu Thái Chay",
        "price": 145000.0
      }
    ],
    "district": "Quận 5",
    "has_parking": true,
    "has_private_room": true,
    "has_outdoor": false,
    "outdoor": false,
    "pet_friendly": false,
    "has_pet_friendly": false,
    "vegetarian_support": true,
    "menus": [
      {
        "name": "Món Đặc Trưng",
        "description": "Các món nổi bật nhất tại Chay Giác Ngộ - Nguyễn Chí Thanh",
        "items": [
          {
            "name": "Mì Xào Giòn Chay",
            "description": "Món bán chạy hàng đầu tại Chay Giác Ngộ - Nguyễn Chí Thanh",
            "price": 75000.0,
            "image_url": "https://images.unsplash.com/photo-1576867757603-05b134ebc379?w=800"
          },
          {
            "name": "Lẩu Thái Chay",
            "description": "Hương vị đặc sắc được thực khách yêu thích",
            "price": 145000.0,
            "image_url": "https://images.unsplash.com/photo-1576867757603-05b134ebc379?w=800"
          }
        ]
      }
    ],
    "images": [
      {
        "image_url": "https://images.unsplash.com/photo-1576867757603-05b134ebc379?w=800",
        "caption": "Không gian và món ngon tại Chay Giác Ngộ - Nguyễn Chí Thanh",
        "is_cover": true
      }
    ],
    "description": "Nhà hàng chay thanh lịch tại Quận 5 phục vụ các món chay phong cách Hoa - Việt tinh tế.",
    "phone_number": "02838332211"
  },
  {
    "id": 80,
    "name": "Hủ Tiếu Hồ - Hậu Giang",
    "address": "185 Hậu Giang, Phường 5, Quận 6, TP. Hồ Chí Minh",
    "lat": 10.7485,
    "lng": 106.6412,
    "category": "vietnamese",
    "cuisineLabel": "Món Việt",
    "priceMin": 45000,
    "priceMax": 80000,
    "rating": 4.5,
    "reviews": 340,
    "parking": true,
    "private_room": false,
    "vegetarian": false,
    "openHours": "06:30 - 21:30",
    "image": "https://images.unsplash.com/photo-1585032226651-759b368d7246?w=800",
    "menu": [
      {
        "name": "Hủ Tiếu Hồ Phá Lấu",
        "price": 58000.0
      },
      {
        "name": "Hủ Tiếu Hồ Khô Đặc Biệt",
        "price": 68000.0
      }
    ],
    "district": "Quận 6",
    "has_parking": true,
    "has_private_room": false,
    "has_outdoor": false,
    "outdoor": false,
    "pet_friendly": false,
    "has_pet_friendly": false,
    "vegetarian_support": false,
    "menus": [
      {
        "name": "Món Đặc Trưng",
        "description": "Các món nổi bật nhất tại Hủ Tiếu Hồ - Hậu Giang",
        "items": [
          {
            "name": "Hủ Tiếu Hồ Phá Lấu",
            "description": "Món bán chạy hàng đầu tại Hủ Tiếu Hồ - Hậu Giang",
            "price": 58000.0,
            "image_url": "https://images.unsplash.com/photo-1585032226651-759b368d7246?w=800"
          },
          {
            "name": "Hủ Tiếu Hồ Khô Đặc Biệt",
            "description": "Hương vị đặc sắc được thực khách yêu thích",
            "price": 68000.0,
            "image_url": "https://images.unsplash.com/photo-1585032226651-759b368d7246?w=800"
          }
        ]
      }
    ],
    "images": [
      {
        "image_url": "https://images.unsplash.com/photo-1585032226651-759b368d7246?w=800",
        "caption": "Không gian và món ngon tại Hủ Tiếu Hồ - Hậu Giang",
        "is_cover": true
      }
    ],
    "description": "Đặc sản hủ tiếu hồ Campuchia hiếm có tại Quận 6 với bánh hủ tiếu bản vuông ăn kèm phá lấu và cải chua.",
    "phone_number": "0908223344"
  },
  {
    "id": 81,
    "name": "Lẩu Bò Khu Bình Phú",
    "address": "45 Đường Số 10, Phường 10, Quận 6, TP. Hồ Chí Minh",
    "lat": 10.7425,
    "lng": 106.6295,
    "category": "bbq",
    "cuisineLabel": "Lẩu Nướng",
    "priceMin": 100000,
    "priceMax": 260000,
    "rating": 4.5,
    "reviews": 290,
    "parking": true,
    "private_room": false,
    "vegetarian": false,
    "openHours": "15:00 - 23:00",
    "image": "https://images.unsplash.com/photo-1588166524941-3bf61a9c41db?w=800",
    "menu": [
      {
        "name": "Lẩu Đuôi Bò Khoai Môn",
        "price": 240000.0
      },
      {
        "name": "Bò Nướng Lụi Sả",
        "price": 135000.0
      }
    ],
    "district": "Quận 6",
    "has_parking": true,
    "has_private_room": false,
    "has_outdoor": true,
    "outdoor": true,
    "pet_friendly": true,
    "has_pet_friendly": true,
    "vegetarian_support": false,
    "menus": [
      {
        "name": "Món Đặc Trưng",
        "description": "Các món nổi bật nhất tại Lẩu Bò Khu Bình Phú",
        "items": [
          {
            "name": "Lẩu Đuôi Bò Khoai Môn",
            "description": "Món bán chạy hàng đầu tại Lẩu Bò Khu Bình Phú",
            "price": 240000.0,
            "image_url": "https://images.unsplash.com/photo-1588166524941-3bf61a9c41db?w=800"
          },
          {
            "name": "Bò Nướng Lụi Sả",
            "description": "Hương vị đặc sắc được thực khách yêu thích",
            "price": 135000.0,
            "image_url": "https://images.unsplash.com/photo-1588166524941-3bf61a9c41db?w=800"
          }
        ]
      }
    ],
    "images": [
      {
        "image_url": "https://images.unsplash.com/photo-1588166524941-3bf61a9c41db?w=800",
        "caption": "Không gian và món ngon tại Lẩu Bò Khu Bình Phú",
        "is_cover": true
      }
    ],
    "description": "Quán lẩu bò sân vườn thoáng mát khu dân cư Bình Phú, thịt bò tươi ngon và bãi đậu ô tô rộng.",
    "phone_number": "0937112299"
  },
  {
    "id": 82,
    "name": "Dimsum Tân Nguyên Thái - Bình Tây",
    "address": "102 Bình Tây, Phường 1, Quận 6, TP. Hồ Chí Minh",
    "lat": 10.7492,
    "lng": 106.651,
    "category": "other",
    "cuisineLabel": "Món Hoa",
    "priceMin": 60000,
    "priceMax": 180000,
    "rating": 4.5,
    "reviews": 410,
    "parking": true,
    "private_room": false,
    "vegetarian": false,
    "openHours": "06:00 - 13:00",
    "image": "https://images.unsplash.com/photo-1598515214211-89d3c73ae83b?w=800",
    "menu": [
      {
        "name": "Xíu Mại Tôm Thịt",
        "price": 55000.0
      },
      {
        "name": "Bánh Cuốn Xá Xíu",
        "price": 52000.0
      }
    ],
    "district": "Quận 6",
    "has_parking": true,
    "has_private_room": false,
    "has_outdoor": false,
    "outdoor": false,
    "pet_friendly": false,
    "has_pet_friendly": false,
    "vegetarian_support": false,
    "menus": [
      {
        "name": "Món Đặc Trưng",
        "description": "Các món nổi bật nhất tại Dimsum Tân Nguyên Thái - Bình Tây",
        "items": [
          {
            "name": "Xíu Mại Tôm Thịt",
            "description": "Món bán chạy hàng đầu tại Dimsum Tân Nguyên Thái - Bình Tây",
            "price": 55000.0,
            "image_url": "https://images.unsplash.com/photo-1598515214211-89d3c73ae83b?w=800"
          },
          {
            "name": "Bánh Cuốn Xá Xíu",
            "description": "Hương vị đặc sắc được thực khách yêu thích",
            "price": 52000.0,
            "image_url": "https://images.unsplash.com/photo-1598515214211-89d3c73ae83b?w=800"
          }
        ]
      }
    ],
    "images": [
      {
        "image_url": "https://images.unsplash.com/photo-1598515214211-89d3c73ae83b?w=800",
        "caption": "Không gian và món ngon tại Dimsum Tân Nguyên Thái - Bình Tây",
        "is_cover": true
      }
    ],
    "description": "Tiệm điểm tâm sáng chuẩn vị người Hoa khu Chợ Bình Tây, bánh cuốn tôm và xíu mại hấp nóng hổi.",
    "phone_number": "02838541234"
  },
  {
    "id": 83,
    "name": "Pizza 4P's Phú Mỹ Hưng",
    "address": "MD2 Nguyễn Văn Linh, Phường Tân Phú, Quận 7, TP. Hồ Chí Minh",
    "lat": 10.7285,
    "lng": 106.7185,
    "category": "western",
    "cuisineLabel": "Món Âu",
    "priceMin": 180000,
    "priceMax": 480000,
    "rating": 4.8,
    "reviews": 920,
    "parking": true,
    "private_room": true,
    "vegetarian": true,
    "openHours": "10:00 - 23:00",
    "image": "https://images.unsplash.com/photo-1600891964599-f61ba0e24092?w=800",
    "menu": [
      {
        "name": "Pizza 4 Cheese",
        "price": 280000.0
      },
      {
        "name": "Mì Ý Cua Cà Chua",
        "price": 245000.0
      }
    ],
    "district": "Quận 7",
    "has_parking": true,
    "has_private_room": true,
    "has_outdoor": true,
    "outdoor": true,
    "pet_friendly": false,
    "has_pet_friendly": false,
    "vegetarian_support": true,
    "menus": [
      {
        "name": "Món Đặc Trưng",
        "description": "Các món nổi bật nhất tại Pizza 4P's Phú Mỹ Hưng",
        "items": [
          {
            "name": "Pizza 4 Cheese",
            "description": "Món bán chạy hàng đầu tại Pizza 4P's Phú Mỹ Hưng",
            "price": 280000.0,
            "image_url": "https://images.unsplash.com/photo-1600891964599-f61ba0e24092?w=800"
          },
          {
            "name": "Mì Ý Cua Cà Chua",
            "description": "Hương vị đặc sắc được thực khách yêu thích",
            "price": 245000.0,
            "image_url": "https://images.unsplash.com/photo-1600891964599-f61ba0e24092?w=800"
          }
        ]
      }
    ],
    "images": [
      {
        "image_url": "https://images.unsplash.com/photo-1600891964599-f61ba0e24092?w=800",
        "caption": "Không gian và món ngon tại Pizza 4P's Phú Mỹ Hưng",
        "is_cover": true
      }
    ],
    "description": "Không gian hiện đại, rộng rãi tại Phú Mỹ Hưng với pizza phô mai tươi Burrata nướng lò củi trứ danh.",
    "phone_number": "02836220501"
  },
  {
    "id": 84,
    "name": "D'Maris Buffet - Lotte Mart Quận 7",
    "address": "Tầng 3 Lotte Mart, 469 Nguyễn Hữu Thọ, Quận 7, TP. Hồ Chí Minh",
    "lat": 10.7412,
    "lng": 106.7018,
    "category": "other",
    "cuisineLabel": "Hải Sản",
    "priceMin": 450000,
    "priceMax": 620000,
    "rating": 4.7,
    "reviews": 1050,
    "parking": true,
    "private_room": true,
    "vegetarian": true,
    "openHours": "11:00 - 22:00",
    "image": "https://images.unsplash.com/photo-1603133872878-684f208fb84b?w=800",
    "menu": [
      {
        "name": "Vé Buffet Hải Sản Cao Cấp",
        "price": 540000.0
      },
      {
        "name": "Sashimi & Hải Sản Không Giới Hạn",
        "price": 540000.0
      }
    ],
    "district": "Quận 7",
    "has_parking": true,
    "has_private_room": true,
    "has_outdoor": false,
    "outdoor": false,
    "pet_friendly": false,
    "has_pet_friendly": false,
    "vegetarian_support": true,
    "menus": [
      {
        "name": "Món Đặc Trưng",
        "description": "Các món nổi bật nhất tại D'Maris Buffet - Lotte Mart Quận 7",
        "items": [
          {
            "name": "Vé Buffet Hải Sản Cao Cấp",
            "description": "Món bán chạy hàng đầu tại D'Maris Buffet - Lotte Mart Quận 7",
            "price": 540000.0,
            "image_url": "https://images.unsplash.com/photo-1603133872878-684f208fb84b?w=800"
          },
          {
            "name": "Sashimi & Hải Sản Không Giới Hạn",
            "description": "Hương vị đặc sắc được thực khách yêu thích",
            "price": 540000.0,
            "image_url": "https://images.unsplash.com/photo-1603133872878-684f208fb84b?w=800"
          }
        ]
      }
    ],
    "images": [
      {
        "image_url": "https://images.unsplash.com/photo-1603133872878-684f208fb84b?w=800",
        "caption": "Không gian và món ngon tại D'Maris Buffet - Lotte Mart Quận 7",
        "is_cover": true
      }
    ],
    "description": "Nhà hàng buffet quốc tế cao cấp hơn 200 món Á - Âu, hải sản, sushi và quầy bánh ngọt khổng lồ.",
    "phone_number": "19000010"
  },
  {
    "id": 85,
    "name": "Marduk Korean BBQ - Phú Mỹ Hưng",
    "address": "56 Hưng Gia 2, Phường Tân Phong, Quận 7, TP. Hồ Chí Minh",
    "lat": 10.7315,
    "lng": 106.7072,
    "category": "other",
    "cuisineLabel": "Món Hàn",
    "priceMin": 200000,
    "priceMax": 550000,
    "rating": 4.7,
    "reviews": 460,
    "parking": true,
    "private_room": true,
    "vegetarian": false,
    "openHours": "11:00 - 23:00",
    "image": "https://images.unsplash.com/photo-1604908176997-125f25cc6f3d?w=800",
    "menu": [
      {
        "name": "Ba Chỉ Heo Ủ Lạnh Nướng",
        "price": 260000.0
      },
      {
        "name": "Canh Kim Chi Thịt Heo",
        "price": 150000.0
      }
    ],
    "district": "Quận 7",
    "has_parking": true,
    "has_private_room": true,
    "has_outdoor": false,
    "outdoor": false,
    "pet_friendly": false,
    "has_pet_friendly": false,
    "vegetarian_support": false,
    "menus": [
      {
        "name": "Món Đặc Trưng",
        "description": "Các món nổi bật nhất tại Marduk Korean BBQ - Phú Mỹ Hưng",
        "items": [
          {
            "name": "Ba Chỉ Heo Ủ Lạnh Nướng",
            "description": "Món bán chạy hàng đầu tại Marduk Korean BBQ - Phú Mỹ Hưng",
            "price": 260000.0,
            "image_url": "https://images.unsplash.com/photo-1604908176997-125f25cc6f3d?w=800"
          },
          {
            "name": "Canh Kim Chi Thịt Heo",
            "description": "Hương vị đặc sắc được thực khách yêu thích",
            "price": 150000.0,
            "image_url": "https://images.unsplash.com/photo-1604908176997-125f25cc6f3d?w=800"
          }
        ]
      }
    ],
    "images": [
      {
        "image_url": "https://images.unsplash.com/photo-1604908176997-125f25cc6f3d?w=800",
        "caption": "Không gian và món ngon tại Marduk Korean BBQ - Phú Mỹ Hưng",
        "is_cover": true
      }
    ],
    "description": "Quán nướng Hàn Quốc chuẩn vị của người Hàn tại khu phố Hàn Phú Mỹ Hưng, thịt heo ủ lạnh mềm ngọt.",
    "phone_number": "02854101234"
  },
  {
    "id": 86,
    "name": "Chay Garden - Nguyễn Thị Thập",
    "address": "128 Nguyễn Thị Thập, Phường Bình Thuận, Quận 7, TP. Hồ Chí Minh",
    "lat": 10.7385,
    "lng": 106.7195,
    "category": "vegetarian",
    "cuisineLabel": "Món Chay",
    "priceMin": 75000,
    "priceMax": 240000,
    "rating": 4.7,
    "reviews": 380,
    "parking": true,
    "private_room": true,
    "vegetarian": true,
    "openHours": "09:00 - 21:30",
    "image": "https://images.unsplash.com/photo-1606787366850-de6330128bfc?w=800",
    "menu": [
      {
        "name": "Gỏi Bưởi Chay",
        "price": 95000.0
      },
      {
        "name": "Lẩu Nấm Hoa Chuối",
        "price": 210000.0
      }
    ],
    "district": "Quận 7",
    "has_parking": true,
    "has_private_room": true,
    "has_outdoor": true,
    "outdoor": true,
    "pet_friendly": true,
    "has_pet_friendly": true,
    "vegetarian_support": true,
    "menus": [
      {
        "name": "Món Đặc Trưng",
        "description": "Các món nổi bật nhất tại Chay Garden - Nguyễn Thị Thập",
        "items": [
          {
            "name": "Gỏi Bưởi Chay",
            "description": "Món bán chạy hàng đầu tại Chay Garden - Nguyễn Thị Thập",
            "price": 95000.0,
            "image_url": "https://images.unsplash.com/photo-1606787366850-de6330128bfc?w=800"
          },
          {
            "name": "Lẩu Nấm Hoa Chuối",
            "description": "Hương vị đặc sắc được thực khách yêu thích",
            "price": 210000.0,
            "image_url": "https://images.unsplash.com/photo-1606787366850-de6330128bfc?w=800"
          }
        ]
      }
    ],
    "images": [
      {
        "image_url": "https://images.unsplash.com/photo-1606787366850-de6330128bfc?w=800",
        "caption": "Không gian và món ngon tại Chay Garden - Nguyễn Thị Thập",
        "is_cover": true
      }
    ],
    "description": "Nhà hàng chay sân vườn xanh mát tại Quận 7, thích hợp cho bữa cơm gia đình cuối tuần.",
    "phone_number": "02837751122"
  },
  {
    "id": 87,
    "name": "Phở Phú Gia - Sky Garden",
    "address": "R1-42 Sky Garden 2, Phường Tân Phong, Quận 7, TP. Hồ Chí Minh",
    "lat": 10.7295,
    "lng": 106.7042,
    "category": "vietnamese",
    "cuisineLabel": "Món Việt",
    "priceMin": 65000,
    "priceMax": 110000,
    "rating": 4.6,
    "reviews": 420,
    "parking": true,
    "private_room": false,
    "vegetarian": false,
    "openHours": "06:30 - 21:30",
    "image": "https://images.unsplash.com/photo-1612929633738-8fe44f7ec841?w=800",
    "menu": [
      {
        "name": "Phở Tái Lăn Hà Nội",
        "price": 85000.0
      },
      {
        "name": "Phở Chín Nạm",
        "price": 75000.0
      }
    ],
    "district": "Quận 7",
    "has_parking": true,
    "has_private_room": false,
    "has_outdoor": false,
    "outdoor": false,
    "pet_friendly": false,
    "has_pet_friendly": false,
    "vegetarian_support": false,
    "menus": [
      {
        "name": "Món Đặc Trưng",
        "description": "Các món nổi bật nhất tại Phở Phú Gia - Sky Garden",
        "items": [
          {
            "name": "Phở Tái Lăn Hà Nội",
            "description": "Món bán chạy hàng đầu tại Phở Phú Gia - Sky Garden",
            "price": 85000.0,
            "image_url": "https://images.unsplash.com/photo-1612929633738-8fe44f7ec841?w=800"
          },
          {
            "name": "Phở Chín Nạm",
            "description": "Hương vị đặc sắc được thực khách yêu thích",
            "price": 75000.0,
            "image_url": "https://images.unsplash.com/photo-1612929633738-8fe44f7ec841?w=800"
          }
        ]
      }
    ],
    "images": [
      {
        "image_url": "https://images.unsplash.com/photo-1612929633738-8fe44f7ec841?w=800",
        "caption": "Không gian và món ngon tại Phở Phú Gia - Sky Garden",
        "is_cover": true
      }
    ],
    "description": "Phở Bắc chuẩn vị Hà Nội tại khu Phú Mỹ Hưng, nước dùng trong vắt thơm mùi gừng nướng và hành hoa.",
    "phone_number": "0908775533"
  },
  {
    "id": 88,
    "name": "The Coffee Bean & Tea Leaf - Crescent Mall",
    "address": "Tầng trệt Crescent Mall, 101 Tôn Dật Tiên, Quận 7, TP. Hồ Chí Minh",
    "lat": 10.729,
    "lng": 106.7198,
    "category": "other",
    "cuisineLabel": "Cà Phê & Bánh",
    "priceMin": 55000,
    "priceMax": 130000,
    "rating": 4.5,
    "reviews": 510,
    "parking": true,
    "private_room": false,
    "vegetarian": true,
    "openHours": "07:30 - 22:30",
    "image": "https://images.unsplash.com/photo-1626082927389-6cd097cdc6ec?w=800",
    "menu": [
      {
        "name": "Ice Blended Mocha",
        "price": 89000.0
      },
      {
        "name": "Bánh Cheesecake Dâu",
        "price": 75000.0
      }
    ],
    "district": "Quận 7",
    "has_parking": true,
    "has_private_room": false,
    "has_outdoor": true,
    "outdoor": true,
    "pet_friendly": true,
    "has_pet_friendly": true,
    "vegetarian_support": true,
    "menus": [
      {
        "name": "Món Đặc Trưng",
        "description": "Các món nổi bật nhất tại The Coffee Bean & Tea Leaf - Crescent Mall",
        "items": [
          {
            "name": "Ice Blended Mocha",
            "description": "Món bán chạy hàng đầu tại The Coffee Bean & Tea Leaf - Crescent Mall",
            "price": 89000.0,
            "image_url": "https://images.unsplash.com/photo-1626082927389-6cd097cdc6ec?w=800"
          },
          {
            "name": "Bánh Cheesecake Dâu",
            "description": "Hương vị đặc sắc được thực khách yêu thích",
            "price": 75000.0,
            "image_url": "https://images.unsplash.com/photo-1626082927389-6cd097cdc6ec?w=800"
          }
        ]
      }
    ],
    "images": [
      {
        "image_url": "https://images.unsplash.com/photo-1626082927389-6cd097cdc6ec?w=800",
        "caption": "Không gian và món ngon tại The Coffee Bean & Tea Leaf - Crescent Mall",
        "is_cover": true
      }
    ],
    "description": "Quán cà phê view hồ Bán Nguyệt thoáng đãng, phục vụ cà phê rang xay và bánh ngọt cao cấp.",
    "phone_number": "02854137788"
  },
  {
    "id": 89,
    "name": "Ốc Tuyết - Dương Bá Trạc",
    "address": "456 Dương Bá Trạc, Phường 1, Quận 8, TP. Hồ Chí Minh",
    "lat": 10.7458,
    "lng": 106.6885,
    "category": "other",
    "cuisineLabel": "Hải Sản",
    "priceMin": 50000,
    "priceMax": 180000,
    "rating": 4.5,
    "reviews": 420,
    "parking": true,
    "private_room": false,
    "vegetarian": false,
    "openHours": "16:00 - 23:30",
    "image": "https://images.unsplash.com/photo-1515003197210-e0cd71810b5f?w=800",
    "menu": [
      {
        "name": "Ốc Móng Tay Xào Rau Muống",
        "price": 65000.0
      },
      {
        "name": "Hàu Nướng Phô Mai",
        "price": 70000.0
      }
    ],
    "district": "Quận 8",
    "has_parking": true,
    "has_private_room": false,
    "has_outdoor": true,
    "outdoor": true,
    "pet_friendly": true,
    "has_pet_friendly": true,
    "vegetarian_support": false,
    "menus": [
      {
        "name": "Món Đặc Trưng",
        "description": "Các món nổi bật nhất tại Ốc Tuyết - Dương Bá Trạc",
        "items": [
          {
            "name": "Ốc Móng Tay Xào Rau Muống",
            "description": "Món bán chạy hàng đầu tại Ốc Tuyết - Dương Bá Trạc",
            "price": 65000.0,
            "image_url": "https://images.unsplash.com/photo-1515003197210-e0cd71810b5f?w=800"
          },
          {
            "name": "Hàu Nướng Phô Mai",
            "description": "Hương vị đặc sắc được thực khách yêu thích",
            "price": 70000.0,
            "image_url": "https://images.unsplash.com/photo-1515003197210-e0cd71810b5f?w=800"
          }
        ]
      }
    ],
    "images": [
      {
        "image_url": "https://images.unsplash.com/photo-1515003197210-e0cd71810b5f?w=800",
        "caption": "Không gian và món ngon tại Ốc Tuyết - Dương Bá Trạc",
        "is_cover": true
      }
    ],
    "description": "Quán ốc bình dân nổi tiếng Quận 8, ốc tươi chế biến đa dạng sốt bơ tỏi, phô mai, rang muối.",
    "phone_number": "0909443322"
  },
  {
    "id": 90,
    "name": "Lẩu Dê 404 - Phạm Hùng",
    "address": "218 Phạm Hùng, Phường 5, Quận 8, TP. Hồ Chí Minh",
    "lat": 10.7392,
    "lng": 106.6758,
    "category": "bbq",
    "cuisineLabel": "Lẩu Nướng",
    "priceMin": 120000,
    "priceMax": 320000,
    "rating": 4.4,
    "reviews": 380,
    "parking": true,
    "private_room": true,
    "vegetarian": false,
    "openHours": "10:00 - 23:00",
    "image": "https://images.unsplash.com/photo-1529042410759-befb1204b468?w=800",
    "menu": [
      {
        "name": "Lẩu Dê Thuốc Bắc",
        "price": 250000.0
      },
      {
        "name": "Vú Dê Nướng Chao",
        "price": 165000.0
      }
    ],
    "district": "Quận 8",
    "has_parking": true,
    "has_private_room": true,
    "has_outdoor": true,
    "outdoor": true,
    "pet_friendly": false,
    "has_pet_friendly": false,
    "vegetarian_support": false,
    "menus": [
      {
        "name": "Món Đặc Trưng",
        "description": "Các món nổi bật nhất tại Lẩu Dê 404 - Phạm Hùng",
        "items": [
          {
            "name": "Lẩu Dê Thuốc Bắc",
            "description": "Món bán chạy hàng đầu tại Lẩu Dê 404 - Phạm Hùng",
            "price": 250000.0,
            "image_url": "https://images.unsplash.com/photo-1529042410759-befb1204b468?w=800"
          },
          {
            "name": "Vú Dê Nướng Chao",
            "description": "Hương vị đặc sắc được thực khách yêu thích",
            "price": 165000.0,
            "image_url": "https://images.unsplash.com/photo-1529042410759-befb1204b468?w=800"
          }
        ]
      }
    ],
    "images": [
      {
        "image_url": "https://images.unsplash.com/photo-1529042410759-befb1204b468?w=800",
        "caption": "Không gian và món ngon tại Lẩu Dê 404 - Phạm Hùng",
        "is_cover": true
      }
    ],
    "description": "Lẩu dê thuốc bắc và vú dê nướng chao đậm vị, không gian rộng rãi có bãi đậu ô tô.",
    "phone_number": "02838509988"
  },
  {
    "id": 91,
    "name": "Cơm Tấm Tài - Tạ Quang Bửu",
    "address": "812 Tạ Quang Bửu, Phường 5, Quận 8, TP. Hồ Chí Minh",
    "lat": 10.7365,
    "lng": 106.6682,
    "category": "vietnamese",
    "cuisineLabel": "Cơm tấm",
    "priceMin": 45000,
    "priceMax": 85000,
    "rating": 4.5,
    "reviews": 270,
    "parking": true,
    "private_room": false,
    "vegetarian": false,
    "openHours": "06:30 - 21:00",
    "image": "https://images.unsplash.com/photo-1534422298391-e4f8c172dddb?w=800&q=80&auto=format&fit=crop&sig=91",
    "menu": [
      {
        "name": "Cơm Tấm Sườn Bì Chả",
        "price": 62000.0
      },
      {
        "name": "Cơm Tấm Đùi Gà Nướng",
        "price": 65000.0
      }
    ],
    "district": "Quận 8",
    "has_parking": true,
    "has_private_room": false,
    "has_outdoor": false,
    "outdoor": false,
    "pet_friendly": false,
    "has_pet_friendly": false,
    "vegetarian_support": false,
    "menus": [
      {
        "name": "Món Đặc Trưng",
        "description": "Các món nổi bật nhất tại Cơm Tấm Tài - Tạ Quang Bửu",
        "items": [
          {
            "name": "Cơm Tấm Sườn Bì Chả",
            "description": "Món bán chạy hàng đầu tại Cơm Tấm Tài - Tạ Quang Bửu",
            "price": 62000.0,
            "image_url": "https://images.unsplash.com/photo-1534422298391-e4f8c172dddb?w=800&q=80&auto=format&fit=crop&sig=91"
          },
          {
            "name": "Cơm Tấm Đùi Gà Nướng",
            "description": "Hương vị đặc sắc được thực khách yêu thích",
            "price": 65000.0,
            "image_url": "https://images.unsplash.com/photo-1534422298391-e4f8c172dddb?w=800&q=80&auto=format&fit=crop&sig=91"
          }
        ]
      }
    ],
    "images": [
      {
        "image_url": "https://images.unsplash.com/photo-1534422298391-e4f8c172dddb?w=800&q=80&auto=format&fit=crop&sig=91",
        "caption": "Không gian và món ngon tại Cơm Tấm Tài - Tạ Quang Bửu",
        "is_cover": true
      }
    ],
    "description": "Cơm tấm sườn nướng mật ong mềm thấm vị, nước mắm kẹo chuẩn vị Sài Gòn.",
    "phone_number": "0903665544"
  },
  {
    "id": 92,
    "name": "Haidilao Hotpot - Vạn Hạnh Mall",
    "address": "Tầng 6 Vạn Hạnh Mall, 11 Sư Vạn Hạnh, Quận 10, TP. Hồ Chí Minh",
    "lat": 10.7705,
    "lng": 106.67,
    "category": "bbq",
    "cuisineLabel": "Lẩu Nướng",
    "priceMin": 300000,
    "priceMax": 650000,
    "rating": 4.8,
    "reviews": 1450,
    "parking": true,
    "private_room": true,
    "vegetarian": true,
    "openHours": "10:00 - 01:00",
    "image": "https://images.unsplash.com/photo-1546069901-d5bfd2cbfb1f?w=800",
    "menu": [
      {
        "name": "Nồi Lẩu 4 Ngăn (Cà Chua - Mala)",
        "price": 280000.0
      },
      {
        "name": "Thịt Bò Haidilao Thượng Hạng",
        "price": 220000.0
      }
    ],
    "district": "Quận 10",
    "has_parking": true,
    "has_private_room": true,
    "has_outdoor": false,
    "outdoor": false,
    "pet_friendly": false,
    "has_pet_friendly": false,
    "vegetarian_support": true,
    "menus": [
      {
        "name": "Món Đặc Trưng",
        "description": "Các món nổi bật nhất tại Haidilao Hotpot - Vạn Hạnh Mall",
        "items": [
          {
            "name": "Nồi Lẩu 4 Ngăn (Cà Chua - Mala)",
            "description": "Món bán chạy hàng đầu tại Haidilao Hotpot - Vạn Hạnh Mall",
            "price": 280000.0,
            "image_url": "https://images.unsplash.com/photo-1546069901-d5bfd2cbfb1f?w=800"
          },
          {
            "name": "Thịt Bò Haidilao Thượng Hạng",
            "description": "Hương vị đặc sắc được thực khách yêu thích",
            "price": 220000.0,
            "image_url": "https://images.unsplash.com/photo-1546069901-d5bfd2cbfb1f?w=800"
          }
        ]
      }
    ],
    "images": [
      {
        "image_url": "https://images.unsplash.com/photo-1546069901-d5bfd2cbfb1f?w=800",
        "caption": "Không gian và món ngon tại Haidilao Hotpot - Vạn Hạnh Mall",
        "is_cover": true
      }
    ],
    "description": "Thương hiệu lẩu Tứ Xuyên dịch vụ 5 sao tại Vạn Hạnh Mall, nổi tiếng với múa mì và lẩu 4 ngăn.",
    "phone_number": "02838621188"
  },
  {
    "id": 93,
    "name": "Cơm Niêu Thiên Lý - Sư Vạn Hạnh",
    "address": "134 Sư Vạn Hạnh, Phường 12, Quận 10, TP. Hồ Chí Minh",
    "lat": 10.7718,
    "lng": 106.6695,
    "category": "vietnamese",
    "cuisineLabel": "Món Việt",
    "priceMin": 85000,
    "priceMax": 220000,
    "rating": 4.6,
    "reviews": 610,
    "parking": true,
    "private_room": false,
    "vegetarian": true,
    "openHours": "10:00 - 21:30",
    "image": "https://images.unsplash.com/photo-1550547660-d9450f859349?w=800",
    "menu": [
      {
        "name": "Cơm Niêu Cháy Giòn",
        "price": 28000.0
      },
      {
        "name": "Cá Bống Kho Tộ",
        "price": 95000.0
      }
    ],
    "district": "Quận 10",
    "has_parking": true,
    "has_private_room": false,
    "has_outdoor": false,
    "outdoor": false,
    "pet_friendly": false,
    "has_pet_friendly": false,
    "vegetarian_support": true,
    "menus": [
      {
        "name": "Món Đặc Trưng",
        "description": "Các món nổi bật nhất tại Cơm Niêu Thiên Lý - Sư Vạn Hạnh",
        "items": [
          {
            "name": "Cơm Niêu Cháy Giòn",
            "description": "Món bán chạy hàng đầu tại Cơm Niêu Thiên Lý - Sư Vạn Hạnh",
            "price": 28000.0,
            "image_url": "https://images.unsplash.com/photo-1550547660-d9450f859349?w=800"
          },
          {
            "name": "Cá Bống Kho Tộ",
            "description": "Hương vị đặc sắc được thực khách yêu thích",
            "price": 95000.0,
            "image_url": "https://images.unsplash.com/photo-1550547660-d9450f859349?w=800"
          }
        ]
      }
    ],
    "images": [
      {
        "image_url": "https://images.unsplash.com/photo-1550547660-d9450f859349?w=800",
        "caption": "Không gian và món ngon tại Cơm Niêu Thiên Lý - Sư Vạn Hạnh",
        "is_cover": true
      }
    ],
    "description": "Cơm niêu cháy giòn rụm ăn kèm cá kho tộ, thịt kho tiêu và canh cua rau đay chuẩn vị nhà làm.",
    "phone_number": "0978785500"
  },
  {
    "id": 94,
    "name": "Bún Thái Hải Sản Cô Ba - Tô Hiến Thành",
    "address": "245 Tô Hiến Thành, Phường 13, Quận 10, TP. Hồ Chí Minh",
    "lat": 10.7782,
    "lng": 106.6652,
    "category": "other",
    "cuisineLabel": "Món Thái",
    "priceMin": 55000,
    "priceMax": 110000,
    "rating": 4.5,
    "reviews": 430,
    "parking": true,
    "private_room": false,
    "vegetarian": false,
    "openHours": "09:00 - 22:00",
    "image": "https://images.unsplash.com/photo-1555126634-323283e090fa?w=800&q=80&auto=format&fit=crop&sig=94",
    "menu": [
      {
        "name": "Bún Thái Hải Sản Đặc Biệt",
        "price": 75000.0
      },
      {
        "name": "Lẩu Thái Tom Yum Mini",
        "price": 110000.0
      }
    ],
    "district": "Quận 10",
    "has_parking": true,
    "has_private_room": false,
    "has_outdoor": false,
    "outdoor": false,
    "pet_friendly": false,
    "has_pet_friendly": false,
    "vegetarian_support": false,
    "menus": [
      {
        "name": "Món Đặc Trưng",
        "description": "Các món nổi bật nhất tại Bún Thái Hải Sản Cô Ba - Tô Hiến Thành",
        "items": [
          {
            "name": "Bún Thái Hải Sản Đặc Biệt",
            "description": "Món bán chạy hàng đầu tại Bún Thái Hải Sản Cô Ba - Tô Hiến Thành",
            "price": 75000.0,
            "image_url": "https://images.unsplash.com/photo-1555126634-323283e090fa?w=800&q=80&auto=format&fit=crop&sig=94"
          },
          {
            "name": "Lẩu Thái Tom Yum Mini",
            "description": "Hương vị đặc sắc được thực khách yêu thích",
            "price": 110000.0,
            "image_url": "https://images.unsplash.com/photo-1555126634-323283e090fa?w=800&q=80&auto=format&fit=crop&sig=94"
          }
        ]
      }
    ],
    "images": [
      {
        "image_url": "https://images.unsplash.com/photo-1555126634-323283e090fa?w=800&q=80&auto=format&fit=crop&sig=94",
        "caption": "Không gian và món ngon tại Bún Thái Hải Sản Cô Ba - Tô Hiến Thành",
        "is_cover": true
      }
    ],
    "description": "Bún Thái hải sản chua cay đậm đà đầy ắp tôm, mực, bò tái và chả cá.",
    "phone_number": "0909113355"
  },
  {
    "id": 95,
    "name": "Chay Thiền Ý - Ba Tháng Hai",
    "address": "368 Đường 3/2, Phường 12, Quận 10, TP. Hồ Chí Minh",
    "lat": 10.772,
    "lng": 106.6735,
    "category": "vegetarian",
    "cuisineLabel": "Món Chay",
    "priceMin": 50000,
    "priceMax": 160000,
    "rating": 4.6,
    "reviews": 350,
    "parking": true,
    "private_room": true,
    "vegetarian": true,
    "openHours": "08:00 - 21:30",
    "image": "https://images.unsplash.com/photo-1559847844-d721426d6edc?w=800",
    "menu": [
      {
        "name": "Buffet Chay Thanh Tịnh",
        "price": 139000.0
      },
      {
        "name": "Cơm Sen Chay",
        "price": 65000.0
      }
    ],
    "district": "Quận 10",
    "has_parking": true,
    "has_private_room": true,
    "has_outdoor": false,
    "outdoor": false,
    "pet_friendly": false,
    "has_pet_friendly": false,
    "vegetarian_support": true,
    "menus": [
      {
        "name": "Món Đặc Trưng",
        "description": "Các món nổi bật nhất tại Chay Thiền Ý - Ba Tháng Hai",
        "items": [
          {
            "name": "Buffet Chay Thanh Tịnh",
            "description": "Món bán chạy hàng đầu tại Chay Thiền Ý - Ba Tháng Hai",
            "price": 139000.0,
            "image_url": "https://images.unsplash.com/photo-1559847844-d721426d6edc?w=800"
          },
          {
            "name": "Cơm Sen Chay",
            "description": "Hương vị đặc sắc được thực khách yêu thích",
            "price": 65000.0,
            "image_url": "https://images.unsplash.com/photo-1559847844-d721426d6edc?w=800"
          }
        ]
      }
    ],
    "images": [
      {
        "image_url": "https://images.unsplash.com/photo-1559847844-d721426d6edc?w=800",
        "caption": "Không gian và món ngon tại Chay Thiền Ý - Ba Tháng Hai",
        "is_cover": true
      }
    ],
    "description": "Buffet chay và gọi món đa dạng hơn 40 món thanh đạm, không gian ấm cúng ngay trung tâm Quận 10.",
    "phone_number": "02838654433"
  },
  {
    "id": 96,
    "name": "Ốc Quang Anh - Tô Hiến Thành",
    "address": "189 Tô Hiến Thành, Phường 13, Quận 10, TP. Hồ Chí Minh",
    "lat": 10.7775,
    "lng": 106.6665,
    "category": "other",
    "cuisineLabel": "Hải Sản",
    "priceMin": 60000,
    "priceMax": 220000,
    "rating": 4.5,
    "reviews": 780,
    "parking": true,
    "private_room": false,
    "vegetarian": false,
    "openHours": "13:00 - 23:00",
    "image": "https://images.unsplash.com/photo-1565299585323-38d6b0865b47?w=800",
    "menu": [
      {
        "name": "Nghêu Hấp Thái Cay",
        "price": 65000.0
      },
      {
        "name": "Ốc Len Xào Dừa",
        "price": 85000.0
      }
    ],
    "district": "Quận 10",
    "has_parking": true,
    "has_private_room": false,
    "has_outdoor": true,
    "outdoor": true,
    "pet_friendly": false,
    "has_pet_friendly": false,
    "vegetarian_support": false,
    "menus": [
      {
        "name": "Món Đặc Trưng",
        "description": "Các món nổi bật nhất tại Ốc Quang Anh - Tô Hiến Thành",
        "items": [
          {
            "name": "Nghêu Hấp Thái Cay",
            "description": "Món bán chạy hàng đầu tại Ốc Quang Anh - Tô Hiến Thành",
            "price": 65000.0,
            "image_url": "https://images.unsplash.com/photo-1565299585323-38d6b0865b47?w=800"
          },
          {
            "name": "Ốc Len Xào Dừa",
            "description": "Hương vị đặc sắc được thực khách yêu thích",
            "price": 85000.0,
            "image_url": "https://images.unsplash.com/photo-1565299585323-38d6b0865b47?w=800"
          }
        ]
      }
    ],
    "images": [
      {
        "image_url": "https://images.unsplash.com/photo-1565299585323-38d6b0865b47?w=800",
        "caption": "Không gian và món ngon tại Ốc Quang Anh - Tô Hiến Thành",
        "is_cover": true
      }
    ],
    "description": "Quán ốc lâu năm siêu đông khách tại Quận 10, nổi tiếng với nghêu hấp sả và sò điệp nướng mỡ hành.",
    "phone_number": "0903778899"
  },
  {
    "id": 97,
    "name": "Sủi Cảo Thiên Thiên - Hà Tôn Quyền",
    "address": "197 Hà Tôn Quyền, Phường 4, Quận 11, TP. Hồ Chí Minh",
    "lat": 10.7595,
    "lng": 106.6562,
    "category": "other",
    "cuisineLabel": "Món Hoa",
    "priceMin": 55000,
    "priceMax": 130000,
    "rating": 4.6,
    "reviews": 980,
    "parking": true,
    "private_room": false,
    "vegetarian": false,
    "openHours": "13:00 - 23:30",
    "image": "https://images.unsplash.com/photo-1565299507177-b0ac66763828?w=800",
    "menu": [
      {
        "name": "Sủi Cảo Thập Cẩm Nước",
        "price": 68000.0
      },
      {
        "name": "Sủi Cảo Chiên Giòn",
        "price": 72000.0
      }
    ],
    "district": "Quận 11",
    "has_parking": true,
    "has_private_room": false,
    "has_outdoor": true,
    "outdoor": true,
    "pet_friendly": false,
    "has_pet_friendly": false,
    "vegetarian_support": false,
    "menus": [
      {
        "name": "Món Đặc Trưng",
        "description": "Các món nổi bật nhất tại Sủi Cảo Thiên Thiên - Hà Tôn Quyền",
        "items": [
          {
            "name": "Sủi Cảo Thập Cẩm Nước",
            "description": "Món bán chạy hàng đầu tại Sủi Cảo Thiên Thiên - Hà Tôn Quyền",
            "price": 68000.0,
            "image_url": "https://images.unsplash.com/photo-1565299507177-b0ac66763828?w=800"
          },
          {
            "name": "Sủi Cảo Chiên Giòn",
            "description": "Hương vị đặc sắc được thực khách yêu thích",
            "price": 72000.0,
            "image_url": "https://images.unsplash.com/photo-1565299507177-b0ac66763828?w=800"
          }
        ]
      }
    ],
    "images": [
      {
        "image_url": "https://images.unsplash.com/photo-1565299507177-b0ac66763828?w=800",
        "caption": "Không gian và món ngon tại Sủi Cảo Thiên Thiên - Hà Tôn Quyền",
        "is_cover": true
      }
    ],
    "description": "Phố sủi cảo Hà Tôn Quyền trứ danh Quận 11, viên sủi cảo nhân tôm tươi nguyên con giòn ngọt.",
    "phone_number": "02838552233"
  },
  {
    "id": 98,
    "name": "Lẩu Cá Kèo Rau Đắng - Lê Đại Hành",
    "address": "112 Lê Đại Hành, Phường 7, Quận 11, TP. Hồ Chí Minh",
    "lat": 10.7618,
    "lng": 106.6585,
    "category": "vietnamese",
    "cuisineLabel": "Món Việt",
    "priceMin": 90000,
    "priceMax": 250000,
    "rating": 4.5,
    "reviews": 340,
    "parking": true,
    "private_room": false,
    "vegetarian": false,
    "openHours": "10:00 - 22:30",
    "image": "https://images.unsplash.com/photo-1571091718767-18b5b1457add?w=800",
    "menu": [
      {
        "name": "Lẩu Cá Kèo Lá Giang",
        "price": 210000.0
      },
      {
        "name": "Cá Kèo Nướng Muối Ớt",
        "price": 110000.0
      }
    ],
    "district": "Quận 11",
    "has_parking": true,
    "has_private_room": false,
    "has_outdoor": true,
    "outdoor": true,
    "pet_friendly": false,
    "has_pet_friendly": false,
    "vegetarian_support": false,
    "menus": [
      {
        "name": "Món Đặc Trưng",
        "description": "Các món nổi bật nhất tại Lẩu Cá Kèo Rau Đắng - Lê Đại Hành",
        "items": [
          {
            "name": "Lẩu Cá Kèo Lá Giang",
            "description": "Món bán chạy hàng đầu tại Lẩu Cá Kèo Rau Đắng - Lê Đại Hành",
            "price": 210000.0,
            "image_url": "https://images.unsplash.com/photo-1571091718767-18b5b1457add?w=800"
          },
          {
            "name": "Cá Kèo Nướng Muối Ớt",
            "description": "Hương vị đặc sắc được thực khách yêu thích",
            "price": 110000.0,
            "image_url": "https://images.unsplash.com/photo-1571091718767-18b5b1457add?w=800"
          }
        ]
      }
    ],
    "images": [
      {
        "image_url": "https://images.unsplash.com/photo-1571091718767-18b5b1457add?w=800",
        "caption": "Không gian và món ngon tại Lẩu Cá Kèo Rau Đắng - Lê Đại Hành",
        "is_cover": true
      }
    ],
    "description": "Lẩu cá kèo lá giang chua thanh ăn kèm rau đắng, bông điên điển chuẩn miền Tây Nam Bộ.",
    "phone_number": "0908334466"
  },
  {
    "id": 99,
    "name": "Cơm Tấm Hồng Calmette - Lạc Long Quân",
    "address": "256 Lạc Long Quân, Phường 10, Quận 11, TP. Hồ Chí Minh",
    "lat": 10.7665,
    "lng": 106.6458,
    "category": "vietnamese",
    "cuisineLabel": "Cơm tấm",
    "priceMin": 50000,
    "priceMax": 95000,
    "rating": 4.4,
    "reviews": 260,
    "parking": true,
    "private_room": false,
    "vegetarian": false,
    "openHours": "07:00 - 21:00",
    "image": "https://images.unsplash.com/photo-1574484284002-952d92456975?w=800",
    "menu": [
      {
        "name": "Cơm Tấm Sườn Chả Trứng Muối",
        "price": 72000.0
      },
      {
        "name": "Canh Rong Biển Thịt Bằm",
        "price": 25000.0
      }
    ],
    "district": "Quận 11",
    "has_parking": true,
    "has_private_room": false,
    "has_outdoor": false,
    "outdoor": false,
    "pet_friendly": false,
    "has_pet_friendly": false,
    "vegetarian_support": false,
    "menus": [
      {
        "name": "Món Đặc Trưng",
        "description": "Các món nổi bật nhất tại Cơm Tấm Hồng Calmette - Lạc Long Quân",
        "items": [
          {
            "name": "Cơm Tấm Sườn Chả Trứng Muối",
            "description": "Món bán chạy hàng đầu tại Cơm Tấm Hồng Calmette - Lạc Long Quân",
            "price": 72000.0,
            "image_url": "https://images.unsplash.com/photo-1574484284002-952d92456975?w=800"
          },
          {
            "name": "Canh Rong Biển Thịt Bằm",
            "description": "Hương vị đặc sắc được thực khách yêu thích",
            "price": 25000.0,
            "image_url": "https://images.unsplash.com/photo-1574484284002-952d92456975?w=800"
          }
        ]
      }
    ],
    "images": [
      {
        "image_url": "https://images.unsplash.com/photo-1574484284002-952d92456975?w=800",
        "caption": "Không gian và món ngon tại Cơm Tấm Hồng Calmette - Lạc Long Quân",
        "is_cover": true
      }
    ],
    "description": "Cơm tấm sườn nướng than hoa thơm nức mũi, chả trứng muối béo ngậy.",
    "phone_number": "0909221133"
  },
  {
    "id": 100,
    "name": "Lẩu Bò Tơ Tây Ninh - Nguyễn Ảnh Thủ",
    "address": "312 Nguyễn Ảnh Thủ, Phường Hiệp Thành, Quận 12, TP. Hồ Chí Minh",
    "lat": 10.8695,
    "lng": 106.6345,
    "category": "vietnamese",
    "cuisineLabel": "Món Việt",
    "priceMin": 100000,
    "priceMax": 280000,
    "rating": 4.5,
    "reviews": 390,
    "parking": true,
    "private_room": true,
    "vegetarian": false,
    "openHours": "10:00 - 23:00",
    "image": "https://images.unsplash.com/photo-1579584425555-c3ce17fd4351?w=800",
    "menu": [
      {
        "name": "Bò Tơ Luộc Cuốn Bánh Tráng",
        "price": 185000.0
      },
      {
        "name": "Lẩu Xí Quách Bò Tơ",
        "price": 240000.0
      }
    ],
    "district": "Quận 12",
    "has_parking": true,
    "has_private_room": true,
    "has_outdoor": true,
    "outdoor": true,
    "pet_friendly": true,
    "has_pet_friendly": true,
    "vegetarian_support": false,
    "menus": [
      {
        "name": "Món Đặc Trưng",
        "description": "Các món nổi bật nhất tại Lẩu Bò Tơ Tây Ninh - Nguyễn Ảnh Thủ",
        "items": [
          {
            "name": "Bò Tơ Luộc Cuốn Bánh Tráng",
            "description": "Món bán chạy hàng đầu tại Lẩu Bò Tơ Tây Ninh - Nguyễn Ảnh Thủ",
            "price": 185000.0,
            "image_url": "https://images.unsplash.com/photo-1579584425555-c3ce17fd4351?w=800"
          },
          {
            "name": "Lẩu Xí Quách Bò Tơ",
            "description": "Hương vị đặc sắc được thực khách yêu thích",
            "price": 240000.0,
            "image_url": "https://images.unsplash.com/photo-1579584425555-c3ce17fd4351?w=800"
          }
        ]
      }
    ],
    "images": [
      {
        "image_url": "https://images.unsplash.com/photo-1579584425555-c3ce17fd4351?w=800",
        "caption": "Không gian và món ngon tại Lẩu Bò Tơ Tây Ninh - Nguyễn Ảnh Thủ",
        "is_cover": true
      }
    ],
    "description": "Bò tơ Củ Chi tươi ngon chế biến tại chỗ, không gian sân vườn cực rộng có bãi đậu ô tô miễn phí.",
    "phone_number": "0908554422"
  },
  {
    "id": 101,
    "name": "Gogi House - Phan Văn Hớn",
    "address": "88 Phan Văn Hớn, Phường Tân Thới Nhất, Quận 12, TP. Hồ Chí Minh",
    "lat": 10.8315,
    "lng": 106.6185,
    "category": "bbq",
    "cuisineLabel": "Lẩu Nướng",
    "priceMin": 199000,
    "priceMax": 389000,
    "rating": 4.6,
    "reviews": 310,
    "parking": true,
    "private_room": true,
    "vegetarian": false,
    "openHours": "10:00 - 22:00",
    "image": "https://images.unsplash.com/photo-1580476262798-bddd9f4b7369?w=800",
    "menu": [
      {
        "name": "Combo Nướng Gia Đình",
        "price": 369000.0
      },
      {
        "name": "Mì Lạnh Hàn Quốc",
        "price": 99000.0
      }
    ],
    "district": "Quận 12",
    "has_parking": true,
    "has_private_room": true,
    "has_outdoor": false,
    "outdoor": false,
    "pet_friendly": false,
    "has_pet_friendly": false,
    "vegetarian_support": false,
    "menus": [
      {
        "name": "Món Đặc Trưng",
        "description": "Các món nổi bật nhất tại Gogi House - Phan Văn Hớn",
        "items": [
          {
            "name": "Combo Nướng Gia Đình",
            "description": "Món bán chạy hàng đầu tại Gogi House - Phan Văn Hớn",
            "price": 369000.0,
            "image_url": "https://images.unsplash.com/photo-1580476262798-bddd9f4b7369?w=800"
          },
          {
            "name": "Mì Lạnh Hàn Quốc",
            "description": "Hương vị đặc sắc được thực khách yêu thích",
            "price": 99000.0,
            "image_url": "https://images.unsplash.com/photo-1580476262798-bddd9f4b7369?w=800"
          }
        ]
      }
    ],
    "images": [
      {
        "image_url": "https://images.unsplash.com/photo-1580476262798-bddd9f4b7369?w=800",
        "caption": "Không gian và món ngon tại Gogi House - Phan Văn Hớn",
        "is_cover": true
      }
    ],
    "description": "Thịt nướng Hàn Quốc không khói tiện lợi cho cư dân khu vực Quận 12 và Hóc Môn.",
    "phone_number": "02873007399"
  },
  {
    "id": 102,
    "name": "Quán Chay Liên Hoa - Lê Văn Khương",
    "address": "145 Lê Văn Khương, Phường Thới An, Quận 12, TP. Hồ Chí Minh",
    "lat": 10.872,
    "lng": 106.6485,
    "category": "vegetarian",
    "cuisineLabel": "Món Chay",
    "priceMin": 35000,
    "priceMax": 110000,
    "rating": 4.6,
    "reviews": 220,
    "parking": true,
    "private_room": false,
    "vegetarian": true,
    "openHours": "07:00 - 21:00",
    "image": "https://images.unsplash.com/photo-1589302168068-964664d93dc0?w=800",
    "menu": [
      {
        "name": "Lẩu Nấm Chay Liên Hoa",
        "price": 110000.0
      },
      {
        "name": "Hủ Tiếu Chay Nam Vang",
        "price": 42000.0
      }
    ],
    "district": "Quận 12",
    "has_parking": true,
    "has_private_room": false,
    "has_outdoor": true,
    "outdoor": true,
    "pet_friendly": false,
    "has_pet_friendly": false,
    "vegetarian_support": true,
    "menus": [
      {
        "name": "Món Đặc Trưng",
        "description": "Các món nổi bật nhất tại Quán Chay Liên Hoa - Lê Văn Khương",
        "items": [
          {
            "name": "Lẩu Nấm Chay Liên Hoa",
            "description": "Món bán chạy hàng đầu tại Quán Chay Liên Hoa - Lê Văn Khương",
            "price": 110000.0,
            "image_url": "https://images.unsplash.com/photo-1589302168068-964664d93dc0?w=800"
          },
          {
            "name": "Hủ Tiếu Chay Nam Vang",
            "description": "Hương vị đặc sắc được thực khách yêu thích",
            "price": 42000.0,
            "image_url": "https://images.unsplash.com/photo-1589302168068-964664d93dc0?w=800"
          }
        ]
      }
    ],
    "images": [
      {
        "image_url": "https://images.unsplash.com/photo-1589302168068-964664d93dc0?w=800",
        "caption": "Không gian và món ngon tại Quán Chay Liên Hoa - Lê Văn Khương",
        "is_cover": true
      }
    ],
    "description": "Thực đơn chay phong phú, giá bình dân, phục vụ cơm trưa và lẩu chay thanh đạm.",
    "phone_number": "0937889900"
  },
  {
    "id": 103,
    "name": "Kichi Kichi - Aeon Mall Bình Tân",
    "address": "Tầng 3 Aeon Mall Bình Tân, 1 Đường Số 17A, Quận Bình Tân, TP. Hồ Chí Minh",
    "lat": 10.7428,
    "lng": 106.6122,
    "category": "bbq",
    "cuisineLabel": "Lẩu Nướng",
    "priceMin": 239000,
    "priceMax": 329000,
    "rating": 4.6,
    "reviews": 580,
    "parking": true,
    "private_room": false,
    "vegetarian": true,
    "openHours": "10:00 - 22:00",
    "image": "https://images.unsplash.com/photo-1594007654729-407eedc4be65?w=800",
    "menu": [
      {
        "name": "Buffet Lẩu Băng Chuyền",
        "price": 279000.0
      },
      {
        "name": "Nước Lẩu Tom Yum & Nấm",
        "price": 0.0
      }
    ],
    "district": "Quận Bình Tân",
    "has_parking": true,
    "has_private_room": false,
    "has_outdoor": false,
    "outdoor": false,
    "pet_friendly": false,
    "has_pet_friendly": false,
    "vegetarian_support": true,
    "menus": [
      {
        "name": "Món Đặc Trưng",
        "description": "Các món nổi bật nhất tại Kichi Kichi - Aeon Mall Bình Tân",
        "items": [
          {
            "name": "Buffet Lẩu Băng Chuyền",
            "description": "Món bán chạy hàng đầu tại Kichi Kichi - Aeon Mall Bình Tân",
            "price": 279000.0,
            "image_url": "https://images.unsplash.com/photo-1594007654729-407eedc4be65?w=800"
          },
          {
            "name": "Nước Lẩu Tom Yum & Nấm",
            "description": "Hương vị đặc sắc được thực khách yêu thích",
            "price": 0.0,
            "image_url": "https://images.unsplash.com/photo-1594007654729-407eedc4be65?w=800"
          }
        ]
      }
    ],
    "images": [
      {
        "image_url": "https://images.unsplash.com/photo-1594007654729-407eedc4be65?w=800",
        "caption": "Không gian và món ngon tại Kichi Kichi - Aeon Mall Bình Tân",
        "is_cover": true
      }
    ],
    "description": "Lẩu băng chuyền Nhật Bản hiện đại tại Aeon Mall Bình Tân với hơn 80 món nhúng tươi ngon.",
    "phone_number": "02873007988"
  },
  {
    "id": 104,
    "name": "Hải Sản Hoàng Gia - Tên Lửa",
    "address": "168 Tên Lửa, Phường Bình Trị Đông B, Quận Bình Tân, TP. Hồ Chí Minh",
    "lat": 10.7475,
    "lng": 106.6148,
    "category": "other",
    "cuisineLabel": "Hải Sản",
    "priceMin": 180000,
    "priceMax": 850000,
    "rating": 4.6,
    "reviews": 440,
    "parking": true,
    "private_room": true,
    "vegetarian": false,
    "openHours": "10:00 - 23:00",
    "image": "https://images.unsplash.com/photo-1604382354936-07c5d9983bd3?w=800",
    "menu": [
      {
        "name": "Cua Hoàng Đế Hấp",
        "price": 750000.0
      },
      {
        "name": "Tôm Sú Rang Muối Hồng Kông",
        "price": 290000.0
      }
    ],
    "district": "Quận Bình Tân",
    "has_parking": true,
    "has_private_room": true,
    "has_outdoor": true,
    "outdoor": true,
    "pet_friendly": false,
    "has_pet_friendly": false,
    "vegetarian_support": false,
    "menus": [
      {
        "name": "Món Đặc Trưng",
        "description": "Các món nổi bật nhất tại Hải Sản Hoàng Gia - Tên Lửa",
        "items": [
          {
            "name": "Cua Hoàng Đế Hấp",
            "description": "Món bán chạy hàng đầu tại Hải Sản Hoàng Gia - Tên Lửa",
            "price": 750000.0,
            "image_url": "https://images.unsplash.com/photo-1604382354936-07c5d9983bd3?w=800"
          },
          {
            "name": "Tôm Sú Rang Muối Hồng Kông",
            "description": "Hương vị đặc sắc được thực khách yêu thích",
            "price": 290000.0,
            "image_url": "https://images.unsplash.com/photo-1604382354936-07c5d9983bd3?w=800"
          }
        ]
      }
    ],
    "images": [
      {
        "image_url": "https://images.unsplash.com/photo-1604382354936-07c5d9983bd3?w=800",
        "caption": "Không gian và món ngon tại Hải Sản Hoàng Gia - Tên Lửa",
        "is_cover": true
      }
    ],
    "description": "Nhà hàng hải sản cao cấp trục đường Tên Lửa, có nhiều phòng VIP tiếp khách và bãi đậu xe rộng.",
    "phone_number": "02837528899"
  },
  {
    "id": 105,
    "name": "Bò Nướng Ngói Gia Bảo - Tên Lửa",
    "address": "245 Tên Lửa, Phường Bình Trị Đông B, Quận Bình Tân, TP. Hồ Chí Minh",
    "lat": 10.751,
    "lng": 106.6135,
    "category": "bbq",
    "cuisineLabel": "Lẩu Nướng",
    "priceMin": 80000,
    "priceMax": 220000,
    "rating": 4.5,
    "reviews": 360,
    "parking": true,
    "private_room": false,
    "vegetarian": false,
    "openHours": "16:00 - 23:30",
    "image": "https://images.unsplash.com/photo-1608039755401-742074f0548d?w=800",
    "menu": [
      {
        "name": "Bò Tảng Nướng Ngói",
        "price": 135000.0
      },
      {
        "name": "Bạch Tuộc Nướng Sa Tế",
        "price": 115000.0
      }
    ],
    "district": "Quận Bình Tân",
    "has_parking": true,
    "has_private_room": false,
    "has_outdoor": true,
    "outdoor": true,
    "pet_friendly": true,
    "has_pet_friendly": true,
    "vegetarian_support": false,
    "menus": [
      {
        "name": "Món Đặc Trưng",
        "description": "Các món nổi bật nhất tại Bò Nướng Ngói Gia Bảo - Tên Lửa",
        "items": [
          {
            "name": "Bò Tảng Nướng Ngói",
            "description": "Món bán chạy hàng đầu tại Bò Nướng Ngói Gia Bảo - Tên Lửa",
            "price": 135000.0,
            "image_url": "https://images.unsplash.com/photo-1608039755401-742074f0548d?w=800"
          },
          {
            "name": "Bạch Tuộc Nướng Sa Tế",
            "description": "Hương vị đặc sắc được thực khách yêu thích",
            "price": 115000.0,
            "image_url": "https://images.unsplash.com/photo-1608039755401-742074f0548d?w=800"
          }
        ]
      }
    ],
    "images": [
      {
        "image_url": "https://images.unsplash.com/photo-1608039755401-742074f0548d?w=800",
        "caption": "Không gian và món ngon tại Bò Nướng Ngói Gia Bảo - Tên Lửa",
        "is_cover": true
      }
    ],
    "description": "Nướng ngói thơm lừng không khói, giá sinh viên và không gian vỉa hè thoáng mát.",
    "phone_number": "0909664422"
  },
  {
    "id": 106,
    "name": "Phở Lệ - Kinh Dương Vương",
    "address": "303 Kinh Dương Vương, Phường An Lạc, Quận Bình Tân, TP. Hồ Chí Minh",
    "lat": 10.741,
    "lng": 106.6175,
    "category": "vietnamese",
    "cuisineLabel": "Món Việt",
    "priceMin": 70000,
    "priceMax": 115000,
    "rating": 4.6,
    "reviews": 510,
    "parking": true,
    "private_room": false,
    "vegetarian": false,
    "openHours": "06:00 - 22:00",
    "image": "https://images.unsplash.com/photo-1617093727343-374698b1b08d?w=800",
    "menu": [
      {
        "name": "Phở Tái Bò Viên",
        "price": 85000.0
      },
      {
        "name": "Phở Thập Cẩm Đặc Biệt",
        "price": 105000.0
      }
    ],
    "district": "Quận Bình Tân",
    "has_parking": true,
    "has_private_room": false,
    "has_outdoor": false,
    "outdoor": false,
    "pet_friendly": false,
    "has_pet_friendly": false,
    "vegetarian_support": false,
    "menus": [
      {
        "name": "Món Đặc Trưng",
        "description": "Các món nổi bật nhất tại Phở Lệ - Kinh Dương Vương",
        "items": [
          {
            "name": "Phở Tái Bò Viên",
            "description": "Món bán chạy hàng đầu tại Phở Lệ - Kinh Dương Vương",
            "price": 85000.0,
            "image_url": "https://images.unsplash.com/photo-1617093727343-374698b1b08d?w=800"
          },
          {
            "name": "Phở Thập Cẩm Đặc Biệt",
            "description": "Hương vị đặc sắc được thực khách yêu thích",
            "price": 105000.0,
            "image_url": "https://images.unsplash.com/photo-1617093727343-374698b1b08d?w=800"
          }
        ]
      }
    ],
    "images": [
      {
        "image_url": "https://images.unsplash.com/photo-1617093727343-374698b1b08d?w=800",
        "caption": "Không gian và món ngon tại Phở Lệ - Kinh Dương Vương",
        "is_cover": true
      }
    ],
    "description": "Thương hiệu Phở Lệ danh tiếng Sài Gòn với nước dùng béo ngọt đậm đà và bò viên giòn sần sật.",
    "phone_number": "02838751122"
  },
  {
    "id": 107,
    "name": "Ẩm Thực Sinh Thái Bình Xuyên - Bình Chánh",
    "address": "C3/18 Phạm Hùng, Xã Bình Hưng, Huyện Bình Chánh, TP. Hồ Chí Minh",
    "lat": 10.7255,
    "lng": 106.6785,
    "category": "vietnamese",
    "cuisineLabel": "Món Việt",
    "priceMin": 120000,
    "priceMax": 420000,
    "rating": 4.6,
    "reviews": 1120,
    "parking": true,
    "private_room": true,
    "vegetarian": true,
    "openHours": "09:00 - 23:00",
    "image": "https://images.unsplash.com/photo-1623428187969-5da2dcea5ebf?w=800",
    "menu": [
      {
        "name": "Gà Nướng Lu Xôi Cháy",
        "price": 280000.0
      },
      {
        "name": "Cá Tai Tượng Chiên Xù",
        "price": 220000.0
      }
    ],
    "district": "Huyện Bình Chánh",
    "has_parking": true,
    "has_private_room": true,
    "has_outdoor": true,
    "outdoor": true,
    "pet_friendly": true,
    "has_pet_friendly": true,
    "vegetarian_support": true,
    "menus": [
      {
        "name": "Món Đặc Trưng",
        "description": "Các món nổi bật nhất tại Ẩm Thực Sinh Thái Bình Xuyên - Bình Chánh",
        "items": [
          {
            "name": "Gà Nướng Lu Xôi Cháy",
            "description": "Món bán chạy hàng đầu tại Ẩm Thực Sinh Thái Bình Xuyên - Bình Chánh",
            "price": 280000.0,
            "image_url": "https://images.unsplash.com/photo-1623428187969-5da2dcea5ebf?w=800"
          },
          {
            "name": "Cá Tai Tượng Chiên Xù",
            "description": "Hương vị đặc sắc được thực khách yêu thích",
            "price": 220000.0,
            "image_url": "https://images.unsplash.com/photo-1623428187969-5da2dcea5ebf?w=800"
          }
        ]
      }
    ],
    "images": [
      {
        "image_url": "https://images.unsplash.com/photo-1623428187969-5da2dcea5ebf?w=800",
        "caption": "Không gian và món ngon tại Ẩm Thực Sinh Thái Bình Xuyên - Bình Chánh",
        "is_cover": true
      }
    ],
    "description": "Khu ẩm thực sinh thái sân vườn ven hồ cực lớn ở Bình Chánh, nổi tiếng với gà nướng lu và hải sản.",
    "phone_number": "02854316316"
  },
  {
    "id": 108,
    "name": "Lẩu Mắm Bà Dú - Trung Sơn Bình Chánh",
    "address": "92 Đường 9A, KDC Trung Sơn, Huyện Bình Chánh, TP. Hồ Chí Minh",
    "lat": 10.7335,
    "lng": 106.6895,
    "category": "vietnamese",
    "cuisineLabel": "Món Việt",
    "priceMin": 95000,
    "priceMax": 260000,
    "rating": 4.6,
    "reviews": 540,
    "parking": true,
    "private_room": true,
    "vegetarian": false,
    "openHours": "10:00 - 22:00",
    "image": "https://images.unsplash.com/photo-1626804475297-41608ea09aeb?w=800",
    "menu": [
      {
        "name": "Lẩu Mắm Thập Cẩm Miền Tây",
        "price": 245000.0
      },
      {
        "name": "Cá Kèo Kho Tộ",
        "price": 115000.0
      }
    ],
    "district": "Huyện Bình Chánh",
    "has_parking": true,
    "has_private_room": true,
    "has_outdoor": false,
    "outdoor": false,
    "pet_friendly": false,
    "has_pet_friendly": false,
    "vegetarian_support": false,
    "menus": [
      {
        "name": "Món Đặc Trưng",
        "description": "Các món nổi bật nhất tại Lẩu Mắm Bà Dú - Trung Sơn Bình Chánh",
        "items": [
          {
            "name": "Lẩu Mắm Thập Cẩm Miền Tây",
            "description": "Món bán chạy hàng đầu tại Lẩu Mắm Bà Dú - Trung Sơn Bình Chánh",
            "price": 245000.0,
            "image_url": "https://images.unsplash.com/photo-1626804475297-41608ea09aeb?w=800"
          },
          {
            "name": "Cá Kèo Kho Tộ",
            "description": "Hương vị đặc sắc được thực khách yêu thích",
            "price": 115000.0,
            "image_url": "https://images.unsplash.com/photo-1626804475297-41608ea09aeb?w=800"
          }
        ]
      }
    ],
    "images": [
      {
        "image_url": "https://images.unsplash.com/photo-1626804475297-41608ea09aeb?w=800",
        "caption": "Không gian và món ngon tại Lẩu Mắm Bà Dú - Trung Sơn Bình Chánh",
        "is_cover": true
      }
    ],
    "description": "Lẩu mắm miền Tây chuẩn vị với hơn 15 loại rau đồng nội tươi rói tại khu Trung Sơn.",
    "phone_number": "02854318899"
  },
  {
    "id": 109,
    "name": "Nhà Hàng Sân Vườn Phú Xuân - Nhà Bè",
    "address": "1850 Huỳnh Tấn Phát, Thị trấn Nhà Bè, Huyện Nhà Bè, TP. Hồ Chí Minh",
    "lat": 10.6953,
    "lng": 106.7312,
    "category": "other",
    "cuisineLabel": "Hải Sản",
    "priceMin": 110000,
    "priceMax": 380000,
    "rating": 4.5,
    "reviews": 310,
    "parking": true,
    "private_room": true,
    "vegetarian": false,
    "openHours": "09:30 - 23:00",
    "image": "https://images.unsplash.com/photo-1509722747041-616f39b57569?w=800",
    "menu": [
      {
        "name": "Tôm Càng Xanh Nướng Mọi",
        "price": 290000.0
      },
      {
        "name": "Lẩu Cá Ngát Nấu Chua",
        "price": 210000.0
      }
    ],
    "district": "Huyện Nhà Bè",
    "has_parking": true,
    "has_private_room": true,
    "has_outdoor": true,
    "outdoor": true,
    "pet_friendly": true,
    "has_pet_friendly": true,
    "vegetarian_support": false,
    "menus": [
      {
        "name": "Món Đặc Trưng",
        "description": "Các món nổi bật nhất tại Nhà Hàng Sân Vườn Phú Xuân - Nhà Bè",
        "items": [
          {
            "name": "Tôm Càng Xanh Nướng Mọi",
            "description": "Món bán chạy hàng đầu tại Nhà Hàng Sân Vườn Phú Xuân - Nhà Bè",
            "price": 290000.0,
            "image_url": "https://images.unsplash.com/photo-1509722747041-616f39b57569?w=800"
          },
          {
            "name": "Lẩu Cá Ngát Nấu Chua",
            "description": "Hương vị đặc sắc được thực khách yêu thích",
            "price": 210000.0,
            "image_url": "https://images.unsplash.com/photo-1509722747041-616f39b57569?w=800"
          }
        ]
      }
    ],
    "images": [
      {
        "image_url": "https://images.unsplash.com/photo-1509722747041-616f39b57569?w=800",
        "caption": "Không gian và món ngon tại Nhà Hàng Sân Vườn Phú Xuân - Nhà Bè",
        "is_cover": true
      }
    ],
    "description": "Không gian chòi lá ven sông thoáng mát tại Nhà Bè, chuyên tôm càng xanh và cá sông tươi sống.",
    "phone_number": "0908991122"
  },
  {
    "id": 110,
    "name": "Bò Tơ Xuân Đào - Hóc Môn",
    "address": "215 Quốc Lộ 22, Xã Tân Xuân, Huyện Hóc Môn, TP. Hồ Chí Minh",
    "lat": 10.8839,
    "lng": 106.5912,
    "category": "vietnamese",
    "cuisineLabel": "Món Việt",
    "priceMin": 90000,
    "priceMax": 280000,
    "rating": 4.6,
    "reviews": 620,
    "parking": true,
    "private_room": true,
    "vegetarian": false,
    "openHours": "09:00 - 22:30",
    "image": "https://images.unsplash.com/photo-1512058564366-18510be2db19?w=800",
    "menu": [
      {
        "name": "Bò Tơ Hấp Gừng Cuốn Rau Rừng",
        "price": 190000.0
      },
      {
        "name": "Thăn Bò Tơ Nướng Y",
        "price": 210000.0
      }
    ],
    "district": "Huyện Hóc Môn",
    "has_parking": true,
    "has_private_room": true,
    "has_outdoor": true,
    "outdoor": true,
    "pet_friendly": true,
    "has_pet_friendly": true,
    "vegetarian_support": false,
    "menus": [
      {
        "name": "Món Đặc Trưng",
        "description": "Các món nổi bật nhất tại Bò Tơ Xuân Đào - Hóc Môn",
        "items": [
          {
            "name": "Bò Tơ Hấp Gừng Cuốn Rau Rừng",
            "description": "Món bán chạy hàng đầu tại Bò Tơ Xuân Đào - Hóc Môn",
            "price": 190000.0,
            "image_url": "https://images.unsplash.com/photo-1512058564366-18510be2db19?w=800"
          },
          {
            "name": "Thăn Bò Tơ Nướng Y",
            "description": "Hương vị đặc sắc được thực khách yêu thích",
            "price": 210000.0,
            "image_url": "https://images.unsplash.com/photo-1512058564366-18510be2db19?w=800"
          }
        ]
      }
    ],
    "images": [
      {
        "image_url": "https://images.unsplash.com/photo-1512058564366-18510be2db19?w=800",
        "caption": "Không gian và món ngon tại Bò Tơ Xuân Đào - Hóc Môn",
        "is_cover": true
      }
    ],
    "description": "Đặc sản bò tơ Củ Chi - Hóc Môn nổi tiếng nhiều năm, thịt mềm ngọt và không gian sân vườn rộng rãi.",
    "phone_number": "02838912233"
  }
];
