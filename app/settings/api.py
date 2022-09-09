import sys
sys.path.append("..")

from fastapi import Depends, HTTPException, APIRouter
from .models import Settings
from config.database import engine, SessionLocal
from sqlalchemy.orm import Session
from pydantic import BaseModel

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


class ProfileSetting(BaseModel):
    firstname: str
    lastname: str

class NetworkSetting(BaseModel):
    ip_address: str
    subnet_mask: str
    gateway: str
    dns: str

class LocationSetting(BaseModel):
    longitude: str
    latitude: str


router = APIRouter(
    prefix="/api",
    tags=["Settings"],
    responses={404: {"description": "Resource not found"}}
)


@router.get('/settings/profile')
async def show_profile_settings(db: Session=Depends(get_db)):
    setting = db.query(Settings).first()
    return {
        'data': setting,
        'status': 200
    }

@router.put('/settings/profile')
async def update_profile_settings(setting: ProfileSetting, db: Session=Depends(get_db)):
    data = db.query(Settings).first()

    if data is None:
        raise HTTPException(status_code=404, detail="Settings not found")

    data.name = setting.firstname
    data.unit = setting.lastname

    db.add(data)
    db.commit()

    return {
        'data': setting,
        'status': 200
    }


@router.get('/settings/network')
async def show_network_settings(db: Session=Depends(get_db)):
    setting = db.query(Settings).first()
    return {
        'data': setting,
        'status': 200
    }

@router.put('/settings/network')
async def update_network_settings(setting: NetworkSetting, db: Session=Depends(get_db)):
    data = db.query(Settings).first()

    if data is None:
        raise HTTPException(status_code=404, detail="Settings not found")

    data.ip_address = setting.ip_address
    data.subnet_mask = setting.subnet_mask
    data.gateway = setting.gateway
    data.dns = setting.dns

    db.add(data)
    db.commit()

    return {
        'data': setting,
        'status': 200
    }


@router.get('/settings/location')
async def show_location_settings(db: Session=Depends(get_db)):
    setting = db.query(Settings).first()
    return {
        'data': setting,
        'status': 200
    }

@router.put('/settings/location')
async def update_location_settings(setting: LocationSetting, db: Session=Depends(get_db)):
    data = db.query(Settings).first()

    if data is None:
        raise HTTPException(status_code=404, detail="Settings not found")

    data.longitude = setting.longitude
    data.latitude = setting.latitude

    db.add(data)
    db.commit()

    return {
        'data': setting,
        'status': 200
    }
