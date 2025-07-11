from redis_om import JsonModel


class CreateUserResource(JsonModel):
    username: str
    email: str
    password: str
