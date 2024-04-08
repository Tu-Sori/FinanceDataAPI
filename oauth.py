from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.security import HTTPBearer
import jwt
import os

router = APIRouter(
         prefix="/user"
)

oauth2_scheme = HTTPBearer()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"

def validation_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload["sub"]
        print(user_id)
        # if user_id is None:
        #     raise HTTPException(status_code=401, detail="Invalid user ID in JWT token")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Expired JWT token")
    except jwt.DecodeError:
        raise HTTPException(status_code=401, detail="Invalid JWT token")

    return user_id

@router.get("/kakao")
async def get_user_id(user_id: int = Depends(validation_token)):
    return {"user_id": user_id}
