from fastapi import APIRouter
from redis_om.model.model import NotFoundError
from starlette.status import HTTP_200_OK

from entities.company import Company, CompanyMember
from entities.user import User
from resources.add_member_to_company_resource import AddMemberToCompanyResource
from resources.company_resource import CompanyResource
from resources.create_company_resource import CreateCompanyResource

router = APIRouter(prefix="/companies", tags=["auth"])


@router.post("/")
async def create_company(resource: CreateCompanyResource):
    dump = resource.model_dump()
    dump["admin_id"] = resource.user_id

    try:
        exists_user = User.get(dump["admin_id"])
    except NotFoundError:
        return {"error": "User not found"}

    # Create a new company instance
    company = Company(**dump)

    # Save the company to the database
    saved_company = company.save()
    if not saved_company:
        return {"error": "Failed to create company"}

    # Return the saved company as a dictionary
    return CompanyResource.model_dump(saved_company)


@router.post("/{company_id}/members")
async def add_member(resource: AddMemberToCompanyResource, company_id: str):
    try:
        company = Company.get(company_id)
    except NotFoundError:
        return {"error": "Company not found"}

    try:
        user = User.get(resource.user_id)
    except NotFoundError:
        return {"error": "User not found"}

    try:
        user_exists_in_company = CompanyMember.find(
            CompanyMember.company_id == company_id and
            CompanyMember.user_id == resource.user_id
        ).first()
    except NotFoundError:
        user_exists_in_company = None

    if user_exists_in_company:
        return {"error": "User is already a member of this company"}

    # Create a new company member instance
    company_member = {
        "company_id": company_id,
        "user_id": resource.user_id,
        "role": resource.role
    }

    # Save the company member to the database
    company_member_entity = CompanyMember(**company_member)

    company_member_entity.save()

    return HTTP_200_OK


@router.get("/{company_id}/members")
async def get_members(company_id: str):
    try:
        company = Company.get(company_id)
    except NotFoundError:
        return {"error": "Company not found"}

    members = CompanyMember.find(CompanyMember.company_id == company_id).all()

    if not members:
        return {"message": "No members found for this company"}

    return [member.model_dump() for member in members]
"""
jonatan : 01JZXEV0FVH8QA456XBRZMHZQ5
mateo: 01JZXEVQN8BTY6WN48T16GXPA3

Registra y no admite duplicados de correo
Valida la contraseña

empresa : 01JZXEW1SB1V9B7801NZ1B4GTW

"""