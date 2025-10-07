from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

load_dotenv()

llm = ChatGroq(
    model="mixtral-8x7b",
    api_key=os.getenv("GROQ_API_KEYS")
)