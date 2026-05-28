import os
import shutil
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

CHROMA_PATH = "data/chroma_db"
DATA_PATH = "data/"

# Delete old database
if os.path.exists(CHROMA_PATH):
    shutil.rmtree(CHROMA_PATH)
    print("Deleted old database")

# Find all PDFs in data folder
pdf_files = [f for f in os.listdir(DATA_PATH) if f.endswith(".pdf")]
print(f"Found {len(pdf_files)} PDFs: {pdf_files}")

def is_useful_page(text):
    if text.count("doi:") > 3: return False
    if text.count("et al.") > 5: return False
    if len(text.strip()) < 200: return False
    return True

all_chunks = []

for pdf_file in pdf_files:
    print(f"\nProcessing {pdf_file}...")
    loader = PyPDFLoader(DATA_PATH + pdf_file)
    pages = loader.load()
    
    # Add source metadata to each page
    for page in pages:
        page.metadata["source"] = pdf_file
    
    filtered = [p for p in pages if is_useful_page(p.page_content)]
    print(f"  {len(pages)} pages → {len(filtered)} useful pages")
    
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        separators=["\n\n", "\n", ". ", " "]
    )
    chunks = splitter.split_documents(filtered)
    print(f"  {len(chunks)} chunks created")
    all_chunks.extend(chunks)

print(f"\nTotal chunks: {len(all_chunks)}")
print("Storing in ChromaDB...")

vectorstore = Chroma.from_documents(
    documents=all_chunks,
    embedding=OpenAIEmbeddings(),
    persist_directory=CHROMA_PATH
)

print(f"Done! Mana's brain updated with {len(all_chunks)} chunks from {len(pdf_files)} guidelines.")