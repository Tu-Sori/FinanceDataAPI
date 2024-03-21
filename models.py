from datetime import datetime
from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class SaveStock(Base):
   __tablename__ = "saveStock"

   stock_id = Column(Integer, primary_key=True, autoincrement=True)
   code = Column(Integer)
   purchase = Column(Float)
   quantity = Column(Integer)
   retention_date = Column(DateTime, default=datetime.utcnow)
   valuation = Column(Float)
   valuation_ratio = Column(Float)
   user_id = Column(Integer, ForeignKey("users.user_id"))

   user = relationship("User", back_populates="save_stocks")

class InterestStock(Base):
   __tablename__ = "interestStock"

   interest_id = Column(Integer, primary_key=True, autoincrement=True)
   code = Column(Integer)
   user_id = Column(Integer, ForeignKey("users.user_id"))

   user = relationship("User", back_populates="interest_stocks")
