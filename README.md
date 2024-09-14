# Document Retrieval Backend

This project implements a document retrieval system for chat applications to use as context. It provides a backend for retrieving documents, storing them in a database, and serving them through a REST API.

**Note: This is a submission by Spandan Kumar (21BCE0301) from VIT University for the Trademarkia AI, ML role.**

## Software Requirements

- Python 3.9+
- Docker


## Features

- Document storage and retrieval
- REST API for accessing documents
- Database integration with SQLAlchemy
- Document embedding using Sentence-Transformers
- Efficient similarity search with FAISS
- Caching with Redis
- Background tasks for scraping news articles
- Monitoring and metrics with Prometheus

## Setup and Installation

1. Clone the repository
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - Unix or MacOS: `source venv/bin/activate`
4. Install the required packages: `pip install -r requirements.txt`
5. Set up the database and run migrations: `alembic upgrade head`
