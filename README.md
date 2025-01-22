# Flask RAG PDF Processor

## Overview

This project is a Flask-based web application that processes PDF files, extracts text, and uses a Retrieval-Augmented Generation (RAG) approach for answering user queries based on the extracted content. It uses semantic chunking to split extracted text into smaller manageable pieces for effective information retrieval.

## Features

- Upload PDF files and extract content.
- Combine extracted text into a single paragraph for display purposes.
- Split text into semantic chunks for efficient retrieval and storage in a vector database.
- Query the stored content using RAG to retrieve relevant information and generate precise answers.

## Prerequisites

- **Python**: Python 3.7 or higher is required.
- **Pip**: Ensure `pip` is installed to manage Python dependencies.
- Install `virtualenv` for isolated environments:
  ```bash
  pip install virtualenv
  ```

## Setup Instructions

- **Step 1**: Clone the Repository

```bash
git clone <https://github.com/Frankie0411/Ottowatt-AI-Assignment>
```

- **Step 2**: Create a virtual environment

```bash
virtualenv venv
source venv/bin/activate # For Linux/MacOS
venv\Scripts\activate # For Windows
```

- **Step 3**: Install Dependencies

```bash
    pip install -r requirements.txt
```

## Running the Application

### Start the flask app

```bash
    python run.py
```

The server will start on http://127.0.0.1:5000/ by default. Open the URL in your browser to access the application.

## Additional Notes

- **File Type Validation**: Only PDF files are accepted.
- **Storage Cleanup**: Uploaded files are automatically deleted after processing.
