
from entities.user import User
from resources.user_response import UserResource

class UserAssembler():

    @staticmethod
    def to_user_resource_from_entity(user: User) -> UserResource:
        """
        Converts a User entity to a UserResource.

        Args:
            user (User): The User entity to convert.

        Returns:
            UserResource: The converted UserResource.
        """
        return UserResource(
            user_id=user.id,
            email=user.email,
            username=user.username,
            platform_role=user.platform_role.value
        )