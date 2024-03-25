from fastapi import FastAPI
from domain import home, sic, mypage
from database.database import engine
from database import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


app.include_router(home.router)
app.include_router(sic.router)
app.include_router(mypage.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
