from sqlalchemy import Column, BigInteger, String
from src.models.base import Base

class User(Base):
    __tablename__ = "users"
    id = Column(BigInteger, primary_key=True, index=True)
    access_level = Column(BigInteger, nullable=False)
    login = Column(String(100), nullable=False, unique=True)
    password = Column(String(64), nullable=False)
