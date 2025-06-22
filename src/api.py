import logging

from fastapi import FastAPI
from fastapi.params import Depends
from fastapi.responses import JSONResponse
from fastapi.security import (HTTPBasic, HTTPBasicCredentials,
                              OAuth2PassworRequestForm)

from auth.oauth2 import auth_user, create_token, get_new_refresh_token
from controller import auth_user, create_user, user_exists
from models.user import UserBase

app = FastAPI(title="EasyFinance", version="0.0.1")
security = HTTPBasic()

logger = logging.getLogger(__name__)
logging.basicConfig()


# User Signup Endpoint
@app.post("/register")
async def register_user(
    credentials: HTTPBasicCredentials = Depends(security),
) -> JSONResponse:
    """Endpoint that will handle registration of a new user"""

    user = UserBase(username=credentials.username, password=credentials.password)

    created_user, err = await db.user_exists(user)

    if err:
        logging.error(err)
        return JSONResponse(
            {"error_message": "An error occorred while registering the user"},
            status_code=500,
        )
    if created_user:
        return JSONResponse(
            {"error_message": "A user with that username already exists"},
            status_code=400,
        )
    logger.info("New user created %s")
    return JSONResponse({"message": "User successfully created"}, status_code=200)


# Token
@app.post("/login")
async def login_user(credentials: OAuth2PassworRequestForm = Depends()):
    """Return JWT token for user future requests"""
    user = await auth_user(credentials=UserBase(credentials.username, credentials.password))

    access_token = create_token(data={"sub": user.username}, token_type="TOKEN")
    refresh_token = create_token(data={"sub": user.username}, token_type="REFRESH")

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


@app.post("/refresh")
async def refresh_token(refresh_token: str):
    new_access_token = get_new_refresh_token(refresh_token)

    return {"access_token": new_access_token, "token_type": "bearer"}

@app.post("/register")
async def register_user(credentials: HTTPBasicCredentials = Depends(security)) -> JSONResponse:
    """Endpoint that will handle registration of a new user"""
    
    username = credentials.username
    password = credentials.password

    user = UserBase(username, password)

    # Check if the user already exists
    created_user, err = await user_exists(user)

    if err:
        logging.error(err)
        return JSONResponse(
            {"error_message": "An error occurred while registering the user"},
            status_code=500,
        )
    
    if created_user:
        return JSONResponse(
            {"error_message": "A user with that username already exists"},
            status_code=400,
        )
    
    # Add new user to database
    err = await create_user(user)
    if err:
        logging.error(err)
        return JSONResponse(
            {"error_message": "An error occurred while registering the user"},
            status_code=500,
        )
    
    logger.info("New user created %s" % username)

