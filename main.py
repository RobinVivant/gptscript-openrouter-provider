import os
from pathlib import Path

import httpx
from fastapi import FastAPI, Request
from dotenv import load_dotenv
from fastapi.responses import JSONResponse, StreamingResponse

debug = os.environ.get("GPTSCRIPT_DEBUG", "false") == "true"

# Load .env file from user's home directory
dotenv_path = Path.home() / ".env"
load_dotenv(dotenv_path)

openrouter_api_key = os.environ.get("OPENROUTER_API_KEY")
if not openrouter_api_key:
    raise ValueError("Please set the OPENROUTER_API_KEY in your ~/.env file or as an environment variable")

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
    model = os.environ.get("GPTSCRIPT_MODEL", "anthropic/claude-3.5-sonnet:beta")
    headers = {
        "Authorization": f"Bearer {openrouter_api_key}",
        "HTTP-Referer": "https://github.com/RobinVivant/gptscript-openrouter-provider",
        "X-Title": "GPTScript Openrouter Provider"
    }

    async def generate():
        try:
            async with client.stream("POST", "/chat/completions", json={**data},
                                     headers=headers) as response:
                response.raise_for_status()
                async for chunk in response.aiter_bytes():
                    yield chunk
        except httpx.HTTPStatusError as e:
            error_message = f"HTTP error occurred: {e.response.status_code} {e.response.reason_phrase}"
            yield error_message.encode()
        except Exception as e:
            error_message = f"An error occurred: {str(e)}"
            yield error_message.encode()

    return StreamingResponse(generate(), media_type="application/json")


if __name__ == "__main__":
    import uvicorn
    import asyncio

    try:
        uvicorn.run("main:app", host="127.0.0.1", port=int(os.environ.get("PORT", "8000")),
                    log_level="debug" if debug else "critical", access_log=debug)
    except (KeyboardInterrupt, asyncio.CancelledError):
        pass
