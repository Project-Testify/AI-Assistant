from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from ..services.generate import generate, generate_list

from ..core.log import logger


class MCQRequest(BaseModel):
    text: str
    examid: str
    choices: int

class EssayQuestionRequest(BaseModel):
    text: str
    examid: str



router = APIRouter()

@router.post("/generate-question/mcq/", response_model=dict)
async def generate_question(request: MCQRequest) -> dict:
    """Endpoint to generate a multiple-choice question for a given text using OpenAI's model."""
    try:
        # Assuming 'prompt' function is synchronous; if it's async, use 'await prompt(text, examid, question_type='mcq', choices=request.choices)'
        question_response = generate(request.text, request.examid, question_type='mcq', choices=request.choices)
        logger.info(f"Generated MCQ: {question_response}")
        return question_response
    except Exception as e:
        logger.error(f"An error occurred while generating the MCQ: {str(e)}")
        raise HTTPException(status_code=500, detail=f"An error occurred while generating the MCQ: {str(e)}")

@router.post("/generate-question/essay/", response_model=dict)
async def generate_essay_question(request: EssayQuestionRequest) -> dict:
    """Endpoint to generate an essay question for a given text using OpenAI's model."""
    try:
        # Assuming 'prompt' function is synchronous; if it's async, use 'await prompt(text, examid, question_type='essay')
        question_response = generate(request.text, request.examid, question_type='essay')
        logger.info(f"Generated essay question: {question_response}")
        return question_response
    except Exception as e:
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
    

@router.post("/generate-questions/essay/", response_model=list[dict])
async def generate_essay_questions(text: str = Query(..., description="The text to generate essay questions for"),
                                      examid: str = Query(..., description="The ID of the exam related to the text"),
                                      num_questions: int = Query(1, description="The number of questions to generate")
                                      ) -> list[dict]:
     """Endpoint to generate essay questions for a given text using OpenAI's model."""
     try:
          # Assuming 'prompt' function is synchronous; if it's async, use 'await prompt(text, examid, question_type='essay')
          question_responses = generate_list(text, examid, question_type='essay', num_questions=num_questions)
          logger.info(f"Generated essay questions: {question_responses}")
          return question_responses
     except Exception as e:
          # Catching a broad exception is not best practice; adjust according to specific exceptions expected from 'prompt'
          logger.error(f"An error occurred while generating the essay questions: {str(e)}")
          raise HTTPException(status_code=500, detail=f"An error occurred while generating the essay questions: {str(e)}")
     