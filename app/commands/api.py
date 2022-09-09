import sys
sys.path.append("..")

from fastapi import Depends, HTTPException, APIRouter
from .models import Commands
from config.database import engine, SessionLocal
from sqlalchemy.orm import Session
from pydantic import BaseModel

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

class Command(BaseModel):
    device_id: int
    address: str
    value: str

router = APIRouter(
    prefix="/api",
    tags=["Commands"],
    responses={404: {"description": "Resource not found"}}
)

@router.get('/commands')
async def list_commands(db: Session=Depends(get_db)):
    commands = db.query(Commands).all()
    return {
        'data': commands,
        'status': 200
    }

@router.post('/commands')
async def store_command(command: Command, db: Session=Depends(get_db)):
    data = Commands()
    data.address = command.address
    data.value = command.value
    data.device_id = command.device_id

    db.add(data)
    db.commit()

    return {
        'data': command,
        'status': 200
    }

@router.get('/commands/{id}')
async def show_command(id: int, db: Session=Depends(get_db)):
    command = db.query(Commands)\
                    .filter(Commands.id == id)\
                    .first()

    if command is not None:
        return {
            'data': command,
            'status': 200
        }
    else:
        raise HTTPException(status_code=404, detail="Command not found")
