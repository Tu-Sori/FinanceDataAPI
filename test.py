from fastapi import APIRouter, Query, HTTPException
from pykrx import stock
from datetime import datetime, timedelta
import pandas as pd
import FinanceDataReader as fdr
import mplfinance as mpf

router = APIRouter()

# 현재, 어제 날짜
current_date = datetime.today()
yesterday = current_date - timedelta(days=1)

# 데이터 조회를 위한 기간
one_week_ago = (current_date - timedelta(days=9)).strftime('%Y-%m-%d')
one_month_ago = (current_date - timedelta(days=32)).strftime('%Y-%m-%d')
three_months_ago = (current_date - timedelta(days=3*30+2)).strftime('%Y-%m-%d')
one_year_ago = (current_date - timedelta(days=367)).strftime('%Y-%m-%d')
three_years_ago = (current_date - timedelta(days=3*365+2)).strftime('%Y-%m-%d')
ten_years_ago = (current_date - timedelta(days=10*365+2)).strftime('%Y-%m-%d')

# KOSPI, KOSDAQ
# 전일, 당일, ((당일(일봉))), 1주(주봉), 한 달(월봉), 3개월, 1년, 3년, 10년
kospi_yesterday = fdr.DataReader('KS11', yesterday)
kospi_today = fdr.DataReader('KS11', current_date)
kospi_weekly = fdr.DataReader('KS11', one_week_ago, current_date)
kospi_monthly = fdr.DataReader('KS11', one_month_ago, current_date)
kospi_3months = fdr.DataReader('KS11', three_months_ago, current_date)
kospi_1years = fdr.DataReader('KS11', one_year_ago, current_date)
kospi_3years = fdr.DataReader('KS11', three_years_ago, current_date)
kospi_10years = fdr.DataReader('KS11', ten_years_ago, current_date)

kosdaq_yesterday = fdr.DataReader('KQ11', yesterday)
kosdaq_today = fdr.DataReader('KQ11', current_date)
kosdaq_weekly = fdr.DataReader('KQ11', one_week_ago, current_date)
kosdaq_monthly = fdr.DataReader('KQ11', one_month_ago, current_date)
kosdaq_3months = fdr.DataReader('KQ11', three_months_ago, current_date)
kosdaq_1years = fdr.DataReader('KQ11', one_year_ago, current_date)
kosdaq_3years = fdr.DataReader('KQ11', three_years_ago, current_date)
kosdaq_10years = fdr.DataReader('KQ11', ten_years_ago, current_date)

@router.get("/home")
async def get_kospi_kosdaq_top5():
    # KOSPI, KOSDAQ
    # 주가, 전일 대비 거래량, 거래비율
    kospi_close = kospi_today['Close'][-1]
    kospi_comp = kospi_today['Comp'][-1]
    # kospi_volume_change = kospi_today['Volume'][-1] / kospi_yesterday['Volume'][-1]

    # 코스닥(KOSDAQ) 종가, 거래량, 거래대금 데이터 가져오기
    kosdaq_close = kosdaq_today['Close'][-1]
    kosdaq_comp = kosdaq_today['Comp'][-1]
    # kosdaq_volume_change = kosdaq_today['Volume'][-1] / kosdaq_yesterday['Volume'][-1]

    # 거래량 기준 top 5개(KOSPI, KOSDAQ)
    # 종목명, 현재가, 전일비, 등락률, 거래량
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

    return (
        kospi_close,
        kospi_comp,
        # kospi_volume_change,
        kosdaq_close,
        kosdaq_comp,
        # kosdaq_volume_change,
        df_kospi_selected.to_dict(orient="records"),
        df_kosdaq_selected.to_dict(orient="records"),
        df_konex_selected.to_dict(orient="records")
    )

