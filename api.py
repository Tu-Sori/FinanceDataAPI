from fastapi import APIRouter, Query, HTTPException, Path
from matplotlib import pyplot as plt
from pykrx import stock
from datetime import datetime, timedelta
import pandas as pd
import FinanceDataReader as fdr
import mplfinance as mpf

router = APIRouter()

# 기간 설정
def calculate_date_ranges():
    current_date = datetime.today()
    yesterday = current_date - timedelta(days=1)

    day_of_week = current_date.weekday()

    if day_of_week == 0:
        two_days_ago = (current_date - timedelta(days=3)).strftime('%Y-%m-%d')
    elif day_of_week == 5:
        two_days_ago = (current_date - timedelta(days=2)).strftime('%Y-%m-%d')
    elif day_of_week == 6:
        two_days_ago = (current_date - timedelta(days=1)).strftime('%Y-%m-%d')
    else:
        two_days_ago = (current_date - timedelta(days=2)).strftime('%Y-%m-%d')

    one_week_ago = (current_date - timedelta(days=9)).strftime('%Y-%m-%d')
    one_month_ago = (current_date - timedelta(days=32)).strftime('%Y-%m-%d')
    three_months_ago = (current_date - timedelta(days=3*30+2)).strftime('%Y-%m-%d')
    one_year_ago = (current_date - timedelta(days=367)).strftime('%Y-%m-%d')
    three_years_ago = (current_date - timedelta(days=3*365+2)).strftime('%Y-%m-%d')
    ten_years_ago = (current_date - timedelta(days=10*365+2)).strftime('%Y-%m-%d')
    return {
        "current_date": current_date,
        "yesterday": yesterday,
        "two_days_ago": two_days_ago,
        "one_week_ago": one_week_ago,
        "one_month_ago": one_month_ago,
        "three_months_ago": three_months_ago,
        "one_year_ago": one_year_ago,
        "three_years_ago": three_years_ago,
        "ten_years_ago": ten_years_ago
    }

# KOSPI, KOSDAQ
def get_stock_data(stock_code, start_date, end_date):
    return fdr.DataReader(stock_code, start_date, end_date)

# 종목 리스트
def get_top_n_stocks(market, n=5):
    df = fdr.StockListing(market)
    df_sorted = df.sort_values(by='Volume', ascending=False)
    selected_columns = ['Name', 'Close', 'Changes', 'ChagesRatio', 'Volume']
    return df_sorted[selected_columns].head(n).to_dict(orient="records")

# KRX, KRX-DESC -> 기준: Code 병합 및 정렬
df_krx_desc = fdr.StockListing('KRX-DESC')
df_krx = fdr.StockListing('KRX')
merged_df = pd.merge(df_krx, df_krx_desc[['Code', 'Sector']], on='Code', how='inner')
merged_df.fillna({'Sector': '우선주'}, inplace=True)

merged_df_sorted = merged_df.sort_values(by='Volume', ascending=False)
merged_df_sorted_m = merged_df.sort_values(by='Marcap', ascending=False)

@router.get("/")
async def read_root():
    return {"message": "Hello, World"}

@router.get("/home")
async def get_kospi_kosdaq_top5():
    # KOSPI, KOSDAQ, USD/KRW
    date_ranges = calculate_date_ranges()
    print(date_ranges)
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

    # 상위 5개(기준: 거래량)
    top_5_kospi = get_top_n_stocks('KOSPI')
    top_5_kosdaq = get_top_n_stocks('KOSDAQ')
    top_5_konex = get_top_n_stocks('KONEX')

    return {
        "kospi": kospi,
        "kosdaq": kosdaq,
        "close_price": close_price,
        "price_change": price_change,
        "percentage_change": percentage_change,
        "top_5_kospi": top_5_kospi,
        "top_5_kosdaq": top_5_kosdaq,
        "top_5_konex": top_5_konex
    }


@router.get("/home/{market}")
async def get_market_chart(
    market: str = Path(..., description="Market: kospi, kosdaq"),
    chart_type: str = Query(..., description="Chart type: weekly, monthly, 3months, 1years, 3years, 10years")):
    date_ranges = calculate_date_ranges()

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

