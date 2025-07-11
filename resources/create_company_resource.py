from pydantic import BaseModel


class CreateCompanyResource(BaseModel):
    user_id: str
    name: str
    description: str
