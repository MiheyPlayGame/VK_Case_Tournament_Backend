from pydantic import BaseModel, HttpUrl
from typing import Optional, List
from datetime import datetime

class ScreenshotBase(BaseModel):
    """Базовая схема скриншота"""
    image_url: str
    order_index: int = 0

class ScreenshotCreate(ScreenshotBase):
    """Схема для создания скриншота"""
    pass

class ScreenshotResponse(ScreenshotBase):
    """Схема ответа скриншота"""
    id: int
    app_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class AppBase(BaseModel):
    """Базовая схема приложения"""
    name: str
    description: str
    short_description: str
    company: str
    icon_url: str
    header_image_url: Optional[str] = None
    category_id: int
    age_rating: str = "0+"
    apk_url: Optional[str] = None
    rating: Optional[float] = None
    file_size: Optional[float] = None
    downloads: Optional[str] = None

class AppCreate(AppBase):
    """Схема для создания приложения"""
    screenshots: Optional[List[ScreenshotCreate]] = []

class AppUpdate(BaseModel):
    """Схема для обновления приложения"""
    name: Optional[str] = None
    description: Optional[str] = None
    short_description: Optional[str] = None
    company: Optional[str] = None
    icon_url: Optional[str] = None
    header_image_url: Optional[str] = None
    category_id: Optional[int] = None
    age_rating: Optional[str] = None
    apk_url: Optional[str] = None
    is_active: Optional[bool] = None
    rating: Optional[float] = None
    file_size: Optional[float] = None
    downloads: Optional[str] = None

class AppResponse(AppBase):
    """Схема ответа приложения"""
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    screenshots: List[ScreenshotResponse] = []
    
    class Config:
        from_attributes = True

class AppListResponse(BaseModel):
    """Схема для списка приложений (упрощенная версия)"""
    id: int
    name: str
    short_description: str
    company: str
    icon_url: str
    header_image_url: Optional[str] = None
    category_id: int
    age_rating: str
    rating: Optional[float] = None
    
    class Config:
        from_attributes = True
