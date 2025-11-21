from typing import List, Dict, Any
from openai import OpenAI

class OllamaClient:
    def __init__(self, config: Dict[str, Any]):
        self.api_key = config.get("OLLAMA_API_KEY", "ollama")
        self.base_url = config.get("OLLAMA_URL", "http://localhost:11434/v1")
        self.model = config.get("OLLAMA_MODEL", "llama3.2:3b")

        self.client = OpenAI(base_url=self.base_url, api_key=self.api_key)

    def chat(self, messages: List[Dict[str, str]], temperature: float = 0.7) -> str:
        """Send a blocking chat request to the Ollama model and return the response."""
        resp = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature
        )
        return resp.choices[0].message.content
    
    def streaming_chat(self, messages: List[Dict[str, str]], temperature: float = 0.7):
        return self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature,
            stream=True
        )

def setup_ollama_client(
    config: Dict[str, Any]
) -> OllamaClient:
    return OllamaClient(config)
