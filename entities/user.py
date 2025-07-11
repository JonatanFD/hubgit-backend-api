from datetime import datetime

from redis_om import Field, JsonModel
from enum import Enum

from env import REDIS_CONN


class PlatformUserRoles(str, Enum):
    ADMIN = "admin"
    USER = "user"


class User(JsonModel, index=True):
    username: str = Field(index=True)
    email: str = Field(index=True)
    password: str = Field(index=True)
    platform_role: PlatformUserRoles = Field(index=True, default=PlatformUserRoles.USER)

    created_at: str = Field(index=True, default_factory=lambda: datetime.now().isoformat())
    class Meta:
        database = REDIS_CONN
