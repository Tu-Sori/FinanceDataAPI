from fastapi import FastAPI
from domain import home, sic, mypage
from database.database import engine


app = FastAPI()

@app.on_event("startup")
def startup():
    engine.connect()

@app.on_event("shutdown")
def shutdown():
    engine.disconnect()

app.include_router(home.router)
app.include_router(sic.router)
app.include_router(mypage.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
