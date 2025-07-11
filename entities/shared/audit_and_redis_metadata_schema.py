from datetime import datetime
from uuid import uuid4

from redis_om import Field
import dotenv
from redis_om import JsonModel, get_redis_connection

REDIS_CONNECTION = dotenv.get_key(".env", "REDIS_URL")
if not REDIS_CONNECTION:
    raise ValueError("REDIS_URL not found in .env file")

print(REDIS_CONNECTION)

class AuditableAndRedisMetadataSchema(JsonModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    created_at: str = Field(default_factory=lambda: datetime.now().isoformat(), description="Creation timestamp")

    class Meta:
        database = get_redis_connection(url=REDIS_CONNECTION)


