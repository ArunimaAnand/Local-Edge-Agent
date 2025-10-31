from typing import List, Dict, Any
from openai import OpenAI

class LMStudioClient:
    def __init__(self, config: Dict[str, Any]):
        self.api_key = config.get("LM_STUDIO_API_KEY", "lm-studio")
        self.base_url = config.get("LM_STUDIO_URL", "http://localhost:1234/v1")
        self.model = config.get("LM_STUDIO_MODEL", "hugging-quants/llama-3.2-3b-instruct")

        self.client = OpenAI(base_url=self.base_url, api_key=self.api_key)

    def chat(self, messages: List[Dict[str, str]], temperature: float = 0.7) -> str:
        """Send a blocking chat request to the LM Studio model and return the response."""
        resp = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature
        )
        return resp.choices[0].message.content
    
    def streaming_chat(self, messages: List[Dict[str, str]], temperature: float = 0.7):
        return self.client.chat.completions.acreate(
            model=self.model,
            messages=messages,
            temperature=temperature,
        )

def setup_lm_studio_client(
    config: Dict[str, Any]
) -> LMStudioClient:
    return LMStudioClient(config)

def lmstudio_chat_completion(
    client: LMStudioClient,
    messages: List[Dict[str, str]],
    temperature: float = 0.7,
    stream: bool = False
) -> Any:
    """Send messages to the LM Studio language model and get a response."""
    if stream:
        return client.streaming_chat(messages, temperature=temperature)
    else:
        return client.chat(messages, temperature=temperature)