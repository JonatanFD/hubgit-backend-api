from pydantic import BaseModel

class AddMemberToCompanyResource(BaseModel):
    user_id: str
    role: str
