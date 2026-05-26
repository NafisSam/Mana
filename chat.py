import gradio as gr
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from src.prompt import get_prompt
from dotenv import load_dotenv

load_dotenv()

# Load vectorstore
def load_vectorstore():
    return Chroma(
        persist_directory="data/chroma_db",
        embedding_function=OpenAIEmbeddings()
    )

vectorstore = load_vectorstore()
retriever = vectorstore.as_retriever(
    search_type="mmr",
    search_kwargs={"k": 6, "fetch_k": 20}
)
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

def chat(message, history):
    # Translate question to English for better retrieval
    translation_response = llm.invoke(
        f"Translate this to English, return ONLY the translation, nothing else: {message}"
    )
    english_question = translation_response.content
    print(f"Translated: {english_question}")
    
    # Search with English question
    docs = retriever.invoke(english_question)
    context = "\n\n".join([doc.page_content for doc in docs])
    
    # Print chunks
    print("\n--- CHUNKS ---")
    for i, doc in enumerate(docs):
        print(f"Chunk {i+1} page {doc.metadata['page']}: {doc.page_content[:100]}")
    print("--- END ---\n")
    
    # Answer in original language
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