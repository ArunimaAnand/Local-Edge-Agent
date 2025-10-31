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
3. Create and activate a virtual environment:
    ```sh
    python3 -m venv venv
    source venv/bin/activate
    ```

From here, please navigate to the instructions for the model backend you want to use:
- [AnythingLLM Backend Instructions](#anythingllm-backend)
- [LM Studio Backend Instructions](#lm-studio-backend)
- [Nexa Backend Instructions](#nexa-backend)

## AnythingLLM Backend

### Requirements
- Python 3.8+

### Setup
1. Install and setup [AnythingLLM](https://anythingllm.com/).
    1. Choose AnythingLLM NPU when prompted to choose an LLM provider to target the NPU
    2. Choose a model of your choice when prompted. This sample uses `Llama 3.1 8B Chat` with 8K context
2. Create an AnythingLLM workspace.
    1. Click "+ New Workspace."
    2. Enter the workspace name `local-agent`. If you prefer a different name, choose a simple workspace name as the slug can sometimes change if there are special characters. See the [troubleshooting section](#troubleshooting) below if you have issues.
    3. If you chose a custom workspace name, make sure to update the `ANYTHINGLLM_WORKSPACE` variable in your `config.yaml` file.
3. Generate an API key
    1. Click the settings button on the bottom of the left panel
    2. Open the "Tools" dropdown
    3. Click "Developer API"
    4. Click "Generate New API Key"
    5. Copy the generated key and paste it into the `ANYTHINGLLM_API_KEY` variable in your `config.yaml` file.
4. Open a PowerShell instance and clone the repo
    ```
    git clone https://github.com/thatrandomfrenchdude/simple-npu-chatbot.git
    ```
5. Create and activate your virtual environment with reqs
    ```
    # 1. navigate to the cloned directory
    cd simple-npu-chatbot

    # 2. create the python virtual environment
    python -m venv llm-venv

    # 3. activate the virtual environment
    ./llm-venv/Scripts/Activate.ps1     # windows
    source \llm-venv\bin\activate       # mac/linux

    # 4. install the requirements
    pip install -r requirements.txt
    ```
6. Create your `config.yaml` file with the following variables
    ```
    api_key: "your-key-here"
    model_server_base_url: "http://localhost:3001/api/v1"
    workspace_slug: "your-slug-here"
    stream: true
    stream_timeout: 60
    ```
    Note: The `workspace_slug` should be the name of the workspace you created in step 2.

### Usage
You have the option to use a terminal or gradio chat interface the talk with the bot. After completing setup, run the app you choose from the command line:
```
# terminal
python src/terminal_chatbot.py
```

### Troubleshooting
***AnythingLLM NPU Runtime Missing***<br>
On a Snapdragon X Elite machine, AnythingLLM NPU should be the default LLM Provider. If you do not see it as an option in the dropdown, you downloaded the AMD64 version of AnythingLLM. Delete the app and install the ARM64 version instead.

***Model Not Downloaded***<br>
Sometimes the selected model fails to download, causing an error in the generation. To resolve, check the model in Settings -> AI Providers -> LLM in AnythingLLM. You should see "uninstall" on the model card if it is installed correctly. If you see "model requires download," choose another model, click save, switch back, then save. You should see the model download in the upper right corner of the AnythingLLM window.

## LM Studio Backend

### Requirements

- Python 3.8+
- `openai` and `pyyaml` Python packages
- A running LM Studio server (or compatible OpenAI API endpoint)

---

### Setup Instructions

1. **Start LM Studio**

   - Download and install [LM Studio](https://lmstudio.ai/) if you haven't already.
   - Open LM Studio.

2. **Download and Run a Model in LM Studio**

   - In LM Studio, go to the "Models" tab and download a compatible model (e.g., llama-3.2-3b-instruct).
   - Once downloaded, click "Run" to start the model server.
   - Make sure the "OpenAI Compatible API" is enabled (check the API tab in LM Studio for the server URL, usually `http://localhost:1234/v1`).

3. **Create and Edit the Configuration File**

   Create a file named `config.yaml` in the project root with the following contents (edit values as needed):

   ```yaml
   MODEL: "hugging-quants/llama-3.2-3b-instruct"
   LM_STUDIO_URL: "http://localhost:1234/v1"
   LM_STUDIO_API_KEY: "lm-studio"
   ```

   - `MODEL`: The model name as shown in LM Studio.
   - `LM_STUDIO_URL`: The API URL for your LM Studio server.
   - `LM_STUDIO_API_KEY`: The API key (default for LM Studio is `"lm-studio"`).

4. **Create and Activate a Virtual Environment**

   ```sh
   python3 -m venv venv
   source venv/bin/activate
   ```

   On Windows, activate with:
   ```sh
   venv\Scripts\activate
   ```

5. **Install Dependencies**

   ```sh
   pip install openai pyyaml requests asyncio httpx
   ```

---

### Usage

1. **Start LM Studio** (or another OpenAI-compatible API server) on your machine.

2. **Run the script:**
   ```sh
   python main.py
   ```

   Example output:
   ```
   Agent result: The current time is 2024-06-01 12:34:56
   ```

3. **To run with different user input:**
   Edit the `asyncio.run(agent.run(...))` line in `main.py` with your prompt.

---

## Nexa Backend

### Setup
### Usage