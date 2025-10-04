from pydantic import BaseModel
from typing import Optional

class CategoryBase(BaseModel):
    """Базовая схема категории"""
    name: str
    description: Optional[str] = None
    tag: Optional[str] = None
    tag_color: Optional[str] = None

class CategoryCreate(CategoryBase):
    """Схема для создания категории"""
    pass

class CategoryUpdate(BaseModel):
    """Схема для обновления категории"""
    name: Optional[str] = None
    description: Optional[str] = None
    tag: Optional[str] = None
    tag_color: Optional[str] = None

class CategoryResponse(CategoryBase):
    """Схема ответа категории"""
    id: int
    apps_count: int
    
    class Config:
        from_attributes = True
