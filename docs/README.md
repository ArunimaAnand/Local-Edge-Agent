# Local Agent Setup and Usage Guide

Use this guide to setup and configure the Local Agent with your choice of local LLM backend.

### Table of Contents
- [Setup](#setup)
- [Usage](#usage)

## Setup
1. Clone the repository:
    ```sh
    git clone https://github.com/thatrandomfrenchdude/local-agent.git
    cd local-agent
    ```
2. Create your configuration file `config.yaml` in the project root using the following template:

   ```yaml
   # general variables
    MODEL_PROVIDER: "your-provider-here"  # options: anythingllm, lmstudio, nexa

    # AnythingLLM configuration
    ANYTHINGLLM_API_KEY: "your-api-key"
    ANYTHINGLLM_WORKSPACE: "local-agent"
    ANYTHINGLLM_URL: "http://localhost:3001/api/v1"

    # LM Studio configuration
    LM_STUDIO_API_KEY: "lm-studio"
    LM_STUDIO_MODEL: "hugging-quants/llama-3.2-3b-instruct"
    LM_STUDIO_URL: "http://localhost:1234/v1"

    # Nexa configuration
    NEXA_API_KEY: "nexa"
    NEXA_URL: "http://127.0.0.1:18181/v1/chat/completions"
   ```
   Adjust the values as needed for the providers you want to use, sensible defaults have been chosen.
   
   **Note**: You only need to fill in the variables relevant to the model backend(s) you plan to use.
3. Create and activate a virtual environment:
    ```sh
    python3 -m venv venv
    source venv/bin/activate
    ```
4. Install the required dependencies:
    ```sh
    pip install openai pyyaml requests asyncio httpx
    ```
5. Follow the additional instructions for the model backend(s) you want to use:
- [AnythingLLM Backend Instructions](anythingllm_setup.md)
- [LM Studio Backend Instructions](lmstudio_setup.md)
- [Nexa Backend Instructions](nexa_setup.md)

## Usage
1. Ensure your chosen LLM server is running locally.
2. Run the local agent:
    ```sh
    python main.py
    ```