import streamlit as st
from utils.pdf_processor import process_pdf
from utils.llm_chain import get_default_priorities, answer_question
from utils.chat_history import load_chat_history, save_chat_history
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Streamlit app configuration
st.set_page_config(page_title="PDF IT Priorities Chatbot", layout="wide")
st.title("PDF IT Priorities Chatbot")
st.write("Upload a PDF to analyze IT priorities and chat with the content.")

# Sidebar for file upload
with st.sidebar:
    uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])
    if uploaded_file:
        st.success("File uploaded successfully!")

# Main content area
if uploaded_file:
    # Process the PDF and create vector store
    if "vector_store" not in st.session_state:
        with st.spinner("Processing PDF..."):
            st.session_state.vector_store = process_pdf(uploaded_file)
            st.session_state.chat_history = load_chat_history()

    # Display default IT priorities and metrics
    st.subheader("Top 5 IT Priorities and Metrics")
    if "priorities" not in st.session_state:
        with st.spinner("Analyzing IT priorities..."):
            priorities = get_default_priorities(st.session_state.vector_store)
            st.session_state.priorities = priorities
    st.write(st.session_state.priorities)

    # Chat interface
    st.subheader("Ask Questions About the PDF")
    user_input = st.text_input("Your question:", key="question_input")
    if st.button("Send"):
        if user_input:
            with st.spinner("Generating response..."):
                response = answer_question(st.session_state.vector_store, user_input)
                st.session_state.chat_history.append({"user": user_input, "bot": response})
                save_chat_history(st.session_state.chat_history)
    
    # Display chat history
    for chat in st.session_state.chat_history:
        st.write(f"**You:** {chat['user']}")
        st.write(f"**Bot:** {chat['bot']}")
else:
    st.info("Please upload a PDF to begin.")