# LM Studio Backend

Before following these steps, ensure you have completed the initial [Setup Guide](README.md).

## Requirements

- Python 3.8+
- `openai` and `pyyaml` Python packages
- A running LM Studio server (or compatible OpenAI API endpoint)

## Setup Instructions

1. **Start LM Studio**

   - Download and install [LM Studio](https://lmstudio.ai/)
   - Open LM Studio.

2. **Download and run a model on the server**

   - In LM Studio, go to the "Models" tab and download a compatible model (e.g., llama-3.2-3b-instruct).
   - Add the model name to the `LM_STUDIO_MODEL` field in your `config.yaml`.
   - Once downloaded, click "Run" to start the model server.
   - Make sure the "OpenAI Compatible API" is enabled (check the API tab in LM Studio for the server URL, usually `http://localhost:1234/v1`).

Return to the [Testing](README.md/#testing) and [Usage](README.md/#usage) sections in the [Setup Guide](README.md) to verify your setup and run the local agent.