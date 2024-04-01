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
            .filter(models.InterestStock.code == code, models.InterestStock.user_id == user_id)
            .first())


def delete_interest_stock(db: Session, code: str,  user_id: int):
    db_interest_stock = db.query(models.InterestStock).filter(
        models.InterestStock.code == code,
        models.InterestStock.user_id == user_id
    ).first()

    db.delete(db_interest_stock)
    db.commit()

    return db_interest_stock


# 매수, 매도 주식
def create_record_stock(db: Session, record_stock: schemas.StockRecordCreate, user_id: int):
    db_record_stock = models.StockRecord(sell_or_buy=record_stock.sell_or_buy, code=record_stock.code
                                       , record_date=record_stock.record_date
                                       , order_price=record_stock.order_price
                                       , contract_price=record_stock.contract_price
                                       , quentity=record_stock.quentity
                                       , proceeds=record_stock.proceeds
                                       , proceeds_rate=record_stock.proceeds_rate, user_id=user_id)
    db.add(db_record_stock)
    db.commit()
    db.refresh(db_record_stock)

    return db_record_stock

def get_record_stock(db: Session, user_id: int):
    record_stock = (db.query(models.StockRecord)
                   .filter(models.StockRecord.user_id == user_id)
                   .all())

    return record_stock

def delete_record_stock(db: Session, record_stock_id: int):
    db_record_stock = (db.query(models.StockRecord)
                     .filter(models.StockRecord.record_stock_id == record_stock_id)
                     .first())
    db.delete(db_record_stock)
    db.commit()

    return db_record_stock

# 보유주식
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
    save_stocks = (db.query(models.SaveStock)
                   .filter(models.SaveStock.user_id == user_id)
                   .all())

    return save_stocks


def delete_save_stock(db: Session, save_stock_id: int):
    db_save_stock = (db.query(models.SaveStock)
                     .filter(models.SaveStock.stock_id == save_stock_id)
                     .first())
    db.delete(db_save_stock)
    db.commit()

    return db_save_stock