@router.get("/kospi")
async def get_kospi_chart(
        chart_type: str = Query(..., description="Chart type: weekly, monthly, 3months, 1years, 3years")):
    if chart_type == "weekly":
        mpf.plot(kospi_weekly, type='candle', volume=True, style='classic', title='KOSPI Weekly')
    elif chart_type == "monthly":
        mpf.plot(kospi_monthly, type='candle', volume=True, style='classic', title='KOSPI Monthly')
    elif chart_type == "3months":
        mpf.plot(kospi_3months, type='line', volume=True, style='classic', title='KOSPI 3months')
    elif chart_type == "1years":
        mpf.plot(kospi_1years, type='line', volume=True, style='classic', title='KOSPI 1years')
    elif chart_type == "3years":
        mpf.plot(kospi_3years, type='line', volume=True, style='classic', title='KOSPI 3years')
    else:
        raise HTTPException(status_code=404, detail="Chart type not found")

    return {chart_type}


@router.get("/kosdaq")
async def get_kosdaq_chart(
        chart_type: str = Query(..., description="Chart type: weekly, monthly, 3months, 1years, 3years")):
    if chart_type == "weekly":
        mpf.plot(kosdaq_weekly, type='candle', volume=True, style='classic', title='KOSDAQ Weekly')
    elif chart_type == "monthly":
        mpf.plot(kosdaq_monthly, type='candle', volume=True, style='classic', title='KOSDAQ Monthly')
    elif chart_type == "3months":
        mpf.plot(kosdaq_3months, type='line', volume=True, style='classic', title='KOSDAQ 3months')
    elif chart_type == "1years":
        mpf.plot(kosdaq_1years, type='line', volume=True, style='classic', title='KOSDAQ 1years')
    elif chart_type == "3years":
        mpf.plot(kosdaq_3years, type='line', volume=True, style='classic', title='KOSDAQ 3years')
    else:
        raise HTTPException(status_code=404, detail="Chart type not found")

    return {chart_type}

@router.get("/wics/{sector}")
async def get_wics(sector: str):
    df_krx_desc = fdr.StockListing('KRX-DESC')
    df_krx = fdr.StockListing('KRX')

    # df_krx에 sector 추가
    merged_df = pd.merge(df_krx, df_krx_desc[['Code', 'Sector']], on='Code', how='inner')

    def get_stock_data_by_sector(sector):
        # 사용자가 선택한 업종에 해당하는 데이터 필터링
        sector_data = merged_df[merged_df['Sector'] == sector]

        # 종목명, 현재가, 전일비, 등락률, 거래량, ((순매수호가잔량))
        selected_columns = ['Name', 'Close', 'Changes', 'ChagesRatio', 'Volume']
        sector_data = sector_data[selected_columns]

        return sector_data.to_dict(orient="records")

    return get_stock_data_by_sector(sector)



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

@router.get("/wics/{sector}/{name}")
async def get_company_info(sector: str, name: str):
    df_krx = fdr.StockListing('KRX')
    sector_data = df_krx[df_krx['Sector'] == sector]
    company_data = sector_data[sector_data['Name'] == name]
    company_code = company_data['Symbol'].values[0]
    company_info = fdr.DataReader(company_code)

    selected_info = {
        'Code': company_code,
        'Volume': company_info['Volume'][-1],
        'Close': company_info['Close'][-1],
        'Open': company_info['Open'][-1],
        'High': company_info['High'][-1],
        'Low': company_info['Low'][-1],
        'MarketCap': company_info['MarketCap'][-1]
    }

    ticker = get_ticker_from_name(name)
    print(ticker)
    if ticker:
        per_pbr_df = get_per_pbr_for_ticker(all_fundamental, ticker)
        per_pbr_dict = per_pbr_df.to_dict()
        return {
            # "name": name,
            "PER": per_pbr_dict['PER'][0],
            "PBR": per_pbr_dict['PBR'][0]
        }, selected_info
    else:
        raise HTTPException(status_code=404, detail="Ticker not found")


