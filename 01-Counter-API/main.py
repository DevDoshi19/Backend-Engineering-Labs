from fastapi import FastAPI
from scalar_fastapi import add_scalar_reference,Theme
import logging

PORT = 8000 

def lifespan(app:FastAPI):
    logging.info("Server is started..")
    yield()
    logging.info("Server is shoutdown")

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
def get_hello() -> dict:
    return {
        "message":"Counter API is running !!"
    }
