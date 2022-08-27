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

api = FastAPI()
api.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@api.get('/api/devices')
async def create_database():
    return {'message': 'Created'}

@api.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("welcome.html", {"request": request})

@api.get("/overview", response_class=HTMLResponse)
async def overview(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@api.get("/devices", response_class=HTMLResponse)
async def devices(request: Request):
    return templates.TemplateResponse("devices.html", {"request": request})

@api.get("/records", response_class=HTMLResponse)
async def records(request: Request):
    return templates.TemplateResponse("records.html", {"request": request})

@api.get("/settings", response_class=HTMLResponse)
async def settings(request: Request):
    return templates.TemplateResponse("settings.html", {"request": request})
