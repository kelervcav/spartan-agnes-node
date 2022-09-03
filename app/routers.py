from fastapi import APIRouter
from .devices import api as devices_api

router = APIRouter()
router.include_router(devices_api.router)