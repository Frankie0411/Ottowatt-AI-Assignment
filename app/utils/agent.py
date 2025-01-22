from typing import List, Dict
from .rag_engine import RAGEngine


class Agent:
    def __init__(self, api_key: str):
        self.rag_engine = RAGEngine(api_key)

    def process_pdf_chunks(self, chunks: List[str]):
        # Process and store PDF chunks in the RAG engine
        self.rag_engine.add_documents(chunks)

    def get_answer(self, question: str) -> str:
        # Get answer for a question using RAG
        # Retrieve relevant context
        relevant_chunks = self.rag_engine.query(question)

        # Generate response
        response = self.rag_engine.generate_response(question, relevant_chunks)

        return response
