from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from database.schemas import User
from database import models, schemas
from database.database import get_db


def get_user(db: Session, user_id: int) -> User:
    user = db.query(user).filter(user_id == user_id).all()

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return user


def create_save_stock(db: Session, save_stock: schemas.SaveStockCreate, user_id: int):
    db_save_sotck = models.SaveStock(code=save_stock.code, purchase=save_stock.purchase,
                                     quantity=save_stock.quantity,
                                     retention_date=save_stock.retention_date,
                                     valuation=save_stock.valuation,
                                     valuation_ratio=save_stock.valuation, user_id=user_id)
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
    db_interest_stock = models.InterestStock(code=interest_stock.code, user_id=user_id)
    db.add(db_interest_stock)
    db.commit()
    db.refresh(db_interest_stock)

    return db_interest_stock



def get_interest_stocks(db: Session, user_id: int):
    interest_stocks = db.query(models.InterestStock).filter(models.InterestStock.user_id == user_id).all()

    if not interest_stocks:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="InterestStock not found")

    return interest_stocks


def get_interest_stock_by_code(db: Session, code: int, user_id: int):
    return db.query(models.InterestStock).filter(
        models.InterestStock.code == code,
        models.InterestStock.user_id == user_id
    ).first()


def delete_interest_stock(db: Session, code: int,  user_id: int):
    db_interest_stock = db.query(models.InterestStock).filter(
        models.InterestStock.code == code,
        models.InterestStock.user_id == user_id
    ).first()

    if db_interest_stock is None:
        raise HTTPException(status_code=404, detail="InterestStock not found")

    db.delete(db_interest_stock)
    db.commit()

    return db_interest_stock

