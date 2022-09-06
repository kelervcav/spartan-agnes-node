from typing import Union, Any
from datetime import datetime
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from config.database import engine, SessionLocal
from .utils import ALGORITHM, JWT_SECRET_KEY
from .models import Users
from jose import jwt
from pydantic import ValidationError, BaseModel


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/login",
    scheme_name="JWT"
)

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

class TokenPayload(BaseModel):
    sub: str = None
    exp: int = None

def token_exception():
    response = HTTPException(
        status_code = status.HTTP_401_UNAUTHORIZED,
        detail="Token expired",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return response

def credentials_exception():
    response = HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return response

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session=Depends(get_db)):
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        token_data = TokenPayload(**payload)
        
        if datetime.fromtimestamp(token_data.exp) < datetime.now():
            raise token_exception()

    except(jwt.JWTError, ValidationError):
        raise credentials_exception()
        
    user = db.query(Users).filter(Users.username == token_data.sub).first()
    
    if user is None:
        raise credentials_exception()
    
    return user