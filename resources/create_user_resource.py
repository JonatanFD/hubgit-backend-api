from redis_om import JsonModel


class CreateUserResource(JsonModel):
    """
    Resource for creating a user.
    This resource is used to define the structure of the data required to create a new user.
    """
    username: str
    email: str
    password: str
