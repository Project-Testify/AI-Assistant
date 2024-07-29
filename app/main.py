from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
from logstash_async.handler import AsynchronousLogstashHandler




from .core.log import logger

logger.info("Testify AI Application Started")



# Create an instance of the FastAPI application with a custom title
app = FastAPI(title="Testify AI")

# Enable CORS (Cross-Origin Resource Sharing) to allow requests from the frontend

origins = [
    'http://127.0.0.1:4500',
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/assistant", response_model=dict)
async def read_root() -> dict:
    """
    Root GET endpoint that provides a simple greeting message.

    Returns:
        dict: A dictionary containing a greeting message.
    """

    logger.info("Root endpoint accessed")

    return {"message": "Welcome to the Testify AI Assistant!"}
