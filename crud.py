from fastapi import HTTPException, status
from sqlalchemy.orm import Session
import schemas
import models


def get_user(db: Session, user_id: int):
    user = db.query(models.User).filter(models.User.user_id == user_id).first()

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return user


def create_save_stock(db: Session, save_stock: schemas.SaveStockCreate, user_id: int):
    db_save_sotck = models.SaveStock(**save_stock.model_dump(), user_id=user_id)
    db.add(db_save_sotck)
    db.commit()
    db.refresh(db_save_sotck)

    return db_save_sotck


def get_save_stock(db: Session, user_id: int):
    save_stocks = db.query(models.SaveStock).filter(models.SaveStock.user_id == user_id).all()

    if not save_stocks:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="SaveStocks not found")

    return save_stocks


def delete_save_stock(db: Session, save_stock_id: int):
    db_save_stock = db.query(models.SaveStock).filter(models.SaveStock.stock_id == save_stock_id).first()

    if db_save_stock is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="SaveStock not found")

    db.delete(db_save_stock)
    db.commit()

    return db_save_stock


def create_interest_stock(db: Session, interest_stock: schemas.InterestStockCreate, user_id: int):
    db_interest_stock = models.InterestStock(**interest_stock.model_dump(), user_id=user_id)
    db.add(db_interest_stock)
    db.commit()
    db.refresh(db_interest_stock)

    return db_interest_stock


def get_interest_stocks(db: Session, user_id: int):
    interest_stocks = db.query(models.InterestStock).filter(models.InterestStock.user_id == user_id).all()

    if not interest_stocks:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="InterestStock not found")

    return interest_stocks


def delete_interest_stock(db: Session, interest_stock_id: int):
    db_interest_stock = db.query(models.InterestStock).filter(
        models.InterestStock.interest_id == interest_stock_id).first()

    if db_interest_stock is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="InterestStock not found")

    db.delete(db_interest_stock)
    db.commit()

    return db_interest_stock

