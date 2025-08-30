from sqlalchemy import create_engine, Index
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.declarative import declarative_base

from .config import Config


engine = create_async_engine(
    Config.DATABASE_URL,
    pool_size=25,
    max_overflow=0,
)
SessionLocal = async_sessionmaker(
    engine,
    autocommit=False,
    autoflush=False,
)
"""
engine = create_engine(
    Config.SQLALCHEMY_DATABASE_URI,
    pool_size=25,
    max_overflow=0,
)
SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)
"""

Base = declarative_base()


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        await db.close()


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        i = Index("rolls_room_uid_idx", Base.metadata.tables["rolls"].c.room_uid)
        await conn.run_sync(i.create, checkfirst=True)
