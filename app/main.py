from .api.api_v1.api import router as api_router
from mangum import Mangum
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hola Mundo de los Heroes"}


app.include_router(api_router, prefix="/first")
handler = Mangum(app)