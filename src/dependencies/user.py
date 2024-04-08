from sqlalchemy import select, true, update
from urllib.request import Request

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.models import UserModel
from src.dependencies.database import provide_database
from src.security.jwt import get_jwt_payload


async def get_user_by_token(
        db=Depends(provide_database),
        jwt_payload=Depends(get_jwt_payload),
):
    session: AsyncSession
    async with db.session() as session:
        statement = (
            select(UserModel)
            .where(
                UserModel.id == jwt_payload["user_id"],
            )
            .limit(1)
        )

        user = await session.scalar(statement)
        return user
