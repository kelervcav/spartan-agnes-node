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
    name: str
    device_id: int
    address: str
    value: str

router = APIRouter(
    prefix="/api",
    tags=["Commands"],
    responses={404: {"description": "Resource not found"}}
)

@router.get('/commands/info')
async def fetch_info_command(command: Command, db: Session=Depends(get_db)):
    data = Commands()

    data.device_id = command.device_id
    data.unit = command.unit
    data.address = command.address
    data.value = command.value

    db.add(data)
    db.commit()

    # Hardware communication here

    return {
        'data': command,
        'status': 200
    }

@router.post('/commands/work')
async def do_work_command(command: Command, db: Session=Depends(get_db)):
    data = Commands()

    data.device_id = command.device_id
    data.unit = command.unit
    data.address = command.address
    data.value = command.value

    db.add(data)
    db.commit()

    # Hardware communication here

    return {
        'data': command,
        'status': 200
    }
