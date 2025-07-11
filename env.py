import dotenv
ENV_PATH = ".env"

REDIS_URL = dotenv.get_key(dotenv_path=ENV_PATH, key_to_get="REDIS_URL")
REDIS_BASE_URL = dotenv.get_key(dotenv_path=ENV_PATH, key_to_get="REDIS_BASE_URL")
REDIS_PORT = int(dotenv.get_key(dotenv_path=ENV_PATH, key_to_get="REDIS_PORT"))