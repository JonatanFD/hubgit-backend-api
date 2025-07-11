from datetime import datetime
from typing import Set

from redis_om import Field, JsonModel, get_redis_connection

from env import REDIS_URL


class Post(JsonModel, index=True):
    created_at: str = Field(default_factory=lambda: datetime.now().isoformat())

    author_id: str = Field(description="ID of the user who is the author of the post")
    company_id: str = Field(description="ID of the company to which the post belongs")
    title: str = Field(default="", description="Title of the post")
    content: str = Field(default="", description="Content of the post")
    tags: Set[str] = Field(default=[], description="List of tags associated with the post")
    likes: Set[str] = Field(default_factory=set, description="ID of the user who liked the post")

    class Meta:
        database = get_redis_connection(url=REDIS_URL)

class PostComment(JsonModel, index=True):
    created_at: str = Field(default_factory=lambda: datetime.now().isoformat())

    post_id: str = Field(description="ID of the post to which the comment belongs")
    author_id: str = Field(description="ID of the user who is the author of the comment")
    content: str = Field(default="", description="Content of the comment")
    likes: Set[str] = Field(description="ID of the user who liked the comment")

    class Meta:
        database = get_redis_connection(url=REDIS_URL)
