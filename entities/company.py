from redis_om import Field
from enum import Enum
from entities.shared.audit_and_redis_metadata_schema import AuditableAndRedisMetadataSchema


class CompanyMemberRoles(str, Enum):
    ADMIN = "admin"
    MEMBER = "member"

class Company(AuditableAndRedisMetadataSchema):
    name: str = Field(default="", description="Name of the company")
    description: str = Field(default="", description="Description of the company")
    admin_id: str = Field(default="", description="ID of the user who is the admin of the company")

class CompanyMember(AuditableAndRedisMetadataSchema):
    company_id: str = Field(default="", description="ID of the company")
    user_id: str = Field(default="", description="ID of the user who is a member of the company")
    role: CompanyMemberRoles = Field(default=CompanyMemberRoles.MEMBER, description="Role of the user in the company (e.g., member, admin)")

