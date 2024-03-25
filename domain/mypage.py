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


@router.get("/{user_id}", response_model=schemas.User)
async def get_my_info(
        user_id: int = Path(..., description="User ID"),
        db: Session = Depends(get_db)):

    user = crud.get_user(db=db, user_id=user_id)

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return user


@router.get("/{user_id}/interests", response_model=List[schemas.InterestStock])
async def get_interests(
        user_id: int = Path(..., description="User ID"),
        db: Session = Depends(get_db)):

    interest_stocks_code = crud.get_interest_stocks(db=db, user_id=user_id)

    interest_stocks = []
    for code in interest_stocks_code:
        stock_data = stockInfo.get_stock_data_by_code(code)
        if not stock_data.empty:
            stock_info_dict = stock_data.iloc[0].to_dict()
            stock_info_dict.update(interest_stocks_code.iloc[0].to_dict())
            interest_stocks.append(stock_info_dict)

    return interest_stocks_code



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

