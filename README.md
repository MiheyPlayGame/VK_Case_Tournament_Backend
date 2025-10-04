# RuStore Backend API

Backend API для мобильного приложения RuStore - российского магазина мобильных приложений.

## Описание

Этот проект представляет собой REST API для витрины мобильных приложений, разработанный на Python с использованием FastAPI, SQLAlchemy и Pydantic.

## Функциональность

- 📱 Управление приложениями (CRUD операции)
- 📂 Управление категориями приложений
- 🔍 Поиск приложений по названию и описанию
- 📸 Управление скриншотами приложений
- 🏷️ Фильтрация приложений по категориям
- 📄 Пагинация результатов
- 🔒 CORS настройки для работы с мобильными приложениями
- 🔐 Проверка целостности данных с помощью хешей
- 🛠️ Автоматическое исправление поврежденных данных
- 🔍 Поиск дублирующихся записей
- ❤️ Health check endpoint для мониторинга

## Технологии

- **FastAPI** - современный веб-фреймворк для создания API
- **SQLAlchemy** - ORM для работы с базой данных
- **Pydantic** - валидация данных и сериализация
- **SQLite** - база данных (по умолчанию)
- **Uvicorn** - ASGI сервер
- **python-dotenv** - управление переменными окружения
- **Alembic** - миграции базы данных
- **python-multipart** - обработка multipart данных
- **python-jose** - работа с JWT токенами
- **passlib** - хеширование паролей
- **pytest** - тестирование
- **httpx** - HTTP клиент для тестов

## Установка и запуск

### 1. Клонирование репозитория
```bash
git clone <repository-url>
cd VK_Case_Tournament_Backend
```

### 2. Установка зависимостей
```bash
pip install -r requirements.txt
```

### 3. Заполнение базы данных тестовыми данными
```bash
python app/seed_data.py
```

### 4. Запуск сервера
```bash
python run.py
```

Сервер будет доступен по адресу: http://localhost:8000

## API Документация

После запуска сервера документация API будет доступна по адресам:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Структура проекта

```
app/
├── __init__.py
├── main.py                 # Точка входа приложения
├── database.py            # Конфигурация базы данных
├── seed_data.py           # Скрипт заполнения тестовыми данными
├── models/                # Модели данных (SQLAlchemy)
│   ├── __init__.py
│   ├── app.py            # Модель приложения
│   ├── category.py       # Модель категории
│   └── screenshot.py     # Модель скриншота
├── schemas/               # Схемы Pydantic
│   ├── __init__.py
│   ├── app.py            # Схемы для приложений
│   └── category.py       # Схемы для категорий
├── services/              # Бизнес-логика
│   ├── __init__.py
│   ├── app_service.py    # Сервис приложений
│   ├── category_service.py # Сервис категорий
│   └── hash_verification_service.py # Сервис проверки целостности
├── utils/                 # Утилиты
│   ├── __init__.py
│   └── hash_utils.py     # Утилиты для хеширования
└── api/                   # API роуты
    ├── __init__.py
    └── routes/
        ├── __init__.py
        ├── apps.py        # Роуты приложений
        ├── categories.py  # Роуты категорий
        └── hash_verification.py # Роуты проверки целостности
```

## API Endpoints

### Приложения
- `GET /api/v1/apps/` - Получить список приложений
- `GET /api/v1/apps/{app_id}` - Получить приложение по ID
- `GET /api/v1/apps/search` - Поиск приложений
- `POST /api/v1/apps/` - Создать приложение
- `PUT /api/v1/apps/{app_id}` - Обновить приложение
- `DELETE /api/v1/apps/{app_id}` - Удалить приложение

### Категории
- `GET /api/v1/categories/` - Получить все категории
- `GET /api/v1/categories/{category_id}` - Получить категорию по ID
- `POST /api/v1/categories/` - Создать категорию
- `PUT /api/v1/categories/{category_id}` - Обновить категорию
- `DELETE /api/v1/categories/{category_id}` - Удалить категорию

