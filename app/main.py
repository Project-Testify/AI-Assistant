from fastapi import FastAPI

# Create an instance of the FastAPI application with a custom title
app = FastAPI(title="Testify AI")

@app.get("/api/assistant", response_model=dict)
async def read_root() -> dict:
    """
    Root GET endpoint that provides a simple greeting message.

    Returns:
        dict: A dictionary containing a greeting message.
    """
    return {"message": "Welcome to the Testify AI Assistant!"}
