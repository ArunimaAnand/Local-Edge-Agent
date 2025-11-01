# AnythingLLM Backend

## Requirements
- Python 3.8+

## Setup
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

## Troubleshooting
***AnythingLLM NPU Runtime Missing***<br>
On a Snapdragon X Elite machine, AnythingLLM NPU should be the default LLM Provider. If you do not see it as an option in the dropdown, you downloaded the AMD64 version of AnythingLLM. Delete the app and install the ARM64 version instead.

***Model Not Downloaded***<br>
Sometimes the selected model fails to download, causing an error in the generation. To resolve, check the model in Settings -> AI Providers -> LLM in AnythingLLM. You should see "uninstall" on the model card if it is installed correctly. If you see "model requires download," choose another model, click save, switch back, then save. You should see the model download in the upper right corner of the AnythingLLM window.
