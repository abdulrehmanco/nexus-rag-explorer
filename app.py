import streamlit as st
import requests

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Nexus RAG | AI Document Intelligence",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    .stApp {
        background-color: #0e1117;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        background-color: #ff4b4b;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True) # Fixed the parameter name here

# --- SESSION STATE ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "processed" not in st.session_state:
    st.session_state.processed = False

# --- SIDEBAR ---
with st.sidebar:
    st.title("Nexus RAG Engine")
    st.markdown("---")
    
    uploaded_file = st.file_uploader("Upload Technical PDF", type="pdf")
    
    if uploaded_file and not st.session_state.processed:
        if st.button("🚀 Initialize Indexing"):
            with st.status("Analyzing Document...") as status:
                files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
                try:
                    response = requests.post("http://127.0.0.1:8000/upload", files=files)
                    if response.status_code == 200:
                        st.session_state.processed = True
                        status.update(label="✅ Indexing Complete!", state="complete")
                    else:
                        st.error("Backend Error")
                except Exception as e:
                    st.error(f"Error: {e}")

    st.markdown("---")
    st.header("🛠️ Tech Stack")
    st.info("FastAPI • Llama 3.1 • ChromaDB • LangChain")
    
    if st.session_state.processed:
        if st.button("🗑️ Reset Session"):
            st.session_state.processed = False
            st.session_state.messages = []
            st.rerun()

# --- CHAT INTERFACE ---
st.title("🛡️ Citadel Intelligence Suite")
st.caption("Retrieval Augmented Generation for Complex Narratives")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask the archives..."):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    if not st.session_state.processed:
        st.warning("Please index a document first.")
    else:
        with st.chat_message("assistant"):
            with st.spinner("Searching..."):
                try:
                    res = requests.get(f"http://127.0.0.1:8000/ask?query={prompt}")
                    answer = res.json().get("answer", "No response found.")
                    st.markdown(answer)
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                except:
                    st.error("Backend unreachable.")