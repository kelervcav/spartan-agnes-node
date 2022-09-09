from fastapi import APIRouter
from .devices import api as devices_api
from .commands import api as commands_api
from .users import api as users_api

router = APIRouter()
router.include_router(devices_api.router)
router.include_router(commands_api.router)
router.include_router(users_api.router)
