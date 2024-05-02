from datetime import datetime
from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime, String, Boolean
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
   __tablename__ = 'user'

   # 사용자 id(PK), 닉네임, 이메일, 가용자산
   user_id = Column(Integer, primary_key=True, index=True)
   email = Column(Integer, unique=True, index=True)
   nickname = Column(String, index=True)
   assets = Column(Integer, default=10000000)

   interest_stocks = relationship("InterestStock", back_populates="user")
   stock_record = relationship("StockRecord", back_populates="user")
   notification = relationship("Notification", back_populates="user")


class InterestStock(Base):
   __tablename__ = "interestStock"

   # 관심주식 id(PK), 기업 코드, 사용자 id(FK)
   interest_id = Column(Integer, primary_key=True, autoincrement=True, index=True)
   code = Column(String(6))
   user_id = Column(Integer, ForeignKey("user.user_id"))

   user = relationship("User", back_populates="interest_stocks")


class StockRecord(Base):
   __tablename__ = "stockRecord"

   # 매수매도 일지 id(PK), 매수매도 구분, 기업 코드, 매수매도 일자,
   # 체결일자, 체결단가, 주문수량, 수익금, 수익률, 사용자 id(FK)
   stock_record_id = Column(Integer, primary_key=True, autoincrement=True, index=True)
   sell_or_buy = Column(Boolean)
   code = Column(String(6))
   sell_or_buy_date = Column(DateTime, default=datetime.utcnow)
   record_date = Column(DateTime, default=datetime.utcnow)
   contract_price = Column(Integer)
   quantity = Column(Integer)
   proceeds = Column(Integer)
   proceeds_rate = Column(Float)
   user_id = Column(Integer, ForeignKey("user.user_id"))

   user = relationship("User", back_populates="stock_record")
   save_stock = relationship("SaveStock", back_populates="stock_record")


class SaveStock(Base):
   __tablename__ = "saveStock"

   # 보유주식 id(PK), 기업 코드, 매입가, 평단가, 보유수량, 매수매도 일지 id(FK)
   stock_id = Column(Integer, primary_key=True, autoincrement=True, index=True)
   code = Column(String(6))
   purchase = Column(Integer)
   average_price = Column(Integer)
   my_quantity = Column(Integer)
   stock_record_id = Column(Integer, ForeignKey("stockRecord.stock_record_id"))

   stock_record = relationship("StockRecord", back_populates="save_stock")


class Notification(Base):
   __tablename__ = "notification"

   notification_id = Column(Integer, primary_key=True, autoincrement=True, index=True)
   content = Column(String(30))
   createdAt = Column(DateTime, default=datetime.utcnow())
   isRead = Column(Boolean)
   user_id = Column(Integer, ForeignKey("user.user_id"))

   user = relationship("User", back_populates="notification")

