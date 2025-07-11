import os
import dotenv
from redis_om import get_redis_connection

ENV_PATH = ".env"
dotenv.load_dotenv(ENV_PATH)

# Usar la URL completa de REDIS_URL del .env
REDIS_URL = os.getenv("REDIS_URL")
REDIS_CONN = get_redis_connection(url=REDIS_URL, decode_responses=True)
