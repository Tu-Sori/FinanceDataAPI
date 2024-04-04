from fastapi import APIRouter, HTTPException, Path, Depends

from pykrx import stock
from datetime import datetime

from sqlalchemy.orm import Session

from domain import stockInfo, crud
from database.database import SessionLocal, engine
from database import models, schemas
from database.database import get_db


router = APIRouter(
         prefix="/sic"
)


@router.get("")
async def get_sic():
    kospi_info = stockInfo.merged_df[stockInfo.merged_df['Market'] == 'KOSPI']
    kosdaq_info = stockInfo.merged_df[stockInfo.merged_df['Market'] == 'KOSDAQ']
    konex_info = stockInfo.merged_df[stockInfo.merged_df['Market'] == 'KONEX']

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


@router.get("/{sector}")
async def get_sic_select(
        sector: str = Path(..., description="sector: 업종명")):
    sector_data = stockInfo.merged_df_sorted_m[stockInfo.merged_df_sorted_m['Sector'] == sector]

    # 종목명, 현재가, 전일비, 등락률, 거래량
    selected_columns = ['Code', 'Name', 'Close', 'Changes', 'ChagesRatio', 'Volume']
    sector_data = sector_data[selected_columns].to_dict(orient="records")

    return sector_data


@router.get("/{sector}/{name}")
async def get_company_info(
        sector: str = Path(..., description="sector: 업종명"),
        name: str = Path(..., description="name: 기업명")):
    stock_data_selected_name = stockInfo.get_stock_data_by_name(name)

    current_date = datetime.today().strftime('%Y%m%d')
    all_fundamental = stock.get_market_fundamental(current_date, market='ALL')

    ticker = stock_data_selected_name['Code'].iloc[-1]
    per_pbr_df = stockInfo.get_per_pbr_for_ticker(all_fundamental, ticker)

    combined_result = stock_data_selected_name.iloc[0].to_dict()
    combined_result.update(per_pbr_df.iloc[0].to_dict())

    # 주식 데이터 가져오기
    # date_ranges = calculate_date_ranges()
    # df_name = fdr.DataReader(ticker, date_ranges["one_month_ago"])

    top_5_stocks_by_sector = stockInfo.get_top_5_stocks_by_sector(sector, name)
    top_5_stocks_info = []
    for idx, row in top_5_stocks_by_sector.iterrows():
        ticker2 = row['Code']
        per_pbr_df = stockInfo.get_per_pbr_for_ticker(all_fundamental, ticker2)

        combined_result2 = row.to_dict()
        combined_result2.update(per_pbr_df.iloc[0].to_dict())

        top_5_stocks_info.append(combined_result2)

    return {
        "sector": sector,
        "company_info": combined_result,
        "top_5_stocks_info": top_5_stocks_info,
    }


@router.post("/{sector}/{code}", response_model=schemas.InterestStock)
async def create_interest_stock(
        sector: str = Path(..., description="sector: 업종명"),
        code: str = Path(..., description="Stock Code"),
        interestStock: schemas.InterestStockCreate = None,
        db: Session = Depends(get_db)):

    user_id = 1

    existing_interest_stock = crud.get_interest_stock_by_code(db=db, code=code, user_id=user_id)

    if existing_interest_stock:
        raise HTTPException(status_code=400, detail="Interest stock with this code already exists")

    if interestStock is None:
        interestStock = schemas.InterestStockCreate(code=code)
    else:
        interestStock.code = code

    created_interest_stock = crud.create_interest_stock(db=db, interest_stock=interestStock, user_id=user_id)

    if created_interest_stock is None:
        raise HTTPException(status_code=400, detail="Failed to create interest stock")

    return created_interest_stock


@router.delete("/sic/{sector}/{code}", response_model=schemas.InterestStock)
async def delete_interest_stock(
        sector: str = Path(..., description="sector: 업종명"),
        code: str = Path(..., description="기업코드"),
        db: Session = Depends(get_db)):

    user_id = 1

    deleted_interest_stock = crud.delete_interest_stock(db=db, code=code, user_id=user_id)

    if deleted_interest_stock is None:
        raise HTTPException(status_code=404, detail="Interest stock not found")

    return deleted_interest_stock
