**Project 01 — Counter API**

Beginner

Python · FastAPI · SQLAlchemy · PostgreSQL

We're not going to make this unnecessarily complicated.

### **Problem statement**

Build a simple counter service where users can create counters, increment them, decrement them and retrieve their current values.

### **Requirements**

| Method | Endpoint                   | Responsibility           |
| ------ | -------------------------- | ------------------------ |
| POST   | `/counters`                | Create a counter         |
| GET    | `/counters`                | Get all counters         |
| GET    | `/counters/{id}`           | Get a particular counter |
| PATCH  | `/counters/{id}/increment` | Increment by 1           |
| PATCH  | `/counters/{id}/decrement` | Decrement by 1           |
| DELETE | `/counters/{id}`           | Delete a counter         |

### **Concepts you'll learn**

1. HTTP methods and status codes.
2. FastAPI routing.
3. Request validation using Pydantic.
4. SQLAlchemy models.
5. Database sessions.
6. CRUD operations.
7. Exception handling.
8. PostgreSQL integration.
9. Project structure and separation of concerns.

Later, we'll revisit this same counter problem to introduce race conditions and database locking. That's where things get interesting!

# **6. Your first assignment**

Assignment 01

**Create the project folder&#x20;**`01-counter-api`**.**

Your first task is only to:

1. Initialize a Python virtual environment.
2. Install FastAPI and Uvicorn.
3. Create a basic FastAPI application.
4. Implement a `GET /` endpoint.
5. Return:

```
{
    "message": "Counter API is running"
}
```

6\. Run the server and test it through `/docs`.

**Don't implement the database or counter functionality yet.** We'll build incrementally.

One last thing: I want you to approach these projects as an engineer, not someone completing tutorials.


# need to understand and implimentation : 

Yes, you use the exact same DeclarativeBase and models with AsyncSession. Your table definitions and column mappings stay completely unchanged, while only the engine, session, and query execution become asynchronous.

How Async Works with DeclarativeBase

• Models Stay Synchronous. DeclarativeBase simply describes your database schema and Python classes. Defining a class does not perform any network I/O, so there is no async version of DeclarativeBase.
• Add AsyncAttrs (Recommended). Mixing AsyncAttrs into your Base class lets you safely await lazy-loaded relationships if you ever need to access them asynchronously.
• Use run_sync for DDL. Methods like Base.metadata.create_all are synchronous under the hood, so you run them through await conn.run_sync(Base.metadata.create_all).
• Async Drivers Required. Your connection string must use an async-compatible driver (such as sqlite+aiosqlite or postgresql+asyncpg).

Complete Async Example

python
import asyncio
from sqlalchemy import String, select
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

# 1. Standard DeclarativeBase (with AsyncAttrs for async relationship support)
class Base(AsyncAttrs, DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))

async def main():
    # 2. Create an async engine with an async driver
    engine = create_async_engine("sqlite+aiosqlite:///async_example.db")

    # 3. Create tables using run_sync
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # 4. Create a session factory and run queries with AsyncSession
    async_session = async_sessionmaker(engine, expire_on_commit=False)

    async with async_session() as session:
        session.add(User(name="Alice"))
        await session.commit()

        stmt = select(User).where(User.name == "Alice")
        result = await session.scalars(stmt)
        user = result.first()
        print(user.name)

    await engine.dispose()

asyncio.run(main())
Use code with caution.

Key Async Gotchas to Remember

• Set expire_on_commit=False. By default, committing a session expires all object attributes, which triggers an implicit database query the next time you read user.name. In async mode, implicit queries raise a MissingGreenlet error, so always set expire_on_commit=False on async_sessionmaker.
• Eager Load Relationships. Avoid relying on default lazy loading for relationships in async code. Use selectinload() or joinedload() inside your select() queries so related data is fetched upfront.
If you are setting this up in a web framework like FastAPI, I can show you how to structure the get_db dependency injection and relationship loading for async endpoints. Would that be helpful?


Yes, that is the exact same lazy loading problem (often causing N+1 queries or crashes in production), and AsyncAttrs is only a fallback—not the main production solution. Separately, run_sync for DDL is simply a bridge that lets SQLAlchemy run synchronous table-creation commands safely inside an asynchronous connection.

1. Lazy Loading vs. AsyncAttrs vs. Production Solutions

When a User has many Posts, SQLAlchemy defaults to lazy loading: it fetches User first, and only runs a second SQL query for Posts the moment you access user.posts.
• Why it breaks in Async. Reading user.posts looks like a normal Python attribute lookup, so you cannot write await user.posts. In async code, SQLAlchemy refuses to run hidden background queries and crashes with a MissingGreenlet error.
• Why it hurts Production Apps. Even in synchronous apps, lazy loading inside a loop causes the N+1 query problem (1 query for 100 users + 100 separate queries for their posts), slowing down production APIs.
• What AsyncAttrs actually does. Adding AsyncAttrs to Base gives your models an .awaitable_attrs helper so you can write await user.awaitable_attrs.posts. It prevents crashes when you forget to preload data, but it still fires a separate query.
• The Real Production Fix (Eager Loading). Tell SQLAlchemy to fetch related records upfront in your select() statement using selectinload() or joinedload().
python
from sqlalchemy import select
from sqlalchemy.orm import selectinload

# BAD in production (causes N+1 queries or MissingGreenlet in async)
stmt = select(User)

# GOOD in production (fetches Users and all their Posts in 2 clean queries)
stmt = select(User).options(selectinload(User.posts))
users = (await session.scalars(stmt)).all()

# Now user.posts is already in memory—no await or extra query needed!
for user in users:
    print(user.name, len(user.posts))
Use code with caution.

2. What "Use run_sync for DDL" Means

• What is DDL? DDL stands for Data Definition Language—SQL commands that define or change database structure rather than data rows (such as CREATE TABLE, ALTER TABLE, and DROP TABLE).
• Why is create_all synchronous? Checking existing tables and emitting CREATE TABLE statements involves complex schema inspection logic written synchronously inside SQLAlchemy's Core engine.
• How conn.run_sync() works. await conn.run_sync(Base.metadata.create_all) takes a synchronous function, temporarily passes it a synchronous-style wrapper around your async connection, runs it safely in the event loop without blocking, and awaits its completion.
• Production Note. You only use Base.metadata.create_all for quick scripts, prototypes, and automated tests. In real production apps, you manage DDL changes using Alembic (SQLAlchemy's database migration tool).
If you'd like to explore the production workflow further, I can show you:
How to choose between selectinload() and joinedload() for different relationship typesHow to set up Alembic with an async SQLAlchemy engine for production migrations
Which one would you like to look at next?
