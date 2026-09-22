# AI Agent

ReAct-style agent with tools: read/write files, run Python, search the web.
FastAPI backend + React chat UI + CLI.

## Architecture

- **Agent** (`agent.py`) — LLM loop; executes tool calls until the model returns plain text.
- **API** (`api.py`) — `/chat` (SSE stream) and `/health`. Serves the built frontend in Docker.
- **CLI** (`main.py`) — terminal chat.
- **Frontend** (`frontend/`) — Vite + React + TS. Markdown rendering + tool-call badges.
- **Tools** (`tools/`) — `read_file`, `write_file`, `list_files`, `run_code`, `search_web`.

## Local dev

Backend:

```bash
python -m venv venv
source venv/bin/activate         # Windows: venv\Scripts\activate
pip install -r requirements.txt
# create .env with GROQ_API_KEY=gsk_...
uvicorn api:app --reload         # http://localhost:8000
```

Frontend (separate terminal):

```bash
cd frontend
npm install
npm run dev                      # http://localhost:5173
```

Vite proxies `/chat` and `/health` to `localhost:8000`, so the UI talks to the backend without CORS issues.

## Docker

```bash
docker compose up --build -d
docker compose logs -f app
```

Open **http://localhost:8000** — one container, one port, frontend + API served together.
The agent's workspace persists in the named volume `workspace` across `docker compose down`.

## CLI

```bash
python main.py
```

## Environment

| Variable | Required | Default |
|---|---|---|
| `GROQ_API_KEY` | yes | — |

## Configuration (`config.py`)

- `MODEL` — Groq model name (default `openai/gpt-oss-120b`).
- `MAX_STEPS` — max agent iterations (default 20).
- `WORKSPACE_DIR` — sandbox for file tools (default `./workspace`).