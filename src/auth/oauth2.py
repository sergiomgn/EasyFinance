import os
from datetime import datetime, timedelta

from fastapi.security import HTTPException, OAuth2PasswordBearer
from jose import JWTError, jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_TOKEN_EXPIRE_DAYS = 7


async def create_token(data: dict, token_type: str):
    to_encode = data.copy()
    expire = datetime.utcnow() + (
        timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
        if token_type == "REFRESH"
        else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, SECRET_KEY, algorith=ALGORITHM)


async def get_new_refresh_token(refresh_token: str):
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorith=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid refresh token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    new_access_token = create_token(data={"sub": username}, token_type="REFRESH")

    return {"access_token": new_access_token, "token_type": "bearer"}
