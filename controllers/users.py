from fastapi import APIRouter
from redis_om import NotFoundError

from entities.company import Company, CompanyMember
from entities.user import User

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/{user_id}")
async def get_user(user_id: str):
    """
    Endpoint to retrieve user information by user ID.
    """
    # check if user exists in the database
    print("Fetching user with ID:", user_id)
    try:
        user = User.get(user_id)
    except NotFoundError:
        return {"error": "User not found"}


    return user.model_dump(exclude={"password": True})



@router.get("/{user_id}/companies")
async def get_user_companies(user_id: str):
    """
    Endpoint to retrieve companies associated with a user.
    """
    print("Fetching user with ID:", user_id)
    try:
        user = User.get(user_id)
    except NotFoundError:
        return {"error": "User not found"}

    companies = CompanyMember.find(CompanyMember.user_id == user.pk).all()

    if not companies:
        return {"message": "No companies found for this user"}

    company_ids = [company.company_id for company in companies]
    company_details = [Company.get(company_id).model_dump() for company_id in company_ids if Company.get(company_id)]

    return {"user_id": user.pk, "companies": company_details}

