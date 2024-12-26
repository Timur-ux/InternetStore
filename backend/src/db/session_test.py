# session_test.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.models.base import Base

SQLALCHEMY_DATABASE_URL_TEST = "sqlite:///test.db"

# Создаем тестовый движок базы данных
engine_test = create_engine(SQLALCHEMY_DATABASE_URL_TEST, connect_args={"check_same_thread": False})

# Сессия для работы с тестовой базой данных
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine_test)

# Создаем все таблицы для тестов
Base.metadata.create_all(bind=engine_test)

# Функция для получения сессии
def get_session_test():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Очистка базы данных после тестов
def cleanup():
    Base.metadata.drop_all(bind=engine_test)
