from sqlalchemy import Column, Integer, Numeric, Integer, DateTime, ForeignKey
from src.models.base import Base

class Buy(Base):
    __tablename__ = "buy"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    item_id = Column(Integer, ForeignKey("item.item_id"), nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    cnt = Column(Integer, nullable=False)
    buy_time = Column(DateTime, nullable=False)
