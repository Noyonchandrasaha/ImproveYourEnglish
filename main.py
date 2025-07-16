import multiprocessing
from app.api.routes import router as api_router
from fastapi import FastAPI
import uvicorn

from bot.telegram_bot import run_bot  # You must define run_bot() in your telegram_bot.py

app = FastAPI()
app.include_router(api_router)


def start_uvicorn():
    uvicorn.run(app, host="0.0.0.0", port=10000)


if __name__ == "__main__":
    # Run FastAPI and Telegram bot together
    p1 = multiprocessing.Process(target=start_uvicorn)
    p2 = multiprocessing.Process(target=run_bot)

    p1.start()
    p2.start()

    p1.join()
    p2.join()
