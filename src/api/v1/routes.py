from fastapi import APIRouter

from src.api.v1.endpoints.rag import router as rag_router

routers = APIRouter()
router_list = [rag_router]

for router in router_list:
    router.tags = routers.tags.append("v1")
    routers.include_router(router)
