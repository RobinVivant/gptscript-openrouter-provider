import os
import sys
import logging

import httpx
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, StreamingResponse

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

debug = os.environ.get("GPTSCRIPT_DEBUG", "false") == "true"
openrouter_api_key = os.environ.get("OPENROUTER_API_KEY")
if not openrouter_api_key:
    raise ValueError("Please set the OPENROUTER_API_KEY environment variable")

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
    return {'status': 'ok', 'message': 'OpenRouter provider is running'}

@app.get("/health")
async def health_check():
    return {'status': 'healthy', 'message': 'OpenRouter provider is healthy'}


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
    logger.info(f"Received request for model: {model}")

    async def generate():
        try:
            async with client.stream("POST", "/chat/completions", json={**data, "model": model},
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
