PDF Search and Query Tool

This program processes PDF files, generates embeddings for each page using Amazon Bedrock, 
stores these embeddings in a SQLite database, and allows you to perform semantic searches across the PDFs. 
It retrieves the most relevant pages based on your search query and generates concise answers using Amazon Bedrock's Claude model.

Features

    Automatically processes and embeds any new PDFs placed in the pdfs folder.
    Stores embeddings in a local SQLite database to avoid reprocessing.
    Uses FAISS for fast similarity searches on embedded PDF content.
    Provides concise answers to user queries using Amazon Bedrock.

Prerequisites

    Python 3.8+
    Make sure you have Python installed on your machine. You can download it from python.org.

    AWS Credentials
        Configure your AWS credentials to use Amazon Bedrock:

            aws configure

        Ensure you have access to the Bedrock runtime and the us-east-1 region.

    SQLite
        SQLite comes pre-installed with Python, but ensure you have it available.


Installation

    Clone the Repository

        git clone <repository_url>
        cd <repository_directory>


    Create a Virtual Environment (Optional but Recommended)

        python -m venv venv
        source venv/bin/activate  # On Windows use: venv\Scripts\activate


    Install Required Libraries

        pip install -r requirements.txt


    Create PDF folder

        create a folder in the root directory called 'pdfs'.  


    Create SQLite Database

        Run this script in a new file.  You can delete the script after db file is created.

            import sqlite3
    
            # Connect to SQLite database (this will create the file if it doesn't exist)
            conn = sqlite3.connect('pdf_embeddings.db')
            cursor = conn.cursor()
            
            # Create the embeddings table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS embeddings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    pdf_path TEXT NOT NULL,
                    page_number INTEGER NOT NULL,
                    embedding BLOB NOT NULL
                )
            ''')
            
            conn.commit()
            conn.close()


Usage

    Add PDFs to Process
        Place your .pdf files in the pdfs folder. The program will process new PDFs automatically.

    Run the Program

    python main.py

    Search PDFs
        After the PDFs are processed, you'll be prompted to enter a search query. The program will:
            Retrieve the most relevant PDF pages using FAISS similarity search.
            Generate a concise answer to your query using Amazon Bedrock.

    View Results
        The results will include:
            The answer generated by the AI.
            References to the PDF pages where the information was found.

Project Structure

├── pdfs/                     # Folder to store PDF files

├── pdf_embeddings.db         # SQLite database for storing embeddings

├── main.py                   # Main script to process PDFs and handle queries

├── database_functions.py     # Functions for database operations

├── process_pdf.py            # Functions for extracting text from PDFs

├── embed.py                  # Functions to generate embeddings using Amazon Bedrock

├── search.py                 # Functions for FAISS-based similarity search

└── call_bedrock.py           # Function to call Amazon Bedrock for query responses

Important Notes

    Amazon Bedrock Costs: Ensure you're aware of any costs associated with using Amazon Bedrock services.
    Batch Processing: Currently, the Bedrock API does not support batch processing, so embedding large PDFs may take time.
    Database Duplication: PDFs already processed will not be re-embedded unless removed from the database.

Troubleshooting

    No PDFs Found: Ensure your .pdf files are placed in the pdfs directory.
    AWS Errors: Verify that your AWS credentials are correctly configured and you have the necessary permissions.
    No Results in Search: Ensure PDFs have been processed correctly, and embeddings exist in the database.
