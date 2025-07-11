from datetime import datetime
from uuid import uuid4

from redis_om import Field, JsonModel, get_redis_connection
from enum import Enum

from env import REDIS_URL


class CompanyMemberRoles(str, Enum):
    ADMIN = "admin"
    MEMBER = "member"

class Company(JsonModel, index=True):
    id: str = Field(default_factory=lambda: str(uuid4()))
    created_at: str = Field(default_factory=lambda: datetime.now().isoformat())

    name: str = Field(default="", description="Name of the company")
    description: str = Field(default="", description="Description of the company")
    admin_id: str = Field(default="", description="ID of the user who is the admin of the company")

    class Meta:
        database = get_redis_connection(url=REDIS_URL)

class CompanyMember(JsonModel, index=True):
    id: str = Field(default_factory=lambda: str(uuid4()))
    created_at: str = Field(default_factory=lambda: datetime.now().isoformat())

    company_id: str = Field(default="", description="ID of the company")
    user_id: str = Field(default="", description="ID of the user who is a member of the company")
    role: CompanyMemberRoles = Field(default=CompanyMemberRoles.MEMBER, description="Role of the user in the company (e.g., member, admin)")

    class Meta:
        database = get_redis_connection(url=REDIS_URL)

