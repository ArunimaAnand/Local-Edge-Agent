

import pytest
import yaml
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from servers.lmstudio import LMStudioClient

def load_config():
    with open("config.yaml", "r") as f:
        return yaml.safe_load(f)

CONFIG = load_config()

def test_server_running():
    import requests
    url = f"{CONFIG['LM_STUDIO_URL']}/models"
    try:
        response = requests.get(url, timeout=5)
        assert response.status_code == 200
    except Exception as e:
        pytest.fail(f"LM Studio server not running or unreachable: {e}")

def test_chat_endpoint():
    client = LMStudioClient(CONFIG)
    messages = [{"role": "user", "content": "Hello, LM Studio!"}]
    reply = client.chat(messages)
    assert isinstance(reply, str)
    assert reply

def test_backend_class_direct():
    """Test direct instantiation and chat method of LMStudioClient backend class."""
    client = LMStudioClient(CONFIG)
    messages = [{"role": "user", "content": "Direct backend test message"}]
    response = client.chat(messages)
    assert isinstance(response, str)
    assert response
