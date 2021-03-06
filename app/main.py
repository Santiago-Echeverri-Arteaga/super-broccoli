from .api.api_v1.api import router as api_router
from mangum import Mangum
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}


app.include_router(api_router, prefix="/v1")
handler = Mangum(app)