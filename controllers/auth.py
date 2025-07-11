from fastapi import APIRouter
from redis_om.model.model import NotFoundError
from datetime import datetime
from resources.create_user_resource import CreateUserResource
from entities.user import User, PlatformUserRoles

router = APIRouter(prefix="/auth", tags=["auth"])


"""
Endpoint for user sign-in.
"""
@router.post("/sign-up")
async def sign_up(req: CreateUserResource):
    dump = req.model_dump(exclude_unset=True)

    print(dump.get("email"))
    print(User.email)

    try:
        found_user = User.find(User.email == dump.get("email")).first()
    except NotFoundError:
        found_user = None

    if found_user:
        return {"message": "User already exists."}

    user = User(**dump)
    saved = user.save()

    return saved.dict()

@router.post("/sign-in")
async def sign_in():
    """
    Endpoint for user sign-up.
    This is a placeholder function that should be implemented with actual registration logic.
    """
    return {"message": "Sign-up endpoint not implemented yet."}
