# OpenRouter Provider for GPTScript ![GPTScript Logo](https://docs.gptscript.ai/img/favicon.ico) ![OpenRouter Logo](https://openrouter.ai/favicon.ico)



This provider allows GPTScript to use models available through OpenRouter, giving you access to a wide range of AI models.

## Setup

1. Get your OpenRouter API key from [OpenRouter](https://openrouter.ai/keys).
2. Set the environment variable:
   ```bash
   export OPENROUTER_API_KEY=YOUR_API_KEY
   ```
   Alternatively, you can add the API key to a `.env` file in your home directory:
   ```
   OPENROUTER_API_KEY=YOUR_API_KEY
   ```

## Usage Examples

### Basic Usage

```bash
export GPTSCRIPT_MODEL=openai/gpt-4-turbo
gptscript --default-model='openai/gpt-4-turbo from github.com/RobinVivant/gptscript-openrouter-provider' examples/helloworld.gpt
```

### Using Anthropic's Claude Model

```bash
gptscript --default-model='anthropic/claude-3.5-sonnet:beta from github.com/RobinVivant/gptscript-openrouter-provider' github.com/gptscript-ai/llm-basics-demo
```

### Listing Available Models

To see all available models through OpenRouter:

```bash
gptscript --list-models github.com/RobinVivant/gptscript-openrouter-provider
```

You can change the `GPTSCRIPT_MODEL` environment variable to use any model available through OpenRouter. Alternatively, you can use the `--default-model` flag when running gptscript. The `--default-model` flag takes precedence over the `GPTSCRIPT_MODEL` environment variable if both are set.

## Development

To run the provider locally:

1. Set up the environment:
   ```bash
   python -m venv .venv
   source ./.venv/bin/activate
   pip install --upgrade -r requirements.txt
   ```

2. Run the provider:
   ```bash
   ./run.sh
   ```

3. In another terminal, use the provider:
   ```bash
   export GPTSCRIPT_DEBUG=true
   export OPENROUTER_API_KEY=your_openrouter_api_key_here
   export GPTSCRIPT_MODEL=openai/gpt-4-turbo

   gptscript --default-model=openai/gpt-4-turbo examples/bob.gpt
   ```

Make sure to replace `your_openrouter_api_key_here` with your actual OpenRouter API key.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

If you encounter any issues or have questions, please [open an issue](https://github.com/RobinVivant/gptscript-openrouter-provider/issues) on GitHub.

---
