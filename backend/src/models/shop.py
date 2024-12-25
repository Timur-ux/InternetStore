from sqlalchemy import Column, BigInteger, String
from models.base import Base
from sqlalchemy.orm import relationship

class Shop(Base):
    __tablename__ = "shop"
    shop_id = Column(BigInteger, primary_key=True, index=True)  # Уникальный идентификатор магазина
    shop_name = Column(String(100), nullable=False)  # Название магазина

    # Определяем отношение к Item
    items = relationship("Item", back_populates="shop")  # Связь с Item