import re
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from transformers import pipeline
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def pdf_loader(pdf):
    logging.info(f"Loading PDF: {pdf}")
    try:
        loader=PyPDFLoader(pdf)
        data=loader.load()
        splitter = RecursiveCharacterTextSplitter(chunk_size=1200,chunk_overlap=250)
        chunks=splitter.split_documents(data)
        embedding_model= HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        faiss_store = FAISS.from_documents(chunks,embedding_model)
        faiss_store.save_local("faiss_index")
        logging.info("FAISS index saved locally.")
    except Exception as e:
        logging.error(f"Error in pdf_loader: {e}")
    
    
def answer(query):
    logging.info(f"Answering query: {query}")
    try:
        embedding_model= HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        faiss_store=FAISS.load_local("faiss_index",embedding_model,allow_dangerous_deserialization=True)
        retriever= faiss_store.similarity_search(query,k=5)
        context = "\n".join([doc.page_content for doc in retriever])
        sen = re.split(r'(?<=[.!?])\s+',context)
        key=query.lower().split()
        scored=[]
        for s in sen:
            score= sum(1 for k in key if k in s.lower())
            if score>0:
                scored.append((score,s.strip()))
        scored = sorted(scored,key=lambda x:x[0],reverse=True)
        best= [s for _,s in scored[:7]]
        # Remove duplicates and strip
        cl = []
        for s in best:
            if s not in cl:
                cl.append(s.strip())
        # Join sentences with spaces
        final = " ".join(cl)
        # --- GRAMMAR + FORMATTING FIXES ---
        # 1. Normalize spacing
        final = re.sub(r'\s+', ' ', final).strip()
        # 2. Ensure sentence ends with proper punctuation
        if not final.endswith(('.', '?', '!')):
            final += '.'
        # 3. Capitalize each sentence
        def capitalize_sentences(text):
            sentences = re.split(r'(?<=[.!?])\s+', text)
            sentences = [s.strip().capitalize() for s in sentences if s.strip()]
            return " ".join(sentences)
        answer = capitalize_sentences(final)
        logging.info(f"Answer generated: {answer}")
        return answer
    except Exception as e:
        logging.error(f"Error in answer function: {e}")
        return "An error occurred while generating the answer."

