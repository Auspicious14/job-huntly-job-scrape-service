from fastapi import FastAPI
from .routes.job_routes import router

app = FastAPI()
app.include_router(router)