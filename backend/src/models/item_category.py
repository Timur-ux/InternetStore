from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from src.models.base import Base

class ItemCategory(Base):
    __tablename__ = "item_category"
    
    item_category_id = Column(Integer, primary_key=True, index=True)  # Уникальный идентификатор категории товара
    item_category_name = Column(String(100), nullable=False)              # Название категории товара
