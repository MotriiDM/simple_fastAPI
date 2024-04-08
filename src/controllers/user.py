from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.exceptions import HTTPException

from src.database.engine import Postgres
from src.database.models import UserModel
from src.dto.user import SignUpModel, LoginModel
from src.security.jwt import create_jwt_token
import hashlib

from src.security.password import encrypt_password


async def create_user(db: Postgres, payload: SignUpModel):
    session: AsyncSession
    async with db.session() as session:
        password = await encrypt_password(payload.password)
        await session.execute(
            insert(UserModel).values(
                first_name=payload.first_name,
                last_name=payload.last_name,
                password=password,
                login=payload.login
            ).returning(UserModel.id)
        )
        await session.commit()


async def create_token(payload: LoginModel, db: Postgres):
    exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    password = await encrypt_password(payload.password)
    session: AsyncSession
    async with db.session() as session:
        user: UserModel = await session.scalar(
            select(UserModel).where(UserModel.login==payload.login)
        )
    if user.password != password:
        raise exception
    token = await create_jwt_token(credentials={"login": user.login, "user_id": user.id})
    return token
