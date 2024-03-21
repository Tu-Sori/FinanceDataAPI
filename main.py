from fastapi import FastAPI
from api import router
from database import EngineConn

app = FastAPI()
app.include_router(router)

engine = EngineConn()
session = engine.sessionmaker()

@app.get("/")
async def index():
    return {
        "Python": "Framework",
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
