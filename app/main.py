from fastapi import FastAPI
import logging
from logstash_async.handler import AsynchronousLogstashHandler

host = 'logstash'
port = 5000

# Create the logger
logger = logging.getLogger("python-logstash-logger")
logger.setLevel(logging.INFO)

# Create the handler
handler = AsynchronousLogstashHandler(host, port, database_path='')
logger.addHandler(handler)

# Create the formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Add the formatter to the handler
handler.setFormatter(formatter)

# Add the handler to the logger
logger.addHandler(handler)

# Test the logger
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
