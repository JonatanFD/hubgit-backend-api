from fastapi import APIRouter

from assemblers.user_assembler import UserAssembler
from entities.user import User as UserModel
from resources.create_user_resource import CreateUserResource

router = APIRouter(prefix="/auth", tags=["auth"])


"""
Endpoint for user sign-in.
"""
@router.post("/sign-up")
async def sign_in(req: CreateUserResource):
    dump = req.model_dump(exclude_unset=True)

    found_user = UserModel.find(UserModel.username == dump["email"]).all()

    print(found_user)
    if found_user:
        return {"message": "User already exists."}

    user = UserModel(**req.model_dump())
    saved = user.save()
    user_resource = UserAssembler.to_user_resource_from_entity(user=saved)
    return user_resource

@router.post("/sign-in")
async def sign_up():
    """
    Endpoint for user sign-up.
    This is a placeholder function that should be implemented with actual registration logic.
    """
    return {"message": "Sign-up endpoint not implemented yet."}
