import PyPDF2
from typing import List
import re


class PDFProcessor:
    def __init__(self):
        self.extracted_text = ""

    def clean_text(self, text: str) -> str:
        """Clean and format extracted text."""
        # Remove excessive whitespace and newlines
        text = re.sub(r'\s+', ' ', text)
        # Fix cases where words are incorrectly split
        text = re.sub(r'(?<=\w)-\s+(?=\w)', '', text)
        return text.strip()

    def extract_text(self, pdf_path: str) -> str:
        """Extract text from PDF file and combine paragraphs."""
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page in reader.pages:
                page_text = page.extract_text()
                page_text = self.clean_text(page_text)
                text += page_text + " "  # Combine into one big paragraph

        self.extracted_text = text.strip()
        return self.extracted_text

    def semantic_chunking(self, text: str, max_chunk_size: int = 1000) -> List[str]:
        """
        Chunk text semantically based on sentences and natural breaks.
        """
        # Clean and split text into sentences
        sentences = re.split(r'(?<=[.!?])\s+', self.clean_text(text))

        chunks = []
        current_chunk = ""

        for sentence in sentences:
            # If adding the sentence exceeds max_chunk_size
            if len(current_chunk) + len(sentence) > max_chunk_size:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = sentence
            else:
                current_chunk += " " + sentence if current_chunk else sentence

        # Add the last chunk if it exists
        if current_chunk:
            chunks.append(current_chunk.strip())

        return chunks
