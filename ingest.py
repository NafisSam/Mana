from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
import os
import shutil

load_dotenv()

# Delete old database first
if os.path.exists("data/chroma_db"):
    shutil.rmtree("data/chroma_db")
    print("Deleted old database")

# Step 1: Load PDF
print("Loading PDF...")
loader = PyPDFLoader("data/standards-of-care-2026.pdf")
pages = loader.load()
print(f"Loaded {len(pages)} pages")

# Step 2: Filter out junk pages
def is_useful_page(text):
    # Skip reference-heavy pages
    if text.count("doi:") > 3:
        return False
    if text.count("et al.") > 5:
        return False
    # Skip very short pages (figures, blank pages)
    if len(text.strip()) < 200:
        return False
    return True

filtered_pages = [p for p in pages if is_useful_page(p.page_content)]
print(f"Kept {len(filtered_pages)} useful pages (filtered {len(pages) - len(filtered_pages)} junk pages)")

# Step 3: Smarter chunking
splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,   # bigger chunks = more context
    chunk_overlap=200, # more overlap = less info lost at edges
    separators=["\n\n", "\n", ". ", " "] # split at natural boundaries
)
chunks = splitter.split_documents(filtered_pages)
print(f"Created {len(chunks)} chunks")

# Step 4: Store in ChromaDB
print("Storing in ChromaDB...")
vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=OpenAIEmbeddings(),
    persist_directory="data/chroma_db"
)
print(f"Done! Mana's brain is ready with {len(chunks)} chunks.")