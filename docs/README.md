# Local Agent Setup Guide

Use this guide to setup and configure the Local Agent with your choice of local LLM backend.

## General Setup
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
- [AnythingLLM Backend Instructions](#anythingllm-backend)
- [LM Studio Backend Instructions](#lm-studio-backend)
- [Nexa Backend Instructions](#nexa-backend)

---

## AnythingLLM Backend

### Requirements
- Python 3.8+

### Setup
1. **Start AnythingLLM**
    - Download and install [AnythingLLM](https://anythingllm.com/).
    - Open AnythingLLM.
2. **Set up the NPU Runtime**
    - Choose `AnythingLLM NPU` when prompted to choose an LLM provider to target the NPU
3. **Download and Run a Model**
    - This sample uses `Llama 3.1 8B Chat` with 8K context
    - The model will take some time to download depending on your internet speed
    - Sometimes a model failes to download properly. See the [troubleshooting section](#troubleshooting) section below if you have issues.
4. **Create a Workspace**
    - Click "+ New Workspace."
    - Enter the workspace name `local-agent`. If you prefer a different name, choose a simple workspace name as the slug can sometimes change if there are special characters. See the [troubleshooting section](#troubleshooting) below if you have issues.
    - If you chose a custom workspace name, make sure to update the `ANYTHINGLLM_WORKSPACE` variable in your `config.yaml` file.
5. **Generate an API key**
    - Click the settings button on the bottom of the left panel
    - Open the "Tools" dropdown
    - Click "Developer API"
    - Click "Generate New API Key"
    - Copy the generated key and paste it into the `ANYTHINGLLM_API_KEY` variable in your `config.yaml` file.

### Troubleshooting
***AnythingLLM NPU Runtime Missing***<br>
On a Snapdragon X Elite machine, AnythingLLM NPU should be the default LLM Provider. If you do not see it as an option in the dropdown, you downloaded the AMD64 version of AnythingLLM. Delete the app and install the ARM64 version instead.

***Model Not Downloaded***<br>
Sometimes the selected model fails to download, causing an error in the generation. To resolve, check the model in Settings -> AI Providers -> LLM in AnythingLLM. You should see "uninstall" on the model card if it is installed correctly. If you see "model requires download," choose another model, click save, switch back, then save. You should see the model download in the upper right corner of the AnythingLLM window.

---

## LM Studio Backend

### Requirements

- Python 3.8+
- `openai` and `pyyaml` Python packages
- A running LM Studio server (or compatible OpenAI API endpoint)

### Setup Instructions

1. **Start LM Studio**

   - Download and install [LM Studio](https://lmstudio.ai/)
   - Open LM Studio.

2. **Download and Run a Model**

   - In LM Studio, go to the "Models" tab and download a compatible model (e.g., llama-3.2-3b-instruct).
   - Add the model name to the `LM_STUDIO_MODEL` field in your `config.yaml`.
   - Once downloaded, click "Run" to start the model server.
   - Make sure the "OpenAI Compatible API" is enabled (check the API tab in LM Studio for the server URL, usually `http://localhost:1234/v1`).

---

## Nexa Backend

### Setup
### Usage