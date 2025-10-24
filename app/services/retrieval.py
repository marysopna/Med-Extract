from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

VECTOR_DB_PATH = "vector_store"

def retrieve_documents(query: str, k: int = 4):
    try:
        embeddings = OpenAIEmbeddings()
        db = FAISS.load_local(VECTOR_DB_PATH, embeddings, allow_dangerous_deserialization=True)
        results = db.similarity_search(query, k=k)

        formatted_docs = []
        for doc in results:
            metadata = doc.metadata if hasattr(doc, "metadata") else {}
            doc_type = metadata.get("type", "text").upper()

            if doc_type == "IMAGE":
                formatted_docs.append({
                    "type": "IMAGE",
                    "content": None,
                    "caption": metadata.get("caption", "No caption available")
                })
            else:
                formatted_docs.append({
                    "type": "TEXT",
                    "content": doc.page_content,
                    "caption": None
                })

        return formatted_docs

    except Exception as e:
        print(f"Error retrieving documents: {e}")
        return []
