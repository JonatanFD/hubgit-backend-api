from redis_om import JsonModel

from entities.user import User


class UserResource(JsonModel):
    user_id: str
    email: str
    username: str
    platform_role: str

    @staticmethod
    def build_from_entity(entity: User):
        return UserResource(
            user_id=entity.pk,
            email=entity.email,
            username=entity.username,
            platform_role=entity.platform_role.value
        ).model_dump()

    @staticmethod
    def build_error(msg: str):
        return {
            "error": msg
        }