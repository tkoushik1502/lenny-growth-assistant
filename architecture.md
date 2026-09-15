# System Architecture Document
## "The Lenny Growth Assistant"

---

## 1. System Topology & Component Diagram

```
                             +-----------------------+
                             | React + Vite Frontend |
                             | (Port 3000 / Nginx)   |
                             +-----------+-----------+
                                         |
                                    HTTP / JSON
                                         v
                             +-----------------------+
                             |   FastAPI API Engine  |
                             |      (Port 8000)      |
                             +---+-------+-------+---+
                                 |       |       |
           +---------------------+       |       +---------------------+
           v                             v                             v
+--------------------+       +-------------------+       +-------------------+
|  LLM Provider Layer|       |    RAG Engine     |       | Async SQLAlchemy  |
| - Ollama (Local)   |       | - Term Weighting  |       | - Postgres/pgvector|
| - Claude (Cloud)   |       | - Chunks & Quotes |       | - SQLite Fallback |
| - OpenAI (Cloud)   |       | - Lenny Dataset   |       +-------------------+
| - Mock Fallback    |       +-------------------+
+--------------------+
```

---

## 2. Database Schema (PostgreSQL / SQLite)

### `chat_sessions`
- `id` (VARCHAR PK): `sess-xxxxxx`
- `title` (VARCHAR): Session topic title
- `created_at` (TIMESTAMP): UTC creation time
- `updated_at` (TIMESTAMP): UTC last update
- `provider_used` (VARCHAR): LLM provider used (`ollama`, `anthropic`, `openai`, `mock`)
- `user_metadata` (JSON): Context metadata (user role, organization, client telemetry)

### `chat_messages`
- `id` (VARCHAR PK): `msg-xxxxxx`
- `session_id` (VARCHAR FK -> `chat_sessions.id`)
- `role` (VARCHAR): `user`, `assistant`, `system`
- `content` (TEXT): Message markdown content
- `citations` (JSON): Array of footnote citation objects
- `skill_used` (VARCHAR): `chat`, `ship30`, `artifact`
- `created_at` (TIMESTAMP)

### `artifacts`
- `id` (VARCHAR PK): `art-xxxxxx`
- `session_id` (VARCHAR FK -> `chat_sessions.id`)
- `title` (VARCHAR): Artifact header title
- `type` (VARCHAR): `html` or `markdown`
- `content` (TEXT): Code content
- `created_at` (TIMESTAMP)

---

## 3. RAG Retrieval & Citation Flow

1. User sends prompt query to `/api/v1/chat`.
2. `RAGEngine` performs weighted term search over transcripts dataset.
3. Top 4 chunks are formatted with metadata (Episode Title, Speaker, Timestamp, Quotes).
4. Prompt is enriched with RAG context and routed to `LLMProvider`.
5. Response generated with footnoted citations `[1]`, `[2]`.

---

## 4. API Endpoint Specifications

- `GET /api/v1/health`: System health & transcript chunk index count.
- `GET /api/v1/models`: List available LLM providers & status.
- `GET /api/v1/sessions`: List past conversations.
- `POST /api/v1/sessions`: Create new session.
- `GET /api/v1/sessions/{id}`: Load session history & artifacts.
- `DELETE /api/v1/sessions/{id}`: Delete session.
- `POST /api/v1/chat`: Send chat prompt, receive grounded response, citations & artifact.
- `GET /api/v1/ingest/status`: Transcript indexing statistics.
