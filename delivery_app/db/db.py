from typing import AsyncContextManager

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine


class AsyncSessionFactory:
    def __init__(
        self, database_dsn: str, echo: bool = False, expire_on_commit: bool = False
    ) -> None:
        self._engine = create_async_engine(database_dsn, echo=echo, future=True)
        self._sessionmaker = async_sessionmaker(self._engine, expire_on_commit=expire_on_commit)

    def __call__(self) -> AsyncContextManager[AsyncSession]:
        return self._sessionmaker()

    async def close_all(self) -> None:
        await self._engine.dispose()