@router.get("/sic")
async def get_sic():
    kospi_info = merged_df[merged_df['Market'] == 'KOSPI']
    kosdaq_info = merged_df[merged_df['Market'] == 'KOSDAQ']
    konex_info = merged_df[merged_df['Market'] == 'KONEX']

    def group_and_classify_by_sector(df_market):
        grouped_by_sector = df_market.groupby('Sector')
        sector_names = list(grouped_by_sector.groups.keys())
        return sector_names

    kospi_sectors = group_and_classify_by_sector(kospi_info)
    kosdaq_sectors = group_and_classify_by_sector(kosdaq_info)
    konex_sectors = group_and_classify_by_sector(konex_info)

    return {
        "KOSPI": kospi_sectors,
        "KOSDAQ": kosdaq_sectors,
        "KONEX": konex_sectors
    }


@router.get("/sic/{sector}")
async def get_sic_select(
        sector: str = Path(..., description="sector: 업종명")):
    sector_data = merged_df_sorted_m[merged_df_sorted_m['Sector'] == sector]

    # 종목명, 현재가, 전일비, 등락률, 거래량
    selected_columns = ['Name', 'Close', 'Changes', 'ChagesRatio', 'Volume']
    sector_data = sector_data[selected_columns].to_dict(orient="records")

    return sector_data


@router.get("/sic/{sector}/{name}")
async def get_company_info(
        sector: str = Path(..., description="sector: 업종명"),
        name: str = Path(..., description="name: 기업명")):
    def get_stock_data_by_name(name):
        name_data = merged_df_sorted_m[merged_df_sorted_m['Name'] == name]

        # 기업코드, 분류, 기업명, 종가, 전일비, 등락률, 시가, 고가, 저가, 상장주식수
        selected_columns = ['Code', 'Market', 'Name', 'Close', 'Changes', 'ChagesRatio', 'Open', 'High', 'Low',
                            'Volume', 'Marcap', 'Stocks']
        name_data = name_data[selected_columns]

        return name_data

    def get_per_pbr_for_ticker(all_fundamental, ticker):
        per_pbr_df = all_fundamental.loc[all_fundamental.index == ticker, ['PER', 'PBR', 'EPS', 'DIV']]
        return per_pbr_df

    def get_top_5_stocks_by_sector(sector, name):
        sector_stocks = merged_df_sorted_m[merged_df_sorted_m['Sector'] == sector]

        # 기업코드, 기업명, 현재가, 전일비, 등락률, 거래량, 시가총액
        selected_columns = ['Code', 'Name', 'Close', 'ChagesRatio', 'Volume', 'Marcap']
        top_5_stocks = sector_stocks[selected_columns]

        if name in top_5_stocks['Name'].values:
            top_5_stocks = top_5_stocks[top_5_stocks['Name'] != name].head(5)
        else:
            top_5_stocks = top_5_stocks.head(5)

        return top_5_stocks

    stock_data_selected_name = get_stock_data_by_name(name)

    current_date = datetime.today().strftime('%Y%m%d')
    all_fundamental = stock.get_market_fundamental(current_date, market='ALL')

    ticker = stock_data_selected_name['Code'].iloc[-1]
    per_pbr_df = get_per_pbr_for_ticker(all_fundamental, ticker)

    combined_result = stock_data_selected_name.iloc[0].to_dict()
    combined_result.update(per_pbr_df.iloc[0].to_dict())

    # 주식 데이터 가져오기
    # date_ranges = calculate_date_ranges()
    # df_name = fdr.DataReader(ticker, date_ranges["one_month_ago"])

    top_5_stocks_by_sector = get_top_5_stocks_by_sector(sector, name)
    top_5_stocks_info = []
    for idx, row in top_5_stocks_by_sector.iterrows():
        ticker2 = row['Code']
        per_pbr_df = get_per_pbr_for_ticker(all_fundamental, ticker2)

        combined_result2 = row.to_dict()
        combined_result2.update(per_pbr_df.iloc[0].to_dict())

        top_5_stocks_info.append(combined_result2)

    return {
        "sector": sector,
        "company_info": combined_result,
        "top_5_stocks_info": top_5_stocks_info,
    }



