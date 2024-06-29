import os
import dotenv
import json
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_pinecone import PineconeVectorStore
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.output_parsers import JsonOutputParser
from langchain.prompts import PromptTemplate

from ..data.questionPrompts import mcq_prompt, essay_prompt

dotenv.load_dotenv()

class QuestionParser(BaseModel):
    question: str = Field(description="The question generated from the text.")
    answer: str = Field(description="The answer to the generated question.")

class MultipleChoiceQuestionParser(BaseModel):
    question: str = Field(description="The multiple choice question generated from the text.")
    options: list[str] = Field(description="The options for the multiple choice question.")
    answer: int = Field(description="The index of the correct answer in the options list.")

def format_docs(docs):
    """Helper function to format document content."""
    return "\n\n".join([d.page_content for d in docs])

def select_prompt(question_type: str,choices:str = 4) -> tuple[str, JsonOutputParser]:
    """Selects the appropriate prompt and parser based on the question type."""
    if question_type == "mcq":
        return mcq_prompt(choices)  # This function is assumed to return a tuple (prompt, parser)
    elif question_type == "essay":
        return essay_prompt()  # This function is assumed to return a tuple (prompt, parser)
    else:
        raise ValueError("Invalid question type. Please select 'mcq' or 'essay'.")

def prompt(text: str, examid: str, question_type: str = "mcq",choices:str = 4 ) -> dict:
    """Generates a question based on the provided text and exam ID."""
    question, parser = select_prompt(question_type, choices)

    embed = OpenAIEmbeddings(
        model="text-embedding-3-large",
        api_key=os.getenv('OPENAI_API_KEY'),
        dimensions=3072
    )

    vectorstore = PineconeVectorStore(
        namespace=examid,
        index_name=os.getenv('PINECONE_INDEX_NAME'),
        embedding=embed
    )

    docs = vectorstore.similarity_search(text)  # Assuming this method returns relevant documents

    llm = ChatOpenAI(
        model="gpt-4o",
        api_key=os.getenv('OPENAI_API_KEY'),
        model_kwargs={"response_format": {"type": "json_object"}}
        
    )

    prompt_template = PromptTemplate(
        template="Generate one question, {question} about {query} from {document}. Output is only json format.",
        input_variables=["query", "document", "question"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
        
    )

    chain = prompt_template | llm | parser

    formatted_docs = format_docs(docs)
    result = chain.invoke({"query": text, "document": formatted_docs, "question": question})

    return result
    return json.dumps(result)  # Converting the result to a JSON string for consistency

