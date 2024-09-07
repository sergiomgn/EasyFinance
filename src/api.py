import logging

from fastapi import FastAPI
from fastapi.params import Depends
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBasic, HTTPBasiscCredentials

from controller.sql import user_exists
from models.user import UserBase

app = FastAPI(title="EasyFinance", version="0.0.1")
security = HTTPBasic()

logger = logging.getLogger(__name__)
logging.basicConfig()


# User Signup Endpoint
@app.post("/register")
async def register_user(
    credentials: HTTPBasiscCredentials = Depends(security),
) -> JSONResponse:
    """Endpoint that will handle registration of a new user"""

    user = UserBase(username=credentials.username, password=credentials.password)

    created_user, err = await user_exists(user)

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


# Login user
@app.post("/login")
async def login_user(credentials: HTTPBasiscCredentials = Depends(security)):
    """Return JWT token for user future requests"""
    pass
