# FinanceDataApi

## Install
> **FastAPI**
```
pip install fastapi
```

<br/>

> **uvicorn**
```
pip install fastapi uvicorn
```

<br/>

> **데이터 유효성 검사 및 설정 관리**
```
pip install pydantic
```

<br />

> **.env 파일 관리**
```
pip install python-dotenv
```

<br />

> **SQL**
```
sudo apt install pkg-config
pip install SQLAlchemy
pip install mysql
```

<br/>

> **FinanceDataReader**
```
pip install finance-datareader
pip install mplfinance
```

<br/>

> **Pykrx**
```
pip install pykrx
```


## Start
```
uvicorn main:app --reload
```

## Reference
- [FinanceDataReader](https://github.com/FinanceData/FinanceDataReader?tab=readme-ov-file)
- [Pykrx](https://github.com/sharebook-kr/pykrx)

## 기타
pip 오류나는 경우
```
python3 -m pip config set global.break-system-packages true
```
