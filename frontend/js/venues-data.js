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
    "district": "Quận 1"
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
    "district": "Quận 1"
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
    "district": "Quận 1"
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
    "district": "Quận 1"
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
    "district": "Quận 1"
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
    "district": "Quận 1"
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
    "district": "Quận 1"
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
    "district": "Quận 1"
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
    "district": "Quận 1"
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
    "district": "Quận 1"
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
    "district": "Quận 1"
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
    "district": "Quận 1"
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
    "district": "Quận 1"
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
    "district": "Quận 1"
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
    "district": "Quận 1"
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
    "district": "Quận 3"
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
    "district": "Quận 3"
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
    "district": "Quận 3"
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
    "district": "Quận 3"
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
    "district": "Quận 3"
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
    "district": "Quận 3"
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
    "district": "Quận 3"
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
    "district": "Quận 3"
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
    "district": "Quận 3"
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
    "district": "Quận 3"
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
    "district": "Quận Bình Thạnh"
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
    "district": "Quận Bình Thạnh"
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
    "district": "Quận Bình Thạnh"
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
    "district": "Quận Bình Thạnh"
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
    "district": "Quận Bình Thạnh"
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
    "district": "Quận Bình Thạnh"
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
    "district": "Quận Bình Thạnh"
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
    "district": "Quận Bình Thạnh"
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
    "district": "Quận Bình Thạnh"
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
    "district": "Quận Bình Thạnh"
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
    "district": "Quận Bình Thạnh"
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
    "district": "Quận Bình Thạnh"
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
    "district": "Quận Bình Thạnh"
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
    "district": "TP. Thủ Đức"
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
    "district": "TP. Thủ Đức"
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
    "district": "TP. Thủ Đức"
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
    "district": "TP. Thủ Đức"
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
    "district": "TP. Thủ Đức"
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
    "district": "TP. Thủ Đức"
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
    "district": "TP. Thủ Đức"
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
    "district": "TP. Thủ Đức"
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
    "district": "TP. Thủ Đức"
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
    "district": "TP. Thủ Đức"
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
    "district": "TP. Thủ Đức"
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
    "district": "TP. Thủ Đức"
  }
];
