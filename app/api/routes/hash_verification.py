"""
API маршруты для проверки целостности данных
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.hash_verification_service import HashVerificationService

router = APIRouter()

@router.get("/verify-all")
async def verify_all_data_integrity(db: Session = Depends(get_db)):
    """Проверить целостность всех данных в базе"""
    hash_service = HashVerificationService(db)
    results = hash_service.verify_all_data()
    return results

@router.get("/verify-categories")
async def verify_categories_integrity(db: Session = Depends(get_db)):
    """Проверить целостность всех категорий"""
    hash_service = HashVerificationService(db)
    results = hash_service.verify_categories_integrity()
    return results

@router.get("/verify-apps")
async def verify_apps_integrity(db: Session = Depends(get_db)):
    """Проверить целостность всех приложений"""
    hash_service = HashVerificationService(db)
    results = hash_service.verify_apps_integrity()
    return results

@router.post("/fix-corrupted")
async def fix_corrupted_data(db: Session = Depends(get_db)):
    """Исправить поврежденные данные, пересчитав хеши"""
    hash_service = HashVerificationService(db)
    results = hash_service.fix_corrupted_data()
    return results

@router.post("/recalculate-all")
async def recalculate_all_hashes(db: Session = Depends(get_db)):
    """Пересчитать все хеши в базе данных"""
    hash_service = HashVerificationService(db)
    results = hash_service.recalculate_all_hashes()
    return results

@router.get("/duplicates")
async def find_duplicates(db: Session = Depends(get_db)):
    """Найти дублирующиеся записи по хешу"""
    from app.services.app_service import AppService
    from app.services.category_service import CategoryService
    
    app_service = AppService(db)
    category_service = CategoryService(db)
    
    return {
        "apps": app_service.find_duplicate_apps(),
        "categories": category_service.find_duplicate_categories()
    }
