import pytest
import yaml
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.servers.ollama import OllamaClient

def load_config():
    with open("config.yaml", "r") as f:
        return yaml.safe_load(f)

CONFIG = load_config()

def test_server_running():
    import requests
    url = f"{CONFIG['OLLAMA_URL'].replace('/v1', '')}/api/tags"
    try:
        response = requests.get(url, timeout=30)
        assert response.status_code == 200
    except Exception as e:
        pytest.fail(f"Ollama server not running or unreachable: {e}")

def test_chat_endpoint():
    client = OllamaClient(CONFIG)
    messages = [{"role": "user", "content": "Hello, Ollama!"}]
    reply = client.chat(messages)
    assert isinstance(reply, str)
    assert reply
