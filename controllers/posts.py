from fastapi import APIRouter
from redis_om import NotFoundError

from entities.company import Company
from entities.post import Post
from resources.create_post_resource import CreatePostResource
from controllers.companies import get_members

router = APIRouter(prefix="/companies", tags=["posts"])


@router.post("/{company_id}/posts")
async def create_post(resource: CreatePostResource, company_id: str):

    # check if the company exists
    try:
        company = Company.get(company_id)
    except NotFoundError:
        return {"error": "Company not found"}

    # check if the user is a member of the company

    members = await get_members(company_id)

    print(members)

    if resource.author_id not in [member["user_id"] for member in members]:
        return {"error": "User is not a member of this company"}

    post_data = {
        "title": resource.title,
        "content": resource.content,
        "tags": resource.tags,
        "company_id": company_id,
        "author_id": resource.author_id
    }
    post = Post(**post_data)

    # Save the post to the database
    saved_post = post.save()
    if not saved_post:
        return {"error": "Failed to create post"}

    # Return the saved post as a dictionary
    return saved_post.model_dump()


@router.get("/{company_id}/posts")
async def get_posts(company_id: str):
    try:
        company = Company.get(company_id)
    except NotFoundError:
        return {"error": "Company not found"}

    # Fetch all posts for the company
    posts = Post.find(Post.company_id == company_id).all()
    if not posts:
        return {"message": "No posts found for this company"}
    return [post.model_dump() for post in posts]