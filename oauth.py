from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer
from jose import jwt, JWTError
import os
from sqlalchemy.orm import Session
from database.database import get_db
from domain import crud

router = APIRouter(
         prefix="/user"
)

oauth2_bearer = HTTPBearer()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"

def validation_token(token: str = Depends(oauth2_bearer)):
    try:
        payload = jwt.decode(token.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        print("Decoded payload:", payload)
        user_id: int = payload["userId"]
        print("User ID from token:", user_id)
        if user_id is None:
            raise HTTPException(status_code=404, detail="User not found")
        return user_id
    except JWTError:
        return HTTPException(status_code=401, detail="Could not validate credentials")

@router.get("/kakao")
async def get_user(user_id: int = Depends(validation_token),
                   db: Session = Depends(get_db)):
    user = crud.get_user(db=db, user_id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user
