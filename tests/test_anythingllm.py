

import pytest
import requests
import yaml
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from servers.anythingllm import AnythingLLMClient

def load_config():
    with open("config.yaml", "r") as f:
        return yaml.safe_load(f)

CONFIG = load_config()

def test_server_running():
    url = f"{CONFIG['ANYTHINGLLM_URL']}/workspace/{CONFIG['ANYTHINGLLM_WORKSPACE']}/chat"
    try:
        response = requests.post(
            url,
            headers={"Authorization": "Bearer " + CONFIG["ANYTHINGLLM_API_KEY"]},
            json={"message": "ping", "mode": "chat", "sessionId": "pytest-session", "attachments": []},
            timeout=30
        )
        assert response.status_code == 200
    except Exception as e:
        pytest.fail(f"Server not running or unreachable: {e}")

def test_chat_endpoint():
    client = AnythingLLMClient(CONFIG)
    reply = client.chat("Hello, AnythingLLM!")
    assert isinstance(reply, str)
    assert reply != "Response is not valid JSON"
    assert not reply.startswith("Chat request failed")

def test_backend_class_direct():
    """Test direct instantiation and chat method of AnythingLLMClient backend class."""
    client = AnythingLLMClient(CONFIG)
    response = client.chat("Direct backend test message")
    assert isinstance(response, str)
    assert response != "Response is not valid JSON"
    assert not response.startswith("Chat request failed")
