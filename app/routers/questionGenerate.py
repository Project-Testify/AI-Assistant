from fastapi import APIRouter, HTTPException, Query
from ..services.prompt import prompt

router = APIRouter()

@router.get("/generate-question/mcq/", response_model=dict)
async def generate_question(text: str = Query(..., description="The text to generate a question for"),
                            examid: str = Query(..., description="The ID of the exam related to the text"),
                            choices: int = Query(4, description="The number of choices for the multiple choice question")
                            ) -> dict:
    """Endpoint to generate a question for a given text using OpenAI's model."""
    try:
        # Assuming 'prompt' function is synchronous; if it's async, use 'await prompt(text, examid)'
        question_response = prompt(text, examid, question_type='mcq', choices=choices)
        return question_response
    except Exception as e:
        # Catching a broad exception is not best practice; adjust according to specific exceptions expected from 'prompt'
        raise HTTPException(status_code=500, detail=f"An error occurred while generating the question: {str(e)}")


@router.get("/generate-question/essay/", response_model=dict)
async def generate_essay_question(text: str = Query(..., description="The text to generate an essay question for"),
                                  examid: str = Query(..., description="The ID of the exam related to the text")) -> dict:
    """Endpoint to generate an essay question for a given text using OpenAI's model."""
    try:
        # Assuming 'prompt' function is synchronous; if it's async, use 'await prompt(text, examid, question_type='essay')
        question_response = prompt(text, examid, question_type='essay')
        return question_response
    except Exception as e:
        # Catching a broad exception is not best practice; adjust according to specific exceptions expected from 'prompt'
        raise HTTPException(status_code=500, detail=f"An error occurred while generating the essay question: {str(e)}")