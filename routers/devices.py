import sys
sys.path.append("..")

from fastapi import Depends, HTTPException, APIRouter
import devices.models as models
from sqlalchemy.orm import Session
from pydantic import BaseModel
from devices.database import engine, SessionLocal

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

router = APIRouter(
    prefix="/api",
    tags=["Devices"],
    responses={404: {"description": "Not found"}}
)

@router.get('/devices')
async def list_devices(db: Session=Depends(get_db)):
    devices = db.query(models.Devices).all()
    return {
        'data': devices,
        'status': 200
    }

@router.get('/devices/{id}')
async def show_device(id: int, db: Session=Depends(get_db)):
    device = db.query(models.Devices)\
                    .filter(models.Devices.id == id)\
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
    data = models.Devices()
    data.nam = device.name
    data.unit = device.unit
    data.address = device.address

    db.add(data)
    db.commit()

    return {
        'data': device,
        'status': 201
    }

@router.put('/devices/{id}')
async def update_device(id: int, device: Device, db: Session=Depends(get_db)):
    data = db.query(models.Devices)\
                    .filter(models.Devices.id == id)\
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
    device = db.query(models.Devices)\
                    .filter(models.Devices.id == id)\
                    .first()

    if device is None:
        raise HTTPException(status_code=404, detail="Device not found")

    db.query(models.Devices)\
        .filter(models.Devices.id == id)\
        .delete()

    db.commit()

    return {
        'status': 200
    }
