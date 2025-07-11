from contextlib import asynccontextmanager

import httpx
from fastapi import FastAPI
from redis import Redis
from redis_om import Migrator

from controllers import auth
from env import REDIS_URL, REDIS_PORT

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.redis = Redis(host=REDIS_URL, port=REDIS_PORT)
    app.state.http_client = httpx.AsyncClient()
    try:
        Migrator().run()
        yield
    finally:
        app.state.redis.close()
        await app.state.http_client.aclose()

app = FastAPI(lifespan=lifespan)

app.include_router(auth.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/health")
async def health_check():
    """
    Health check endpoint to verify the service is running.
    """
    import redis
    r = redis.Redis.from_url("redis://localhost:6379")
    print(r.ping())  # → Debería dar True
    print(r.execute_command("command", "info", "json.set"))

    return {"status": "ok", "message": "Service is running"}