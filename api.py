from fastapi import APIRouter, Query, HTTPException
from pykrx import stock
from datetime import datetime, timedelta
import pandas as pd
import FinanceDataReader as fdr
import mplfinance as mpf

router = APIRouter()

# 함수 내부에서 사용할 기간 변수 정의
def calculate_date_ranges():
    current_date = datetime.today()
    one_week_ago = (current_date - timedelta(days=9)).strftime('%Y-%m-%d')
    one_month_ago = (current_date - timedelta(days=32)).strftime('%Y-%m-%d')
    three_months_ago = (current_date - timedelta(days=3*30+2)).strftime('%Y-%m-%d')
    one_year_ago = (current_date - timedelta(days=367)).strftime('%Y-%m-%d')
    three_years_ago = (current_date - timedelta(days=3*365+2)).strftime('%Y-%m-%d')
    ten_years_ago = (current_date - timedelta(days=10*365+2)).strftime('%Y-%m-%d')
    return {
        "current_date": current_date,
        "one_week_ago": one_week_ago,
        "one_month_ago": one_month_ago,
        "three_months_ago": three_months_ago,
        "one_year_ago": one_year_ago,
        "three_years_ago": three_years_ago,
        "ten_years_ago": ten_years_ago
    }

# KOSPI, KOSDAQ 데이터 호출 함수
def get_stock_data(stock_code, start_date, end_date):
    return fdr.DataReader(stock_code, start_date, end_date)

@router.get("/home")
async def get_kospi_kosdaq_top5():
    # 데이터 조회를 위한 기간 변수 가져오기
    date_ranges = calculate_date_ranges()

    # KOSPI, KOSDAQ 데이터 호출
    kospi_today = get_stock_data('KS11', date_ranges["current_date"], date_ranges["current_date"])
    kosdaq_today = get_stock_data('KQ11', date_ranges["current_date"], date_ranges["current_date"])

    # 주가, 전일 대비 거래량, 거래비율 등을 계산
    kospi_close = kospi_today['Close'][-1]
    kospi_comp = kospi_today['Comp'][-1]
    kosdaq_close = kosdaq_today['Close'][-1]
    kosdaq_comp = kosdaq_today['Comp'][-1]

    # 거래량 기준 상위 5개 종목 정보 가져오기
    selected_columns = ['Name', 'Close', 'Changes', 'ChagesRatio', 'Volume']
    df_kospi = fdr.StockListing('KOSPI')
    df_kospi_sorted = df_kospi.sort_values(by='Volume', ascending=False)
    df_kospi_selected = df_kospi_sorted[selected_columns].head(5)

    df_kosdaq = fdr.StockListing('KOSDAQ')
    df_kosdaq_sorted = df_kosdaq.sort_values(by='Volume', ascending=False)
    df_kosdaq_selected = df_kosdaq_sorted[selected_columns].head(5)

    df_konex = fdr.StockListing('KONEX')
    df_konex_sorted = df_konex.sort_values(by='Volume', ascending=False)
    df_konex_selected = df_konex_sorted[selected_columns].head(5)

    return {
        # "kospi_close": kospi_close,
        # "kospi_comp": kospi_comp,
        # "kosdaq_close": kosdaq_close,
        # "kosdaq_comp": kosdaq_comp,
        "top_5_kospi": df_kospi_selected.to_dict(orient="records"),
        "top_5_kosdaq": df_kosdaq_selected.to_dict(orient="records"),
        "top_5_konex": df_konex_selected.to_dict(orient="records")
    }

@router.get("/kospi")
async def get_kospi_chart(
    chart_type: str = Query(..., description="Chart type: weekly, monthly, 3months, 1years, 3years")):
    # 데이터 조회를 위한 기간 변수 가져오기
    date_ranges = calculate_date_ranges()

    # KOSPI 데이터 호출
    kospi_data = None
    if chart_type == "weekly":
        kospi_data = get_stock_data('KS11', date_ranges["one_week_ago"], date_ranges["current_date"])
    elif chart_type == "monthly":
        kospi_data = get_stock_data('KS11', date_ranges["one_month_ago"], date_ranges["current_date"])
    elif chart_type == "3months":
        kospi_data = get_stock_data('KS11', date_ranges["three_months_ago"], date_ranges["current_date"])
    elif chart_type == "1years":
        kospi_data = get_stock_data('KS11', date_ranges["one_year_ago"], date_ranges["current_date"])
    elif chart_type == "3years":
        kospi_data = get_stock_data('KS11', date_ranges["three_years_ago"], date_ranges["current_date"])
    else:
        raise HTTPException(status_code=404, detail="Chart type not found")

    if kospi_data is not None:
        mpf.plot(kospi_data, type='candle', volume=True, style='classic', title='KOSPI ' + chart_type)
    else:
        raise HTTPException(status_code=404, detail="Data not found")

