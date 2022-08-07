from pydantic import BaseModel
from uuid import UUID
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import Optional
import fastapi

api = FastAPI()
api.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

class Drawer(BaseModel):
    id: UUID
    size: str
    icon: str
    price: int


drawers = [
    {
        'id': 'c69460ea-3505-468b-98fc-15e27d6aa31d',
        'size': 'small',
        'icon': 'select_small',
        'price': 20
    },
    {
        'id': '8c0014c5-1bcd-4455-b4cf-9d00df7014bb',
        'size': 'medium',
        'icon': 'select_medium',
        'price': 20
    },
    {
        'id': '344edf36-c35c-4a11-b412-151e58a65415',
        'size': 'large',
        'icon': 'select_large',
        'price': 30
    },
    {
        'id': '9adbe85c-c879-4a51-8b18-be6901a181e7',
        'size': 'extra-large',
        'icon': 'select_extra_large',
        'price': 40
    }
]

responseData = {
    'data': drawers,
    'status': 200
}

@api.get('/')
async def index():
    return responseData

@api.get('/drawers/all/metrics')
async def metrics(size: str = 'all', bucket: Optional[int] = None):
    if bucket is None:
        res = '{"message": "Bucket is required", "status": 422}'
        return fastapi.Response(content=res,
                                    media_type="application/json",
                                    status_code=422
                                )
    all = {
        'small': {
            'icon': 'small_icon',
            'price': 20,
            'available': 2,
            'occupied': 1,
        },
         'medium': {
            'icon': 'medium_icon',
            'price': 30,
            'available': 3,
            'occupied': 1,
        },
           'large': {
            'icon': 'large_icon',
            'price': 40,
            'available': 3,
            'occupied': 1,
        },
            'extra_large': {
            'icon': 'extra_large_icon',
            'price': 50,
            'available': 3,
            'occupied': 1,
        },
    }

    result = all

    return {
        'data': result,
        'status': 200
    }

@api.get('/drawers/{id}')
async def show(id: int):
    drawer = drawers[id - 1]

    return {
        'data': drawer,
        'status': 200
    }

@api.post('/drawers')
async def store(drawer: Drawer):
    drawers.append(drawer)

    return {
        'data': drawers,
        'status': 200
    }

@api.get("/overview", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@api.get("/devices", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("devices.html", {"request": request})

@api.get("/records", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("records.html", {"request": request})

@api.get("/settings", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("settings.html", {"request": request})
