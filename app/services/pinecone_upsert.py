from typing import  BinaryIO
import os
import dotenv
import pdfplumber
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone

dotenv.load_dotenv()

pinecone = Pinecone(api_key=os.getenv('PINECONE_API_KEY'))

def generate_embeddings_from_pdf(pdf_file: BinaryIO) -> str:
    """Generates embeddings from a PDF file using OpenAI's model."""

    print(pdf_file.filename)
    full_text = ""
    with pdfplumber.open(pdf_file.file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                full_text += page_text + "\n"

    if not full_text.strip():
        raise ValueError("No text found in the PDF.")

    return full_text

def upsert(pdf_file: BinaryIO, examid: str) -> str:
    """Upserts PDF text into a Pinecone vector store and returns the extracted text."""
    
    text = generate_embeddings_from_pdf(pdf_file)

    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-large",
        api_key=os.getenv('OPENAI_API_KEY'),
        dimensions=3072
    )

    PineconeVectorStore.from_texts(
        texts=[text],
        embedding=embeddings,
        namespace=examid,
        index_name="abc"
    )

    return text
