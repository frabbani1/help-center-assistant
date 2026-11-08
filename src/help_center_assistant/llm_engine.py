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


def build_query_engine(role):
    docs = get_permissions(load_data(), role)
    index = VectorStoreIndex.from_documents(docs)
    return index.as_query_engine()

if __name__ == "__main__":
    question = "do refunds need manager approval"

    for role in ["customer","staff"]:
        engine = build_query_engine(role)
        response = engine.query(question)
        print("*"*10, role.upper(),"*"*10)
        print(response)
        print("Sources: ", [n.metadata["file_name"] for n in response.source_nodes])


    