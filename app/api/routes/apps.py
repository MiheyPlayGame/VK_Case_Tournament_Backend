from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.services.app_service import AppService
from app.schemas.app import AppResponse, AppCreate, AppUpdate, AppListResponse

router = APIRouter()

@router.get("/", response_model=List[AppListResponse])
async def get_apps(
    category_id: Optional[int] = Query(None, description="ID категории для фильтрации"),
    limit: int = Query(50, ge=1, le=100, description="Количество приложений на странице"),
    offset: int = Query(0, ge=0, description="Смещение для пагинации"),
    db: Session = Depends(get_db)
):
    """Получить список приложений"""
    app_service = AppService(db)
    apps = app_service.get_apps(category_id=category_id, limit=limit, offset=offset)
    return apps

@router.get("/search", response_model=List[AppListResponse])
async def search_apps(
    q: str = Query(..., description="Поисковый запрос"),
    limit: int = Query(50, ge=1, le=100, description="Количество результатов"),
    offset: int = Query(0, ge=0, description="Смещение для пагинации"),
    db: Session = Depends(get_db)
):
    """Поиск приложений"""
    app_service = AppService(db)
    apps = app_service.search_apps(query=q, limit=limit, offset=offset)
    return apps

@router.get("/{app_id}", response_model=AppResponse)
async def get_app(app_id: int, db: Session = Depends(get_db)):
    """Получить приложение по ID"""
    app_service = AppService(db)
    app = app_service.get_app_by_id(app_id)
    
    if not app:
        raise HTTPException(status_code=404, detail="Приложение не найдено")
    
    return app

@router.post("/", response_model=AppResponse)
async def create_app(app_data: AppCreate, db: Session = Depends(get_db)):
    """Создать новое приложение"""
    app_service = AppService(db)
    try:
        app = app_service.create_app(app_data)
        return app
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{app_id}", response_model=AppResponse)
async def update_app(
    app_id: int, 
    app_data: AppUpdate, 
    db: Session = Depends(get_db)
):
    """Обновить приложение"""
    app_service = AppService(db)
    app = app_service.update_app(app_id, app_data)
    
    if not app:
        raise HTTPException(status_code=404, detail="Приложение не найдено")
    
    return app

@router.delete("/{app_id}")
async def delete_app(app_id: int, db: Session = Depends(get_db)):
    """Удалить приложение"""
    app_service = AppService(db)
    success = app_service.delete_app(app_id)
    
    if not success:
        raise HTTPException(status_code=404, detail="Приложение не найдено")
    
    return {"message": "Приложение успешно удалено"}

@router.get("/{app_id}/verify")
async def verify_app_integrity(app_id: int, db: Session = Depends(get_db)):
    """Проверить целостность данных приложения"""
    app_service = AppService(db)
    is_valid = app_service.verify_app_integrity(app_id)
    
    if not is_valid:
        raise HTTPException(status_code=400, detail="Данные приложения повреждены")
    
    return {"message": "Данные приложения целостны", "app_id": app_id}

@router.post("/{app_id}/recalculate-hash")
async def recalculate_app_hash(app_id: int, db: Session = Depends(get_db)):
    """Пересчитать хеш приложения"""
    app_service = AppService(db)
    new_hash = app_service.recalculate_app_hash(app_id)
    
    if not new_hash:
        raise HTTPException(status_code=404, detail="Приложение не найдено")
    
    return {"message": "Хеш пересчитан", "app_id": app_id, "new_hash": new_hash}