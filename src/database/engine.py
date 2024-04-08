from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import AsyncContextManager

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker


@dataclass
class Postgres:
    engine: AsyncEngine
    sessionmaker: sessionmaker

    @classmethod
    def create(cls, url: str) -> "Postgres":
        engine: AsyncEngine = create_async_engine(
            url,
            pool_recycle=3600,
            pool_pre_ping=True,
            pool_size=50,
            max_overflow=30,
            pool_timeout=60
        )
        async_session: sessionmaker = sessionmaker(
            engine,
            autocommit=False,
            expire_on_commit=False,
            class_=AsyncSession,
            future=True,
        )

        return cls(engine=engine, sessionmaker=async_session)

    @asynccontextmanager
    async def session(self) -> AsyncContextManager[AsyncSession]:
        async with self.sessionmaker() as db:
            yield db
