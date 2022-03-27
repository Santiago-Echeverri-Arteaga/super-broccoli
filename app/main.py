from .api.api_v1.api import router as api_router
from mangum import Mangum
from fastapi import FastAPI
from .core import config
app = FastAPI()

@app.get("/")
async def root():
    return {"message": f"Hola Mundo de los SUPERHeroes: {config.settings.secret_key}"}


app.include_router(api_router, prefix=config.settings.prefix)
handler = Mangum(app)