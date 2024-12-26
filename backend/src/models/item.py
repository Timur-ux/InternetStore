from sqlalchemy import Column, Integer, String, Numeric, Integer, Date, ForeignKey, Table
from sqlalchemy.orm import relationship
from src.models.base import Base

# Define the association table
item_shop = Table(
    'item_shop', Base.metadata,
    Column('item_id', Integer, ForeignKey('item.item_id'), primary_key=True),
    Column('shop_id', Integer, ForeignKey('shop.shop_id'), primary_key=True),
)

class Item(Base):
    __tablename__ = "item"
    
    item_id = Column(Integer, primary_key=True, index=True, autoincrement=True)  
    item_name = Column(String(100), nullable=False)          
    uri = Column(String(255), nullable=False)                 
    item_category_id = Column(Integer, nullable=False)   
    item_price = Column(Numeric(10, 2), nullable=False)      
    item_cnt_day = Column(Integer)                             
    date = Column(Date)                                         
    date_block_num = Column(Integer)                         
    item_category_name = Column(String(100), nullable=False)   

    shops = relationship("Shop", secondary=item_shop, back_populates="items")