import sys
sys.path.append("..")

from fastapi import FastAPI, status, HTTPException, APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import RedirectResponse
from .models import Users
from .services.utils import (
    get_password_hash, 
    verify_password, 
    create_access_token, 
    create_refresh_token
)
from config.database import engine, SessionLocal
from sqlalchemy.orm import Session
from pydantic import BaseModel
from .services.auth import get_current_user


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

class User(BaseModel):
    firstname: str
    lastname: str
    username: str
    email: str
    password: str

router = APIRouter(
    prefix="/api",
    tags=["Authentication"],
    responses={404: {"description": "Resource not found"}}
)

def user_exception():
    response = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Incorrect email or password"
    )

    return response

def authenticate_user(username: str, password: str, db):
    user = db.query(Users).filter(Users.username == username).first()

    if user is None:
        raise user_exception()

    if not verify_password(password, user.password):
        raise user_exception()

    return user


@router.post('/login', summary="Verify user and create new tokens")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session=Depends(get_db)):
    user = authenticate_user(form_data.username, form_data.password, db)
    return {
        "token_type": "bearer",
        "access_token": create_access_token(user.username),
        "refresh_token": create_refresh_token(user.username),
    }
