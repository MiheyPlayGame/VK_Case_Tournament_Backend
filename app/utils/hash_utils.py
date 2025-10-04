"""
Утилиты для хеширования данных и проверки целостности
"""
import hashlib
import json
from typing import Any, Dict, Optional


class HashUtils:
    """Утилиты для работы с хешами данных"""
    
    @staticmethod
    def calculate_data_hash(data: Dict[str, Any], exclude_fields: Optional[list] = None) -> str:
        """
        Вычисляет хеш для данных
        
        Args:
            data: Словарь с данными для хеширования
            exclude_fields: Поля, которые нужно исключить из хеширования
            
        Returns:
            SHA-256 хеш в виде строки
        """
        default_exclude = ['id', 'created_at', 'updated_at', 'data_hash']
        if exclude_fields is None:
            exclude_fields = default_exclude
        else:
            exclude_fields = list(set(exclude_fields + default_exclude))
        
        # Создаем копию данных без исключенных полей
        hash_data = {k: v for k, v in data.items() if k not in exclude_fields}
        
        # Сортируем ключи для консистентности
        sorted_data = dict(sorted(hash_data.items()))
        
        # Преобразуем в JSON строку
        json_str = json.dumps(sorted_data, sort_keys=True, ensure_ascii=False)
        
        # Вычисляем SHA-256 хеш
        return hashlib.sha256(json_str.encode('utf-8')).hexdigest()
    
    @staticmethod
    def verify_data_integrity(data: Dict[str, Any], stored_hash: str, exclude_fields: Optional[list] = None) -> bool:
        """
        Проверяет целостность данных по хешу
        
        Args:
            data: Данные для проверки
            stored_hash: Сохраненный хеш
            exclude_fields: Поля, которые нужно исключить из хеширования
            
        Returns:
            True если данные не изменились, False если изменились
        """
        current_hash = HashUtils.calculate_data_hash(data, exclude_fields)
        return current_hash == stored_hash
    
    @staticmethod
    def calculate_app_hash(app_data: Dict[str, Any]) -> str:
        """
        Вычисляет хеш для приложения
        
        Args:
            app_data: Данные приложения
            
        Returns:
            SHA-256 хеш приложения
        """
        return HashUtils.calculate_data_hash(app_data)
    
    @staticmethod
    def calculate_category_hash(category_data: Dict[str, Any]) -> str:
        """
        Вычисляет хеш для категории
        
        Args:
            category_data: Данные категории
            
        Returns:
            SHA-256 хеш категории
        """
        return HashUtils.calculate_data_hash(category_data)
    
    @staticmethod
    def get_data_for_hash(obj: Any) -> Dict[str, Any]:
        """
        Преобразует объект в словарь для хеширования
        
        Args:
            obj: Объект модели SQLAlchemy
            
        Returns:
            Словарь с данными объекта
        """
        if hasattr(obj, 'to_dict'):
            return obj.to_dict()
        elif hasattr(obj, '__dict__'):
            # Исключаем служебные поля SQLAlchemy
            return {k: v for k, v in obj.__dict__.items() 
                   if not k.startswith('_') and k not in ['id', 'created_at', 'updated_at', 'data_hash']}
        else:
            return {}
