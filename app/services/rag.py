from app.services.retrieval import retrieve_documents
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate

import os
from dotenv import load_dotenv

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

template = """
Use the following context to answer the question.
If you don't know the answer, say you don't know.

Context:
{context}

Question:
{question}
"""

prompt = PromptTemplate.from_template(template)

llm = ChatOpenAI(temperature=0)

async def answer_question(question: str) -> str:
    docs = retrieve_documents(question)

    # Format context by modality
    context_parts = []
    for doc in docs:
        doc_type = doc.get("type", "text").upper()
        content = doc.get("content", "")
        caption = doc.get("caption", "")
        if doc_type == "IMAGE" and caption:
            context_parts.append(f"[{doc_type}] Caption: {caption}")
        else:
            context_parts.append(f"[{doc_type}]\n{content}")

    context = "\n\n".join(context_parts)
    print(context, "context")

    chain = prompt | llm
    return chain.invoke({"context": context, "question": question})
