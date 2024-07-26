import os
import dotenv
import json
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_pinecone import PineconeVectorStore
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.output_parsers import JsonOutputParser
from langchain.prompts import PromptTemplate

from ..data import questionPrompts, responseHandle
from ..core import log

dotenv.load_dotenv()

class QuestionParser(BaseModel):
    question: str = Field(description="The question generated from the text.")
    answer: str = Field(description="The answer to the generated question.")

class MultipleChoiceQuestionParser(BaseModel):
    question: str = Field(description="The multiple choice question generated from the text.")
    options: list[str] = Field(description="The options for the multiple choice question.")
    answer: int = Field(description="The index of the correct answer in the options list.")

class QuestionGenerator:
    def __init__(self, examid: str):
        self.examid = examid
        self.embed = OpenAIEmbeddings(
            model="text-embedding-3-large",
            api_key=os.getenv('OPENAI_API_KEY'),
            dimensions=3072
        )
        self.vectorstore = PineconeVectorStore(
            namespace=self.examid,
            index_name=os.getenv('PINECONE_INDEX_NAME'),
            embedding=self.embed
        )
        self.llm = ChatOpenAI(
            model="gpt-4o",
            api_key=os.getenv('OPENAI_API_KEY'),
            model_kwargs={"response_format": {"type": "json_object"}}
        )

    def format_docs(self, docs):
        """Helper function to format document content."""
        return "\n\n".join([d.page_content for d in docs])

    def select_prompt(self, question_type: str, choices: int = 4):
        """Selects the appropriate prompt and parser based on the question type."""
        if question_type == "mcq":
            return questionPrompts.mcq_prompt(choices)  # This function returns a tuple (prompt, parser)
        elif question_type == "essay":
            return questionPrompts.essay_prompt()  # This function returns a tuple (prompt, parser)
        else:
            log.logger.error("Invalid question type selected.")
            raise ValueError("Invalid question type. Please select 'mcq' or 'essay'.")

    def generate(self, text: str, question_type: str = "mcq", choices: int = 4):
        log.logger.info(f"Generating a question for text: {text}")
        question, parser = self.select_prompt(question_type, choices)

        docs = self.vectorstore.similarity_search(text)  # Assuming this method returns relevant documents
        formatted_docs = self.format_docs(docs)

        prompt_template = PromptTemplate(
            template="Generate one question, {question} about {query} from {document}. Output is only json format.",
            input_variables=["query", "document", "question"],
            partial_variables={"format_instructions": parser.get_format_instructions()}
        )

        chain = prompt_template | self.llm | parser
        result = chain.invoke({"query": text, "document": formatted_docs, "question": question})
        log.logger.info(f"Generated question: {result['question']}")

        if question_type == "mcq":
            return responseHandle.handle_mcq(result)
        return result


def generate(text: str, examid: str, question_type: str = "mcq", choices: int = 4):
    generator = QuestionGenerator(examid)
    return generator.generate(text, question_type, choices)