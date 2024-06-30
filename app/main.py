from fastapi import FastAPI
import logging
from logstash_async.handler import AsynchronousLogstashHandler


from .core.log import logger

logger.info("Testify AI Application Started")



# Create an instance of the FastAPI application with a custom title
app = FastAPI(title="Testify AI")

@app.get("/api/assistant", response_model=dict)
async def read_root() -> dict:
    """
    Root GET endpoint that provides a simple greeting message.

    Returns:
        dict: A dictionary containing a greeting message.
    """

    logger.info("Root endpoint accessed")

    return {"message": "Welcome to the Testify AI Assistant!"}
