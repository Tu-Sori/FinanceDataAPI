from sqlalchemy.orm import Session
from database import models, schemas


# user 정보
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.user_id == user_id).first()


# 관심 주식
def create_interest_stock(db: Session, interest_stock: schemas.InterestStockCreate, user_id: int):
    db_interest_stock = models.InterestStock(code=interest_stock.code, user_id=user_id)
    db.add(db_interest_stock)
    db.commit()
    db.refresh(db_interest_stock)

    return db_interest_stock


def get_interest_stocks_code(db: Session, user_id: int):
    interest_stocks = (db.query(models.InterestStock)
                       .filter(models.InterestStock.user_id == user_id)
                       .all())

    return interest_stocks


def get_interest_stock_by_code(db: Session, code: str, user_id: int):
    return (db.query(models.InterestStock)
            .filter(models.InterestStock.code == code,
                    models.InterestStock.user_id == user_id)
            .first())


def delete_interest_stock(db: Session, code: str,  user_id: int):
    db_interest_stock = (db.query(models.InterestStock)
                         .filter(models.InterestStock.code == code,
                                 models.InterestStock.user_id == user_id)
                         .first())

    db.delete(db_interest_stock)
    db.commit()

    return db_interest_stock


# 매수, 매도 주식
def get_stock_record(db: Session, user_id: int):
    stock_record = (db.query(models.StockRecord)
                   .filter(models.StockRecord.user_id == user_id)
                   .all())

    return stock_record


# 보유주식
def get_save_stocks_code(db: Session, stock_record_id: int):
    save_stocks = (db.query(models.SaveStock)
                   .filter(models.SaveStock.stock_record_id == stock_record_id)
                   .all())

    return save_stocks
