"""
Скрипт для заполнения базы данных тестовыми данными
"""
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app.models.app import App
from app.models.category import Category
from app.models.screenshot import Screenshot
from app.database import Base
from app.utils.hash_utils import HashUtils

def create_categories():
    """Создание категорий"""
    categories_data = [
        {
            "name": "Финансы",
            "description": "Банковские приложения, кошельки, инвестиции"
        },
        {
            "name": "Инструменты", 
            "description": "Полезные утилиты и инструменты"
        },
        {
            "name": "Игры",
            "description": "Мобильные игры и развлечения"
        },
        {
            "name": "Государственные",
            "description": "Госуслуги и официальные приложения"
        },
        {
            "name": "Транспорт",
            "description": "Такси, каршеринг, общественный транспорт"
        }
    ]
    
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

def create_apps():
    """Создание приложений"""
    db = SessionLocal()
    try:
        # Получаем категории
        categories = db.query(Category).all()
        category_map = {cat.name: cat.id for cat in categories}
        
        apps_data = [
            {
                "name": "Сбербанк Онлайн",
                "description": "Мобильное приложение Сбербанка для управления финансами, переводами и платежами. Безопасные операции с картами и вкладами.",
                "short_description": "Управление финансами и картами",
                "company": "Сбербанк",
                "icon_url": "https://example.com/sberbank-icon.png",
                "header_image_url": "https://example.com/sberbank-header.png",
                "category_name": "Финансы",
                "age_rating": "0+",
                "apk_url": "https://example.com/sberbank.apk",
                "screenshots": [
                    "https://example.com/sberbank-1.png",
                    "https://example.com/sberbank-2.png",
                    "https://example.com/sberbank-3.png"
                ]
            },
            {
                "name": "ВТБ Онлайн",
                "description": "Официальное приложение ВТБ для мобильного банкинга. Переводы, платежи, управление картами и вкладами.",
                "short_description": "Мобильный банк ВТБ",
                "company": "ВТБ",
                "icon_url": "https://example.com/vtb-icon.png",
                "header_image_url": "https://example.com/vtb-header.png",
                "category_name": "Финансы",
                "age_rating": "0+",
                "apk_url": "https://example.com/vtb.apk",
                "screenshots": [
                    "https://example.com/vtb-1.png",
                    "https://example.com/vtb-2.png"
                ]
            },
            {
                "name": "Госуслуги",
                "description": "Единый портал государственных услуг. Получение справок, запись к врачу, оплата штрафов и налогов.",
                "short_description": "Государственные услуги онлайн",
                "company": "Минцифры России",
                "icon_url": "https://example.com/gosuslugi-icon.png",
                "header_image_url": "https://example.com/gosuslugi-header.png",
                "category_name": "Государственные",
                "age_rating": "0+",
                "apk_url": "https://example.com/gosuslugi.apk",
                "screenshots": [
                    "https://example.com/gosuslugi-1.png",
                    "https://example.com/gosuslugi-2.png",
                    "https://example.com/gosuslugi-3.png",
                    "https://example.com/gosuslugi-4.png"
                ]
            },
            {
                "name": "Яндекс.Такси",
                "description": "Заказ такси в любом городе России. Быстро, удобно и безопасно. Отслеживание поездки в реальном времени.",
                "short_description": "Заказ такси онлайн",
                "company": "Яндекс",
                "icon_url": "https://example.com/yandex-taxi-icon.png",
                "header_image_url": "https://example.com/yandex-taxi-header.png",
                "category_name": "Транспорт",
                "age_rating": "0+",
                "apk_url": "https://example.com/yandex-taxi.apk",
                "screenshots": [
                    "https://example.com/yandex-taxi-1.png",
                    "https://example.com/yandex-taxi-2.png"
                ]
            },
            {
                "name": "Telegram",
                "description": "Быстрый и безопасный мессенджер. Отправка сообщений, файлов, голосовых и видеозвонков.",
                "short_description": "Безопасный мессенджер",
                "company": "Telegram FZ-LLC",
                "icon_url": "https://example.com/telegram-icon.png",
                "header_image_url": "https://example.com/telegram-header.png",
                "category_name": "Инструменты",
                "age_rating": "12+",
                "apk_url": "https://example.com/telegram.apk",
                "screenshots": [
                    "https://example.com/telegram-1.png",
                    "https://example.com/telegram-2.png",
                    "https://example.com/telegram-3.png"
                ]
            },
            {
                "name": "2048",
                "description": "Классическая головоломка с числами. Объединяйте плитки с одинаковыми числами, чтобы получить 2048!",
                "short_description": "Головоломка с числами",
                "company": "Gabriele Cirulli",
                "icon_url": "https://example.com/2048-icon.png",
                "header_image_url": "https://example.com/2048-header.png",
                "category_name": "Игры",
                "age_rating": "0+",
                "apk_url": "https://example.com/2048.apk",
                "screenshots": [
                    "https://example.com/2048-1.png",
                    "https://example.com/2048-2.png"
                ]
            }
        ]
        
        for app_data in apps_data:
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
                apk_url=app_data["apk_url"]
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
