import os

from dotenv import load_dotenv
from execute_llm import get_permissions, load_data
from llama_index.core import Settings, VectorStoreIndex
from llama_index.embeddings.google_genai import GoogleGenAIEmbedding
from llama_index.llms.google_genai import GoogleGenAI

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

Settings.llm = GoogleGenAI(model="gemini-2.5-flash")
Settings.embed_model = GoogleGenAIEmbedding()


def build_query_agent(role):
    docs = get_permissions(load_data(), role)
    index = VectorStoreIndex.from_documents(docs)
    return index.as_query_engine()
