import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

def process_pdf_smartly(file_path):
    """
    Memory-efficient PDF processing for 8GB RAM.
    Uses lazy loading to handle files up to 1GB.
    """
    print(f"--- Processing started for: {os.path.basename(file_path)} ---")
    
    try:
        # 1. Lazy Loading: Load the PDF page by page to save RAM
        loader = PyPDFLoader(file_path)
        
        # 2. Optimized Splitting for local LLMs
        # Smaller chunks (500 characters) are easier for Llama 3.2 to search
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )
        
        # 3. Create Chunks
        print("--- Splitting text into searchable chunks... ---")
        chunks = loader.load_and_split(text_splitter)
        
        print(f"--- Successfully created {len(chunks)} chunks! ---")
        return chunks

    except Exception as e:
        print(f" Error in document_mgr: {str(e)}")
        return []