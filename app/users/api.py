from fastapi import FastAPI, status, HTTPException, APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import RedirectResponse
from .models import Users
from .utils import get_password_hash, verify_password, create_access_token, create_refresh_token
from config.database import engine, SessionLocal
from sqlalchemy.orm import Session
from pydantic import BaseModel
from .auth import get_current_user


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
    tags=["Users"],
    responses={404: {"description": "Not found"}}
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

@router.post('/signup', summary="Create new user")
async def create_user(user: User, db: Session=Depends(get_db)):
    data = Users()
    data.email = user.email
    data.username = user.username
    data.firstname = user.firstname
    data.lastname = user.lastname
    data.password = get_password_hash(user.password)
    db.add(data)
    db.commit()
    return {
        'data': user,
        'status': 200
    }


@router.post('/login', summary="Create access and refresh tokens for user")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session=Depends(get_db)):
    user = authenticate_user(form_data.username, form_data.password, db)
    return {
        "token_type": "bearer",
        "access_token": create_access_token(user.username),
        "refresh_token": create_refresh_token(user.username),
    }

@router.get('/users', dependencies=[Depends(get_current_user)])
async def list_users(db: Session=Depends(get_db)):  
    users = db.query(Users).all()
    return {
        'data': users,
        'status': 200
    }