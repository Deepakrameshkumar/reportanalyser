import PyPDF2
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS

def process_pdf(uploaded_file):
    # Extract text from PDF
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()

    # Split text into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = text_splitter.split_text(text)

    # Create embeddings and vector store
    embeddings = OpenAIEmbeddings(OPENAI_API_KEY="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")
    vector_store = FAISS.from_texts(chunks, embeddings)
    return vector_store