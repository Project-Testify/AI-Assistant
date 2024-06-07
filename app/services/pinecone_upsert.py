from langchain_openai import OpenAIEmbeddings
from pinecone import Pinecone, ServerlessSpec


from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA  
import time
from langchain_pinecone import PineconeVectorStore
import pdfplumber

import os
import dotenv
dotenv.load_dotenv()



pinecone = Pinecone(api_key=os.getenv('PINECONE_API_KEY'))


# create embeddings from pdf

def generate_embeddings_from_pdf(pdf_file):
    # Initialize the OpenAIEmbeddings class

    print(pdf_file.filename)
    # Extract text from the PDF,
    full_text = ""
    with pdfplumber.open(pdf_file.file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                full_text += page_text + "\n"

   
    # Check if any text was extracted
    if not full_text.strip():
        raise ValueError("No text found in the PDF.")
    # Generate embeddings from the text
    # embeddings = openai.run(full_text)

    return full_text
    







def upsert(pdf_file,examid):
    # Initialize the Pinecone service


    # Generate embeddings from the PDF
    text = generate_embeddings_from_pdf(pdf_file)

    embeddings = OpenAIEmbeddings(model="text-embedding-3-large" , api_key=os.getenv('OPENAI_API_KEY'), dimensions=3072)

    doc = PineconeVectorStore.from_texts(
        texts=[text],
        embedding=embeddings,
        namespace=examid,
        index_name="abc",
        

    
    )


    return text









    # create 

