from fastapi import APIRouter, Path, Depends, HTTPException

from sqlalchemy.orm import Session
from domain import stockInfo, crud
from database.database import engine
from database import models, schemas
from database.database import get_db

from datetime import datetime

router = APIRouter(
         prefix="/mypage"
)


@router.get("/{user_id}")
async def get_user_info(
        user_id: int = Path(..., description="User ID"),
        db: Session = Depends(get_db)):
    user = crud.get_user(db=db, user_id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    # 관심 주식 정보
    interest_stocks_code = crud.get_interest_stocks_code(db=db, user_id=user_id)
    interest_stocks = []
    for stock in interest_stocks_code:
        stock_data = stockInfo.get_stock_data_by_code(stock.code)
        stock_dict = stock_data.to_dict(orient='records')
        interest_stocks.extend(stock_dict)

    # 거래 기록 정보
    stock_records = crud.get_stock_record(db=db, user_id=user_id)
    if not stock_records:
        raise HTTPException(status_code=404, detail="Stock records not found")

    # 기업 코드, 종목명
    # (DB) 매수일자, 체결일자, 주문수량, 수익금, 수익률
    records = []
    for stock_record_obj in stock_records:
        code = stock_record_obj.code
        stock_data = stockInfo.get_record_stock_data_by_code(code)
        for i in range(len(stock_data)):
            if code == stock_data['Code'].iloc[i]:
                record_dict = stock_record_obj.__dict__
                record_dict['name'] = stock_data['Name'].iloc[i]
                records.append(record_dict)

    # 저장된 주식 정보
    sell_stock_records = [{
        "stock_record_id": record.stock_record_id,
        "record_date": record.record_date
    } for record in stock_records if record.sell_or_buy]

    save_stocks = []
    for stock_record in sell_stock_records:
        save_stock = crud.get_save_stocks(db=db, stock_record_id=stock_record["stock_record_id"])
        if not save_stock:
            raise HTTPException(status_code=404, detail="Save stocks not found")
        save_stocks.extend(save_stock)

    # 기업코드, 종목명, 현재가, 평가손익금, 평가손익률, 보유일(체결일자 기준)
    # (DB) 매입가, 평단가, 보유수량
    saves = []
    current_date = datetime.today().date()
    for save_stock in save_stocks:
        stock_data = stockInfo.get_save_stock_data_by_code(save_stock.code)
        for i in range(len(stock_data)):
            if save_stock.code == stock_data['Code'].iloc[i]:
                record_dict = save_stock.__dict__
                record_dict['name'] = stock_data['Name'].iloc[i]
                record_dict['close'] = stock_data['Close'].iloc[i]
                # 평가손익금 = 현재가 - 매입가
                valuation = (int(stock_data['Close'].iloc[i]) - save_stock.purchase)
                record_dict['valuation'] = valuation
                # 평가손익률 = 평가손익금 / 매입가 * 100
                valuation_rate = valuation / save_stock.purchase * 100
                record_dict['valuation_rate'] = valuation_rate
                # 보유일
                record_date = sell_stock_records[i]["record_date"]
                difference = current_date - record_date
                record_dict['retention_date'] = difference.days
                saves.append(record_dict)

    return {
        'user_info': user,
        'interest_stocks': interest_stocks,
        'stock_records': records,
        'save_stocks': saves
    }


@router.delete("/{user_id}/{code}", response_model=schemas.InterestStock)
async def delete_interest_stock(
        user_id: int = Path(..., description="User ID"),
        code: str = Path(..., description="기업코드"),
        db: Session = Depends(get_db)):
    deleted_interest_stock = crud.delete_interest_stock(db=db, code=code, user_id=user_id)

    if deleted_interest_stock is None:
        raise HTTPException(status_code=404, detail="Interest stock not found")

    return deleted_interest_stock