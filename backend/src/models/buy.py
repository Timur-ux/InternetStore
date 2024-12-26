from sqlalchemy import Column, BigInteger, Numeric, Integer, DateTime, ForeignKey
from src.models.base import Base

class Buy(Base):
    __tablename__ = "buy"
    id = Column(BigInteger, primary_key=True, index=True)
    user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    cnt = Column(Integer, nullable=False)
    buy_time = Column(DateTime, nullable=False)
