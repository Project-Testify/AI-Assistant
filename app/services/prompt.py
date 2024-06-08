from typing import Any, BinaryIO
import os
import dotenv
import pdfplumber
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone, ServerlessSpec

from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA



dotenv.load_dotenv()

pinecone = Pinecone(api_key=os.getenv('PINECONE_API_KEY'))




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

    vectorstore.similarity_search(
        text,
        # top_k=5
    )

    llm = ChatOpenAI(
        model="gpt-3.5-turbo",
        api_key=os.getenv('OPENAI_API_KEY')
    )

    qa = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vectorstore.as_retriever()
    )

    print(qa.invoke(text))
    return "Question generated successfully."




    



    

