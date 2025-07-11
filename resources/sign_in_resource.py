from redis_om import JsonModel


class SignInResource(JsonModel):
    email: str
    password: str
