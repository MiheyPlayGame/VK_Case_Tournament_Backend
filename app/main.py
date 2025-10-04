from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import apps, categories, hash_verification
from app.database import engine, Base

# Создаем таблицы в базе данных
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="RuStore Backend API",
    description="Backend API для мобильного приложения RuStore",
    version="1.0.0"
)

# Настройка CORS для работы с Android приложением
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # В продакшене указать конкретные домены
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключение роутов
app.include_router(apps.router, prefix="/api/v1/apps", tags=["apps"])
app.include_router(categories.router, prefix="/api/v1/categories", tags=["categories"])
app.include_router(hash_verification.router, prefix="/api/v1/hash", tags=["hash-verification"])

@app.get("/")
async def root():
    return {"message": "RuStore Backend API", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
