import os
import dotenv
import json

from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_pinecone import PineconeVectorStore
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.output_parsers import JsonOutputParser
from langchain.prompts import PromptTemplate


from ..data.questionPrompts import mcq_prompt, essay_prompt
from ..data.responseHandle import handle_mcq

from ..core.log import logger

dotenv.load_dotenv()



