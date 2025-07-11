import dotenv
from redis_om import get_redis_connection

ENV_PATH = ".env"

REDIS_URL = dotenv.get_key(dotenv_path=ENV_PATH, key_to_get="REDIS_URL")
print("REDIS_URL:", REDIS_URL)


REDIS_CONN = get_redis_connection(url=REDIS_URL, decode_responses=True, )