import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from src.prompt import get_prompt
from dotenv import load_dotenv
import gradio as gr

load_dotenv()

CHROMA_PATH = "data/chroma_db"

def build_vectorstore():
    print("Building vectorstore from PDF...")
    loader = PyPDFLoader("data/standards-of-care-2026.pdf")
    pages = loader.load()
    
    def is_useful_page(text):
        if text.count("doi:") > 3: return False
        if text.count("et al.") > 5: return False
        if len(text.strip()) < 200: return False
        return True
    
    filtered = [p for p in pages if is_useful_page(p.page_content)]
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = splitter.split_documents(filtered)
    
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=OpenAIEmbeddings(),
        persist_directory=CHROMA_PATH
    )
    print(f"Done! {len(chunks)} chunks stored.")
    return vectorstore

# Build or load vectorstore
if not os.path.exists(CHROMA_PATH):
    vectorstore = build_vectorstore()
else:
    vectorstore = Chroma(
        persist_directory=CHROMA_PATH,
        embedding_function=OpenAIEmbeddings()
    )

retriever = vectorstore.as_retriever(
    search_type="mmr",
    search_kwargs={"k": 6, "fetch_k": 20}
)
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

def chat(message, history):
    translation = llm.invoke(f"Translate to English, return ONLY translation: {message}")
    english = translation.content
    docs = retriever.invoke(english)
    context = "\n\n".join([doc.page_content for doc in docs])
    prompt = get_prompt(context, message)
    response = llm.invoke(prompt)
    return response.content

demo = gr.ChatInterface(
    fn=chat,
    title="🩺 مانا | Mana",
    description="مراقب آشنای سلامت شما | Your Trusted Health Companion",
    chatbot=gr.Chatbot(rtl=True),
    textbox=gr.Textbox(placeholder="سوال خود را بپرسید | Ask your question..."),
)

demo.launch()