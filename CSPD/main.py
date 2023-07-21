from datetime import datetime
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field
from base import *
from fastapi_users import fastapi_users, FastAPIUsers
from security import *
from jose import jwt
from jose import JWTError
from fastapi import HTTPException

from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

app = FastAPI(
    title="Salary_Promotion_Date"
)


# Благодаря этой функции клиент видит ошибки, происходящие на сервере, вместо "Internal server error"
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors()}),
    )

credentials_exception = HTTPException(       #вывод ошибки при невалидном токене
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )

@app.post("/login/get_token", response_model=None)    #пост-запрос проверки логина и пароля со связью с имитированной базой данных из base.py и выдача токена
def get_user(email: str, password: str):
    answer = []
    for user in database_security:
        if user.get("email") == email and user.get("hashed_password") == password:
            answer.append(user)
            return "Your token, which will be valid for 30 minutes, is ready:  " + create_access_token({'data': database_data[database_security.index(user)]})
    if answer == []:
        return  " Incorrect username or password"



@app.post("/token_input", response_model=None)  #пост-запрос на проверку валидности токена с выдачей данных либо ошибки
def token_input(token: str):
    try:
        payload = jwt.decode(
            token, SECRET_KEY, algorithms=[ALGORITHM]
        )
    except JWTError:
        raise credentials_exception 
    return payload
    