__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

import os
import shutil
from fastapi import FastAPI, UploadFile, File, HTTPException
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

load_dotenv()
app = FastAPI()

persist_directory = "./chroma_db"

# --- HELPER FUNCTION TO GET MODELS ---
def get_models():
    """This function ensures models are always available without NameErrors."""
    embeds = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    model = ChatGroq(
        model_name="llama-3.1-8b-instant", 
        groq_api_key=os.getenv("GROQ_API_KEY"),
        temperature=0.3
    )
    return embeds, model

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    try:
        # Get models locally to avoid scope issues
        embeddings_local, _ = get_models()
        
        temp_path = f"temp_{file.filename}"
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        loader = PyPDFLoader(temp_path)
        documents = loader.load()
        
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        chunks = text_splitter.split_documents(documents)
        
        if os.path.exists(persist_directory):
            shutil.rmtree(persist_directory)
            
        Chroma.from_documents(chunks, embeddings_local, persist_directory=persist_directory)
        os.remove(temp_path)
        return {"message": "Knowledge Base Built"}
    except Exception as e:
        print(f"Upload Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/ask")
async def ask_question(query: str):
    # --- THE FIX: Define them directly inside the endpoint ---
    # This prevents the "NameError" because 'llm_internal' is defined right here.
    embeddings_internal, llm_internal = get_models()
    
    if not os.path.exists(persist_directory):
        return {"answer": "No documents found. Please upload a PDF first."}

    vector_db = Chroma(persist_directory=persist_directory, embedding_function=embeddings_internal)
    retriever = vector_db.as_retriever(search_kwargs={"k": 3})

    template = """You are a wise Sage. Use the context to answer:
    Context: {context}
    Question: {question}
    Answer:"""
    
    prompt = ChatPromptTemplate.from_template(template)

    # We use 'llm_internal' which was JUST defined 10 lines above
    rag_chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm_internal
        | StrOutputParser()
    )
    
    try:
        response = rag_chain.invoke(query)
        return {"answer": response}
    except Exception as e:
        return {"answer": f"The archives are blocked. Error: {str(e)}"}