from fastapi import (APIRouter, HTTPException, Depends)
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from redis_om.model.model import NotFoundError
from resources.create_user_resource import CreateUserResource
from resources.sign_in_resource import SignInResource
from resources.sign_in_resource_with_token import SignInResourceWithToken
from resources.user_resource import UserResource
from entities.user import User
from services.jwt import create_access_token, verify_access_token
import bcrypt

SALT_SIZE = 10

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

    # Hash the password using bcrypt
    hashed_password = bcrypt.hashpw(dump.get("password").encode("utf-8"), bcrypt.gensalt(SALT_SIZE))
    dump["password"] = hashed_password.decode("utf-8")

    user = User(**dump)
    print("created ", user)
    saved_user = user.save()

    return UserResource.build_from_entity(saved_user)

@router.post("/sign-in")
async def sign_in(req: SignInResource):
    dump = req.model_dump()

    try:
        found_user = User.find(User.email == dump.get("email")).first()
    except NotFoundError:
        found_user = None

    if not found_user or not bcrypt.checkpw(dump.get("password").encode("utf-8"), found_user.password.encode("utf-8")):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    # Generate JWT token
    access_token = create_access_token({"sub": found_user.email})

    return SignInResourceWithToken.build_from_entity(found_user.pk, found_user.email, access_token)


