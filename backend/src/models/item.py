from sqlalchemy import Column, BigInteger, String, Numeric, Integer, Date, ForeignKey, Table
from sqlalchemy.orm import relationship
from models.base import Base

# Define the association table
item_shop = Table(
    'item_shop', Base.metadata,
    Column('item_id', BigInteger, ForeignKey('item.item_id'), primary_key=True),
    Column('shop_id', BigInteger, ForeignKey('shop.shop_id'), primary_key=True),
    # You can add additional fields here if needed, e.g., price
)

class Item(Base):
    __tablename__ = "item"
    
    item_id = Column(BigInteger, primary_key=True, index=True)  # Unique item identifier
    item_name = Column(String(100), nullable=False)             # Item name
    uri = Column(String(255), nullable=False)                   # URL for item data
    item_category_id = Column(BigInteger, nullable=False)       # Unique category identifier
    item_price = Column(Numeric(10, 2), nullable=False)        # Current item price
    item_cnt_day = Column(Integer)                              # Number of items sold per day
    date = Column(Date)                                         # Date in dd/mm/yyyy format
    date_block_num = Column(Integer)                           # Month number (0 - January 2013, etc.)
    item_category_name = Column(String(100), nullable=False)   # Category name

    # Define the relationship to shops through the association table
    shops = relationship("Shop", secondary=item_shop, back_populates="items")