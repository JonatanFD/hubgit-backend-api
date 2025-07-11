from datetime import datetime
from uuid import uuid4

from redis_om import Field, get_redis_connection, JsonModel
from enum import Enum

from env import REDIS_URL


class PlatformUserRoles(str, Enum):
    ADMIN = "admin"
    USER = "user"


class User(JsonModel, index=True):
    id: str = Field(default_factory=lambda: str(uuid4()), index=True)
    created_at: str = Field(default_factory=lambda: datetime.now().isoformat(), index=True)

    username: str = Field(default="", description="Username of the user", index=True)
    email: str = Field(default="", description="User email address", index=True)
    password: str = Field(default="", description="Password of the user", exclude=True, index=True)
    platform_role: PlatformUserRoles = Field(default=PlatformUserRoles.USER, description="User roles in the platform",
                                             index=True)

    class Meta:
        database = get_redis_connection(url=REDIS_URL)
