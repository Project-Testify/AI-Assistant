from fastapi import APIRouter, HTTPException, Query
from ..services.generate import generate, generate_list

from ..core.log import logger

router = APIRouter()

@router.post("/generate-question/mcq/", response_model=dict)
async def generate_question(text: str = Query(..., description="The text to generate a question for"),
                            examid: str = Query(..., description="The ID of the exam related to the text"),
                            choices: int = Query(4, description="The number of choices for the multiple choice question")
                            ) -> dict:
    """Endpoint to generate a question for a given text using OpenAI's model."""
    try:
        # Assuming 'prompt' function is synchronous; if it's async, use 'await prompt(text, examid)'
        question_response = generate(text, examid, question_type='mcq', choices=choices)
        logger.info(f"Generated question: {question_response}")
        return question_response
    except Exception as e:
        # Catching a broad exception is not best practice; adjust according to specific exceptions expected from 'prompt'
        logger.error(f"An error occurred while generating the question: {str(e)}")
        raise HTTPException(status_code=500, detail=f"An error occurred while generating the question: {str(e)}")


@router.post("/generate-question/essay/", response_model=dict)
async def generate_essay_question(text: str = Query(..., description="The text to generate an essay question for"),
                                  examid: str = Query(..., description="The ID of the exam related to the text")) -> dict:
    """Endpoint to generate an essay question for a given text using OpenAI's model."""
    try:
        # Assuming 'prompt' function is synchronous; if it's async, use 'await prompt(text, examid, question_type='essay')
        question_response = generate(text, examid, question_type='essay')
        logger.info(f"Generated essay question: {question_response}")
        return question_response
    except Exception as e:
        # Catching a broad exception is not best practice; adjust according to specific exceptions expected from 'prompt'
        logger.error(f"An error occurred while generating the essay question: {str(e)}")
        raise HTTPException(status_code=500, detail=f"An error occurred while generating the essay question: {str(e)}")
    

@router.post("/generate-questions/mcq/", response_model=list[dict])
async def generate_mcq_questions(text: str = Query(..., description="The text to generate multiple choice questions for"),
                                 examid: str = Query(..., description="The ID of the exam related to the text"),
                                 choices: int = Query(4, description="The number of choices for the multiple choice questions"),
                                 num_questions: int = Query(1, description="The number of questions to generate")
                                 ) -> list[dict]:
    """Endpoint to generate multiple choice questions for a given text using OpenAI's model."""
    try:
        # Assuming 'prompt' function is synchronous; if it's async, use 'await prompt(text, examid)'
        question_responses = generate_list(text, examid, question_type='mcq', choices=choices, num_questions=num_questions)
        logger.info(f"Generated multiple choice questions: {question_responses}")
        return question_responses
    except Exception as e:
        # Catching a broad exception is not best practice; adjust according to specific exceptions expected from 'prompt'
        logger.error(f"An error occurred while generating the multiple choice questions: {str(e)}")
        raise HTTPException(status_code=500, detail=f"An error occurred while generating the multiple choice questions: {str(e)}")
    
