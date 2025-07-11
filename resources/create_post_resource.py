from redis_om import JsonModel


class CreatePostResource(JsonModel):
    title: str
    content: str
    author_id: str
    tags: list[str]