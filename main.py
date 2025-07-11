from contextlib import asynccontextmanager
from http.client import HTTPException

from fastapi import FastAPI, Request
from fastapi.routing import APIRoute
from redis_om import Migrator

from controllers import auth, companies
from services.jwt import verify_access_token


@asynccontextmanager
async def lifespan(app: FastAPI):
    Migrator().run()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(auth.router)
app.include_router(companies.router)

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    bearer_token = request.headers.get("Authorization")
    # path
    print(request.base_url)

    if bearer_token and bearer_token.startswith("Bearer "):
        token = bearer_token.split("Bearer ")[1]
        try:
            verify_access_token(token)
        except HTTPException:
            return HTTPException(status_code=401, detail="Unauthorized")

    response = await call_next(request)
    return response

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

def jwt_protected_routes(app: FastAPI):
    for route in app.routes:
        if isinstance(route, APIRoute):
            if route.path not in ["/auth/sign-in", "/auth/sign-up"]:
                original_endpoint = route.endpoint

                async def protected_endpoint(request: Request, *args, **kwargs):
                    bearer_token = request.headers.get("Authorization")
                    if not bearer_token or not bearer_token.startswith("Bearer "):
                        raise HTTPException(status_code=401, detail="Unauthorized")
                    token = bearer_token.split("Bearer ")[1]
                    try:
                        verify_access_token(token)
                    except Exception:
                        raise HTTPException(status_code=401, detail="Invalid or expired token")
                    return await original_endpoint(*args, **kwargs)

                route.endpoint = protected_endpoint

jwt_protected_routes(app)
