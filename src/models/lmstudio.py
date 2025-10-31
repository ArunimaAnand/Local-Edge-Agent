from typing import List, Dict, Any
from openai import OpenAI

def setup_lm_studio_client(
    config: Dict[str, Any]
) -> OpenAI:
    LM_STUDIO_URL = config.get("LM_STUDIO_URL", "http://localhost:1234/v1")
    LM_STUDIO_API_KEY = config.get("LM_STUDIO_API_KEY", "lm-studio")
    client = OpenAI(base_url=LM_STUDIO_URL, api_key=LM_STUDIO_API_KEY)
    return client

def lmstudio_chat_completion(
    client: OpenAI,
    model: str,
    messages: List[Dict[str, str]],
    temperature: float = 0.7,
    stream: bool = False
) -> Any:
    """Send messages to the LM Studio language model and get a response."""
    if stream:
        return client.chat.completions.acreate(
            model=model,
            messages=messages,
            temperature=temperature,
            stream=stream
        )
    
    # Non-streaming response
    resp = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature
    )
    return resp.choices[0].message.content