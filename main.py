from fastapi import FastAPI
from contextlib import asynccontextmanager
import asyncio
from app.api.routes import router as api_router
from bot.telegram_bot import run_bot_async

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("✅ Starting Telegram bot...")
    asyncio.create_task(run_bot_async())
    yield
    print("🛑 Shutting down app...")

app = FastAPI(lifespan=lifespan)
app.include_router(api_router)
