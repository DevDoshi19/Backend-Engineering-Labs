import logging
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI
from scalar_fastapi import Theme, add_scalar_reference
from sqlalchemy import text

from app.database import engine

load_dotenv()
logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

@asynccontextmanager
async def lifespan(app:FastAPI):
    logging.info("Server is started..")
    async with engine.connect() as conn:
        await conn.execute(text("SELECT 1"))  # Test the connection

    logging.info("Database connection is established")

    yield
    await engine.dispose()  # Close the database connection pool
    logging.info("Server is shut down")

app = FastAPI(
    title="Counter-Project",
    lifespan=lifespan,
    version="0.1.0",
    docs_url=None
)

add_scalar_reference(
    app,
    route="/docs",
    theme=Theme.KEPLER,
)

@app.get("/",status_code=200)
async def get_hello() -> dict:
    return {
        "message":"Counter API is running !!"
    }
