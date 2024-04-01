from datetime import datetime
from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime, String, Boolean
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
   __tablename__ = 'user'

   user_id = Column(Integer, primary_key=True, index=True)
   assets = Column(Integer, default=10000000)
   email = Column(Integer, unique=True, index=True)
   nickname = Column(String, index=True)

   interest_stocks = relationship("InterestStock", back_populates="user")
   stock_record = relationship("StockRecord", back_populates="user")


class InterestStock(Base):
   __tablename__ = "interestStock"

   interest_id = Column(Integer, primary_key=True, autoincrement=True, index=True)
   code = Column(String(6), unique=True)
   user_id = Column(Integer, ForeignKey("user.user_id"))

   user = relationship("User", back_populates="interest_stocks")


class StockRecord(Base):
   __tablename__ = "stockRecord"

   stock_record_id = Column(Integer, primary_key=True, autoincrement=True, index=True)
   sell_or_buy = Column(Boolean)
   code = Column(String(6), unique=True)
   record_date = Column(DateTime, default=datetime.utcnow)
   order_price = Column(Integer)
   contract_price = Column(Integer)
   quentity = Column(Integer)
   proceeds = Column(Integer)
   proceeds_rate = Column(Float)
   user_id = Column(Integer, ForeignKey("user.user_id"))

   user = relationship("User", back_populates="stock_record")
   save_stock = relationship("SaveStock", back_populates="stock_record")


class SaveStock(Base):
   __tablename__ = "saveStock"

   stock_id = Column(Integer, primary_key=True, autoincrement=True, index=True)
   code = Column(String(6), unique=True)
   purchase = Column(Integer)
   average_price = Column(Integer)
   my_quantity = Column(Integer)
   valuation = Column(Integer)
   valuation_ratio = Column(Float)
   user_id = Column(Integer, ForeignKey("stockRecord.stock_record_id"))

   stock_record = relationship("StockRecord", back_populates="save_stock")





