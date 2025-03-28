from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

# Default prompt for IT priorities
DEFAULT_PROMPT = """
Given the content of the uploaded PDF, identify the top 5 IT priorities for the company and suggest metrics to improve those priorities. Provide your answer in a clear, numbered list format.
"""

# Custom question prompt
CUSTOM_PROMPT_TEMPLATE = PromptTemplate(
    input_variables=["context", "question"],
    template="Based on the following context: {context}, answer the question: {question}"
)

def get_default_priorities(vector_store):
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vector_store.as_retriever(),
        return_source_documents=False
    )
    response = qa_chain.run(DEFAULT_PROMPT)
    return response

def answer_question(vector_store, question):
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vector_store.as_retriever(),
        chain_type_kwargs={"prompt": CUSTOM_PROMPT_TEMPLATE}
    )
    response = qa_chain.run(question)
    return response