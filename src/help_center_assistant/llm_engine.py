import os

from dotenv import load_dotenv
from execute_llm import ALLOWED, BASE_DIR, get_permissions, load_data
from llama_index.core import (
    Settings,
    StorageContext,
    VectorStoreIndex,
    load_index_from_storage,
)
from llama_index.embeddings.google_genai import GoogleGenAIEmbedding
from llama_index.llms.google_genai import GoogleGenAI

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

Settings.llm = GoogleGenAI(model="gemini-2.5-flash")
Settings.embed_model = GoogleGenAIEmbedding()


def build_query_engine(role):

    persist_dir = BASE_DIR / "storage" / role

    if persist_dir.exists():
        storage_context = StorageContext.from_defaults(persist_dir=str(persist_dir))
        index = load_index_from_storage(storage_context)
    else:
        docs = get_permissions(load_data(), role)
        index = VectorStoreIndex.from_documents(docs)
        index.storage_context.persist(persist_dir=str(persist_dir))
    return index.as_query_engine()


def chat():
    role = ""
    while role not in ALLOWED:
        role = input("Role (Customer/Staff): ").strip().lower()
    engine = build_query_engine(role)

    while True:
        question = input("Ask question\n type quit to exit: ").strip()
        if question.lower() in ("quit", "exit"):
            break
        response = engine.query(question)
        print("Response: ", response)
        print("Sources: ", [n.metadata["file_name"] for n in response.source_nodes])


if __name__ == "__main__":
    chat()
