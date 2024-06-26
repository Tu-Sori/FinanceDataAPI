from datetime import datetime
from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    user_id: int


class User(BaseModel):
    user_id: int
    assets: int
    email: int
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


class StockRecord(BaseModel):
    stock_record_id: int
    sell_or_buy: int
    code: str
    sell_or_buy_date: datetime
    record_date: datetime
    contract_price: int
    quantity: int
    proceeds: int
    proceeds_rate: float
    user_id: int

    class Config:
        orm_mode = True


class SaveStock(BaseModel):
    stock_id: int
    code: str
    purchase: int
    average_price: int
    my_quantity: int
    stock_record_id: int

    class Config:
        orm_mode = True


class Notification(BaseModel):
    notification_id: int
    content: str
    createdAt: datetime
    isRead: bool

    class Config:
        orm_mode = True