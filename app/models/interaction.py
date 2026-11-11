# filepath: app/models/interaction.py
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime
from app.core.database import Base


class Restaurant(Base):
    """Bảng lưu trữ thông tin Nhà hàng & Tọa độ địa lý (Restaurants)"""
    __tablename__ = "restaurants"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(150), nullable=False, index=True)
    address = Column(String(255), nullable=False)
    latitude = Column(Float, nullable=False, index=True)
    longitude = Column(Float, nullable=False, index=True)
    category = Column(String(100), nullable=True, default="Món Việt")
    price_min = Column(Integer, nullable=True, default=50000)
    price_max = Column(Integer, nullable=True, default=200000)
    rating_avg = Column(Float, nullable=True, default=4.5)
    open_time = Column(String(20), nullable=True, default="08:00")
    close_time = Column(String(20), nullable=True, default="22:00")
    image_url = Column(String(500), nullable=True)
    status = Column(String(20), nullable=False, default="active")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)