from datetime import datetime
from pydantic import BaseModel


class User(BaseModel):
    user_id: int
    assets: int
    nickname: str

    class Config:
        orm_mode = True


class InterestStockBase(BaseModel):
    code: str

class InterestStockCreate(InterestStockBase):
    pass

class InterestStock(InterestStockBase):
    interest_id: int
    user_id: int

    class Config:
        orm_mode = True

class StockRecordBase(BaseModel):
    sell_or_buy: bool
    code: str
    record_date: datetime
    order_price: int
    contract_price: int
    quentity: int
    proceeds: int
    proceeds_rate: float

class StockRecordCreate(StockRecordBase):
    pass

class StockRecord(StockRecordBase):
    stock_record_id: int
    user_id: int

    class Config:
        orm_mode = True

class SaveStockBase(BaseModel):
    code: str
    purchase: float
    quantity: int
    retention_date: datetime
    valuation: float
    valuation_ratio: float

class SaveStockCreate(SaveStockBase):
    pass

class SaveStock(SaveStockBase):
    stock_record_id: int
    user_id: int

    class Config:
        orm_mode = True