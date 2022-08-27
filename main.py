from pydantic import BaseModel
from uuid import UUID
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import Optional
import devices.models as models
from devices.database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)

description = """
Agnes Node helps you do awesome stuff. 🚀

## Devices

You will be able to:

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
        "name": "Devices",
        "description": "Operations with devices."
    },
    {
        "name": "Settings",
        "description": "Manage settings."
    },
]


api = FastAPI(
        title="Agnes Node",
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

api.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@api.get('/api/devices', tags=["Devices"])
async def create_database():
    return {'message': 'Created'}

@api.get("/", response_class=HTMLResponse, include_in_schema=False)
async def home(request: Request):
    return templates.TemplateResponse("welcome.html", {"request": request})

@api.get("/overview", response_class=HTMLResponse, include_in_schema=False)
async def overview(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@api.get("/devices", response_class=HTMLResponse, include_in_schema=False)
async def devices(request: Request):
    return templates.TemplateResponse("devices.html", {"request": request})

@api.get("/records", response_class=HTMLResponse, include_in_schema=False)
async def records(request: Request):
    return templates.TemplateResponse("records.html", {"request": request})

@api.get("/settings", response_class=HTMLResponse, include_in_schema=False)
async def settings(request: Request):
    return templates.TemplateResponse("settings.html", {"request": request})
