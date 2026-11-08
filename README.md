# Help Center Assistant

A command-line help-centre chatbot built with LlamaIndex and Google Gemini. It answers questions from Markdown files and enforces role-based access: customers only see customer-facing content, while staff see everything.

## How it works

1. Loads every `.md` file under `help/` and `staff/` with `SimpleDirectoryReader`.
2. Tags each document with an `access_level`: `help/` is `user`, `staff/` is `staff`.
3. Hides the tag from embeddings and LLM prompts, so it is used only for filtering.
4. Builds a separate vector index per role from only the documents that role may see:
   - `customer` sees `user` documents only.
   - `staff` sees `user` and `staff` documents.
5. Answers each question with Gemini using only the retrieved chunks. If the answer isn't in the documents, it replies: "Sorry, I don't have information on that."
6. Saves each role's index to `storage/` so documents are not re-embedded on every run.

## Project structure

```
help-center-assistant/
├── src/
│   └── help_center_assistant/
│       ├── llm_engine.py
│       ├── help/        # customer-facing .md files
│       └── staff/       # staff-only .md files
├── storage/             # saved indexes (auto-created)
└── README.md
```

## Setup

1. Create and activate a virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
2. Install dependencies:
   ```bash
   python -m pip install llama-index llama-index-llms-google-genai llama-index-embeddings-google-genai
   ```
3. Set your Gemini API key (never put it in code or commit it):
   ```bash
   export GOOGLE_API_KEY="your-key-here"
   ```

## Run

```bash
python src/help_center_assistant/llm_engine.py
```

Choose a role (`customer` or `staff`), then ask questions. Type `quit` to exit. Each answer lists its source files and their access levels.

## Notes

- The first run for each role is slow because it embeds the documents and saves the index. Later runs load the saved index.
- If you add, edit, or delete any `.md` file, delete the `storage/` folder so the indexes rebuild.
- Add `storage/` and `.venv/` to `.gitignore`.

## Testing the permissions

Ask both roles a question that only a file in `staff/` can answer. The customer should get "Sorry, I don't have information on that," and staff should get the real answer. The printed sources show which files were used.