from typing import Dict

from sqlalchemy import insert, select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.exceptions import HTTPException

from src.database.engine import Postgres
from src.database.models import UserModel, PostModel
from src.dto.posts import CreatePostModel


async def create_post(user: UserModel, payload: CreatePostModel, db: Postgres):
    session: AsyncSession
    async with db.session() as session:
        post_id = await session.execute(
            insert(PostModel).values(user_id=user.id, text=payload.text).returning(PostModel.id)
        )
        await session.commit()
        return post_id.fetchone()[0]


async def get_post_info(user: UserModel, db: Postgres):
    session: AsyncSession
    async with db.session() as session:
        result = []
        posts = await session.stream_scalars(
            select(PostModel).where(PostModel.user_id == user.id)
        )
        async for post in posts:
            result.append(
                {
                    "post_id": post.id,
                    "text": post.text
                }
            )
    return result


async def delete_user_post(user: UserModel, post_id: int, db: Postgres):
    session: AsyncSession
    async with db.session() as session:
        await session.execute(
            delete(PostModel)
            .where(PostModel.user_id == user.id, PostModel.id == post_id))
        await session.commit()
