from redis_om import Field
from enum import Enum

from entities.shared.audit_and_redis_metadata_schema import AuditableAndRedisMetadataSchema


class PlatformUserRoles(str, Enum):
    ADMIN = "admin"
    USER = "user"

class User(AuditableAndRedisMetadataSchema):
    username: str = Field(default="", description="Username of the user")
    email: str = Field(default="", description="User email address")
    password: str = Field(default="", description="Password of the user", exclude=True)
    platform_role: PlatformUserRoles = Field(default=PlatformUserRoles.USER, description="User roles in the platform")