@router.get("/kosdaq")
async def get_kosdaq_chart(
        chart_type: str = Query(..., description="Chart type: weekly, monthly, 3months, 1years, 3years")):
    # 데이터 조회를 위한 기간 변수 가져오기
    date_ranges = calculate_date_ranges()

    # KOSDAQ 데이터 호출
    kosdaq_data = None
    if chart_type == "weekly":
        kosdaq_data = get_stock_data('KQ11', date_ranges["one_week_ago"], date_ranges["current_date"])
    elif chart_type == "monthly":
        kosdaq_data = get_stock_data('KQ11', date_ranges["one_month_ago"], date_ranges["current_date"])
    elif chart_type == "3months":
        kosdaq_data = get_stock_data('KQ11', date_ranges["three_months_ago"], date_ranges["current_date"])
    elif chart_type == "1years":
        kosdaq_data = get_stock_data('KQ11', date_ranges["one_year_ago"], date_ranges["current_date"])
    elif chart_type == "3years":
        kosdaq_data = get_stock_data('KQ11', date_ranges["three_years_ago"], date_ranges["current_date"])
    else:
        raise HTTPException(status_code=404, detail="Chart type not found")

    if kosdaq_data is not None:
        mpf.plot(kosdaq_data, type='candle', volume=True, style='classic', title='KOSDAQ ' + chart_type)
    else:
        raise HTTPException(status_code=404, detail="Data not found")

@router.get("/wics/{sector}")
async def get_wics(sector: str):
    # KRX, KRX-DESC 데이터 가져오기
    df_krx_desc = fdr.StockListing('KRX-DESC')
    df_krx = fdr.StockListing('KRX')

    # 업종 정보를 포함한 데이터 병합
    merged_df = pd.merge(df_krx, df_krx_desc[['Code', 'Sector']], on='Code', how='inner')

    # 사용자가 선택한 업종에 해당하는 데이터 필터링
    sector_data = merged_df[merged_df['Sector'] == sector]

    # 필요한 정보 선택
    selected_columns = ['Name', 'Close', 'Changes', 'ChagesRatio', 'Volume']
    sector_data = sector_data[selected_columns]

    return sector_data.to_dict(orient="records")

current_date = datetime.today().strftime('%Y%m%d')
yesterday = (datetime.today() - timedelta(days=1)).strftime('%Y%m%d')

def get_ticker_from_name(name):
    ticker_list = stock.get_market_ticker_list(market="ALL")
    for ticker in ticker_list:
        ticker_name = stock.get_market_ticker_name(ticker)
        if ticker_name == name:
            return ticker
    return None

all_fundamental = stock.get_market_fundamental(current_date, market='ALL')

def get_per_pbr_for_ticker(all_fundamental, ticker):
    per_pbr_df = all_fundamental.loc[all_fundamental.index == ticker, ['PER', 'PBR']]
    return per_pbr_df

# @router.get("/wics/{sector}/{name}")
# async def get_company_info(sector: str, name: str):
#     # KRX, KRX-DESC 데이터 가져오기
#     df_krx_desc = fdr.StockListing('KRX-DESC')
#     df_krx = fdr.StockListing('KRX')
#
#     # 업종 정보를 포함한 데이터 병합
#     merged_df = pd.merge(df_krx, df_krx_desc[['Code', 'Sector']], on='Code', how='inner')
#
#     # 사용자가 선택한 업종에 해당하는 데이터 필터링
#     sector_data = merged_df[merged_df['Sector'] == sector]
#     company_data = sector_data[sector_data['Name'] == name]
#     company_code = company_data['Symbol'].values[0]
#     company_info = fdr.DataReader(company_code)
#
#     selected_info = {
#         'Code': company_code,
#         'Volume': company_info['Volume'][-1],
#         'Close': company_info['Close'][-1],
#         'Open': company_info['Open'][-1],
#         'High': company_info['High'][-1],
#         'Low': company_info['Low'][-1],
#         'MarketCap': company_info['MarketCap'][-1]
#     }
#
#     ticker = get_ticker_from_name(name)
#     print(ticker)
#     if ticker:
#         per_pbr_df = get_per_pbr_for_ticker(all_fundamental, ticker)
#         per_pbr_dict = per_pbr_df.to_dict()
#         return {
#             # "name": name,
#             "PER": per_pbr_dict['PER'][0],
#             "PBR": per_pbr_dict['PBR'][0]
#         }, selected_info
#     else:
#         raise HTTPException(status_code=404, detail="Ticker not found")
#
#
