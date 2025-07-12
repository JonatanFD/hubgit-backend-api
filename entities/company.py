from datetime import datetime

from redis_om import Field, JsonModel
from enum import Enum

from env import REDIS_CONN


class CompanyMemberRoles(str, Enum):
    ADMIN = "admin"
    MEMBER = "member"

class Company(JsonModel, index=True):
    name: str = Field(default="", description="Name of the company")
    description: str = Field(default="", description="Description of the company")
    admin_id: str = Field(default="", description="ID of the user who is the admin of the company")

    created_at: str = Field(default_factory=lambda: datetime.now().isoformat())
    class Meta:
        database = REDIS_CONN

class CompanyMember(JsonModel, index=True):
    created_at: str = Field(default_factory=lambda: datetime.now().isoformat())

    company_id: str = Field(default="", description="ID of the company", index=True)
    user_id: str = Field(default="", description="ID of the user who is a member of the company", index=True)
    role: CompanyMemberRoles = Field(default=CompanyMemberRoles.MEMBER, description="Role of the user in the company (e.g., member, admin)")

    class Meta:
        database = REDIS_CONN

