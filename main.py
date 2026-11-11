import os
import shutil
import re
import logging
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from transformers import pipeline
from langchain_core.prompts import PromptTemplate

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# -------------------------
# Global objects (loaded once)
# -------------------------
embedding_model = None
qa_pipeline = None

def get_embedding_model():
    global embedding_model
    if embedding_model is None:
        embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    return embedding_model

def get_qa_pipeline():
    """Small local LLM for rewriting answers cleanly."""
    global qa_pipeline
    if qa_pipeline is None:
        # flan-t5-small is light (~80 MB) and works well offline
        qa_pipeline = pipeline(
            "text2text-generation",
            model="google/flan-t5-small",
            max_new_tokens=256,
            do_sample=False
        )
    return qa_pipeline

def clear_old_index():
    """Completely remove previous FAISS index so only the new PDF is used."""
    if os.path.exists("faiss_index"):
        shutil.rmtree("faiss_index")
        logging.info("Old FAISS index deleted.")

def pdf_loader(pdf_path: str):
    """
    Load a single PDF, clear any previous index, and create a fresh FAISS store
    that contains ONLY the current PDF.
    """
    logging.info(f"Loading PDF: {pdf_path}")
    try:
        # 1. Always start clean → no past PDFs
        clear_old_index()

        # 2. Load & split
        loader = PyPDFLoader(pdf_path)
        data = loader.load()
        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        chunks = splitter.split_documents(data)

        if not chunks:
            raise ValueError("No text could be extracted from the PDF.")

        # 3. Create brand-new index from only this PDF
        emb = get_embedding_model()
        faiss_store = FAISS.from_documents(chunks, emb)
        faiss_store.save_local("faiss_index")
        logging.info(f"Fresh FAISS index created with {len(chunks)} chunks from current PDF.")
        return True
    except Exception as e:
        logging.error(f"Error in pdf_loader: {e}")
        raise

def answer(query: str) -> str:
    logging.info(f"Answering query: {query}")
    try:
        if not os.path.exists("faiss_index"):
            return "No PDF has been uploaded yet. Please upload a PDF first."

        emb = get_embedding_model()
        faiss_store = FAISS.load_local(
            "faiss_index",
            emb,
            allow_dangerous_deserialization=True
        )

        # Get documents + similarity scores
        docs_and_scores = faiss_store.similarity_search_with_score(query, k=6)

        if not docs_and_scores:
            return "I could not find relevant information in the uploaded PDF."

        # Filter by relevance (lower score = more similar in FAISS L2)
        # You can adjust the threshold (0.8–1.2 is a good starting range for MiniLM)
        RELEVANCE_THRESHOLD = 1.05
        relevant_docs = [doc for doc, score in docs_and_scores if score < RELEVANCE_THRESHOLD]

        if not relevant_docs:
            return "This question does not appear to be related to the content of the uploaded PDF."

        context = "\n\n".join([doc.page_content for doc in relevant_docs])

        prompt = f"""Answer the question using ONLY the context below.
Write a clear, grammatical English answer. Do not invent information.
If the context does not contain the answer, say "The document does not contain information about this."

Context:
{context}

Question: {query}

Answer:"""

        pipe = get_qa_pipeline()
        result = pipe(prompt)[0]["generated_text"].strip()

        result = re.sub(r'\s+', ' ', result).strip()
        if not result.endswith(('.', '?', '!')):
            result += '.'
        return result

    except Exception as e:
        logging.error(f"Error in answer: {e}")
        return "An error occurred while generating the answer."