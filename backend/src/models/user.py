from sqlalchemy import Column, Integer, String, Numeric
from src.models.base import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True) 
    access_level = Column(Integer, nullable=False, default=1)
    login = Column(String(100), nullable=False, unique=True)
    password = Column(String(64), nullable=False)
    balance = Column(Numeric(10, 2), default=0.00)  
