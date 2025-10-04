from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base

class Category(Base):
    """Модель категории приложений"""
    __tablename__ = "categories"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True, index=True)
    description = Column(String(500), nullable=True)
    tag = Column(String(10), nullable=True)
    tag_color = Column(String(9), nullable=True)
    data_hash = Column(String(64), nullable=True)  # SHA-256 хеш данных для проверки целостности
    
    # Связи
    apps = relationship("App", back_populates="category")
    
    def __repr__(self):
        return f"<Category(id={self.id}, name='{self.name}')>"
    
    @property
    def apps_count(self):
        """Количество приложений в категории"""
        return len(self.apps) if self.apps else 0
    
    def to_dict(self):
        """Преобразование объекта в словарь для API"""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "tag": self.tag,
            "tag_color": self.tag_color,
            "data_hash": self.data_hash,
            "apps_count": self.apps_count
        }
