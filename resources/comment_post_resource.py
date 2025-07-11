from redis_om import JsonModel


class CommentPostResource(JsonModel):
    author_id: str
    content: str
