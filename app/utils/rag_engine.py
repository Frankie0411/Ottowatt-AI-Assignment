from typing import List, Dict
import chromadb
from chromadb.config import Settings
import os
from openai import OpenAI
import json


class RAGEngine:
    def __init__(self, api_key: str):
        # Initialize ChromaDB client with persistent directory and tenant settings
        self.client = chromadb.PersistentClient(
            path="./chroma_db",
            settings=Settings(
                allow_reset=True,
                is_persistent=True
            )
        )

        # Check if 'pdf_collection' already exists
        existing_collections = self.client.list_collections()

        if "pdf_collection" in existing_collections:
            print("Reusing existing 'pdf_collection'.")
            self.collection = self.client.get_collection("pdf_collection")
        else:
            print("Creating new 'pdf_collection'.")
            self.collection = self.client.create_collection("pdf_collection")

        self.openai_client = OpenAI(api_key=api_key)

    def add_documents(self, chunks: List[str], metadata: List[Dict] = None):
        """Add document chunks to the vector database."""
        try:
            # Delete existing collection if it exists
            try:
                self.client.delete_collection("pdf_collection")
            except Exception:
                pass

            # Create a new collection
            self.collection = self.client.create_collection("pdf_collection")

            # Generate metadata if none provided
            if not metadata:
                metadata = [{"chunk_id": str(i)} for i in range(len(chunks))]

            # Add documents and metadata to the collection
            self.collection.add(
                documents=chunks,
                metadatas=metadata,
                ids=[f"id{i}" for i in range(len(chunks))]
            )
        except Exception as e:
            print(f"Error adding documents: {str(e)}")
            raise

    def query(self, question: str, k: int = 3) -> List[str]:
        """Query the vector database for relevant chunks."""
        results = self.collection.query(
            query_texts=[question],
            n_results=k
        )
        return results['documents'][0]

    def generate_response(self, question: str, context: List[str]) -> str:
        """Generate response using OpenAI API."""
        prompt = f"""Based on the following context, answer the question concisely and precisely. 
        If the answer is not in the context, say 'I cannot answer this based on the provided document.'

        Context:
        {' '.join(context)}

        Question: {question}

        Answer:"""

        response = self.openai_client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that provides short, precise answers based on the given context."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150,
            temperature=0.3
        )

        return response.choices[0].message.content
