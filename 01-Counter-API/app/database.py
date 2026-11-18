import os
from collections.abc import AsyncGenerator

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import (
    AsyncAttrs,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.engine import make_url

load_dotenv()

# define databse url
DATABASE_URL = os.getenv("DATABASE_URL")
print(
    "Database URL:",
    make_url(DATABASE_URL).render_as_string(hide_password=True)
)

if not DATABASE_URL:
    raise RuntimeError("DATABASE URL is not configured")

# configured our engine

engine = create_async_engine(
        DATABASE_URL,
        pool_size=5, # keep 5 connection in the pool 
        max_overflow=10, # allow upto 10 connection when needed 
        pool_pre_ping=True, # check connection health before using it 
        echo=True # print genrated sql query 
)

# create a session
SessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autoflush=False, # don't automatically flush before every query 
    expire_on_commit=False # keep loaded objects accessible after commit 
) 

# base class 
class Base(AsyncAttrs,DeclarativeBase):
    pass

#one session per request 
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as db:
        yield db