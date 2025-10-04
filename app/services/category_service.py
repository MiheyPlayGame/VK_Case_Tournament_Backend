from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from app.models.category import Category
from app.schemas.category import CategoryCreate, CategoryUpdate
from app.utils.hash_utils import HashUtils
from fastapi import HTTPException

class CategoryService:
    """Сервис для работы с категориями"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_categories(self) -> List[Category]:
        """Получить все категории"""
        return self.db.query(Category).all()
    
    def get_category_by_id(self, category_id: int) -> Optional[Category]:
        """Получить категорию по ID"""
        return self.db.query(Category).filter(Category.id == category_id).first()
    
    def get_category_by_name(self, name: str) -> Optional[Category]:
        """Получить категорию по названию"""
        return self.db.query(Category).filter(Category.name == name).first()
    
    def get_category_by_hash(self, data_hash: str) -> Optional[Category]:
        """Получить категорию по хешу данных"""
        return self.db.query(Category).filter(Category.data_hash == data_hash).first()
    
    def create_category(self, category_data: CategoryCreate) -> Category:
        """Создать новую категорию"""
        # Создаем временный объект для вычисления хеша
        temp_category = Category(
            name=category_data.name,
            description=category_data.description
        )
        temp_category_dict = HashUtils.get_data_for_hash(temp_category)
        expected_hash = HashUtils.calculate_category_hash(temp_category_dict)
        
        # Проверяем, что категория с таким хешем не существует
        existing_category = self.get_category_by_hash(expected_hash)
        if existing_category:
            raise HTTPException(status_code=400, detail="Категория с такими данными уже существует")
        
        category = Category(
            name=category_data.name,
            description=category_data.description
        )
        
        self.db.add(category)
        self.db.flush()  # Получаем ID категории
        
        # Вычисляем и сохраняем хеш данных
        category_dict = HashUtils.get_data_for_hash(category)
        category.data_hash = HashUtils.calculate_category_hash(category_dict)
        
        self.db.commit()
        self.db.refresh(category)
        return category
    
    def update_category(self, category_id: int, category_data: CategoryUpdate) -> Optional[Category]:
        """Обновить категорию"""
        category = self.get_category_by_id(category_id)
        if not category:
            return None
        
        # Создаем временный объект с обновленными данными для проверки хеша
        update_data = category_data.dict(exclude_unset=True)
        temp_category = Category(
            name=update_data.get('name', category.name),
            description=update_data.get('description', category.description)
        )
        temp_category_dict = HashUtils.get_data_for_hash(temp_category)
        expected_hash = HashUtils.calculate_category_hash(temp_category_dict)
        
        # Проверяем, что категория с таким хешем не существует (кроме текущей)
        existing_category = self.get_category_by_hash(expected_hash)
        if existing_category and existing_category.id != category_id:
            raise HTTPException(status_code=400, detail="Категория с такими данными уже существует")
        
        # Применяем обновления
        for field, value in update_data.items():
            setattr(category, field, value)
        
        # Пересчитываем хеш после обновления
        category_dict = HashUtils.get_data_for_hash(category)
        category.data_hash = HashUtils.calculate_category_hash(category_dict)
        
        self.db.commit()
        self.db.refresh(category)
        return category
    
    def delete_category(self, category_id: int) -> bool:
        """Удалить категорию"""
        category = self.get_category_by_id(category_id)
        if not category:
            return False
        
        self.db.delete(category)
        self.db.commit()
        return True
    
    def verify_category_integrity(self, category_id: int) -> bool:
        """Проверка целостности данных категории"""
        category = self.get_category_by_id(category_id)
        if not category or not category.data_hash:
            return False
        
        category_dict = HashUtils.get_data_for_hash(category)
        return HashUtils.verify_data_integrity(category_dict, category.data_hash)
    
    def recalculate_category_hash(self, category_id: int) -> Optional[str]:
        """Пересчитать хеш категории"""
        category = self.get_category_by_id(category_id)
        if not category:
            return None
        
        category_dict = HashUtils.get_data_for_hash(category)
        new_hash = HashUtils.calculate_category_hash(category_dict)
        category.data_hash = new_hash
        
        self.db.commit()
        return new_hash
    
    def find_duplicate_categories(self) -> List[Dict[str, Any]]:
        """Найти дублирующиеся категории по хешу"""
        from sqlalchemy import func
        
        # Находим хеши, которые встречаются более одного раза
        duplicate_hashes = self.db.query(Category.data_hash).group_by(
            Category.data_hash
        ).having(func.count(Category.id) > 1).all()
        
        duplicates = []
        for (data_hash,) in duplicate_hashes:
            categories_with_same_hash = self.db.query(Category).filter(
                Category.data_hash == data_hash
            ).all()
            
            duplicates.append({
                "hash": data_hash,
                "count": len(categories_with_same_hash),
                "categories": [{"id": cat.id, "name": cat.name} for cat in categories_with_same_hash]
            })
        
        return duplicates
