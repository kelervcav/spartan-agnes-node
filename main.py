from fastapi import FastAPI, Depends, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import Optional
from devices.database import engine, SessionLocal
from routers import devices

description = """
Spartan is a sensor node for Agnes, which serve as a swiss army knife for data acquisition and a controller in smart agriculture. 🚀

## Devices

You will be able to:

* **Create device**
* **Read specific device**
* **Edit specific device**
* **Remove specific device**
* **Read all the devices**
* **Retrieve specific sensor value** (_not implemented_).
* **Switch on/off specific device** (_not implemented_).

## Settings

You will be able to:

* **Update account settings** (_not implemented_).
* **Set gateway details** (_not implemented_).

## Authentication

You will be able to:

* **Login and get the token** (_not implemented_).

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
        title="Spartan - Agnes Node",
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

api.include_router(devices.router)

api.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

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
