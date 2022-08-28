from pydantic import BaseModel
from uuid import UUID
from fastapi import FastAPI, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import Optional
import devices.models as models
from sqlalchemy.orm import Session
from devices.database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)

description = """
Spartan is a sensor node for Agnes, which serve as a swiss army knife for data acquisition and a controller in smart agriculture. 🚀

## Devices

You will be able to:

* **Create device** (_not implemented_).
* **Read specific device** (_not implemented_).
* **Edit specific device** (_not implemented_).
* **Remove specific device** (_not implemented_).
* **Read all the devices** (_not implemented_).
* **Read all the devices by type** (_not implemented_).
* **Retrieve specific sensor value** (_not implemented_).
* **Switch on/off specific device** (_not implemented_).

## Settings

You will be able to:

* **Update account settings** (_not implemented_).
* **Set gateway details** (_not implemented_).

"""

tags_metadata = [
     {
        "name": "Overview",
        "description": "Statistics and Analytics."
    },
    {
        "name": "Devices",
        "description": "Operations with devices."
    },
    {
        "name": "Settings",
        "description": "Manage settings."
    },
]

api = FastAPI(
        title="Spartan - Agnes Sensor Node",
        description=description,
        version="0.3.0",
        terms_of_service="https://www.linkedin.com/in/sydel-palinlin/",
        contact={
            "name": "Sydel Palinlin",
            "url": "https://www.linkedin.com/in/sydel-palinlin/",
            "email": "sydel.palinlin@gmail.com",
        },
        openapi_tags=tags_metadata
    )

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


api.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@api.get('/api/devices', tags=["Devices"])
async def list_devices(db: Session=Depends(get_db)):
    devices = db.query(models.Devices).all()
    return {
        'data': devices,
        'status': 200
    }

@api.get('/api/devices/{id}', tags=["Devices"])
async def show_device(id: int, db: Session=Depends(get_db)):
    device = db.query(models.Devices)\
                    .filter(models.Devices.id == id)\
                    .first()
    return {
        'data': device,
        'status': 200
    }

@api.get("/", response_class=HTMLResponse, include_in_schema=False)
async def home(request: Request):
    return templates.TemplateResponse("welcome.html", {"request": request})

@api.get("/overview", response_class=HTMLResponse, include_in_schema=False)
async def overview(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@api.get("/devices", response_class=HTMLResponse, include_in_schema=False)
async def devices(request: Request):
    return templates.TemplateResponse("devices.html", {"request": request})

@api.get("/settings", response_class=HTMLResponse, include_in_schema=False)
async def settings(request: Request):
    return templates.TemplateResponse("settings.html", {"request": request})
