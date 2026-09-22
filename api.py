import json
import os
import asyncio
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from openai import AsyncOpenAI

from config import API_KEY, BASE_URL, MODEL, MAX_STEPS
from prompts import SYSTEM_PROMPT
from schemas import tools
from tools import TOOL_MAP

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = AsyncOpenAI(api_key=API_KEY, base_url=BASE_URL)


class ChatRequest(BaseModel):
    message: str


@app.post("/chat")
async def chat(req: ChatRequest):
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": req.message},
    ]

    async def event_stream():
        try:
            for _ in range(MAX_STEPS):
                response = await client.chat.completions.create(
                    model=MODEL,
                    messages=messages,
                    tools=tools,
                    tool_choice="auto",
                )
                msg = response.choices[0].message
                messages.append(msg.model_dump(exclude_none=True))

                if not msg.tool_calls:
                    if msg.content:
                        payload = {"type": "text", "content": msg.content}
                        yield f"data: {json.dumps(payload)}\n\n"
                    yield f"data: {json.dumps({'type': 'done'})}\n\n"
                    return

                for tool_call in msg.tool_calls:
                    name = tool_call.function.name
                    try:
                        args = json.loads(tool_call.function.arguments)
                    except json.JSONDecodeError:
                        args = {}

                    yield f"data: {json.dumps({'type': 'tool_start', 'tool': name, 'args': args})}\n\n"

                    func = TOOL_MAP.get(name)
                    if func is None:
                        result = f"Unknown tool: {name}"
                    else:
                        result = await asyncio.to_thread(func, **args)

                    yield f"data: {json.dumps({'type': 'tool_end', 'tool': name, 'result': str(result)[:300]})}\n\n"

                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": str(result),
                    })

            yield f"data: {json.dumps({'type': 'error', 'message': 'Max steps reached'})}\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'type': 'error', 'message': str(e)})}\n\n"

    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )


@app.get("/health")
def health():
    return {"status": "ok"}


# --- Serve the built frontend (present in Docker, absent in local dev) ---
STATIC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")

if os.path.isdir(STATIC_DIR):
    assets_dir = os.path.join(STATIC_DIR, "assets")
    if os.path.isdir(assets_dir):
        app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")

    RESERVED = ("chat", "health", "docs", "redoc", "openapi.json", "assets")

    @app.get("/{full_path:path}")
    async def spa(full_path: str):
        if full_path.startswith(RESERVED):
            raise HTTPException(status_code=404)
        candidate = os.path.join(STATIC_DIR, full_path)
        if full_path and os.path.isfile(candidate):
            return FileResponse(candidate)
        return FileResponse(os.path.join(STATIC_DIR, "index.html"))