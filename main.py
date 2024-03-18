from fastapi import FastAPI
from api import router
from database import engineconn
from models import Test

app = FastAPI()
app.include_router(router)
# engine = engineconn()
# session = engine.sessionmaker()

# @app.get("/")
# async def test_db():
#     example = session.query(Test).all()
#     return example

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
