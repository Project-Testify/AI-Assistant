from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

from ..services.grade import grade 

from ..core.log import logger

class gradeRequest(BaseModel):
    question: str
    answer: str
    valid_points: list[str]



router = APIRouter()

@router.post("/grade/", response_model=dict)
async def grade_answer(request: gradeRequest) -> dict:
    """Endpoint to grade an answer."""
    try:
        print(request.valid_points)
        print("Sending grade answer")
        grade_result = grade(request.question, request.answer, request.valid_points)
        return grade_result
    except Exception as e:
        logger.error(f"An error occurred while grading the answer: {str(e)}")
        raise HTTPException(status_code=500, detail=f"An error occurred while grading the answer: {str(e)}")

