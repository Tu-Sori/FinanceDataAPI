from fastapi import APIRouter, Query, HTTPException, Path, Depends

import FinanceDataReader as fdr
import mplfinance as mpf

from domain import stockInfo
from database.database import SessionLocal, engine
from database import models, schemas
from database.database import get_db


router = APIRouter(
         prefix="/home"
)


@router.get("/")
async def get_kospi_kosdaq_top5():
    # KOSPI, KOSDAQ, USD/KRW
    date_ranges = stockInfo.calculate_date_ranges()
    kospi_today = stockInfo.get_stock_data('KS11', date_ranges["yesterday"], date_ranges["current_date"])
    kosdaq_today = stockInfo.get_stock_data('KQ11', date_ranges["yesterday"], date_ranges["current_date"])
    usdkrw_today = fdr.DataReader('USD/KRW', date_ranges["yesterday"], date_ranges["current_date"])

    # 종가, 전일비, 등락률
    selected_columns = ['Close', 'Comp', 'Change']
    kospi = kospi_today[selected_columns].iloc[0].to_dict()
    kosdaq = kosdaq_today[selected_columns].iloc[0].to_dict()

    close_price = usdkrw_today['Close'][-1]
    yesterday_close = usdkrw_today['Close'][-2]
    price_change = close_price - yesterday_close
    percentage_change = (price_change / yesterday_close) * 100

    usdkrw_data = {
        "close_price": close_price,
        "price_change": price_change,
        "percentage_change": percentage_change
    }

    # 상위 5개(기준: 거래량)
    top_5_kospi = stockInfo.get_top_n_stocks('KOSPI')
    top_5_kosdaq = stockInfo.get_top_n_stocks('KOSDAQ')
    top_5_konex = stockInfo.get_top_n_stocks('KONEX')

    return {
        "kospi": kospi,
        "kosdaq": kosdaq,
        "usdkrw_data": usdkrw_data,
        "top_5_kospi": top_5_kospi,
        "top_5_kosdaq": top_5_kosdaq,
        "top_5_konex": top_5_konex
    }


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

