from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

# Load existing database
vectorstore = Chroma(
    persist_directory="data/chroma_db",
    embedding_function=OpenAIEmbeddings()
)

# Create retriever
retriever = vectorstore.as_retriever(
    search_type="mmr",
    search_kwargs={"k": 6, "fetch_k": 20}
)
# Create LLM
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# Ask a question
question = "What is the recommended HbA1c target for diabetic patients?"
# Get relevant chunks from PDF
docs = retriever.invoke(question)
print("\n--- CHUNKS RETRIEVED FROM PDF ---")
for i, doc in enumerate(docs):
    print(f"\nChunk {i+1} (page {doc.metadata['page']}):")
    print(doc.page_content)
print("--- END OF CHUNKS ---\n")
context = "\n\n".join([doc.page_content for doc in docs])

# Build prompt manually
from src.prompt import get_prompt

prompt = get_prompt(context, question)

# Get answer
response = llm.invoke(prompt)
print(f"Question: {question}\n")
print(f"Answer: {response.content}")