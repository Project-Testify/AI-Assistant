from fastapi import FastAPI

# Initialize the FastAPI app with a custom title
app = FastAPI(title="Testify AI")

@app.get("/api/assistant", response_model=dict)
async def read_root() -> dict:
    """
    Root GET endpoint to return a simple greeting.
    Returns a JSON object with a greeting message.
    """
    return {"message": "Welcome to the Testify AI Assistant!"}
