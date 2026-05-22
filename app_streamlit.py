import streamlit as st
import main
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Page configuration
st.set_page_config(
    page_title="PDF QA System",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-title {
        color: #FF6B6B;
        text-align: center;
        font-size: 2.5em;
        margin-bottom: 10px;
    }
    .subtitle {
        text-align: center;
        color: #666;
        margin-bottom: 30px;
    }
    .upload-section {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    .qa-section {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #e0e0e0;
    }
    </style>
    """, unsafe_allow_html=True)

# Title
st.markdown("<h1 class='main-title'>📄 PDF Question Answering System</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Ask questions directly from your PDF documents - No LLM needed!</p>", unsafe_allow_html=True)

# Sidebar
st.sidebar.title("ℹ️ About")
st.sidebar.info("""
    This is a lightweight, offline Question Answering system that answers user queries 
    directly from PDF content without using any LLM or AI model for generation.
    
    **Features:**
    - 📤 Upload PDF files
    - 🔍 Fast semantic search
    - ⚡ Offline processing
    - 🔒 Complete privacy
    - 💬 Question answering
""")

# Create two columns
col1, col2 = st.columns([1, 2])

# ================= LEFT COLUMN (PDF Upload Section) ======================
with col1:
    st.markdown("<div class='upload-section'>", unsafe_allow_html=True)
    st.subheader("📤 Upload PDF")
    
    # File uploader
    uploaded_file = st.file_uploader("Select a PDF file", type="pdf")
    
    if uploaded_file is not None:
        # Save uploaded file temporarily
        with open("temp_upload.pdf", "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # Display file info
        st.success(f"✅ File uploaded: {uploaded_file.name}")
        st.info(f"File size: {uploaded_file.size / 1024:.2f} KB")
        
        # Process PDF
        try:
            with st.spinner("🔄 Processing PDF... Please wait..."):
                main.pdf_loader("temp_upload.pdf")
            st.success("✅ PDF processed successfully!")
            st.session_state.pdf_loaded = True
        except Exception as e:
            st.error(f"❌ Error processing PDF: {str(e)}")
            logging.error(f"Error uploading PDF: {e}")
            st.session_state.pdf_loaded = False
    else:
        st.warning("📌 Please upload a PDF file to get started")
        st.session_state.pdf_loaded = False
    
    st.markdown("</div>", unsafe_allow_html=True)

# ================= RIGHT COLUMN (Question + Answer Section) ======================
with col2:
    st.markdown("<div class='qa-section'>", unsafe_allow_html=True)
    st.subheader("❓ Ask a Question")
    
    # Initialize session state for question history
    if "question_history" not in st.session_state:
        st.session_state.question_history = []
    
    if "pdf_loaded" not in st.session_state:
        st.session_state.pdf_loaded = False
    
    # Question input
    question = st.text_area(
        "Enter your question about the PDF:",
        placeholder="Type your question here...",
        height=100,
        disabled=not st.session_state.pdf_loaded
    )
    
    # Ask button
    col_ask, col_clear = st.columns([3, 1])
    
    with col_ask:
        ask_button = st.button(
            "🔍 Ask Question",
            use_container_width=True,
            disabled=not st.session_state.pdf_loaded or not question.strip()
        )
    
    with col_clear:
        if st.button("🗑️ Clear", use_container_width=True):
            st.session_state.question_history = []
            st.rerun()
    
    # Process question
    if ask_button:
        if not st.session_state.pdf_loaded:
            st.error("❌ Please upload and process a PDF first!")
        elif not question.strip():
            st.error("❌ Please enter a question!")
        else:
            try:
                with st.spinner("⏳ Finding answer... Please wait..."):
                    answer = main.answer(question)
                
                # Store in history
                st.session_state.question_history.append({
                    "question": question,
                    "answer": answer
                })
                
                st.success("✅ Answer found!")
                
                # Display answer
                st.subheader("💬 Answer:")
                st.info(answer)
                
                logging.info(f"Answer provided: {answer}")
            except Exception as e:
                st.error(f"❌ Error generating answer: {str(e)}")
                logging.error(f"Error updating UI: {e}")
    
    st.markdown("</div>", unsafe_allow_html=True)

# ================= QUESTION HISTORY ======================
if st.session_state.question_history:
    st.markdown("---")
    st.subheader("📜 Question History")
    
    for idx, item in enumerate(st.session_state.question_history, 1):
        with st.expander(f"Question {idx}: {item['question'][:50]}..."):
            st.write(f"**Q:** {item['question']}")
            st.write(f"**A:** {item['answer']}")

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #999; margin-top: 20px;'>
        <p>Made with ❤️ | PDF QA System v1.0 | Lightweight & Offline</p>
    </div>
    """, unsafe_allow_html=True)
