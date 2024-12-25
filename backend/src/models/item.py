from sqlalchemy import Column, BigInteger, String, Numeric, Integer, Date, ForeignKey, Table
from sqlalchemy.orm import relationship
from models.base import Base

# Промежуточная таблица для связи многие-ко-многим
item_shop_association = Table(
    'item_shop', Base.metadata,
    Column('item_id', BigInteger, ForeignKey('item.id'), primary_key=True),
    Column('shop_id', BigInteger, ForeignKey('shop.shop_id'), primary_key=True)
)

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
    item_category_name = Column(String(100), nullable=False)

    # Определяем отношение к Shop через промежуточную таблицу
    shops = relationship("Shop", secondary=item_shop_association, back_populates="items")  # Связь с несколькими магазинами