from fastapi import APIRouter, Query, HTTPException, Path, Depends, Header

import pandas as pd
import FinanceDataReader as fdr
import mplfinance as mpf

from sqlalchemy.orm import Session
from domain import stockInfo, crud
from database import models, schemas
from database.database import get_db

router = APIRouter(
         prefix="/home"
)


@router.get("")
async def get_data(user_id: int = None, db: Session = Depends(get_db)):
    market_data = stockInfo.get_market_data()
    # 상위 5개(기준: 거래량)
    top_5_kospi = stockInfo.get_top_n_stocks('KOSPI')
    top_5_kosdaq = stockInfo.get_top_n_stocks('KOSDAQ')
    top_5_konex = stockInfo.get_top_n_stocks('KONEX')

    if user_id is not None:
        user = crud.get_user(db=db, user_id=user_id)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")

        stock_record = crud.get_stock_record(db=db, user_id=user_id)
        if stock_record is None:
            raise HTTPException(status_code=404, detail="stock_record not found")

        codes = [stock.code for stock in stock_record]
        save_stocks = []
        for code in codes:
            stock_data = stockInfo.get_top_n_save_stocks(code)
            save_stocks.append(stock_data)

        user_data = {
            "user": user,
            "save_stocks": save_stocks
        }

        data = {
            **market_data,
            "user_data": user_data,
            "top_5_kospi": top_5_kospi,
            "top_5_kosdaq": top_5_kosdaq,
            "top_5_konex": top_5_konex
        }
    else:
        data = {
            **market_data,
            "top_5_kospi": top_5_kospi,
            "top_5_kosdaq": top_5_kosdaq,
            "top_5_konex": top_5_konex
        }

    return data


@router.get("/{market}")
async def get_market_chart(
    market: str = Path(..., description="Market: kospi, kosdaq"),
    chart_type: str = Query(..., description="Chart type: weekly, monthly, 3months, 1years, 3years, 10years")):
    date_ranges = stockInfo.calculate_date_ranges()

    market_data = None
    if market.lower() == "kospi":
        if chart_type == "weekly":
            market_data = stockInfo.get_stock_data('KS11', date_ranges["one_week_ago"], date_ranges["current_date"])
            mpf.plot(market_data, type='candle', volume=True, style='classic', title='KOSPI Weekly Chart')
        elif chart_type == "monthly":
            market_data = stockInfo.get_stock_data('KS11', date_ranges["one_month_ago"], date_ranges["current_date"])
            mpf.plot(market_data, type='candle', volume=True, style='classic', title='KOSPI Monthly Chart')
        elif chart_type == "3months":
            market_data = stockInfo.get_stock_data('KS11', date_ranges["three_months_ago"], date_ranges["current_date"])
            mpf.plot(market_data, type='candle', volume=True, style='classic', title='KOSPI 3 Months Chart')
        elif chart_type == "1years":
            market_data = stockInfo.get_stock_data('KS11', date_ranges["one_year_ago"], date_ranges["current_date"])
            mpf.plot(market_data, type='line', volume=False, style='classic', title='KOSPI 1 Year Chart')
        elif chart_type == "3years":
            market_data = stockInfo.get_stock_data('KS11', date_ranges["three_years_ago"], date_ranges["current_date"])
            mpf.plot(market_data, type='line', volume=False, style='classic', title='KOSPI 3 Years Chart')
        elif chart_type == "10years":
            market_data = stockInfo.get_stock_data('KS11', date_ranges["ten_years_ago"], date_ranges["current_date"])
            mpf.plot(market_data, type='line', volume=False, style='classic', title='KOSPI 10 Years Chart')
        else:
            raise HTTPException(status_code=404, detail="Chart type not found")
    elif market.lower() == "kosdaq":
        if chart_type == "weekly":
            market_data = stockInfo.get_stock_data('KQ11', date_ranges["one_week_ago"], date_ranges["current_date"])
            mpf.plot(market_data, type='candle', volume=True, style='classic', title='KOSDAQ Weekly Chart')
        elif chart_type == "monthly":
            market_data = stockInfo.get_stock_data('KQ11', date_ranges["one_month_ago"], date_ranges["current_date"])
            mpf.plot(market_data, type='candle', volume=True, style='classic', title='KOSDAQ Monthly Chart')
        elif chart_type == "3months":
            market_data = stockInfo.get_stock_data('KQ11', date_ranges["three_months_ago"], date_ranges["current_date"])
            mpf.plot(market_data, type='line', volume=True, style='classic', title='KOSDAQ 3 Months Chart')
        elif chart_type == "1years":
            market_data = stockInfo.get_stock_data('KQ11', date_ranges["one_year_ago"], date_ranges["current_date"])
            mpf.plot(market_data, type='line', volume=False, style='classic', title='KOSDAQ 1 Year Chart')
        elif chart_type == "3years":
            market_data = stockInfo.get_stock_data('KQ11', date_ranges["three_years_ago"], date_ranges["current_date"])
            mpf.plot(market_data, type='line', volume=False, style='classic', title='KOSDAQ 3 Years Chart')
        elif chart_type == "10years":
            market_data = stockInfo.get_stock_data('KQ11', date_ranges["ten_years_ago"], date_ranges["current_date"])
            mpf.plot(market_data, type='line', volume=False, style='classic', title='KOSDAQ 10 Years Chart')
        else:
            raise HTTPException(status_code=404, detail="Chart type not found")
    else:
        raise HTTPException(status_code=404, detail="Market not found")

