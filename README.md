# Local Agent

A simple Python agent framework that connects to a local LLM (via LM Studio) and can call custom Python tools/functions based on LLM output. The agent interprets LLM responses, detects tool calls, executes them, and returns the final answer.

**Features:**
- Connects to a local LLM server (AnythingLLM, LM Studio, and Nexa)
- Supports tool use to expand LLM capabilities
- Easily extensible with custom tools

### Table of Contents
- [Setup](#setup)
- [Quick Start](#quick-start)
- [Adding More Tools](#adding-more-tools)
- [Contributing](#contributing)
- [License](#license)

---

## Setup

The local component **requires** you to have an LLM server configured and running on your machine. Please refer to the [Setup Guide](docs/README.md) for detailed setup and usage instructions.

## Quick Start
This Quickstart assumes you have setup the LM Studio server, properly configured the `config.yaml` file as per the [Setup Guide](docs/README.md).
1. setup and activate a virtual environment
   ```sh
   python3 -m venv venv
   source venv/bin/activate
   ```
2. Install dependencies
   ```sh
   pip install openai httpx pyyaml requests
   ```
3. Run the local agent
   ```sh
   python main.py
   ```

## Adding More Tools

You can add new tools by defining a Python function and registering it with the agent.

### 1. Define your tool function

```python
def my_tool(arg: str) -> str:
    # Your logic here
    return f"Processed: {arg}"
```

### 2. Create a `Tool` object

```python
from src.tools import Tool

my_tool_obj = Tool(
    "MyTool",
    my_tool,
    "Describe what your tool does. Usage: MyTool(argument)"
)
```

### 3. Add it to the `tools` list

```python
tools = [
    Tool(
        "Echo",
        echo_tool,
        "Prints the input text prefixed with ECHO. Usage: return the string 'Echo(<text>)' where <text> is the text to echo."
    ),
    Tool(
        "Time",
        time_tool,
        "Prints the current date and time. Usage: return the string 'Time()'"
    ),
    my_tool_obj,  # Add your tool here
]
```

### 4. Update the instructions (handled automatically in the script)

The script will automatically include your tool in the agent's instructions.

---

## Contributing
I welcome contributions! Please follow these steps:
1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes, commit them, and push to your branch.
4. Create a pull request explaining your changes.

---

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---