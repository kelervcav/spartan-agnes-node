import sys
sys.path.append("..")

from fastapi import Depends, HTTPException, status, APIRouter
from pydantic import BaseModel
from typing import Optional
import devices.models as models
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from devices.database import SessionLocal, engine
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from datetime import datetime, timedelta
from jose import jwt, JWTError

SECRET_KEY = "fkw2hhTPuNAcKXLKxPJ2TgroiUbnbm4p"
ALGORITHM = "HS256"


class Register(BaseModel):
    firstname: str
    lastname: str
    username: str
    email: str
    password: str


bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

models.Base.metadata.create_all(bind=engine)

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="token")


router = APIRouter(
    prefix="/api/auth",
    tags=["Authentication"],
    responses={401: {"message": "You are not authorized"}}
)


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

def get_password_hash(password):
    return bcrypt_context.hash(password)

def verify_password(plain_password, hashed_password):
    return bcrypt_context.verify(plain_password, hashed_password)

def authenticate_user(username: str, password: str, db):
    user = db.query(models.Users)\
        .filter(models.Users.username == username)\
        .first()

    if not user:
        return False

    if not verify_password(password, user.password):
        return False

    return user

def create_access_token(username: str, user_id: int,
                        expires_delta: Optional[timedelta] = None):

    encode = {"sub": username, "id": user_id}
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    encode.update({"exp": expire})

    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(token: str = Depends(oauth2_bearer)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("id")

        if username is None or user_id is None:
            raise user_exception()

        return {"username": username, "id": user_id}

    except JWTError:
        raise user_exception()


@router.post("/register")
async def create_new_user(user: Register, db: Session = Depends(get_db)):
    data = models.Users()
    data.email = user.email
    data.username = user.username
    data.firstname = user.firstname
    data.lastname = user.lastname

    hashed_password = get_password_hash(user.password)

    data.password = hashed_password
    data.is_active = True

    db.add(data)
    db.commit()


@router.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(),
                                 db: Session = Depends(get_db)):

    user = authenticate_user(form_data.username, form_data.password, db)

    if not user:
        raise token_exception()

    token_expires = timedelta(minutes=20)
    token = create_access_token(user.username,
                                user.id,
                                expires_delta=token_expires)

    return {"token": token}


def user_exception():
    response = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    return response


def token_exception():
    response = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"},
    )

    return response
