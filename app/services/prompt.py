from typing import Any, BinaryIO
import os
import dotenv
import pdfplumber
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone, ServerlessSpec

from typing import Optional
from langchain_core.pydantic_v1 import BaseModel, Field


# from langchain.chat_models import ChatOpenAI
# from langchain_community.chat_models import ChatOpenAI
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA

from langchain_core.prompts import PromptTemplate

# json output parser

import json



# jsonoutputparser
from langchain_core.output_parsers import JsonOutputParser

LLMChain = ChatOpenAI()




dotenv.load_dotenv()

pinecone = Pinecone(api_key=os.getenv('PINECONE_API_KEY'))


class QuestionParser(BaseModel):
    question: str = Field(description="The question generated from the text.")
    answer: str= Field(description="The answer to the generated question.")

def format_docs(docs):
    return "\n\n".join([d.page_content for d in docs])


def prompt(text: str, examid: str) -> str:
    """Upserts PDF text into a Pinecone vector store and returns the extracted text."""
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

    parser = JsonOutputParser(pydantic_object=QuestionParser)

    prompt = PromptTemplate(
    template="Generate One Question, Question with answers about {query} from {document}.output is json",
    input_variables=["query", "document"],
    partial_variables={"format_instructions": parser.get_format_instructions()},
    )

    chain = prompt | llm  | parser

    print(text)

    result = chain.invoke({"query": text, "document": format_docs(doc)})

    print(result)

    return json.dumps(result)





    
    # print(qa.invoke(text))

    return "Question generated successfully."




    



    

