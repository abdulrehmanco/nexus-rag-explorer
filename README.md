# Nexus RAG | Citadel Intelligence Suite

**Retrieval-Augmented Generation for Intelligent Document Analysis**

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-Latest-red.svg)](https://streamlit.io)

---

## 📋 Overview

**Nexus RAG** is an intelligent document analysis platform that leverages Retrieval-Augmented Generation (RAG) to enable AI-powered Q&A over uploaded PDF documents. Upload any technical PDF, and the system will intelligently retrieve relevant content and generate accurate answers to your questions.

### Key Features

- 🤖 **AI-Powered Q&A** - Ask questions about your documents using advanced LLM (Llama 3.1)
- 📄 **PDF Document Processing** - Automatically parse and chunk PDF files for optimal retrieval
- 🔍 **Vector Search** - Fast semantic search using HuggingFace embeddings and ChromaDB
- 💬 **Interactive Chat Interface** - User-friendly Streamlit frontend
- ⚡ **FastAPI Backend** - High-performance REST API for document processing and querying
- 📦 **Persistent Storage** - Vector database stores embeddings for quick retrieval

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────┐
│   Streamlit Frontend (app.py)           │
│   "Citadel Intelligence Suite"          │
└──────────────┬──────────────────────────┘
               │ HTTP Requests
               ▼
┌─────────────────────────────────────────┐
│   FastAPI Backend (main.py)             │
│   - /upload  (POST)                     │
│   - /ask     (GET)                      │
└──────────────┬──────────────────────────┘
               │
      ┌────────┴────────┐
      ▼                 ▼
  ┌────────┐      ┌──────────┐
  │ChromaDB│      │LangChain │
  │Vector  │      │RAG Chain │
  │Storage │      │          │
  └────────┘      └──────────┘
```

### Tech Stack

- **Frontend**: [Streamlit](https://streamlit.io) - Modern web framework for data apps
- **Backend**: [FastAPI](https://fastapi.tiangolo.com) - High-performance Python web API
- **LLM**: [Groq API](https://groq.com) with **Llama 3.1 8B Instant**
- **Embeddings**: [HuggingFace](https://huggingface.co) - `all-MiniLM-L6-v2` model
- **PDF Processing**: [LangChain](https://www.langchain.com) with PyPDF
- **Vector Database**: [ChromaDB](https://www.trychroma.com) - Vector embeddings storage
- **Environment**: Python-dotenv for API key management

---

## 📦 Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/linkedin-rag-project.git
cd linkedin-rag-project
```

### Step 2: Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

**Common dependencies include:**
```
fastapi
uvicorn
streamlit
requests
langchain
langchain-groq
langchain-huggingface
langchain-community
chromadb
pysqlite3
pypdf
python-dotenv
```

### Step 4: Configure Environment Variables

Create a `.env` file in the project root:

```bash
cp .env.example .env  # If available, or create manually
```

Add your API keys:

```env
GROQ_API_KEY=your_groq_api_key_here
```

**Getting a Groq API Key:**
1. Visit [https://console.groq.com](https://console.groq.com)
2. Sign up or log in
3. Create an API key in your dashboard
4. Add it to your `.env` file

---

## 🚀 Running the Project

### Option 1: Run Both Services (Recommended)

**Terminal 1 - Start FastAPI Backend:**
```bash
uvicorn main:app --reload --port 8000
```

You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete
```

**Terminal 2 - Start Streamlit Frontend:**
```bash
streamlit run app.py
```

You should see:
```
Local URL: http://localhost:8501
Network URL: http://192.168.x.x:8501
```

Open your browser to `http://localhost:8501` and start using the app!

### Option 2: Run with Docker (Optional)

> Add docker setup for production deployment

---

## 💡 How to Use

### 1. **Upload a PDF Document**
   - Click the file uploader in the sidebar
   - Select a technical PDF file
   - Click **"🚀 Initialize Indexing"**
   - Wait for the status to show "✅ Indexing Complete!"

### 2. **Ask Questions**
   - Once indexing is complete, type your question in the chat input
   - Examples:
     - *"What are the main topics covered in this document?"*
     - *"Explain the key concepts mentioned in Chapter 3"*
     - *"Summarize the findings"*
   - The AI will search the document and provide an answer

### 3. **Reset Session**
   - Click the **"🗑️ Reset Session"** button to clear chat history and start fresh

---

## 📚 API Endpoints

### 1. `POST /upload`
Uploads and processes a PDF file for indexing.

**Request:**
```bash
curl -X POST "http://localhost:8000/upload" \
  -F "file=@document.pdf"
```

**Response:**
```json
{
  "message": "Knowledge Base Built"
}
```

**What it does:**
- Loads the PDF using PyPDFLoader
- Splits text into chunks (1000 chars with 200 char overlap)
- Generates embeddings using HuggingFace
- Stores embeddings in ChromaDB
- Clears previous knowledge base

---

### 2. `GET /ask`
Queries the indexed documents using RAG.

**Request:**
```bash
curl "http://localhost:8000/ask?query=What%20is%20the%20main%20topic?"
```

**Response:**
```json
{
  "answer": "The document primarily covers... [AI-generated answer based on document context]"
}
```

**What it does:**
- Retrieves top 3 relevant document chunks using similarity search
- Creates a RAG chain with the LLM
- Generates an answer based on the context
- Returns the AI-generated response

---

## 🗂️ Project Structure

```
linkedin-rag-project/
├── main.py                 # FastAPI backend application
├── app.py                  # Streamlit frontend application
├── .env                    # API keys (not in git)
├── .env.example            # Template for environment variables
├── chroma_db/              # ChromaDB vector storage (auto-created)
│   ├── chroma.sqlite3
│   └── [embeddings]
├── venv/                   # Python virtual environment
└── README.md               # This file
```

---

## 🔧 Configuration

### Modify Model Settings

Edit `main.py` to change:

**Temperature (Creativity vs Accuracy):**
```python
model = ChatGroq(
    model_name="llama-3.1-8b-instant",
    groq_api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.3  # Lower = more deterministic, Higher = more creative
)
```

**Chunk Size and Overlap:**
```python
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,        # Size of each text chunk
    chunk_overlap=200       # Overlap between chunks (helps context)
)
```

**Retrieval Count:**
```python
retriever = vector_db.as_retriever(search_kwargs={"k": 3})  # Returns top 3 chunks
```

---

## 🐛 Troubleshooting

### Issue: "Backend unreachable"
**Solution:** Ensure FastAPI is running on port 8000
```bash
uvicorn main:app --reload --port 8000
```

### Issue: "No documents found"
**Solution:** Upload and index a PDF first using the frontend

### Issue: "GROQ_API_KEY not found"
**Solution:** 
1. Create `.env` file in project root
2. Add: `GROQ_API_KEY=your_key_here`
3. Install python-dotenv: `pip install python-dotenv`

### Issue: SQLite compatibility error
**Solution:** This project uses pysqlite3 for compatibility. Already configured in `main.py`

---

## 📊 Example Workflow

```
User uploads "AI_Trends_2024.pdf"
         ↓
FastAPI processes file:
  • Extracts text from PDF
  • Splits into 1000-char chunks
  • Creates embeddings (1536-dim vectors)
  • Stores in ChromaDB
         ↓
User asks: "What are the latest AI trends?"
         ↓
System performs:
  • Embeds the query
  • Searches for 3 most similar chunks
  • Sends chunks + query to Llama 3.1
  • LLM generates answer based on context
         ↓
User receives: "Based on the document, the latest trends are..."
```

---

## 🚀 Future Enhancements

- [ ] Support for multiple file formats (DOCX, TXT, MD)
- [ ] Batch document processing
- [ ] Memory/conversation history
- [ ] Document management UI (delete, re-index)
- [ ] Different embedding models
- [ ] Custom prompts and system messages
- [ ] Rate limiting and authentication
- [ ] Deploy to cloud (AWS, GCP, Azure)

---

## 📝 License

This project is open source and available under the MIT License.

---

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests

---

## 📧 Contact

For questions or suggestions, reach out via LinkedIn or open an issue on GitHub.

---

## 🙏 Acknowledgments

- [LangChain](https://www.langchain.com) - RAG framework
- [Groq](https://groq.com) - Fast LLM inference
- [ChromaDB](https://www.trychroma.com) - Vector database
- [FastAPI](https://fastapi.tiangolo.com) - Modern Python web framework
- [Streamlit](https://streamlit.io) - Rapid app development

---

**Happy Querying! 🚀**
