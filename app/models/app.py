from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Boolean, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class App(Base):
    """Модель приложения"""
    __tablename__ = "apps"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=False)
    short_description = Column(String(500), nullable=False)
    company = Column(String(255), nullable=False)
    icon_url = Column(String(500), nullable=False)
    header_image_url = Column(String(500), nullable=True)  # Ссылка на изображение заголовка
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    age_rating = Column(String(10), nullable=False, default="0+")
    apk_url = Column(String(500), nullable=True)  # Ссылка на APK файл
    is_active = Column(Boolean, default=True)
    data_hash = Column(String(64), nullable=True)  # SHA-256 хеш данных для проверки целостности
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    rating = Column(Float, nullable=True)
    file_size = Column(Float, nullable=True)
    downloads = Column(String(64), nullable=True)
    
    # Связи
    category = relationship("Category", back_populates="apps")
    screenshots = relationship("Screenshot", back_populates="app", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<App(id={self.id}, name='{self.name}')>"
    
    def to_dict(self):
        """Преобразование объекта в словарь для API"""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "short_description": self.short_description,
            "company": self.company,
            "icon_url": self.icon_url,
            "header_image_url": self.header_image_url,
            "category_id": self.category_id,
            "age_rating": self.age_rating,
            "apk_url": self.apk_url,
            "is_active": self.is_active,
            "data_hash": self.data_hash,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "rating": self.rating,
            "file_size": self.file_size,
            "downloads": self.downloads
        }
