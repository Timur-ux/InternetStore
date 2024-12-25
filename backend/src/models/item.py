from sqlalchemy import Column, BigInteger, String, Numeric, Integer, Date
from models.base import Base

class Item(Base):
    __tablename__ = "item"
    id = Column(BigInteger, primary_key=True, index=True)
    item_id = Column(BigInteger, nullable=False)
    item_name = Column(String(100), nullable=False)
    uri = Column(String(255), nullable=False)
    item_category_id = Column(BigInteger, nullable=False)
    item_price = Column(Numeric(10, 2), nullable=False)
    item_cnt_day = Column(Integer)
    date = Column(Date)
    date_block_num = Column(Integer)
    shop_id = Column(BigInteger, nullable=False)
    shop_name = Column(String(100), nullable=False)
    item_category_name = Column(String(100), nullable=False)
