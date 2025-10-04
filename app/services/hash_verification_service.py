"""
Сервис для проверки целостности данных с помощью хешей
"""
from sqlalchemy.orm import Session
from typing import List, Dict, Any, Tuple
from app.models.app import App
from app.models.category import Category
from app.utils.hash_utils import HashUtils


class HashVerificationService:
    """Сервис для проверки целостности данных"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def verify_all_data(self) -> Dict[str, Any]:
        """
        Проверяет целостность всех данных в базе
        
        Returns:
            Словарь с результатами проверки
        """
        results = {
            "categories": self.verify_categories_integrity(),
            "apps": self.verify_apps_integrity(),
            "summary": {}
        }
        
        # Подсчитываем общую статистику
        total_categories = len(results["categories"]["verified"]) + len(results["categories"]["corrupted"])
        total_apps = len(results["apps"]["verified"]) + len(results["apps"]["corrupted"])
        
        results["summary"] = {
            "total_categories": total_categories,
            "corrupted_categories": len(results["categories"]["corrupted"]),
            "total_apps": total_apps,
            "corrupted_apps": len(results["apps"]["corrupted"]),
            "overall_integrity": (total_categories + total_apps - 
                                len(results["categories"]["corrupted"]) - 
                                len(results["apps"]["corrupted"])) / (total_categories + total_apps) * 100
        }
        
        return results
    
    def verify_categories_integrity(self) -> Dict[str, List[Dict[str, Any]]]:
        """
        Проверяет целостность всех категорий
        
        Returns:
            Словарь с результатами проверки категорий
        """
        categories = self.db.query(Category).all()
        verified = []
        corrupted = []
        
        for category in categories:
            if not category.data_hash:
                corrupted.append({
                    "id": category.id,
                    "name": category.name,
                    "issue": "No hash found"
                })
                continue
            
            category_dict = HashUtils.get_data_for_hash(category)
            is_valid = HashUtils.verify_data_integrity(category_dict, category.data_hash)
            
            if is_valid:
                verified.append({
                    "id": category.id,
                    "name": category.name,
                    "hash": category.data_hash
                })
            else:
                corrupted.append({
                    "id": category.id,
                    "name": category.name,
                    "stored_hash": category.data_hash,
                    "calculated_hash": HashUtils.calculate_category_hash(category_dict),
                    "issue": "Hash mismatch"
                })
        
        return {
            "verified": verified,
            "corrupted": corrupted
        }
    
    def verify_apps_integrity(self) -> Dict[str, List[Dict[str, Any]]]:
        """
        Проверяет целостность всех приложений
        
        Returns:
            Словарь с результатами проверки приложений
        """
        apps = self.db.query(App).filter(App.is_active == True).all()
        verified = []
        corrupted = []
        
        for app in apps:
            if not app.data_hash:
                corrupted.append({
                    "id": app.id,
                    "name": app.name,
                    "issue": "No hash found"
                })
                continue
            
            app_dict = HashUtils.get_data_for_hash(app)
            is_valid = HashUtils.verify_data_integrity(app_dict, app.data_hash)
            
            if is_valid:
                verified.append({
                    "id": app.id,
                    "name": app.name,
                    "hash": app.data_hash
                })
            else:
                corrupted.append({
                    "id": app.id,
                    "name": app.name,
                    "stored_hash": app.data_hash,
                    "calculated_hash": HashUtils.calculate_app_hash(app_dict),
                    "issue": "Hash mismatch"
                })
        
        return {
            "verified": verified,
            "corrupted": corrupted
        }
    
    def fix_corrupted_data(self) -> Dict[str, Any]:
        """
        Исправляет поврежденные данные, пересчитывая хеши
        
        Returns:
            Словарь с результатами исправления
        """
        results = self.verify_all_data()
        fixed = {
            "categories": {"fixed": [], "failed": []},
            "apps": {"fixed": [], "failed": []}
        }
        
        # Исправляем категории
        for corrupted_category in results["categories"]["corrupted"]:
            try:
                category = self.db.query(Category).filter(
                    Category.id == corrupted_category["id"]
                ).first()
                
                if category:
                    category_dict = HashUtils.get_data_for_hash(category)
                    new_hash = HashUtils.calculate_category_hash(category_dict)
                    category.data_hash = new_hash
                    
                    fixed["categories"]["fixed"].append({
                        "id": category.id,
                        "name": category.name,
                        "new_hash": new_hash
                    })
                else:
                    fixed["categories"]["failed"].append({
                        "id": corrupted_category["id"],
                        "issue": "Category not found"
                    })
            except Exception as e:
                fixed["categories"]["failed"].append({
                    "id": corrupted_category["id"],
                    "issue": f"Error: {str(e)}"
                })
        
        # Исправляем приложения
        for corrupted_app in results["apps"]["corrupted"]:
            try:
                app = self.db.query(App).filter(
                    App.id == corrupted_app["id"]
                ).first()
                
                if app:
                    app_dict = HashUtils.get_data_for_hash(app)
                    new_hash = HashUtils.calculate_app_hash(app_dict)
                    app.data_hash = new_hash
                    
                    fixed["apps"]["fixed"].append({
                        "id": app.id,
                        "name": app.name,
                        "new_hash": new_hash
                    })
                else:
                    fixed["apps"]["failed"].append({
                        "id": corrupted_app["id"],
                        "issue": "App not found"
                    })
            except Exception as e:
                fixed["apps"]["failed"].append({
                    "id": corrupted_app["id"],
                    "issue": f"Error: {str(e)}"
                })
        
        # Сохраняем изменения
        try:
            self.db.commit()
            fixed["commit_success"] = True
        except Exception as e:
            self.db.rollback()
            fixed["commit_success"] = False
            fixed["commit_error"] = str(e)
        
        return fixed
    
    def recalculate_all_hashes(self) -> Dict[str, Any]:
        """
        Пересчитывает все хеши в базе данных
        
        Returns:
            Словарь с результатами пересчета
        """
        results = {
            "categories": {"recalculated": 0, "errors": []},
            "apps": {"recalculated": 0, "errors": []}
        }
        
        # Пересчитываем хеши категорий
        categories = self.db.query(Category).all()
        for category in categories:
            try:
                category_dict = HashUtils.get_data_for_hash(category)
                new_hash = HashUtils.calculate_category_hash(category_dict)
                category.data_hash = new_hash
                results["categories"]["recalculated"] += 1
            except Exception as e:
                results["categories"]["errors"].append({
                    "id": category.id,
                    "name": category.name,
                    "error": str(e)
                })
        
        # Пересчитываем хеши приложений
        apps = self.db.query(App).filter(App.is_active == True).all()
        for app in apps:
            try:
                app_dict = HashUtils.get_data_for_hash(app)
                new_hash = HashUtils.calculate_app_hash(app_dict)
                app.data_hash = new_hash
                results["apps"]["recalculated"] += 1
            except Exception as e:
                results["apps"]["errors"].append({
                    "id": app.id,
                    "name": app.name,
                    "error": str(e)
                })
        
        # Сохраняем изменения
        try:
            self.db.commit()
            results["commit_success"] = True
        except Exception as e:
            self.db.rollback()
            results["commit_success"] = False
            results["commit_error"] = str(e)
        
        return results
