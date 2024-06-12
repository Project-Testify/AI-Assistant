from fastapi import APIRouter, HTTPException, Query
from ..services.prompt import prompt

router = APIRouter()

@router.get("/generate-question/", response_model=dict)
async def generate_question(text: str = Query(..., description="The text to generate a question for"),
                            examid: str = Query(..., description="The ID of the exam related to the text")) -> dict:
    """Endpoint to generate a question for a given text using OpenAI's model."""
    try:
        # Assuming 'prompt' function is synchronous; if it's async, use 'await prompt(text, examid)'
        question_response = prompt(text, examid)
        return question_response
    except Exception as e:
        # Catching a broad exception is not best practice; adjust according to specific exceptions expected from 'prompt'
        raise HTTPException(status_code=500, detail=f"An error occurred while generating the question: {str(e)}")
