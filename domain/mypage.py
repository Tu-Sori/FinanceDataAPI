from typing import List

from fastapi import APIRouter, Path, Depends, HTTPException

from sqlalchemy.orm import Session


from domain import stockInfo, crud
from database.database import engine
from database import models, schemas
from database.database import get_db


router = APIRouter(
         prefix="/mypage"
)

@router.get("/{user_id}")
async def get_user_with_interests(
        user_id: int = Path(..., description="User ID"),
        db: Session = Depends(get_db)):

    # 사용자 정보 조회
    user = crud.get_user(db=db, user_id=user_id)

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    # 관심 주식 정보 조회
    interest_stocks_code = crud.get_interest_stocks_code(db=db, user_id=user_id)
    codes = [stock.code for stock in interest_stocks_code]

    interest_stocks = []
    for code in codes:
        stock_data = stockInfo.get_stock_data_by_code(code)
        stock_dict = stock_data.to_dict(orient='records')
        interest_stocks.extend(stock_dict)

    # 사용자 정보와 관심 주식 정보를 합쳐서 반환
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


@router.get("/{user_id}/saves")
async def get_saves(
        user_id: int = Path(..., description="User ID"),
        db: Session = Depends(get_db)):

    user = crud.get_user(db=db, user_id=user_id)

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    else:
        stock_record = crud.get_stock_record(db=db, user_id=user_id)

        if stock_record is None:
            raise HTTPException(status_code=404, detail="stock_record not found")
        else:
            codes = [stock.code for stock in stock_record]
            print(codes)

    save_stocks = []
    for code in codes:
        stock_data = stockInfo.get_save_stock_data_by_code(code)
        stock_dict = stock_data.to_dict(orient='records')
        save_stocks.extend(stock_dict)

    result = {
        'stock_record': stock_record,
        'save_stocks': save_stocks
    }

    return result

