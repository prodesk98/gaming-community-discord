from asyncio import current_task

from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession, async_scoped_session

from .sqlite import engine

async_session = async_sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)


async def get_session():
    session = async_scoped_session(async_session, scopefunc=current_task)
    return session
