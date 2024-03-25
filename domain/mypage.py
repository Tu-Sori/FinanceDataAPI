from fastapi import APIRouter, Path, Depends

from sqlalchemy.orm import Session

from domain import stockInfo, crud
from database.database import SessionLocal, engine
from database import models, schemas
from database.database import get_db

models.Base.metadata.create_all(bind=engine)
router = APIRouter(
         prefix="/mypage"
)


@router.get("/{user_id}", response_model=schemas.User)
async def get_my_info(
        user_id: int = Path(..., description="User ID"),
        db: Session = Depends(get_db)):

    user = crud.get_user(db, user_id)

    return user

@router.get("/{user_id}/interests", response_model=schemas.InterestStock)
async def get_interests(
        user_id: int = Path(..., description="User ID"),
        db: Session = Depends(get_db)):

    interest_stocks_code = crud.get_interest_stocks(db, user_id)

    interest_stocks = []
    for code in interest_stocks_code:
        stock_data = stockInfo.get_stock_data_by_code(code)
        interest_stock = stock_data.to_dict(orient='records')
        interest_stocks.append(interest_stock)

    return interest_stocks
