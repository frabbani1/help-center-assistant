from pathlib import Path

from llama_index.core import SimpleDirectoryReader

BASE_DIR = Path(__file__).parent

FOLDER_TO_LEVEL = {"help": "user", "staff": "staff"}


def load_data():
    """Runs once per file, Returns metadata attached to it"""
    documents = []

    for folder, level in FOLDER_TO_LEVEL.items():
        docs = SimpleDirectoryReader(
            input_dir=str(BASE_DIR / folder), recursive=True, required_exts=".md"
        ).load_data()

        for doc in docs:
            doc.metadata["access_level"] = level
            doc.excluded_embed_metadata_keys = ["access_level"]
            doc.excluded_llm_metadata_keys = ["access_level"]

        documents.extend(docs)

    return documents


ALLOWED = {"staff": ["staff", "user"], "customer": ["user"]}


def get_permissions(documents, role):
    return [d for d in documents if d.metadata["access_level"] in ALLOWED[role]]

