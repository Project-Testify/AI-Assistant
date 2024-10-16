import os
import dotenv
import json
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_pinecone import PineconeVectorStore
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.output_parsers import JsonOutputParser
from langchain.prompts import PromptTemplate

from ..data import gradePrompts
from ..core import log

## generate List
from pinecone.grpc import PineconeGRPC as Pinecone


dotenv.load_dotenv()


class Grader:
    def __init__(self, question: str, answer: str, valid_points: list[str]):
        self.question = question
        self.answer = answer
        self.valid_points = ",".join(valid_points)

        print(self.valid_points)

        log.logger.info("Grader initialized")
        self.llm = ChatOpenAI(
            model="gpt-4o",
            api_key=os.getenv('OPENAI_API_KEY'),
            model_kwargs={"response_format": {"type": "json_object"}}
        )

    def grade(self):
        prompt_text, parser = gradePrompts.grade_prompt(self.question, self.answer, self.valid_points)

        prompt_template = PromptTemplate(
            template="Grade the answer to the question: {question} with the answer: {answer} and valid points: {valid_points}. return the correct and incorrect points as a json object",
            input_variables=["question", "answer", "valid_points"],
            partial_variables={"format_instructions": parser.get_format_instructions()}

        )

        chain = prompt_template | self.llm | parser
        result = chain.invoke({"question": self.question, "answer": self.answer, "valid_points": self.valid_points})
        print("Grading the answer.")

        print(result)
        return result

        

# valid_points  is list of strings
def grade (question: str, answer: str, valid_points: list[str]):
    grader = Grader(question, answer, valid_points)
    return grader.grade()