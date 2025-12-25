# embed_docs.py
import os
from pipeline import embed_documents

DOCS_FOLDER = "/Users/nicolabuttigieg/PycharmProjects/financial-qa/docs"

docs = []
for file in os.listdir(DOCS_FOLDER):
    file_path = os.path.join(DOCS_FOLDER, file)
    if os.path.isfile(file_path) and file.endswith(".txt"):
        with open(file_path, "r", encoding="utf-8") as f:
            docs.append(f.read())

if not docs:
    print("No documents found in DOCS_FOLDER.")
else:
    embed_documents(docs)
    print(f"Vectorstore created with {len(docs)} documents.")
