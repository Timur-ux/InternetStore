from sqlalchemy import Column, BigInteger, String
from sqlalchemy.orm import relationship
from src.models.base import Base
from .item import item_shop

class Shop(Base):
    __tablename__ = "shop"
    
    shop_id = Column(BigInteger, primary_key=True, index=True)  # Unique shop identifier
    shop_name = Column(String(100), nullable=False)             # Shop name

    # Define the relationship to items through the association table
    items = relationship("Item", secondary=item_shop, back_populates="shops")
