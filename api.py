from fastapi import APIRouter, Query, HTTPException, Path
from matplotlib import pyplot as plt
from pykrx import stock
from datetime import datetime, timedelta
import pandas as pd
import FinanceDataReader as fdr
import mplfinance as mpf

router = APIRouter()

# 함수 내부에서 사용할 기간 변수 정의
def calculate_date_ranges():
    current_date = datetime.today()
    yesterday = current_date - timedelta(days=1)
    two_days_ago = current_date - timedelta(days=2)
    one_week_ago = (current_date - timedelta(days=9)).strftime('%Y-%m-%d')
    one_month_ago = (current_date - timedelta(days=32)).strftime('%Y-%m-%d')
    three_months_ago = (current_date - timedelta(days=3*30+2)).strftime('%Y-%m-%d')
    one_year_ago = (current_date - timedelta(days=367)).strftime('%Y-%m-%d')
    three_years_ago = (current_date - timedelta(days=3*365+2)).strftime('%Y-%m-%d')
    ten_years_ago = (current_date - timedelta(days=10*365+2)).strftime('%Y-%m-%d')
    return {
        "current_date": current_date,
        "yesterday" : yesterday,
        "two_days_ago" : two_days_ago,
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

# 종목 리스트 가져오는 함수
def get_top_n_stocks(market, n=5):
    df = fdr.StockListing(market)
    df_sorted = df.sort_values(by='Volume', ascending=False)
    selected_columns = ['Name', 'Close', 'Changes', 'ChagesRatio', 'Volume']
    return df_sorted[selected_columns].head(n).to_dict(orient="records")

@router.get("/home")
async def get_kospi_kosdaq_top5():
    date_ranges = calculate_date_ranges()

    # KOSPI, KOSDAQ, USD/KRW 데이터 호출
    kospi_today = get_stock_data('KS11', date_ranges["two_days_ago"], date_ranges["current_date"])
    kosdaq_today = get_stock_data('KQ11', date_ranges["two_days_ago"], date_ranges["current_date"])
    usdkrw_today = fdr.DataReader('USD/KRW', date_ranges["two_days_ago"], date_ranges["current_date"])

    # 종가, 전일비, 등락률
    selected_columns = ['Close', 'Comp', 'Change']

    kospi = kospi_today[selected_columns].to_dict(orient="records")
    kosdaq = kosdaq_today[selected_columns].to_dict(orient="records")

    close_price = usdkrw_today['Close'][-1]
    yesterday_close = usdkrw_today['Close'][-2]
    price_change = close_price - yesterday_close
    percentage_change = (price_change / yesterday_close) * 100

    # 거래량 기준 상위 5개 종목 정보 가져오기
    top_5_kospi = get_top_n_stocks('KOSPI')
    top_5_kosdaq = get_top_n_stocks('KOSDAQ')
    top_5_konex = get_top_n_stocks('KONEX')

    return {
        "kospi": kospi,
        "kosdaq": kosdaq,
        "close_price": close_price,
        "price_change": price_change,
        "percentage_change" : percentage_change,
        "top_5_kospi": top_5_kospi,
        "top_5_kosdaq": top_5_kosdaq,
        "top_5_konex": top_5_konex
    }

@router.get("/home/{market}")
async def get_market_chart(
    market: str = Path(..., description="Market: kospi, kosdaq"),
    chart_type: str = Query(..., description="Chart type: weekly, monthly, 3months, 1years, 3years, 10years")):
    # 데이터 조회를 위한 기간 변수 가져오기
    date_ranges = calculate_date_ranges()

    # 시장 데이터 호출
    market_data = None
    if market.lower() == "kospi":
        if chart_type == "weekly":
            market_data = get_stock_data('KS11', date_ranges["one_week_ago"], date_ranges["current_date"])
            mpf.plot(market_data, type='candle', volume=True, style='classic', title='KOSPI Weekly Chart')
        elif chart_type == "monthly":
            market_data = get_stock_data('KS11', date_ranges["one_month_ago"], date_ranges["current_date"])
            mpf.plot(market_data, type='candle', volume=True, style='classic', title='KOSPI Monthly Chart')
        elif chart_type == "3months":
            market_data = get_stock_data('KS11', date_ranges["three_months_ago"], date_ranges["current_date"])
            mpf.plot(market_data, type='candle', volume=True, style='classic', title='KOSPI 3 Months Chart')
        elif chart_type == "1years":
            market_data = get_stock_data('KS11', date_ranges["one_year_ago"], date_ranges["current_date"])
            mpf.plot(market_data, type='line', volume=False, style='classic', title='KOSPI 1 Year Chart')
        elif chart_type == "3years":
            market_data = get_stock_data('KS11', date_ranges["three_years_ago"], date_ranges["current_date"])
            mpf.plot(market_data, type='line', volume=False, style='classic', title='KOSPI 3 Years Chart')
        elif chart_type == "10years":
            market_data = get_stock_data('KS11', date_ranges["ten_years_ago"], date_ranges["current_date"])
            mpf.plot(market_data, type='line', volume=False, style='classic', title='KOSPI 10 Years Chart')
        else:
            raise HTTPException(status_code=404, detail="Chart type not found")
    elif market.lower() == "kosdaq":
        if chart_type == "weekly":
            market_data = get_stock_data('KQ11', date_ranges["one_week_ago"], date_ranges["current_date"])
            mpf.plot(market_data, type='candle', volume=True, style='classic', title='KOSDAQ Weekly Chart')
        elif chart_type == "monthly":
            market_data = get_stock_data('KQ11', date_ranges["one_month_ago"], date_ranges["current_date"])
            mpf.plot(market_data, type='candle', volume=True, style='classic', title='KOSDAQ Monthly Chart')
        elif chart_type == "3months":
            market_data = get_stock_data('KQ11', date_ranges["three_months_ago"], date_ranges["current_date"])
            mpf.plot(market_data, type='line', volume=True, style='classic', title='KOSDAQ 3 Months Chart')
        elif chart_type == "1years":
            market_data = get_stock_data('KQ11', date_ranges["one_year_ago"], date_ranges["current_date"])
            mpf.plot(market_data, type='line', volume=False, style='classic', title='KOSDAQ 1 Year Chart')
        elif chart_type == "3years":
            market_data = get_stock_data('KQ11', date_ranges["three_years_ago"], date_ranges["current_date"])
            mpf.plot(market_data, type='line', volume=False, style='classic', title='KOSDAQ 3 Years Chart')
        elif chart_type == "10years":
            market_data = get_stock_data('KQ11', date_ranges["ten_years_ago"], date_ranges["current_date"])
            mpf.plot(market_data, type='line', volume=False, style='classic', title='KOSDAQ 10 Years Chart')
        else:
            raise HTTPException(status_code=404, detail="Chart type not found")
    else:
        raise HTTPException(status_code=404, detail="Market not found")

# KRX, KRX-DESC 데이터 가져오기
df_krx_desc = fdr.StockListing('KRX-DESC')
df_krx = fdr.StockListing('KRX')

# 업종 정보를 포함한 데이터 병합
merged_df = pd.merge(df_krx, df_krx_desc[['Code', 'Sector']], on='Code', how='inner')

@router.get("/wics/{sector}")
async def get_wics(
        sector: str = Path(..., description="sector: 업종명")):
    # 사용자가 선택한 업종에 해당하는 데이터 필터링
    sector_data = merged_df[merged_df['Sector'] == sector]

    # 필요한 정보 선택
    selected_columns = ['Name', 'Close', 'Changes', 'ChagesRatio', 'Volume']
    sector_data = sector_data[selected_columns]

    return sector_data.to_dict(orient="records")


# def save_stock_chart(df, filename):
#     mpf.plot(df, type='candle', volume=True, style='classic')
#     # fdr.chart.plot(df)
#     plt.savefig(filename)
#     plt.close()

@router.get("/wics/{sector}/{name}")
async def get_company_info(
        sector: str = Path(..., description="sector: 업종명"),
        name: str = Path(..., description="name: 기업명")):
    def get_stock_data_by_name(name):
        # 사용자가 선택한 기업명에 해당하는 데이터 필터링
        name_data = merged_df[merged_df['Name'] == name]

        # 기업코드, 분류, 기업명, 종가, 전일비, 등락률, 시가, 고가, 저가
        selected_columns = ['Code', 'Market', 'Name', 'Close', 'Changes', 'ChagesRatio', 'Open', 'High', 'Low',
                            'Volume', 'Marcap']
        name_data = name_data[selected_columns]

        return name_data

    def get_per_pbr_for_ticker(all_fundamental, ticker):
        per_pbr_df = all_fundamental.loc[all_fundamental.index == ticker, ['PER', 'PBR']]
        return per_pbr_df

    # 선택한 기업에 대한 주식 데이터 가져오기
    stock_data_selected_name = get_stock_data_by_name(name)

    # 현재 날짜와 어제 날짜 설정
    current_date = datetime.today().strftime('%Y%m%d')
    # yesterday = (datetime.today() - timedelta(days=1)).strftime('%Y%m%d')

    # 시장의 모든 종목의 재무제표
    all_fundamental = stock.get_market_fundamental(current_date, market='ALL')

    # 기업명으로부터 티커 가져오기
    ticker = stock_data_selected_name['Code'].iloc[-1]

    # PER 및 PBR 가져오기
    per_pbr_df = get_per_pbr_for_ticker(all_fundamental, ticker)

    # 주식 데이터 가져오기
    date_ranges = calculate_date_ranges()
    df_name = fdr.DataReader(ticker, date_ranges["one_month_ago"])

    # 그래프로 주식 데이터 플로팅
    # image_path = f"{name}_stock_chart.png"
    # save_stock_chart(df_name, image_path)

    return {
        "sector": sector,
        "stock_data": stock_data_selected_name.to_dict(orient="records"),
        "per_pbr_info": per_pbr_df.to_dict(),
        # "stock_chart_image": image_path
    }



