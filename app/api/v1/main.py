from fastapi import APIRouter

from . import routes

api_router_v1 = APIRouter()
# Include the AuthAPI router
api_router_v1.include_router(routes.WeatherEndpointsAPI.collect_router())
