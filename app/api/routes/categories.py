from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.services.category_service import CategoryService
from app.schemas.category import CategoryResponse, CategoryCreate, CategoryUpdate

router = APIRouter()

@router.get("/", response_model=List[CategoryResponse])
async def get_categories(db: Session = Depends(get_db)):
    """Получить все категории"""
    category_service = CategoryService(db)
    categories = category_service.get_categories()
    return categories

@router.get("/{category_id}", response_model=CategoryResponse)
async def get_category(category_id: int, db: Session = Depends(get_db)):
    """Получить категорию по ID"""
    category_service = CategoryService(db)
    category = category_service.get_category_by_id(category_id)
    
    if not category:
        raise HTTPException(status_code=404, detail="Категория не найдена")
    
    return category

@router.post("/", response_model=CategoryResponse)
async def create_category(category_data: CategoryCreate, db: Session = Depends(get_db)):
    """Создать новую категорию"""
    category_service = CategoryService(db)
    try:
        category = category_service.create_category(category_data)
        return category
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{category_id}", response_model=CategoryResponse)
async def update_category(
    category_id: int, 
    category_data: CategoryUpdate, 
    db: Session = Depends(get_db)
):
    """Обновить категорию"""
    category_service = CategoryService(db)
    category = category_service.update_category(category_id, category_data)
    
    if not category:
        raise HTTPException(status_code=404, detail="Категория не найдена")
    
    return category

@router.delete("/{category_id}")
async def delete_category(category_id: int, db: Session = Depends(get_db)):
    """Удалить категорию"""
    category_service = CategoryService(db)
    success = category_service.delete_category(category_id)
    
    if not success:
        raise HTTPException(status_code=404, detail="Категория не найдена")
    
    return {"message": "Категория успешно удалена"}

@router.get("/{category_id}/verify")
async def verify_category_integrity(category_id: int, db: Session = Depends(get_db)):
    """Проверить целостность данных категории"""
    category_service = CategoryService(db)
    is_valid = category_service.verify_category_integrity(category_id)
    
    if not is_valid:
        raise HTTPException(status_code=400, detail="Данные категории повреждены")
    
    return {"message": "Данные категории целостны", "category_id": category_id}

@router.post("/{category_id}/recalculate-hash")
async def recalculate_category_hash(category_id: int, db: Session = Depends(get_db)):
    """Пересчитать хеш категории"""
    category_service = CategoryService(db)
    new_hash = category_service.recalculate_category_hash(category_id)
    
    if not new_hash:
        raise HTTPException(status_code=404, detail="Категория не найдена")
    
    return {"message": "Хеш пересчитан", "category_id": category_id, "new_hash": new_hash}