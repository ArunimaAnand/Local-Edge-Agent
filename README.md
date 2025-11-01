# Local Agent

An Edge Agent framework built in pure Python that connects to an edge language model server.

**Features:**
- Connects to a local language model server (AnythingLLM, LM Studio, and Nexa)
- Supports tool use to expand language model capabilities
- Easily extensible with custom tools

### Table of Contents
- [Quick Start](#quick-start)
- [Contributing](#contributing)
- [License](#license)

## Quick Start

1. Refer to the [Setup Guide](docs/README.md) to configure the application.
2. Create a virtual environment and install Python dependencies:
   ```sh
   python3 -m venv venv
   
   # Windows PowerShell
   .\venv\Scripts\Activate.ps1
   
   # Mac/Linux
   source venv/bin/activate
   
   pip install openai httpx pyyaml requests pytest
   ```
3. Run the tests to verify the configuration
   ```
   # Windows PowerShell
    .\scripts\run_tests.ps1 -l

   # Mac/Linux
   ./scripts/run_tests.sh -l
   ```
4. Run the local agent
   ```sh
   python main.py
   ```

## Contributing

I welcome contributions! Please follow these steps:
1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes, commit them, and push to your branch.
4. Create a pull request explaining your changes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.