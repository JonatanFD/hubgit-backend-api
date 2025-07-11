from fastapi import APIRouter
from redis_om import NotFoundError

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

