import dotenv
ENV_PATH = ".env"

REDIS_URL = dotenv.get_key(dotenv_path=ENV_PATH, key_to_get="REDIS_URL")
print("REDIS_URL:", REDIS_URL)