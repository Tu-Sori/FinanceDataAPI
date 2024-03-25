from datetime import datetime
from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime, String
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
   __tablename__ = 'user'

   user_id = Column(Integer, primary_key=True, index=True)
   assets = Column(Integer, default=10000000)
   email = Column(Integer, unique=True, index=True)
   nickname = Column(String, index=True)

   interest_stocks = relationship("InterestStock", back_populates="user")
   save_stocks = relationship("SaveStock", back_populates="user")


class InterestStock(Base):
   __tablename__ = "interestStock"

   interest_id = Column(Integer, primary_key=True, autoincrement=True, index=True)
   code = Column(Integer, unique=True)
   user_id = Column(Integer, ForeignKey("user.user_id"))

   user = relationship("User", back_populates="interest_stocks")


class SaveStock(Base):
   __tablename__ = "saveStock"

   stock_id = Column(Integer, primary_key=True, autoincrement=True, index=True)
   code = Column(Integer, unique=True)
   purchase = Column(Float)
   quantity = Column(Integer)
   retention_date = Column(DateTime, default=datetime.utcnow)
   valuation = Column(Float)
   valuation_ratio = Column(Float)
   user_id = Column(Integer, ForeignKey("user.user_id"))

   user = relationship("User", back_populates="save_stocks")