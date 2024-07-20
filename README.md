# Openrouter Provider for GPTScript

This provider allows GPTScript to use models available through Openrouter.

## Usage Example

```
export OPENROUTER_API_KEY=your_openrouter_api_key_here
export GPTSCRIPT_MODEL=openai/gpt-4-turbo
gptscript --default-model='openai/gpt-4-turbo from github.com/RobinVivant/gptscript-openrouter-provider' examples/helloworld.gpt
```

You can change the `GPTSCRIPT_MODEL` environment variable to use any model available through Openrouter.

## Development

To run the provider locally:

```
python -m venv .venv
source ./.venv/bin/activate
pip install --upgrade -r requirements.txt
./run.sh
```

Then, in another terminal:

```
export OPENAI_BASE_URL=http://127.0.0.1:8000/v1
export GPTSCRIPT_DEBUG=true
export OPENROUTER_API_KEY=your_openrouter_api_key_here
export GPTSCRIPT_MODEL=openai/gpt-4-turbo

gptscript --default-model=openai/gpt-4-turbo examples/bob.gpt
```

Make sure to replace `your_openrouter_api_key_here` with your actual Openrouter API key.
