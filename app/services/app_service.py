from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import List, Optional, Dict, Any
from app.models.app import App
from app.models.screenshot import Screenshot
from app.schemas.app import AppCreate, AppUpdate
from app.utils.hash_utils import HashUtils
from fastapi import HTTPException

class AppService:
    """Сервис для работы с приложениями"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_apps(self, category_id: Optional[int] = None, limit: int = 50, offset: int = 0) -> List[App]:
        """Получить список приложений"""
        query = self.db.query(App).filter(App.is_active == True)
        
        if category_id:
            query = query.filter(App.category_id == category_id)
        
        return query.offset(offset).limit(limit).all()
    
    def get_app_by_id(self, app_id: int) -> Optional[App]:
        """Получить приложение по ID"""
        return self.db.query(App).filter(
            and_(App.id == app_id, App.is_active == True)
        ).first()
    
    def get_app_by_hash(self, data_hash: str) -> Optional[App]:
        """Получить приложение по хешу данных"""
        return self.db.query(App).filter(
            and_(App.data_hash == data_hash, App.is_active == True)
        ).first()
    
    def create_app(self, app_data: AppCreate) -> App:
        """Создать новое приложение"""
        # Создаем временный объект для вычисления хеша
        app = App(
            name=app_data.name,
            description=app_data.description,
            short_description=app_data.short_description,
            company=app_data.company,
            icon_url=app_data.icon_url,
            category_id=app_data.category_id,
            age_rating=app_data.age_rating,
            apk_url=app_data.apk_url,
            rating=app_data.rating,
            file_size=app_data.file_size,
            downloads=app_data.downloads
        )
        app_dict = HashUtils.get_data_for_hash(app)
        expected_hash = HashUtils.calculate_app_hash(app_dict)
        
        # Проверяем, что приложение с таким хешем не существует
        existing_app = self.get_app_by_hash(expected_hash)
        if existing_app:
            raise HTTPException(status_code=400, detail="Приложение с такими данными уже существует")
        
        self.db.add(app)
        self.db.flush()  # Получаем ID приложения
        
        # Добавляем скриншоты
        if app_data.screenshots:
            for screenshot_data in app_data.screenshots:
                screenshot = Screenshot(
                    app_id=app.id,
                    image_url=screenshot_data.image_url,
                    order_index=screenshot_data.order_index
                )
                self.db.add(screenshot)
        
        # Вычисляем и сохраняем хеш данных
        app_dict = HashUtils.get_data_for_hash(app)
        app.data_hash = HashUtils.calculate_app_hash(app_dict)
        
        self.db.commit()
        self.db.refresh(app)
        return app
    
    def update_app(self, app_id: int, app_data: AppUpdate) -> Optional[App]:
        """Обновить приложение"""
        app = self.get_app_by_id(app_id)
        if not app:
            return None
        
        # Создаем временный объект с обновленными данными для проверки хеша
        update_data = app_data.dict(exclude_unset=True)
        temp_app = App(
            name=update_data.get('name', app.name),
            description=update_data.get('description', app.description),
            short_description=update_data.get('short_description', app.short_description),
            company=update_data.get('company', app.company),
            icon_url=update_data.get('icon_url', app.icon_url),
            category_id=update_data.get('category_id', app.category_id),
            age_rating=update_data.get('age_rating', app.age_rating),
            apk_url=update_data.get('apk_url', app.apk_url),
            rating=update_data.get('rating', app.rating),
            file_size=update_data.get('file_size', app.file_size),
            downloads=update_data.get('downloads', app.downloads)
        )
        temp_app_dict = HashUtils.get_data_for_hash(temp_app)
        expected_hash = HashUtils.calculate_app_hash(temp_app_dict)
        
        # Проверяем, что приложение с таким хешем не существует (кроме текущего)
        existing_app = self.get_app_by_hash(expected_hash)
        if existing_app and existing_app.id != app_id:
            raise HTTPException(status_code=400, detail="Приложение с такими данными уже существует")
        
        # Применяем обновления
        for field, value in update_data.items():
            setattr(app, field, value)
        
        # Пересчитываем хеш после обновления
        app_dict = HashUtils.get_data_for_hash(app)
        app.data_hash = HashUtils.calculate_app_hash(app_dict)
        
        self.db.commit()
        self.db.refresh(app)
        return app
    
    def delete_app(self, app_id: int) -> bool:
        """Удалить приложение (мягкое удаление)"""
        app = self.get_app_by_id(app_id)
        if not app:
            return False
        
        app.is_active = False
        self.db.commit()
        return True
    
    def search_apps(self, query: str, limit: int = 50, offset: int = 0) -> List[App]:
        """Поиск приложений по названию и описанию"""
        return self.db.query(App).filter(
            and_(
                App.is_active == True,
                App.name.ilike(f"%{query}%")
            )
        ).offset(offset).limit(limit).all()
    
    def verify_app_integrity(self, app_id: int) -> bool:
        """Проверка целостности данных приложения"""
        app = self.get_app_by_id(app_id)
        if not app or not app.data_hash:
            return False
        
        app_dict = HashUtils.get_data_for_hash(app)
        return HashUtils.verify_data_integrity(app_dict, app.data_hash)
    
    def recalculate_app_hash(self, app_id: int) -> Optional[str]:
        """Пересчитать хеш приложения"""
        app = self.get_app_by_id(app_id)
        if not app:
            return None
        
        app_dict = HashUtils.get_data_for_hash(app)
        new_hash = HashUtils.calculate_app_hash(app_dict)
        app.data_hash = new_hash
        
        self.db.commit()
        return new_hash
    
    def get_featured_apps(self, limit: int = 5) -> List[App]:
        """Получить топ приложений по рейтингу"""
        return self.db.query(App).filter(
            and_(App.is_active == True, App.rating.isnot(None))
        ).order_by(App.rating.desc()).limit(limit).all()
    
    def find_duplicate_apps(self) -> List[Dict[str, Any]]:
        """Найти дублирующиеся приложения по хешу"""
        from sqlalchemy import func
        
        # Находим хеши, которые встречаются более одного раза
        duplicate_hashes = self.db.query(App.data_hash).filter(
            App.is_active == True
        ).group_by(App.data_hash).having(func.count(App.id) > 1).all()
        
        duplicates = []
        for (data_hash,) in duplicate_hashes:
            apps_with_same_hash = self.db.query(App).filter(
                and_(App.data_hash == data_hash, App.is_active == True)
            ).all()
            
            duplicates.append({
                "hash": data_hash,
                "count": len(apps_with_same_hash),
                "apps": [{"id": app.id, "name": app.name} for app in apps_with_same_hash]
            })
        
        return duplicates
