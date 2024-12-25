from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


# перенести в .env или конфиг
DATABASE_URL = "postgresql://user:password@localhost/InternetStore"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
