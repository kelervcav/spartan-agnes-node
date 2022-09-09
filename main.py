from fastapi import FastAPI, Depends, Request, HTTPException
from functools import lru_cache
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import Optional
from config.database import engine, SessionLocal
from app.routers import router as api_router
from config.settings import Settings

@lru_cache()
def get_settings():
    return Settings()

description = f"""
{get_settings().APP_NAME} is a sensor node for Agnes, which serve as a swiss army knife for data acquisition and a controller in smart agriculture. 🚀

## Devices

You will be able to:

* **Create device**
* **Read specific device**
* **Edit specific device**
* **Remove specific device**
* **Read all the devices**


## Commands

You will be able to:

* **Retrieve specific sensor value** (_not implemented_).
* **Switch on/off specific device** (_not implemented_).


## Settings

You will be able to:

* **Update account settings** (_not implemented_).
* **Set gateway details**

## Authentication

You will be able to:

* **Login and get the token**

"""

tags_metadata = [
    {
        "name": "Devices",
        "description": "Operations with devices."
    },
    {
        "name": "Commands",
        "description": "Operations with commands."
    },
    {
        "name": "Authentication",
        "description": "User validation and verification."
    },
    {
        "name": "Settings",
        "description": "Manage settings."
    },
]

api = FastAPI(
        title="Spartan",
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

api.include_router(api_router)

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
