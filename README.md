# 🚀 The Lenny Growth Assistant

> **Forward Deployed Engineer Take-Home Assignment Solution**  
> A full-stack, AI-powered conversational web application grounded strictly in **Lenny’s Podcast transcripts**. Features grounded RAG, a dedicated **Ship 30 for 30 Content Skill**, side-by-side **Artifact Viewer** with sandboxed HTML rendering, and flexible LLM provider toggling (Ollama local fallback + Cloud Claude/OpenAI).

---

## 🌟 Key Features

1. **Grounded Conversational RAG**: Answers product management and growth questions strictly from Lenny's transcripts (Brian Chesky, Shreyas Doshi, Elena Verna, Marty Cagan, Gokul Rajaram) with footnoted citations and transcript links.
2. **Ship 30 for 30 Essay Skill**: Dedicated skill generating ~1,250-word viral growth essays with strong hooks, 3 narrative pillars, skimmable bullet points, bold key takeaways, and grounded claims.
3. **In-App Artifact Viewer**: Renders interactive HTML/CSS dashboards, growth matrices, and markdown roadmaps side-by-side with chat inside an isolated, sandboxed `<iframe>` with DOMPurify sanitization.
4. **Flexible LLM Provider Configuration**: Switch dynamically between **Ollama (Local LLM)**, **Anthropic Claude**, **OpenAI GPT-4o**, or the zero-dependency **Lenny Mock Engine**.
5. **Session Management & Persistence**: Multi-session support backed by PostgreSQL / Async SQLite with full conversation history and artifact retention.

---

## 🛠 Tech Stack

- **Frontend**: React 18, Vite, Vanilla CSS Design System (Dark Glassmorphism), Lucide Icons, DOMPurify, React Markdown.
- **Backend**: FastAPI (Async Python 3.11), Pydantic v2, Async SQLAlchemy.
- **Database**: PostgreSQL (pgvector compatible) with embedded Async SQLite fallback.
- **LLM Layer**: Ollama (Llama 3.2 local), Anthropic API, OpenAI API, Mock Provider.

---

## 🚀 Quick Start (One-Command Docker Setup)