### Проверка целостности данных
- `GET /api/v1/hash/verify-all` - Проверить целостность всех данных
- `GET /api/v1/hash/verify-categories` - Проверить целостность категорий
- `GET /api/v1/hash/verify-apps` - Проверить целостность приложений
- `POST /api/v1/hash/fix-corrupted` - Исправить поврежденные данные
- `POST /api/v1/hash/recalculate-all` - Пересчитать все хеши
- `GET /api/v1/hash/duplicates` - Найти дублирующиеся записи

### Системные
- `GET /` - Информация о API
- `GET /health` - Проверка состояния сервера

## Примеры использования

### Получение списка приложений
```bash
curl http://localhost:8000/api/v1/apps/
```

### Поиск приложений
```bash
curl "http://localhost:8000/api/v1/apps/search?q=банк"
```

### Фильтрация по категории
```bash
curl "http://localhost:8000/api/v1/apps/?category_id=1"
```

### Получение всех категорий
```bash
curl http://localhost:8000/api/v1/categories/
```

### Проверка целостности данных
```bash
# Проверить целостность всех данных
curl http://localhost:8000/api/v1/hash/verify-all

# Проверить только категории
curl http://localhost:8000/api/v1/hash/verify-categories

# Проверить только приложения
curl http://localhost:8000/api/v1/hash/verify-apps

# Исправить поврежденные данные
curl -X POST http://localhost:8000/api/v1/hash/fix-corrupted

# Пересчитать все хеши
curl -X POST http://localhost:8000/api/v1/hash/recalculate-all

# Найти дублирующиеся записи
curl http://localhost:8000/api/v1/hash/duplicates
```

### Системные запросы
```bash
# Информация о API
curl http://localhost:8000/

# Проверка состояния сервера
curl http://localhost:8000/health
```

## Проверка целостности данных

API включает в себя систему проверки целостности данных с помощью SHA-256 хешей:

### Как это работает

1. **Автоматическое хеширование**: При создании или обновлении записей автоматически вычисляется хеш данных
2. **Проверка целостности**: Система может проверить, не были ли данные изменены без ведома
3. **Автоматическое исправление**: Поврежденные данные можно автоматически исправить
4. **Поиск дубликатов**: Система может найти дублирующиеся записи

### Использование

```bash
# Проверить все данные на целостность
curl http://localhost:8000/api/v1/hash/verify-all

# Исправить поврежденные данные
curl -X POST http://localhost:8000/api/v1/hash/fix-corrupted
```

## Разработка

### Добавление новых моделей
1. Создайте модель в `app/models/`
2. Создайте схемы Pydantic в `app/schemas/`
3. Создайте сервис в `app/services/`
4. Создайте роуты в `app/api/routes/`
5. Подключите роуты в `app/main.py`

### Тестирование
```bash
pytest
```

## Конфигурация

Настройки приложения можно изменить в файле `config.py` или через переменные окружения в файле `.env`:

### Переменные окружения

- `DATABASE_URL` - URL базы данных (по умолчанию: `sqlite:///./rustore.db`)
- `DEBUG` - Режим отладки (по умолчанию: `True`)
- `SECRET_KEY` - Секретный ключ для безопасности
- `ALLOWED_ORIGINS` - Разрешенные домены для CORS (по умолчанию: `*`)

### Создание файла .env

Создайте файл `.env` в корне проекта:

```env
DATABASE_URL=sqlite:///./rustore.db
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_ORIGINS=*
```

### Настройка для продакшена

Для продакшена рекомендуется:

1. Изменить `DEBUG=False`
2. Установить надежный `SECRET_KEY`
3. Ограничить `ALLOWED_ORIGINS` конкретными доменами
4. Использовать PostgreSQL вместо SQLite

## Лицензия

Этот проект создан в рамках VK Case Tournament.
