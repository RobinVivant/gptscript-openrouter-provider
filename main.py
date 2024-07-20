import json
import os
import sys

import boto3
import claude3_provider_common
from anthropic import AsyncAnthropicBedrock
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, StreamingResponse

try:
    client = boto3.client('sts')
    response = client.get_caller_identity()
except Exception as e:
    print("Please authenticate with AWS - ", e, file=sys.stderr)
    sys.exit(1)

debug = os.environ.get("GPTSCRIPT_DEBUG", "false") == "true"
client = AsyncAnthropicBedrock()
app = FastAPI()


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
    return await claude3_provider_common.list_models(client)


@app.post("/v1/chat/completions")
async def completions(request: Request) -> StreamingResponse:
    data = await request.body()
    input = json.loads(data)
    return await claude3_provider_common.completions(client, input)


if __name__ == "__main__":
    import uvicorn
    import asyncio

    try:
        uvicorn.run("main:app", host="127.0.0.1", port=int(os.environ.get("PORT", "8000")),
                log_level="debug" if debug else "critical", access_log=debug)
    except (KeyboardInterrupt, asyncio.CancelledError):
        pass
