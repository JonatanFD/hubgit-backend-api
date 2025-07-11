from pydantic import BaseModel


class CompanyResource(BaseModel):
    pk: str
    name: str
    description: str
    admin_id: str


    @staticmethod
    def dump(company):
        return {
            "pk": company.pk,
            "name": company.name,
            "description": company.description,
            "admin_id": company.admin_id
        }