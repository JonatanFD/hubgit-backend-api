from fastapi import APIRouter
from redis_om.model.model import NotFoundError
from resources.create_user_resource import CreateUserResource
from resources.user_resource import UserResource
from entities.user import User

router = APIRouter(prefix="/auth", tags=["auth"])


"""
Endpoint for user sign-in.
"""
@router.post("/sign-up")
async def sign_up(req: CreateUserResource):
    dump = req.model_dump()

    try:
        found_user = User.find(User.email == dump.get("email")).first()
    except NotFoundError:
        found_user = None

    if found_user:
        return UserResource.build_error("User already exists with this email.")

    '''
    Here should the some contrains to check if the user information is valid.
    '''

    user = User(**dump)
    saved_user = user.save()

    return UserResource.build_from_entity(saved_user)

@router.post("/sign-in")
async def sign_in():
    """
    Endpoint for user sign-up.
    This is a placeholder function that should be implemented with actual registration logic.
    """
    return {"message": "Sign-up endpoint not implemented yet."}
