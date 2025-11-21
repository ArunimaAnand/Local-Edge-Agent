# Ollama Backend

Before following these steps, ensure you have completed the initial [Setup Guide](README.md).

## Requirements

- Python 3.8+
- `openai` and `pyyaml` Python packages
- Ollama installed and running on your system

## Setup Instructions

1. **Install Ollama**

   - Download and install [Ollama](https://ollama.ai) for your operating system:
     - **macOS/Linux**: Run `curl -fsSL https://ollama.com/install.sh | sh`
     - **Windows**: Download from [https://ollama.com/download](https://ollama.com/download)
   - Or visit the official website for manual installation instructions.

2. **Start Ollama Service**

   - Ollama typically runs as a background service after installation
   - To verify it's running, open a terminal and run:
     ```sh
     ollama list
     ```
   - This should show installed models (if any) without errors

3. **Download and Run a Model**

   - Pull a model using the Ollama CLI. For example, to download Llama 3.2 3B:
     ```sh
     ollama pull llama3.2:3b
     ```
   - Other recommended models:
     - `llama3.2:1b` - Smallest, fastest (1.3GB)
     - `llama3.2:3b` - Balanced performance (2GB)
     - `mistral:7b` - Larger, more capable (4.1GB)
     - `phi3:mini` - Efficient small model (2.3GB)
   
4. **Configure Your Application**

   - Create a `config.yaml` file in the project root with the following settings:
     ```yaml
     MODEL_PROVIDER: "ollama"
     OLLAMA_URL: "http://localhost:11434/v1"
     OLLAMA_API_KEY: "ollama"  # Can be any value; Ollama doesn't require auth by default
     OLLAMA_MODEL: "llama3.2:3b"  # Use the model name you pulled
     
     # Memory settings
     SHORT_MEMORY_SIZE: 20
     LONG_MEMORY_SIZE: 5096
     DISABLE_SHORT_MEMORY: False
     DISABLE_LONG_MEMORY: True
     STREAM: False
     STREAM_TIMEOUT: 30
     ```

5. **Verify the Setup**

   - Test that Ollama is responding:
     ```sh
     curl http://localhost:11434/api/tags
     ```
   - This should return a JSON list of installed models

## Troubleshooting

- **Port Already in Use**: Ollama uses port 11434 by default. If it's in use, you can change the port by setting the `OLLAMA_HOST` environment variable:
  ```sh
  export OLLAMA_HOST=0.0.0.0:11435
  ```
  Then update `OLLAMA_URL` in your `config.yaml` accordingly.

- **Model Not Found**: Ensure you've pulled the model using `ollama pull <model-name>` before running the application.

- **Connection Refused**: Make sure the Ollama service is running. On macOS/Linux, you can restart it with:
  ```sh
  ollama serve
  ```

## API Compatibility

Ollama provides an OpenAI-compatible API endpoint at `http://localhost:11434/v1`, which this application uses. This means you can use the same Python `openai` package to interact with Ollama models.

Return to the [Testing](README.md#testing) and [Usage](README.md#usage) sections in the [Setup Guide](README.md) to verify your setup and run the local agent.
