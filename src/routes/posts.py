from fastapi import APIRouter, Depends, Query

from src.controllers.posts import create_post, get_post_info, delete_user_post
from src.controllers.user import create_user, create_token
from src.database.models import UserModel
from src.dependencies.database import provide_database
from src.dto.base_response import BaseResponse
from src.dto.posts import CreatePostModel, ResponseCreatedPostModel, ResponsePostsModel
from src.dto.user import LoginModel, SignUpResponse, SignUpModel
from src.security.jwt import create_jwt_token, get_jwt_payload
from src.dependencies.user import get_user_by_token

post_router = APIRouter(prefix="/posts", tags=["Posts"])


@post_router.post("", response_model=ResponseCreatedPostModel)
async def create_user_post(
        payload: CreatePostModel,
        user: UserModel = Depends(get_user_by_token),
        db=Depends(provide_database)
):
    post_id = await create_post(db=db, user=user, payload=payload)
    return ResponseCreatedPostModel(status=True, data={"post_id": post_id})


@post_router.get("", response_model=ResponsePostsModel)
async def get_post(
        user: UserModel = Depends(get_user_by_token),
        db=Depends(provide_database)
):
    posts = await get_post_info(user=user, db=db)
    return ResponsePostsModel(status=True, data=posts)


@post_router.delete("")
async def delete_post(
        post_id: int = Query(..., description="post id"),
        user: UserModel = Depends(get_user_by_token),
        db=Depends(provide_database)
):
    await delete_user_post(db=db, user=user, post_id=post_id)
    return BaseResponse(status=True)