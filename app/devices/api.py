import sys
sys.path.append("..")

from fastapi import Depends, HTTPException, APIRouter
from .models import Devices, Commands
from config.database import engine, SessionLocal
from sqlalchemy.orm import Session
from pydantic import BaseModel

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

class Device(BaseModel):
    name: str
    unit: int
    address: int

class Command(BaseModel):
    device_id: int
    address: str
    value: str

router = APIRouter(
    prefix="/api",
    tags=["Devices"],
    responses={404: {"description": "Not found"}}
)

@router.get('/devices')
async def list_devices(db: Session=Depends(get_db)):
    devices = db.query(Devices).all()
    return {
        'data': devices,
        'status': 200
    }

@router.get('/devices/{id}')
async def show_device(id: int, db: Session=Depends(get_db)):
    device = db.query(Devices)\
                    .filter(Devices.id == id)\
                    .first()

    if device is not None:
        return {
            'data': device,
            'status': 200
        }
    else:
        raise HTTPException(status_code=404, detail="Device not found")

@router.post('/devices')
async def store_device(device: Device, db: Session=Depends(get_db)):
    data = Devices()
    data.name = device.name
    data.unit = device.unit
    data.address = device.address

    db.add(data)
    db.commit()

    return {
        'data': device,
        'status': 200
    }

@router.put('/devices/{id}')
async def update_device(id: int, device: Device, db: Session=Depends(get_db)):
    data = db.query(Devices)\
                    .filter(Devices.id == id)\
                    .first()

    if device is None:
        raise HTTPException(status_code=404, detail="Device not found")

    data.name = device.name
    data.unit = device.unit
    data.address = device.address

    db.add(data)
    db.commit()

    return {
        'data': device,
        'status': 200
    }

@router.delete('/devices/{id}')
async def delete_device(id: int, db: Session=Depends(get_db)):
    device = db.query(Devices)\
                    .filter(Devices.id == id)\
                    .first()

    if device is None:
        raise HTTPException(status_code=404, detail="Device not found")

    db.query(Devices)\
        .filter(Devices.id == id)\
        .delete()

    db.commit()

    return {
        'status': 200
    }

# ===================== Commands Endpoint ==============================

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