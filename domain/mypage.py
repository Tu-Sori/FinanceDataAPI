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


# @router.get("/{user_id}/saves", response_model=list[schemas.SaveStock])
# async def get_saves(
#         user_id: int = Path(..., description="User ID"),
#         db: Session = Depends(get_db()):
#
#     save_stocs_code = crud.get_save_stock(db, user_id)
#
#     save_stocks = []
#
#
# return save_stocks

