from typing import Any, BinaryIO
import os
import dotenv
import pdfplumber
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone, ServerlessSpec

from typing import Optional
from langchain_core.pydantic_v1 import BaseModel, Field

# JSONresponse
from fastapi.responses import JSONResponse


# from langchain.chat_models import ChatOpenAI
# from langchain_community.chat_models import ChatOpenAI
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA

from langchain_core.prompts import PromptTemplate

# json output parser

import json

from ..data.questionPrompts import mcq_prompt, essay_prompt

# jsonoutputparser
from langchain_core.output_parsers import JsonOutputParser

LLMChain = ChatOpenAI()




dotenv.load_dotenv()

pinecone = Pinecone(api_key=os.getenv('PINECONE_API_KEY'))


class QuestionParser(BaseModel):
    question: str = Field(description="The question generated from the text.")
    answer: str= Field(description="The answer to the generated question.")


class MultipleChoiceQuestionParser(BaseModel):
    question: str = Field(description="The multiple choice question generated from the text.")
    options: list[str] = Field(description="The options for the multiple choice question.")
    answer: int = Field(description="The index of the correct answer in the options list.")

def format_docs(docs):
    return "\n\n".join([d.page_content for d in docs])


def select_prompt(question_type: str) -> tuple[str, JsonOutputParser]:
    """Selects the appropriate prompt and parser based on the question type."""
    if question_type == "mcq":
        return mcq_prompt(4)
    elif question_type == "essay":
        return essay_prompt()
    else:
        raise ValueError("Invalid question type. Please select 'mcq' or 'essay'.")



def prompt(text: str, examid: str, question_type: str = "mcq") -> any:
    """Upserts PDF text into a Pinecone vector store and returns the extracted text."""




    question , parser = select_prompt(question_type)



    embed = OpenAIEmbeddings(
        model="text-embedding-3-large",
        api_key=os.getenv('OPENAI_API_KEY'),
        dimensions=3072
    )

    vectorstore = PineconeVectorStore(
        namespace=examid,
        index_name="abc",
        embedding=embed

    )

    doc = vectorstore.similarity_search(
        text,
        # top_k=5
    )

   

    # print(doc)

    llm = ChatOpenAI(
        model="gpt-3.5-turbo",
        api_key=os.getenv('OPENAI_API_KEY'),

    )



    

    # qa = RetrievalQA.from_chain_type(
    #     llm=llm,
    #     chain_type="stuff",
        
    #     retriever=vectorstore.as_retriever(),
        
        
    # )

    # parser = JsonOutputParser(pydantic_object=QuestionParser)
    # parser = JsonOutputParser(pydantic_object=MultipleChoiceQuestionParser)

    prompt = PromptTemplate(
    template="Generate One Question, {question} about {query} from {document}.output is json",
    input_variables=["query", "document", "question"],
    partial_variables={"format_instructions": parser.get_format_instructions()},
    )

    chain = prompt | llm  | parser

    print(text)

    result = chain.invoke({"query": text, "document": format_docs(doc), "question": question})

    print(result)
    print(type(json.dumps(result)))

    return result

    # return json.dumps(result)
    # dict_result = json.loads(result)
    # return dict_result


    # return result





    
    # print(qa.invoke(text))

    # return "Question generated successfully."




    



    

