from sqlalchemy import create_engine, Index
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .config import Config


# engine = create_async_engine(Config.DATABASE_URL)
# SessionLocal = async_sessionmaker(sync_session_class=sessionmaker(autocommit=False, autoflush=False, bind=engine))
engine = create_engine(
    Config.SQLALCHEMY_DATABASE_URI,
    pool_size=25,
    max_overflow=0,
)
SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    Base.metadata.create_all(bind=engine)

    i = Index("rolls_room_uid_idx", Base.metadata.tables["rolls"].c.room_uid)
    i.create(engine, checkfirst=True)
