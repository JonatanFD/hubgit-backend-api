from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI
from redis_om import Migrator, get_redis_connection

from controllers import auth, companies, posts, users
from env import REDIS_URL

load_dotenv(verbose=True)


REDIS_CONN = get_redis_connection(url=REDIS_URL, decode_responses=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    Migrator().run()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(auth.router)
app.include_router(companies.router)
app.include_router(posts.router)

app.include_router(users.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/health")
async def health_check():
    """
    Health check endpoint to verify the service is running.
    """
    print("Redis url", REDIS_URL)
    print(REDIS_CONN.ping())  # → Debería dar True
    print(REDIS_CONN.execute_command("command", "info", "json.set"))

    return {"status": "ok", "message": "Service is running"}

