import streamlit as st
from src.prompt import get_prompt
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="مانا | Mana",
    page_icon="🩺",
    layout="centered"
)

st.title("🩺 مانا")
st.caption("مراقب آشنای سلامت شما | Your Trusted Health Companion")
st.divider()

@st.cache_resource
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

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if question := st.chat_input("سوال خود را بپرسید | Ask your question..."):
    
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.write(question)

    with st.chat_message("assistant"):
        with st.spinner("در حال جستجو در راهنماها..."):
            
            docs = retriever.invoke(question)
            context = "\n\n".join([doc.page_content for doc in docs])
            prompt = get_prompt(context, question)
            response = llm.invoke(prompt)
            answer = response.content
            
            st.write(answer)
            
            with st.expander("📚 منابع | Sources"):
                for i, doc in enumerate(docs):
                    st.caption(f"Chunk {i+1} — Page {doc.metadata['page']}")
                    st.write(doc.page_content)
                    st.divider()
            
            st.session_state.messages.append({"role": "assistant", "content": answer})