from fastapi import APIRouter

from .endpoints import heroes

router = APIRouter()
router.include_router(heroes.router, prefix="/heroes", tags=["Heroes"])

@router.get("/")
async def root():
    return {"message": "Esta es la versión 1.0\nEstá apenas en construcción"}