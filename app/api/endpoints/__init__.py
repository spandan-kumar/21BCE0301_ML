from fastapi import APIRouter
from .health import router as health_router
from .search import router as search_router
from .documents import router as documents_router

api_router = APIRouter()

api_router.include_router(health_router, prefix="/health", tags=["health"])
api_router.include_router(search_router, prefix="/search", tags=["search"])
api_router.include_router(documents_router, prefix="/documents", tags=["documents"])
