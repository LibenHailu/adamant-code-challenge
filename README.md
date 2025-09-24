# Adamant Challenge Backend

FastAPI backend for uploading PDFs, indexing their content in ChromaDB, and handling user messages via simple classification and RAG/Weather flows.

[![Watch the demo](https://img.youtube.com/vi/-upnbiS0G_w/0.jpg)](https://youtu.be/-upnbiS0G_w?si=FpO1S6N96jrpmDEj)
## Tech Stack

- FastAPI, Starlette (API)
- SQLAlchemy, Alembic (DB & migrations)
- PostgreSQL (storage)
- ChromaDB local store (vector search)
- LangChain with OpenAI and Groq (LLMs)
- Dependency Injector (DI)
- httpx (HTTP client)

## Prerequisites

- Python 3.12+
- PostgreSQL database (for `DATABASE_URL`)
- API keys as needed:
  - `OPENAI_API_KEY` (for `ChatOpenAI`)
  - `GROQ_API_KEY` (for `ChatGroq`)
  - `WEATHER_API_KEY` (for Weather API)

## Quick Start

1. Clone and enter the project directory:

```bash
git clone https://github.com/LibenHailu/adamant-code-challenge.git
cd adamant-code-challenge
```

2. Create and activate a virtual environment (optional if `venv/` already present activate the virtual environment and proceed):

```bash
python -m venv venv
source venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements-dev.txt
```

4. Configure environment variables (create a `.env` file in project root):

```dotenv
# Server
ENV=test
DATABASE_URL=
# External APIs / LLMs
OPENAI_API_KEY=sk-...
GROQ_API_KEY=...
WEATHER_API_KEY=...
```

5. Run database migrations:

```bash
alembic upgrade head
```

6. Start the server:

```bash
uvicorn src.main:app --reload
```

7. Open API docs: `http://localhost:8000/docs`

8. Run tests:

```bash
pytest
```

## Project Structure

```
src/
  main.py                 # App factory & router mounting
  api/v1/                 # API v1 routers and endpoints
    endpoints/rag.py      # /documents and /messages
    routes.py             # aggregates routers
  core/                   # config, DI container, db, clients, middleware
  model/                  # SQLAlchemy models
  repository/             # DB access & vector search helpers
  schema/                 # Pydantic request/response models
  services/               # Business logic (documents, messages)
uploads/                  # Uploaded PDF files
chroma_db/                # Local ChromaDB storage
migrations/               # Alembic migration scripts
```

## Endpoints (base path: `/api/v1`)

- POST `/documents` — Upload and index a PDF

  - Request: `multipart/form-data` with `file` (content-type `application/pdf`)
  - Response: `DocumentResponse`

- POST `/messages` — Handle a user message
  - Request: JSON `MessageCreate { content: string }`
  - Behavior:
    - Classifies as Food / Weather / None using OpenAI.
    - Food: performs vector search over uploaded PDFs and answers with context (RAG).
    - Weather: fetches current weather via external API.
  - Response: `MessageResponse`

