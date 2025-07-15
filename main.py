from fastapi import FastAPI
from app.api.routes import router as api_router

app = FastAPI(title="IELTS Grammar Correction API")

app.include_router(api_router)
