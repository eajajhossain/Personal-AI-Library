from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

def process_pdf_smartly(file_path):
    """
    Industry-level PDF processing with memory management for 8GB RAM.
    """
    # 1. Load the document lazily to save RAM
    loader = PyPDFLoader(file_path)
    
    # 2. Recursive splitting: it tries to split by paragraph, then sentence
    # This prevents the AI from getting "half-sentences" that don't make sense.
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,   # Ideal for small local models like Llama 3.2
        chunk_overlap=150,  # Keeps context between chunks
        length_function=len,
        separators=["\n\n", "\n", ".", " ", ""]
    )
    
    # 3. Create chunks
    pages = loader.load_and_split(text_splitter)
    return pages