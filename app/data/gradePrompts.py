from typing import List
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.output_parsers import JsonOutputParser



class GradePromptParser(BaseModel):
   correct_points: List[str] = Field(description="The correct points for the answer.")
   incorrect_points: List[str] = Field(description="The incorrect points for the answer.")




def grade_prompt(question: str, answer:str, valid_points:List[str]) -> tuple[str, JsonOutputParser]:
    """
    Generates a prompt for grading an answer along with a JSON output parser.

    Returns:
        tuple[str, JsonOutputParser]: A tuple containing the prompt and the JSON output parser.
    """
    prompt_text = f"Return the correct and incorrect points for the answer to the question: {question} with the answer: {answer} and valid points: {valid_points}"
    parser = JsonOutputParser(pydantic_object=GradePromptParser)
    return (prompt_text, parser) 
