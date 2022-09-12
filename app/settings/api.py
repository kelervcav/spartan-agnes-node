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


class Setting(BaseModel):
    firstname: str
    lastname: str
    ip_address: str
    subnet_mask: str
    gateway: str
    dns: str
    longitude: str
    latitude: str

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


@router.post('/settings')
async def store_setting(setting: Setting, db: Session=Depends(get_db)):
    data = Settings()
    data.firstname = setting.firstname
    data.lastname = setting.lastname
    data.ip_address = setting.ip_address
    data.subnet_mask = setting.subnet_mask
    data.gateway = setting.gateway
    data.dns = setting.dns
    data.longitude = setting.longitude
    data.latitude = setting.latitude

    db.add(data)
    db.commit()

    return {
        'data': setting,
        'status': 200
    }


@router.get('/settings/{id}/profile')
async def show_profile_settings(id: int, db: Session=Depends(get_db)):
    setting = db.query(Settings)\
                    .filter(Settings.id == id)\
                    .first()

    if setting is not None:
        return {
            'data': setting,
            'status': 200
        }
    else:
        raise HTTPException(status_code=404, detail="Profile not found")

@router.put('/settings/{id}/profile')
async def update_profile_settings(id: int, setting: ProfileSetting, db: Session=Depends(get_db)):
    data = db.query(Settings)\
                    .filter(Settings.id == id)\
                    .first()

    if data is None:
        raise HTTPException(status_code=404, detail="Profile not found")

    data.firstname = setting.firstname
    data.lastname = setting.lastname

    db.commit()

    return {
        'data': setting,
        'status': 200
    }


@router.get('/settings/{id}/network')
async def show_network_settings(id: int, db: Session=Depends(get_db)):
    setting = db.query(Settings)\
                    .filter(Settings.id == id)\
                    .first()

    if setting is not None:
        return {
            'data': setting,
            'status': 200
        }
    else:
        raise HTTPException(status_code=404, detail="Network not found")

@router.put('/settings/{id}/network')
async def update_network_settings(id: int, setting: NetworkSetting, db: Session=Depends(get_db)):
    data = db.query(Settings).first()

    if data is None:
        raise HTTPException(status_code=404, detail="Network not found")

    data.ip_address = setting.ip_address
    data.subnet_mask = setting.subnet_mask
    data.gateway = setting.gateway
    data.dns = setting.dns

    db.commit()

    return {
        'data': setting,
        'status': 200
    }


@router.get('/settings/{id}/location')
async def show_location_settings(id: int, db: Session=Depends(get_db)):
    setting = db.query(Settings)\
                    .filter(Settings.id == id)\
                    .first()

    if setting is not None:
        return {
            'data': setting,
            'status': 200
        }
    else:
        raise HTTPException(status_code=404, detail="Location not found")

@router.put('/settings/{id}/location')
async def update_location_settings(id: int, setting: LocationSetting, db: Session=Depends(get_db)):
    data = db.query(Settings).first()

    if data is None:
        raise HTTPException(status_code=404, detail="Location not found")

    data.longitude = setting.longitude
    data.latitude = setting.latitude

    db.commit()

    return {
        'data': setting,
        'status': 200
    }
