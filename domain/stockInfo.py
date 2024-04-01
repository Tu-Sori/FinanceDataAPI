from pykrx import stock
from datetime import datetime, timedelta
import pandas as pd
import FinanceDataReader as fdr


# KRX, KRX-DESC -> 기준: Code 병합 및 정렬
df_krx_desc = fdr.StockListing('KRX-DESC')
df_krx = fdr.StockListing('KRX')
merged_df = pd.merge(df_krx, df_krx_desc[['Code', 'Sector']], on='Code', how='inner')
merged_df.fillna({'Sector': '우선주'}, inplace=True)

merged_df_sorted = merged_df.sort_values(by='Volume', ascending=False)
merged_df_sorted_m = merged_df.sort_values(by='Marcap', ascending=False)


# 기간 설정
def calculate_date_ranges():
    current_date = datetime.today()
    day_of_week = current_date.weekday()

    if day_of_week == 0:
        yesterday = (current_date - timedelta(days=3)).strftime('%Y-%m-%d')
    elif day_of_week == 5:
        yesterday = (current_date - timedelta(days=2)).strftime('%Y-%m-%d')
    elif day_of_week == 6:
        yesterday = (current_date - timedelta(days=1)).strftime('%Y-%m-%d')
    else:
        yesterday = (current_date - timedelta(days=1)).strftime('%Y-%m-%d')
        print(yesterday)

    two_days_ago = (current_date - timedelta(days=2)).strftime('%Y-%m-%d')
    print(two_days_ago)

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

# 종목 리스트 5개
def get_top_n_stocks(market, n=5):
    df = fdr.StockListing(market)
    df_sorted = df.sort_values(by='Volume', ascending=False)
    selected_columns = ['Name', 'Close', 'Changes', 'ChagesRatio', 'Volume']
    return df_sorted[selected_columns].head(n).to_dict(orient="records")

def get_top_n_save_stocks(code, n=5):
    sector_data = merged_df_sorted[merged_df_sorted['Code'] == code]
    selected_columns = ['Name', 'Close', 'Changes', 'ChagesRatio', 'Volume']
    return sector_data[selected_columns].head(n).to_dict(orient="records")

# 이름 -> 기업정보
def get_stock_data_by_name(name):
    name_data = merged_df_sorted_m[merged_df_sorted_m['Name'] == name]

    # 기업코드, 분류, 기업명, 종가, 전일비, 등락률, 시가, 고가, 저가, 상장주식수
    selected_columns = ['Code', 'Market', 'Name', 'Close', 'Changes', 'ChagesRatio',
                        'Open', 'High', 'Low', 'Volume', 'Marcap', 'Stocks']
    name_data = name_data[selected_columns]

    return name_data

# 기업코드 -> 기업정보
def get_stock_data_by_code(code):
    sector_data = merged_df_sorted_m[merged_df_sorted_m['Code'] == code]

    # 기업코드, 종목명, 현재가, 전일비, 등락률, 시가, 고가, 저가, 거래량, 시가총액
    selected_columns = ['Code', 'Name', 'Sector', 'Close', 'Changes', 'ChagesRatio', 'Open', 'High', 'Low', 'Volume', 'Marcap']
    sector_data = sector_data[selected_columns]

    return sector_data

def get_save_stock_data_by_code(code):
    sector_data = merged_df_sorted_m[merged_df_sorted_m['Code'] == code]

    selected_columns = ['Code', 'Name']
    sector_data = sector_data[selected_columns]

    return sector_data

# 'PER', 'PBR', 'EPS', 'DIV'
def get_per_pbr_for_ticker(all_fundamental, ticker):
    per_pbr_df = all_fundamental.loc[all_fundamental.index == ticker, ['PER', 'PBR', 'EPS', 'DIV']]
    return per_pbr_df

# 동일 업종 기업 5개
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















