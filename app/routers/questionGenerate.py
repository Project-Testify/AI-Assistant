from fastapi import APIRouter, Query
from ..services.prompt import prompt


router = APIRouter()

@router.get("/generate-question/", response_model=dict)
async def generate_question(text: str = Query(..., description="The text to generate a question for"),
                            examid: str = Query(..., description="The ID of the exam related to the text")) -> any:
    """Endpoint to generate a question for a given text using OpenAI's model."""
    
    return prompt(text, examid) 
