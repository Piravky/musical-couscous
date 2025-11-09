from fastapi import APIRouter

from .v1.books import router as books_router

api_router = APIRouter(prefix="/api")

api_router_v1 = APIRouter(prefix="/v1")
api_router_v1.include_router(books_router)

api_router.include_router(api_router_v1)
