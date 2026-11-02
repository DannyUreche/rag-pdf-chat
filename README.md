# 🚀 High-Performance Asynchronous RAG Engine

A local, containerized, asynchronous Retrieval-Augmented Generation (RAG) backend engine built with **FastAPI**, **Celery**, **Redis**, and **PostgreSQL + pgvector**.

## 🏗️ Architecture & Key Features

* **Async REST API:** Built with FastAPI for handling high-throughput asynchronous file uploads (`HTTP 202 Accepted`).
* **Background Processing Queue:** Offloads heavy CPU operations (PDF parsing, text chunking, embedding generation) to Celery workers backed by Redis without blocking the API event loop.
* **Vector Embeddings:** Local execution of `sentence-transformers` (`all-MiniLM-L6-v2`) generating 384-dimensional dense embeddings.
* **Vector Database:** Native storage and similarity search in PostgreSQL using the `pgvector` extension via SQLAlchemy 2.0 (`asyncpg`).
* **Connection Lifecycle Management:** Explicit DB connection pool handling (`engine.dispose()`) to bridge async SQLAlchemy operations inside synchronous Celery workers.

## 🛠️ Tech Stack

* **Framework:** FastAPI
* **Background Queue:** Celery + Redis
* **Database & Vector Store:** PostgreSQL 16 + `pgvector`
* **ORM:** SQLAlchemy 2.0 (Async) + `asyncpg`
* **AI/ML:** PyMuPDF, `sentence-transformers`
* **Infrastructure:** Docker & Docker Compose

## 🚀 Quick Start Guide

### Prerequisites
* Docker & Docker Compose
* Python 3.11+

### Installation & Execution

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/UTILIZATORUL_TAU/rag-pdf-chat.git](https://github.com/UTILIZATORUL_TAU/rag-pdf-chat.git)
   cd rag-pdf-chat