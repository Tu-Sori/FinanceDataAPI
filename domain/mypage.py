from fastapi import APIRouter, Path, Depends, HTTPException

from sqlalchemy.orm import Session
from domain import stockInfo, crud
from database import schemas
from database.database import get_db
from oauth import validation_token

from datetime import datetime


router = APIRouter(
         prefix="/mypage"
)


# 관심 주식 정보
async def get_interest_stocks(user_id: int, db: Session):
    interest_stocks_code = crud.get_interest_stocks_code(db=db, user_id=user_id)
    interest_stocks = []
    for stock in interest_stocks_code:
        stock_data = stockInfo.get_stock_data_by_code(stock.code)
        stock_dict = stock_data.to_dict(orient='records')
        interest_stocks.extend(stock_dict)
    return interest_stocks


# 거래 기록 정보
async def get_trade_records(stock_records):
    # 기업 코드, 종목명
    # (DB) 매수일자, 체결일자, 주문수량, 수익금, 수익률
    sell_records = []
    buy_records = []
    for stock_record_obj in stock_records:
        sell_or_buy = int.from_bytes(stock_record_obj.sell_or_buy, byteorder='little', signed=True)
        code = stock_record_obj.code
        stock_data = stockInfo.get_record_stock_data_by_code(code)
        for i in range(len(stock_data)):
            if code == stock_data['Code'].iloc[i]:
                record_dict = stock_record_obj.__dict__
                record_dict['name'] = stock_data['Name'].iloc[i]
                if sell_or_buy == 1:
                    buy_records.append(record_dict)
                else:
                    sell_records.append(record_dict)
    return sell_records, buy_records


async def get_save_stocks(buy_stock_records, db: Session):
    save_stocks = []
    for stock_record in buy_stock_records:
        save_stock = crud.get_save_stocks(db=db, stock_record_id=stock_record["stock_record_id"])
        if save_stock:
            save_stocks.extend(save_stock)
    return save_stocks


# 기업코드, 종목명, 현재가, 평가손익금, 평가손익률, 보유일(체결일자 기준)
# (DB) 매입가, 평단가, 보유수량
async def get_saved_stocks_data(save_stocks, buy_stock_records):
    saves = []
    current_date = datetime.today().date()
    for save_stock in save_stocks:
        stock_data = stockInfo.get_save_stock_data_by_code(save_stock.code)
        for i in range(len(stock_data)):
            if save_stock.code == stock_data['Code'].iloc[i]:
                record_dict = save_stock.__dict__
                record_dict['name'] = stock_data['Name'].iloc[i]
                record_dict['close'] = stock_data['Close'].iloc[i]
                valuation = (int(stock_data['Close'].iloc[i]) - save_stock.purchase)
                record_dict['valuation'] = valuation
                valuation_rate = valuation / save_stock.purchase * 100
                record_dict['valuation_rate'] = valuation_rate
                record_date = buy_stock_records[i]["record_date"]
                difference = current_date - record_date
                record_dict['retention_date'] = difference.days
                saves.append(record_dict)
    return saves


@router.get("")
async def get_user_info(user_id: int = Depends(validation_token),
                        db: Session = Depends(get_db)):
    user = crud.get_user(db=db, user_id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    interest_stocks = await get_interest_stocks(user_id, db)

    stock_records = crud.get_stock_record(db=db, user_id=user_id)
    sell_records, buy_records = await get_trade_records(stock_records)

    # 저장된 주식 정보
    buy_stock_records = [{"stock_record_id": record["stock_record_id"]
                             , "record_date": record["record_date"]} for record in buy_records]
    save_stocks = await get_save_stocks(buy_stock_records, db)
    saves = await get_saved_stocks_data(save_stocks, buy_stock_records)

    return {
        'user_info': user,
        'interest_stocks': interest_stocks if interest_stocks else None,
        'sell_records': sell_records if sell_records else None,
        'buy_records': buy_records if buy_records else None,
        'save_stocks': saves if saves else None
    }