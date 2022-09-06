from datetime import datetime, timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext


JWT_SECRET_KEY = "fkw2hhTPuNAcKXLKxPJ2TgroiUbnbm4p"
JWT_REFRESH_SECRET_KEY = "SflKxwRJSMeKKF2QT4fwpMeJf36PO"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15  # 15 minutes
REFRESH_TOKEN_EXPIRE_MINUTES = 60 # 60 minutes

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password):
    return password_context.hash(password)

def verify_password(plain_password, hashed_password):
    return password_context.verify(plain_password, hashed_password)

def create_access_token(username: str, expires_delta: int = None):

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode = {"sub": username, "exp": expire}
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

def create_refresh_token(username: str, expires_delta: int = None):
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    
    to_encode = {"sub": username, "exp": expire}
    encoded_jwt = jwt.encode(to_encode, JWT_REFRESH_SECRET_KEY, ALGORITHM)
    return encoded_jwt
