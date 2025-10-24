from pdf2image import convert_from_path
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from fastapi import UploadFile
import tempfile
import os
from PIL import Image
import pytesseract
from pdf2image import convert_from_path
from langchain_core.documents import Document
import hashlib

def get_chunk_hash(text: str) -> str:
    return hashlib.md5(text.encode()).hexdigest()

def extract_text_from_image(image: Image.Image) -> str:
    return pytesseract.image_to_string(image)

def tag_chunks(chunks, doc_id="doc_001"):
    tagged = []
    for chunk in chunks:
        metadata = chunk.metadata if hasattr(chunk, "metadata") else {}
        metadata["doc_id"] = doc_id
        tagged.append(Document(page_content=chunk.page_content, metadata=metadata))
    return tagged

VECTOR_DB_PATH = "vector_store"

async def process_document(file: UploadFile):
    with tempfile.NamedTemporaryFile(delete=False, suffix=file.filename) as tmp:
        contents = await file.read()
        tmp.write(contents)
        tmp_path = tmp.name

    loader = PyPDFLoader(tmp_path) if file.filename.endswith(".pdf") else TextLoader(tmp_path)
    documents = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(documents)
    tagged_chunks = tag_chunks(chunks, doc_id=file.filename)

    # OCR chunks (optional)
    ocr_chunks = []
    if file.filename.endswith(".pdf"):
        images = convert_from_path(tmp_path)
        for image in images:
            ocr_text = extract_text_from_image(image)
            if ocr_text.strip():
                ocr_chunks.append(Document(page_content=ocr_text, metadata={"doc_id": file.filename, "type": "ocr"}))

    all_chunks = tagged_chunks + ocr_chunks

    # Deduplicate
    existing_hashes = set()
    unique_chunks = []
    for chunk in all_chunks:
        chunk_hash = get_chunk_hash(chunk.page_content)
        if chunk_hash not in existing_hashes:
            existing_hashes.add(chunk_hash)
            unique_chunks.append(chunk)

    # Store in FAISS
    embeddings = OpenAIEmbeddings()
    db = FAISS.from_documents(unique_chunks, embeddings)
    db.save_local(VECTOR_DB_PATH)

    return [chunk.page_content for chunk in unique_chunks]