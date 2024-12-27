from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from src.models.base import Base
from .item import item_shop

class Shop(Base):
    __tablename__ = "shop"
    
    shop_id = Column(Integer, primary_key=True, index=True, autoincrement=True)  # Unique shop identifier
    shop_name = Column(String(100), nullable=False)             # Shop name

    # Define the relationship to items through the association table
    items = relationship("Item", secondary=item_shop, back_populates="shops")
