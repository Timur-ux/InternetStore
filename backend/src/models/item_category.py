from sqlalchemy import Column, BigInteger, String
from sqlalchemy.orm import relationship
from models.base import Base

class ItemCategory(Base):
    __tablename__ = "item_category"
    
    item_category_id = Column(BigInteger, primary_key=True, index=True)  # Уникальный идентификатор категории товара
    item_category_name = Column(String(100), nullable=False)              # Название категории товара
