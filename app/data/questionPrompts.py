from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.output_parsers import JsonOutputParser



# Define a Pydantic model for a standard question and answer format.
class QuestionParser(BaseModel):
    question: str = Field(description="The question generated from the text.")
    valid_answer: list[str] = Field(description="Valid answers for the generated question.")

# # Define a Pydantic model for multiple-choice questions.
# class Answer(BaseModel):
#     char: str = Field(description="The character representing the answer, e.g., 'A', 'B', 'C', 'D'.")
#     text: str = Field(description="The text of the answer.")

class MultipleChoiceQuestionParser(BaseModel):
    question: str = Field(description="The multiple choice question generated from the text.")
    options: list[str] = Field(description="The options for the multiple choice question, should be a list of Answer objects.")
    answer: str = Field(description="The character representing the correct answer")

# Function to generate a prompt and corresponding parser for creating multiple-choice questions.
def mcq_prompt(options: int) -> tuple[str, JsonOutputParser]:
    """
    Generates a prompt for creating multiple-choice questions along with a JSON output parser.

    Args:
        options_count (int): The number of options for the multiple-choice question.

    Returns:
        tuple[str, JsonOutputParser]: A tuple containing the prompt and the JSON output parser.
    """
    prompt_text = f"Generate a multiple choice question with {options} options and indicate the correct answer."
    parser = JsonOutputParser(pydantic_object=MultipleChoiceQuestionParser)
    return (prompt_text, parser)

# Function to generate a prompt and corresponding parser for creating essay-type questions.
def essay_prompt() -> tuple[str, JsonOutputParser]:
    """
    Generates a prompt for creating question along with a JSON output parser.

    Returns:
        tuple[str, JsonOutputParser]: A tuple containing the prompt and the JSON output parser.
    """
    prompt_text = "Generate an question and all valid answers"
    parser = JsonOutputParser(pydantic_object=QuestionParser)
    return (prompt_text, parser)


def mcq_list(options:int) -> tuple[str, JsonOutputParser]:
    """
    Generates a prompt for creating multiple choice questions list with  options along with a JSON output parser.

    Returns:
        tuple[str, JsonOutputParser]: A tuple containing the prompt and the JSON output parser.
    """
    prompt_text = f"Generate a multiple choice questions list with {options} options and indicate the correct answer."
    parser = JsonOutputParser(pydantic_object=MultipleChoiceQuestionParser)
    return (prompt_text, parser)


def essay_list() -> tuple[str, JsonOutputParser]:
    """
    Generates a prompt for creating essay-type questions list along with a JSON output parser.

    Returns:
        tuple[str, JsonOutputParser]: A tuple containing the prompt and the JSON output parser.
    """
    prompt_text = "Generate a question list and all valid answers"
    parser = JsonOutputParser(pydantic_object=QuestionParser)
    return (prompt_text, parser)