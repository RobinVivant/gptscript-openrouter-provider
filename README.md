# Openrouter Provider for GPTScript

This provider allows GPTScript to use models available through Openrouter, giving you access to a wide range of AI models.

## Setup

1. Get your Openrouter API key from [Openrouter](https://openrouter.ai/keys).
2. Set the environment variable:
   ```
   export OPENROUTER_API_KEY=YOUR_API_KEY
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

To see all available models through Openrouter:

```bash
gptscript --list-models github.com/RobinVivant/gptscript-openrouter-provider
```

You can change the `GPTSCRIPT_MODEL` environment variable to use any model available through Openrouter. Alternatively, you can use the `--default-model` flag when running gptscript. The `--default-model` flag takes precedence over the `GPTSCRIPT_MODEL` environment variable if both are set.

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

Make sure to replace `your_openrouter_api_key_here` with your actual Openrouter API key.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

[Insert your license information here]
