from typing import Optional
from fastapi import APIRouter, Query, HTTPException, Path, Depends, Header
from fastapi.responses import FileResponse

import mplfinance as mpf
import matplotlib.pyplot as plt

from sqlalchemy.orm import Session
from domain import stockInfo, crud
from database.database import get_db
from oauth import validation_token


router = APIRouter(
         prefix="/home"
)


@router.get("")
async def get_data():
    market_data = stockInfo.get_market_data()
    # 상위 5개(기준: 거래량)
    top_5_kospi = stockInfo.get_top_n_stocks('KOSPI')
    top_5_kosdaq = stockInfo.get_top_n_stocks('KOSDAQ')
    top_5_konex = stockInfo.get_top_n_stocks('KONEX')

    data = {
        **market_data,
        "top_5_kospi": top_5_kospi,
        "top_5_kosdaq": top_5_kosdaq,
        "top_5_konex": top_5_konex
    }

    return data


@router.get("/user")
async def get_data(user_id: Optional[int] = Depends(validation_token),
                   db: Session = Depends(get_db)):
    user_data = None

    if user_id is not None:
        user = crud.get_user(db=db, user_id=user_id)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")

        stock_records = crud.get_stock_record(db=db, user_id=user_id)
        if stock_records is None:
            raise HTTPException(status_code=404, detail="stock_record not found")

        sell_or_buy = [int.from_bytes(record.sell_or_buy, byteorder='little', signed=True) for record in stock_records]
        codes = [record.code for record, buy_sell in zip(stock_records, sell_or_buy) if buy_sell == 1]
        save_stocks = []
        for code in codes:
            stock_data = stockInfo.get_top_n_save_stocks(code)
            save_stocks.append(stock_data)

        user_data = {
            "user": user,
            "save_stocks": save_stocks
        }

    return {
        "user_data": user_data,
    }


@router.get("/{market}")
async def get_market_chart(market: str = Path(..., description="Market: kospi, kosdaq"),
                           chart_type: str = Query(..., description="Chart type: weekly, monthly, 3months, 1years, 3years, 10years")):
    date_ranges = stockInfo.calculate_date_ranges()

    market_data = None
    if market.lower() == "kospi":
        if chart_type == "weekly":
            market_data = stockInfo.get_stock_data('KS11', date_ranges["one_week_ago"], date_ranges["current_date"])
            mpf.plot(market_data, type='candle', volume=True, style='classic', title='KOSPI Weekly Chart')
            image_path = "kospi_weekly_chart.png"
            plt.savefig(image_path)
        elif chart_type == "monthly":
            market_data = stockInfo.get_stock_data('KS11', date_ranges["one_month_ago"], date_ranges["current_date"])
            mpf.plot(market_data, type='candle', volume=True, style='classic', title='KOSPI Monthly Chart')
            image_path = "kospi_monthly_chart.png"
            plt.savefig(image_path)
        elif chart_type == "3months":
            market_data = stockInfo.get_stock_data('KS11', date_ranges["three_months_ago"], date_ranges["current_date"])
            mpf.plot(market_data, type='candle', volume=True, style='classic', title='KOSPI 3 Months Chart')
            image_path = "kospi_3months_chart.png"
            plt.savefig(image_path)
        elif chart_type == "1years":
            market_data = stockInfo.get_stock_data('KS11', date_ranges["one_year_ago"], date_ranges["current_date"])
            mpf.plot(market_data, type='line', volume=False, style='classic', title='KOSPI 1 Year Chart')
            image_path = "kospi_1years_chart.png"
            plt.savefig(image_path)
        elif chart_type == "3years":
            market_data = stockInfo.get_stock_data('KS11', date_ranges["three_years_ago"], date_ranges["current_date"])
            mpf.plot(market_data, type='line', volume=False, style='classic', title='KOSPI 3 Years Chart')
            image_path = "kospi_3years_chart.png"
            plt.savefig(image_path)
        elif chart_type == "10years":
            market_data = stockInfo.get_stock_data('KS11', date_ranges["ten_years_ago"], date_ranges["current_date"])
            mpf.plot(market_data, type='line', volume=False, style='classic', title='KOSPI 10 Years Chart')
            image_path = "kospi_10years_chart.png"
            plt.savefig(image_path)
        else:
            raise HTTPException(status_code=404, detail="Chart type not found")
    elif market.lower() == "kosdaq":
        if chart_type == "weekly":
            market_data = stockInfo.get_stock_data('KQ11', date_ranges["one_week_ago"], date_ranges["current_date"])
            mpf.plot(market_data, type='candle', volume=True, style='classic', title='KOSDAQ Weekly Chart')
            image_path = "kosdaq_weekly_chart.png"
            plt.savefig(image_path)
        elif chart_type == "monthly":
            market_data = stockInfo.get_stock_data('KQ11', date_ranges["one_month_ago"], date_ranges["current_date"])
            mpf.plot(market_data, type='candle', volume=True, style='classic', title='KOSDAQ Monthly Chart')
            image_path = "kosdaq_monthly_chart.png"
            plt.savefig(image_path)
        elif chart_type == "3months":
            market_data = stockInfo.get_stock_data('KQ11', date_ranges["three_months_ago"], date_ranges["current_date"])
            mpf.plot(market_data, type='line', volume=True, style='classic', title='KOSDAQ 3 Months Chart')
            image_path = "kosdaq_3months_chart.png"
            plt.savefig(image_path)
        elif chart_type == "1years":
            market_data = stockInfo.get_stock_data('KQ11', date_ranges["one_year_ago"], date_ranges["current_date"])
            mpf.plot(market_data, type='line', volume=False, style='classic', title='KOSDAQ 1 Year Chart')
            image_path = "kosdaq_1years_chart.png"
            plt.savefig(image_path)
        elif chart_type == "3years":
            market_data = stockInfo.get_stock_data('KQ11', date_ranges["three_years_ago"], date_ranges["current_date"])
            mpf.plot(market_data, type='line', volume=False, style='classic', title='KOSDAQ 3 Years Chart')
            image_path = "kosdaq_3years_chart.png"
            plt.savefig(image_path)
        elif chart_type == "10years":
            market_data = stockInfo.get_stock_data('KQ11', date_ranges["ten_years_ago"], date_ranges["current_date"])
            mpf.plot(market_data, type='line', volume=False, style='classic', title='KOSDAQ 10 Years Chart')
            image_path = "kosdaq_10years_chart.png"
            plt.savefig(image_path)
        else:
            raise HTTPException(status_code=404, detail="Chart type not found")
    else:
        raise HTTPException(status_code=404, detail="Market not found")

    return FileResponse(image_path, media_type="image/png")