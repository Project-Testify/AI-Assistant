from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.output_parsers import JsonOutputParser

# Define a Pydantic model for a standard question and answer format.
class QuestionParser(BaseModel):
    question: str = Field(description="The question generated from the text.")
    answer: str = Field(description="The answer to the generated question.")

# Define a Pydantic model for multiple-choice questions.
class Answer(BaseModel):
    char: str = Field(description="The character representing the answer. (e.g. 'A', 'B', 'C', 'D')")
    text: str = Field(description="The text of the answer.")


class MultipleChoiceQuestionParser(BaseModel):
    question: str = Field(description="The multiple choice question generated from the text.")
    options: list[Answer] = Field(description="The options for the multiple choice question. Should be a list of Answer objects. Answer objects should have a 'char' field and a 'text' field.")
    answer: str = Field(description="The character representing the correct answer.(e.g. 'A', 'B', 'C', 'D'")

# Function to generate a prompt and corresponding parser for creating multiple-choice questions.
def mcq_prompt(options: int) -> tuple[str, JsonOutputParser]:
    q = f"Generate a multiple choice question with {options} options and a correct answer."
    parser = JsonOutputParser(pydantic_object=MultipleChoiceQuestionParser)
    return (q, parser)

# Function to generate a prompt and corresponding parser for creating essay-type questions.
def essay_prompt() -> tuple[str, JsonOutputParser]:
    q = "Generate an essay question."
    parser = JsonOutputParser(pydantic_object=QuestionParser)
    return (q, parser)
