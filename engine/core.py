from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

class SentinelEngine:
    def __init__(self):
        # Optimized for i5/8GB RAM
        self.model_name = "llama3.2:3b"
        self.embeddings = OllamaEmbeddings(model=self.model_name)
        self.llm = ChatOllama(model=self.model_name, temperature=0.1)
        self.db_path = "./db"
        
        # Initialize Vector Store
        self.vector_db = Chroma(
            persist_directory=self.db_path,
            embedding_function=self.embeddings
        )

        self.prompt = ChatPromptTemplate.from_template(
            """Answer the question based ONLY on the following context. 
            If the answer is not in the context, say "I couldn't find the answer in the uploaded books."

            Context:
            {context}

            Question:
            {question}
            """
        )

    def ingest_documents(self, chunks):
        """Adds new book chunks to the database and saves to disk."""
        print(f"--- Adding {len(chunks)} chunks to Vector DB... ---")
        self.vector_db.add_documents(chunks)
        # ChromaDB automatically persists, but we verify the count
        print(f"--- Database updated. Total documents in library: {self.vector_db._collection.count()} ---")

    def get_answer(self, query: str):
        """Builds the chain dynamically to include all recently uploaded books."""
        
        # Check if DB is empty before searching
        doc_count = self.vector_db._collection.count()
        if doc_count == 0:
            return "Your library is empty. Please upload a PDF book first."

        # Create a fresh retriever to include the newest uploads
        retriever = self.vector_db.as_retriever(search_kwargs={"k": 5})
        
        # Build the chain
        chain = (
            {
                "context": retriever,
                "question": RunnablePassthrough()
            }
            | self.prompt
            | self.llm
            | StrOutputParser() # Ensures we get a clean string back
        )

        print(f"--- Searching library for: {query} ---")
        return chain.invoke(query)

# Global instance
ai_handler = SentinelEngine()