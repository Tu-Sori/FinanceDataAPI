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
async def get_user_with_interests(
        user_id: int = Path(..., description="User ID"),
        db: Session = Depends(get_db)):
    user = crud.get_user(db=db, user_id=user_id)

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    interest_stocks_code = crud.get_interest_stocks_code(db=db, user_id=user_id)
    codes = [stock.code for stock in interest_stocks_code]

    interest_stocks = []
    for code in codes:
        stock_data = stockInfo.get_stock_data_by_code(code)
        stock_dict = stock_data.to_dict(orient='records')
        interest_stocks.extend(stock_dict)

    user_with_interests = {
        "user_info": user,
        "interests": interest_stocks
    }

    return user_with_interests


@router.delete("/{user_id}/{code}", response_model=schemas.InterestStock)
async def delete_interest_stock(
        user_id: int = Path(..., description="User ID"),
        code: str = Path(..., description="기업코드"),
        db: Session = Depends(get_db)):
    deleted_interest_stock = crud.delete_interest_stock(db=db, code=code, user_id=user_id)

    if deleted_interest_stock is None:
        raise HTTPException(status_code=404, detail="Interest stock not found")

    return deleted_interest_stock


@router.get("/{user_id}/records_and_saves")
async def get_records_and_saves(
        user_id: int = Path(..., description="User ID"),
        db: Session = Depends(get_db)):
    user = crud.get_user(db=db, user_id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    stock_records = crud.get_stock_record(db=db, user_id=user_id)
    if not stock_records:
        raise HTTPException(status_code=404, detail="Stock records not found")

    records = []
    for stock_record_obj in stock_records:
        code = stock_record_obj.code
        stock_data = stockInfo.get_record_stock_data_by_code(code)
        for i in range(len(stock_data)):
            if code == stock_data['Code'].iloc[i]:
                record_dict = stock_record_obj.__dict__
                record_dict['name'] = stock_data['Name'].iloc[i]
                records.append(record_dict)

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

    saves = []
    current_date = datetime.today().date()
    for save_stock in save_stocks:
        stock_data = stockInfo.get_save_stock_data_by_code(save_stock.code)
        for i in range(len(stock_data)):
            if save_stock.code == stock_data['Code'].iloc[i]:
                record_dict = save_stock.__dict__
                record_dict['name'] = stock_data['Name'].iloc[i]
                record_dict['close'] = stock_data['Close'].iloc[i]
                record_date = sell_stock_records[i]["record_date"]
                difference = current_date - record_date
                record_dict['retention_date'] = difference.days
                saves.append(record_dict)

    return {
        'stockRecord': records,
        'saveStock': saves
    }
