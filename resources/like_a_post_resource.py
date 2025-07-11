from redis_om import JsonModel


class LikePostResource(JsonModel):
    user_id: str