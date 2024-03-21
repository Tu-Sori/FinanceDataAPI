from datetime import datetime
from pydantic import BaseModel


class User(BaseModel):
    user_id: int
    nickname: str
    email: str
    assets: int

    class Config:
        orm_mode = True

class SaveStockBase(BaseModel):
    code: int
    purchase: float
    quantity: int
    retention_date: datetime
    valuation: float
    valuation_ratio: float

class SaveStockCreate(SaveStockBase):
    pass

class SaveStock(SaveStockBase):
    stock_id: int
    user_id: int

    class Config:
        orm_mode = True

class InterestStockBase(BaseModel):
    code: int

class InterestStockCreate(InterestStockBase):
    pass

class InterestStock(InterestStockBase):
    interest_id: int
    user_id: int

    class Config:
        orm_mode = True