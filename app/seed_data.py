"""
Скрипт для заполнения базы данных тестовыми данными
"""
import sys
import json
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')

from app.database import SessionLocal, engine
from app.models.app import App
from app.models.category import Category
from app.models.screenshot import Screenshot
from app.database import Base
from app.utils.hash_utils import HashUtils

def load_categories_from_json():
    """Загрузка категорий из JSON файла"""
    data_dir = Path(__file__).parent.parent / "data"
    categories_file = data_dir / "categories.json"
    
    try:
        with open(categories_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"⚠️ Файл {categories_file} не найден")
        return []

def create_categories():
    """Создание категорий"""
    categories_data = load_categories_from_json()
    
    db = SessionLocal()
    try:
        for cat_data in categories_data:
            # Создаем временный объект для вычисления хеша
            category = Category(**cat_data)
            category_dict = HashUtils.get_data_for_hash(category)
            expected_hash = HashUtils.calculate_category_hash(category_dict)
            
            # Проверяем, существует ли уже категория с таким хешем
            existing_by_hash = db.query(Category).filter(Category.data_hash == expected_hash).first()
            if existing_by_hash:
                print(f"   ⚠️  Категория '{cat_data['name']}' уже существует (пропускаем)")
            else:
                # Проверяем, существует ли категория с таким именем, но с другим хешем
                existing_by_name = db.query(Category).filter(Category.name == cat_data["name"]).first()
                if existing_by_name:
                    # Обновляем существующую категорию
                    existing_by_name.description = cat_data["description"]
                    existing_by_name.tag = cat_data["tag"]
                    existing_by_name.tag_color = cat_data["tag_color"]
                    existing_by_name.data_hash = expected_hash
                    print(f"   🔄 Обновлена категория: {cat_data['name']}")
                else:
                    # Создаем новую категорию
                    category.data_hash = expected_hash  # Устанавливаем хеш перед сохранением
                    db.add(category)
                    db.flush()  # Получаем ID категории
                    print(f"   ✅ Создана категория: {cat_data['name']}")
        
        db.commit()
        print("✅ Категории созданы")
    except Exception as e:
        print(f"❌ Ошибка при создании категорий: {e}")
        db.rollback()
    finally:
        db.close()

def load_apps_from_json():
    """Загрузка приложений из JSON файлов"""
    data_dir = Path(__file__).parent.parent / "data"
    apps_dir = data_dir / "apps"
    apps_data = []
    
    if not apps_dir.exists():
        print(f"⚠️  Директория {apps_dir} не найдена")
        return []
    
    # Загружаем все JSON файлы из директории apps
    for json_file in apps_dir.glob("*.json"):
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                app_data = json.load(f)
                apps_data.append(app_data)
                print(f"   📄 Загружен файл: {json_file.name}")
        except Exception as e:
            print(f"   ❌ Ошибка при загрузке {json_file.name}: {e}")
    
    return apps_data

def create_apps():
    """Создание приложений"""
    db = SessionLocal()
    try:
        # Получаем категории
        categories = db.query(Category).all()
        category_map = {cat.name: cat.id for cat in categories}
        
        # Загружаем данные из JSON файлов
        apps_data = load_apps_from_json()
        
        for app_data in apps_data:
            # Проверяем, что категория существует
            if app_data["category_name"] not in category_map:
                print(f"   ⚠️  Категория '{app_data['category_name']}' не найдена для приложения '{app_data['name']}' (пропускаем)")
                continue
                
            # Создаем временный объект для вычисления хеша
            app = App(
                name=app_data["name"],
                description=app_data["description"],
                short_description=app_data["short_description"],
                company=app_data["company"],
                icon_url=app_data["icon_url"],
                header_image_url=app_data["header_image_url"],
                category_id=category_map[app_data["category_name"]],
                age_rating=app_data["age_rating"],
                apk_url=app_data["apk_url"],
                rating=app_data["rating"],
                file_size=app_data["file_size"],
                downloads=app_data["downloads"]
            )
            app_dict = HashUtils.get_data_for_hash(app)
            expected_hash = HashUtils.calculate_app_hash(app_dict)
            
            # Проверяем, существует ли уже приложение с таким хешем
            existing_by_hash = db.query(App).filter(App.data_hash == expected_hash).first()
            if existing_by_hash:
                print(f"   ⚠️  Приложение '{app_data['name']}' уже существует (пропускаем)")
            else:
                # Проверяем, существует ли приложение с таким именем, но с другим хешем
                existing_by_name = db.query(App).filter(App.name == app_data["name"]).first()
                if existing_by_name:
                    # Обновляем существующее приложение
                    existing_by_name.description = app_data["description"]
                    existing_by_name.short_description = app_data["short_description"]
                    existing_by_name.company = app_data["company"]
                    existing_by_name.icon_url = app_data["icon_url"]
                    existing_by_name.header_image_url = app_data["header_image_url"]
                    existing_by_name.category_id = category_map[app_data["category_name"]]
                    existing_by_name.age_rating = app_data["age_rating"]
                    existing_by_name.apk_url = app_data["apk_url"]
                    existing_by_name.rating = app_data["rating"]
                    existing_by_name.file_size = app_data["file_size"]
                    existing_by_name.downloads = app_data["downloads"]
                    existing_by_name.data_hash = expected_hash
                    
                    # Удаляем старые скриншоты
                    db.query(Screenshot).filter(Screenshot.app_id == existing_by_name.id).delete()
                    
                    # Добавляем новые скриншоты
                    for i, screenshot_url in enumerate(app_data["screenshots"]):
                        screenshot = Screenshot(
                            app_id=existing_by_name.id,
                            image_url=screenshot_url,
                            order_index=i
                        )
                        db.add(screenshot)
                    
                    print(f"   🔄 Обновлено приложение: {app_data['name']}")
                else:
                    # Создаем новое приложение
                    app.data_hash = expected_hash  # Устанавливаем хеш перед сохранением
                    
                    db.add(app)
                    db.flush()  # Получаем ID приложения
                    
                    # Добавляем скриншоты
                    for i, screenshot_url in enumerate(app_data["screenshots"]):
                        screenshot = Screenshot(
                            app_id=app.id,
                            image_url=screenshot_url,
                            order_index=i
                        )
                        db.add(screenshot)
                    
                    print(f"   ✅ Создано приложение: {app_data['name']}")
        
        db.commit()
        print("✅ Приложения созданы")
    except Exception as e:
        print(f"❌ Ошибка при создании приложений: {e}")
        db.rollback()
    finally:
        db.close()

def seed_database():
    """Заполнение базы данных тестовыми данными"""
    print("Начинаем заполнение базы данных...")
    
    # Создаем таблицы
    Base.metadata.create_all(bind=engine)
    print("✅ Таблицы созданы")
    
    # Создаем категории
    create_categories()
    
    # Создаем приложения
    create_apps()
    
    print("База данных успешно заполнена!")

if __name__ == "__main__":
    seed_database()