### Prerequisites
- Docker & Docker Compose installed.
- (Optional) [Ollama](https://ollama.ai/) running locally on port `11434` with `llama3.2` pulled.

### 1. Clone & Configure Environment
```bash
git clone https://github.com/your-username/lenny-growth-assistant.git
cd lenny-growth-assistant

# Copy sample environment configuration
cp .env.example .env
```

### 2. Launch with Docker Compose
```bash
docker-compose up --build
```

Access the application in your browser:
- **Frontend App**: `http://localhost:3000`
- **FastAPI API Docs**: `http://localhost:8000/docs`
- **Health Endpoint**: `http://localhost:8000/api/v1/health`

---

## 💻 Manual Local Development (Without Docker)

### Backend Setup
```bash
# 1. Create virtual environment
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Start FastAPI server
uvicorn backend.app.main:app --reload --port 8000
```

### Frontend Setup
```bash
cd frontend

# 1. Install Node dependencies
npm install

# 2. Start Vite development server
npm run dev
```
Open `http://localhost:3000` in your browser.

---

## 🤖 Running with Ollama (Mandatory for Demo)

1. Download and install [Ollama](https://ollama.ai/).
2. Pull the default demo model:
   ```bash
   ollama pull llama3.2
   ```
3. Ensure Ollama is running (`ollama serve` or background tray app on `http://localhost:11434`).
4. Select **"Ollama (Local LLM)"** in the top-right header dropdown inside the application.
   *(Note: If Ollama is not running, the application will automatically fall back gracefully to the built-in Mock LLM Engine without crashing!)*

---

## 🧪 Running Automated Tests

Run the backend test suite using `pytest`:

```bash
# Set PYTHONPATH and execute pytest
pytest backend/tests -v
```

### 📋 Short Manual UI Test Plan (For Evaluators)
See full details in [`backend/tests/manual_test_plan.md`](file:///c:/Users/KOUSHIK/.gemini/antigravity-ide/scratch/lenny-growth-assistant/backend/tests/manual_test_plan.md).
1. **Model Switcher**: In the top-right header, toggle between *Ollama (Local)*, *Anthropic*, *OpenAI*, and *Mock Provider*. Confirm graceful fallback indicator if Ollama is not running.
2. **Grounded Q&A & Citations**: Click prompt *"Explain Brian Chesky's Founder Mode vs Manager Mode"*. Verify `[Brian Chesky, Ep. 101]` footnote chip displays timestamp, quotes, and transcript link.
3. **Out-of-Scope Negative Test**: Ask *"How do I bake sourdough bread?"*. Verify the assistant states it is not covered in the transcripts.
4. **Ship 30 for 30 Skill**: Select *"✍️ Ship 30 Essay"* button and ask for an essay on *LNO framework*. Verify ~1,250-word structured output with hook, 3 pillars, bullets, and playbook.
5. **Artifact Viewer & Sandbox**: Select *"🎨 Artifact"* button and ask for *"an interactive growth matrix dashboard"*. Confirm split-screen 50/50 view opens with Sandboxed `<iframe>` preview and Code toggle.
6. **Session Context Persistence**: Click *"+ New Chat"*, create another conversation, then switch back to the previous session in sidebar. Confirm history, citations, and artifacts restore accurately.

---

## 🎬 Demo Video Outline & Script (2-3 Minutes)

When recording your video for submission:
1. **0:00 - 0:30 (Problem & Brief)**: Introduce yourself, explain the prompt (turning Lenny's transcripts into a grounded internal growth assistant with artifacts and skills).
2. **0:30 - 1:15 (Grounded Chat & Citations)**: Ask "Explain Brian Chesky's Founder Mode vs Manager Mode". Highlight footnote citations, guest names, timestamps, and direct transcript links.
3. **1:15 - 1:55 (Ship 30 for 30 Skill & Local Ollama)**: Toggle model to Ollama local LLM. Select "Ship 30 for 30 Skill" and ask for an essay on LNO task prioritization. Point out the ~1,250-word structure, hook, bold emphasis, and takeaways.
4. **1:55 - 2:30 (Artifact Viewer & Security)**: Ask to generate an interactive HTML growth framework dashboard. Demonstrate the side-by-side split screen, Code vs. Preview tabs, and explain the `iframe` sandbox and DOMPurify security isolation strategy.
5. **2:30 - 3:00 (Architecture & Handoff)**: Highlight `docker-compose.yml`, zero-dependency mock fallback, FastAPI architecture, and test suite.

---

## 📁 Repository Structure

```
lenny-growth-assistant/
├── docker-compose.yml          # One-command orchestration
├── Dockerfile.backend          # Backend container spec
├── Dockerfile.frontend         # Frontend container spec
├── .env.example                # Documented env configuration
├── README.md                   # Setup & evaluators guide
├── PRD.md                      # Product Requirements Document
├── design.md                   # Design rationale & UX spec
├── architecture.md             # System & DB topology
├── requirements.txt            # Python dependencies
├── agent_transcripts/          # Coding agent execution trajectory
│   └── build_and_debug_trajectory.md
├── backend/
│   ├── app/
│   │   ├── main.py             # FastAPI entrypoint
│   │   ├── config.py           # Settings & Env vars
│   │   ├── database.py         # SQLAlchemy & Session setup
│   │   ├── models/             # Pydantic & DB Schemas
│   │   ├── services/
│   │   │   ├── llm_provider.py # Provider abstraction (Ollama/Cloud/Mock)
│   │   │   ├── rag_engine.py   # Transcript indexing & search
│   │   │   ├── agent_service.py# Router & artifact extraction
│   │   │   └── skills/
│   │   │       └── ship30_skill.py # ~1,250-word Ship 30 for 30 skill
│   │   └── api/                # Health, Models, Sessions, Chat, Ingest
│   └── tests/                  # API, RAG, and LLM test suite
├── data/
│   └── transcripts/            # Lenny transcript knowledge base
└── frontend/
    ├── src/
    │   ├── components/         # React components (ArtifactViewer, etc.)
    │   ├── services/           # API fetch client
    │   ├── App.jsx             # Main application state
    │   └── index.css           # Glassmorphism styling system
    └── index.html
```
