from redis_om import JsonModel


class SignInResourceWithToken(JsonModel):
    username: str
    pk: str
    token: str

    @staticmethod
    def build_from_entity(pk: str, username: str, token: str):
        return SignInResourceWithToken(
            username=username,
            pk=pk,
            token=token
        )
