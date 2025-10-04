from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Screenshot(Base):
    """Модель скриншота приложения"""
    __tablename__ = "screenshots"
    
    id = Column(Integer, primary_key=True, index=True)
    app_id = Column(Integer, ForeignKey("apps.id"), nullable=False)
    image_url = Column(String(500), nullable=False)
    order_index = Column(Integer, default=0)  # Порядок отображения скриншотов
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Связи
    app = relationship("App", back_populates="screenshots")
    
    def __repr__(self):
        return f"<Screenshot(id={self.id}, app_id={self.app_id})>"
    
    def to_dict(self):
        """Преобразование объекта в словарь для API"""
        return {
            "id": self.id,
            "app_id": self.app_id,
            "image_url": self.image_url,
            "order_index": self.order_index,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
