import json
import os
import sys
import httpx
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, StreamingResponse

debug = os.environ.get("GPTSCRIPT_DEBUG", "false") == "true"
openrouter_api_key = os.environ.get("OPENROUTER_API_KEY")
if not openrouter_api_key:
    print("Please set the OPENROUTER_API_KEY environment variable", file=sys.stderr)
    sys.exit(1)

app = FastAPI()
client = httpx.AsyncClient(base_url="https://openrouter.ai/api/v1")

def log(*args):
    if debug:
        print(*args)

@app.middleware("http")
async def log_body(request: Request, call_next):
    body = await request.body()
    log("HTTP REQUEST BODY: ", body)
    return await call_next(request)

@app.post("/")
async def post_root():
    return 'ok'

@app.get("/")
async def get_root():
    return 'ok'

@app.get("/v1/models")
async def list_models() -> JSONResponse:
    response = await client.get("/models", headers={"Authorization": f"Bearer {openrouter_api_key}"})
    return JSONResponse(response.json())

@app.post("/v1/chat/completions")
async def completions(request: Request) -> StreamingResponse:
    data = await request.json()
    model = os.environ.get("GPTSCRIPT_MODEL", "openai/gpt-3.5-turbo")
    headers = {
        "Authorization": f"Bearer {openrouter_api_key}",
        "HTTP-Referer": "https://github.com/RobinVivant/gptscript-openrouter-provider",
        "X-Title": "GPTScript Openrouter Provider"
    }
    
    async def generate():
        async with client.stream("POST", "/chat/completions", json={**data, "model": model}, headers=headers) as response:
            async for chunk in response.aiter_bytes():
                yield chunk

    return StreamingResponse(generate(), media_type="application/json")

if __name__ == "__main__":
    import uvicorn
    import asyncio

    try:
        uvicorn.run("main:app", host="127.0.0.1", port=int(os.environ.get("PORT", "8000")),
                log_level="debug" if debug else "critical", access_log=debug)
    except (KeyboardInterrupt, asyncio.CancelledError):
        pass
