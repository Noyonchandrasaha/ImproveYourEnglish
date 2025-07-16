from fastapi import FastAPI
import asyncio
from app.api.routes import router as api_router
from bot.telegram_bot import run_bot_async

app = FastAPI()
app.include_router(api_router)

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(run_bot_async())
    print("Starting Telegram bot...")