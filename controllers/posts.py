from fastapi import APIRouter
from redis_om import NotFoundError
from starlette.status import HTTP_200_OK

from entities.company import Company
from entities.post import Post, PostComment
from resources.create_post_resource import CreatePostResource
from controllers.companies import get_members
from resources.comment_post_resource import CommentPostResource
from resources.get_post_by_id_and_user_id_resource import GetCompanyDetailsResource
from resources.like_a_comment_resource import LikeCommentResource
from resources.like_a_post_resource import LikePostResource

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


@router.post("/{company_id}/posts/{post_id}", description="used to get the post by id but using the body to pass the user_id")
async def get_post(resource: GetCompanyDetailsResource, company_id: str, post_id: str):
    # check if the company exists
    try:
        company = Company.get(company_id)
    except NotFoundError:
        return {"error": "Company not found"}

    # check if the post exists
    try:
        post = Post.get(post_id)
    except NotFoundError:
        return {"error": "Post not found"}

    # check if the user is a member of the company
    members = await get_members(company_id)
    if resource.user_id not in [member["user_id"] for member in members]:
        return {"error": "User is not a member of this company"}

    # Return the post if the user is a member of the company
    # Return the post as a dictionary
    return post.model_dump()


@router.post("/{company_id}/posts/{post_id}/comments")
async def comment_post(resource: CommentPostResource ,company_id: str, post_id: str):
    # check if the company exists
    try:
        company = Company.get(company_id)
    except NotFoundError:
        return {"error": "Company not found"}

    # check if the post exists
    try:
        post = Post.get(post_id)
    except NotFoundError:
        return {"error": "Post not found"}

    # check if the user is a member of the company
    members = await get_members(company_id)
    if resource.author_id not in [member["user_id"] for member in members]:
        return {"error": "User is not a member of this company"}

    comment_data = {
        "post_id": post_id,
        "author_id": resource.author_id,
        "content": resource.content
    }

    comment = PostComment(**comment_data)
    # Save the comment to the database
    saved_comment = comment.save()
    if not saved_comment:
        return {"error": "Failed to create comment"}
    # Return the saved comment as a dictionary
    return saved_comment.model_dump()

@router.post("/{company_id}/posts/{post_id}/likes")
async def like_post(company_id: str, post_id: str, resource: LikePostResource):
    # check if the company exists
    try:
        company = Company.get(company_id)
    except NotFoundError:
        return {"error": "Company not found"}

    # check if the post exists
    try:
        post = Post.get(post_id)
    except NotFoundError:
        return {"error": "Post not found"}

    # check if the user is a member of the company
    members = await get_members(company_id)
    if resource.user_id not in [member["user_id"] for member in members]:
        return {"error": "User is not a member of this company"}

    # Add the user to the likes set
    post.likes.add(resource.user_id)
    post.save()

    return HTTP_200_OK

@router.post("/{company_id}/posts/{post_id}/comments/{comment_id}/likes")
async def like_comment(company_id: str, post_id: str, comment_id: str, resource: LikeCommentResource):
    # check if the company exists
    try:
        company = Company.get(company_id)
    except NotFoundError:
        return {"error": "Company not found"}

    # check if the post exists
    try:
        post = Post.get(post_id)
    except NotFoundError:
        return {"error": "Post not found"}

    # check if the comment exists
    try:
        comment = PostComment.get(comment_id)
    except NotFoundError:
        return {"error": "Comment not found"}

    # check if the user is a member of the company
    members = await get_members(company_id)
    if resource.user_id not in [member["user_id"] for member in members]:
        return {"error": "User is not a member of this company"}

    # Add the user to the likes set of the comment
    comment.likes.add(resource.user_id)
    comment.save()

    return HTTP_200_OK

@router.get("/{company_id}/posts/{post_id}/comments")
async def get_comments(company_id: str, post_id: str):
    # check if the company exists
    try:
        company = Company.get(company_id)
    except NotFoundError:
        return {"error": "Company not found"}

    # check if the post exists
    try:
        post = Post.get(post_id)
    except NotFoundError:
        return {"error": "Post not found"}

    # Fetch all comments for the post
    comments = PostComment.find(PostComment.post_id == post_id).all()
    if not comments:
        return {"message": "No comments found for this post"}

    return [comment.model_dump() for comment in comments]

"""
jonatan : 01JZXH2GW5V24620DHNBTFBDTC
mateo: 01JZXH334ZR2DPPMHDGK9PK7Q9

Registra y no admite duplicados de correo
Valida la contraseña

empresa : 01JZXH3E8XGNY4VQ5A8Y05Q7AX

agrega y devuelve los miembros de la empresa

post : 01JZXH54DQ7BKRAYD8M2MXZFJ9
comment: 01JZXHEDN6CER75YQYF6VJC819
"""