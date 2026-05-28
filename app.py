from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from src.prompt import get_prompt
from dotenv import load_dotenv
import gradio as gr

load_dotenv()

# Always load — never rebuild
vectorstore = Chroma(
    persist_directory="data/chroma_db",
    embedding_function=OpenAIEmbeddings()
)

retriever = vectorstore.as_retriever(
    search_type="mmr",
    search_kwargs={"k": 6, "fetch_k": 20}
)
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

def chat(message, history):
    # Combine translation and answering in ONE API call
    docs = retriever.invoke(message)
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

demo.launch(auth=("mana", "test1234"))