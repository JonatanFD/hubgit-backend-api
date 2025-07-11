from redis_om import Field
from typing import Set
from entities.shared.audit_and_redis_metadata_schema import AuditableAndRedisMetadataSchema



class Post(AuditableAndRedisMetadataSchema):
    author_id: str = Field(description="ID of the user who is the author of the post")
    company_id: str = Field(description="ID of the company to which the post belongs")
    title: str = Field(default="", description="Title of the post")
    content: str = Field(default="", description="Content of the post")
    tags: Set[str] = Field(default=[], description="List of tags associated with the post")
    likes: Set[str] = Field(description="ID of the user who liked the post")

class PostComment(AuditableAndRedisMetadataSchema):
    post_id: str = Field(description="ID of the post to which the comment belongs")
    author_id: str = Field(description="ID of the user who is the author of the comment")
    content: str = Field(default="", description="Content of the comment")
    likes: Set[str] = Field(description="ID of the user who liked the comment")

