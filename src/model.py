import yaml
from typing import List, Dict, Any
# from openai import OpenAI

from src.models.lmstudio import setup_lm_studio_client, lmstudio_chat_completion

# A message is a dictionary with a role and content
Message = Dict[str, str]

class ModelInterface:
    def __init__(self):
        """Initialize the model interface."""
        # read the configuration file
        with open("config.yaml", "r") as f:
            config = yaml.safe_load(f)
        
        # initialize the model parameters
        self.model = config.get("MODEL", "hugging-quants/llama-3.2-3b-instruct")
        self.model_provider = config.get("MODEL_PROVIDER", None)
        self.client = self._setup_client(config)

    def _setup_client(self, config: Dict[str, Any]):
        """Setup the model client based on the provider."""
        if not self.model_provider:
            raise ValueError("MODEL_PROVIDER is not set in config.yaml")
        
        if self.model_provider.lower() == "anythingllm":
            raise NotImplementedError("AnythingLLM support is not implemented yet.")
        elif self.model_provider.lower() == "lmstudio":
            return setup_lm_studio_client(config)
        elif self.model_provider.lower() == "nexa":
            raise NotImplementedError("Nexa support is not implemented yet.")
        else:
            raise ValueError(f"Unsupported MODEL_PROVIDER: {self.model_provider}")

    def chat_completion(
        self,
        messages: List[Message],
        temperature: float = 0.7,
        stream: bool = False
    ) -> Any:
        """Send messages to the language model and get a response."""
        if not self.model_provider:
            raise ValueError("MODEL_PROVIDER is not set in config.yaml")
        
        if self.model_provider.lower() == "anythingllm":
            raise NotImplementedError("AnythingLLM support is not implemented yet.")
        elif self.model_provider.lower() == "lmstudio":
            return lmstudio_chat_completion(
                client=self.client,
                model=self.model,
                messages=messages,
                temperature=temperature,
                stream=stream
            )
        elif self.model_provider.lower() == "nexa":
            raise NotImplementedError("Nexa support is not implemented yet.")
        else:
            raise ValueError(f"Unsupported MODEL_PROVIDER: {self.model_provider}")
    
    # def lmstudio_chat_completion(
    #     self,
    #     messages: List[Dict[str, str]],
    #     temperature: float = 0.7,
    #     stream: bool = False
    # ) -> Any:
    #     """Send messages to the LM Studio language model and get a response."""
    #     if stream:
    #         return self.client.chat.completions.acreate(
    #             model=self.model,
    #             messages=messages,
    #             temperature=temperature,
    #             stream=stream
    #         )
        
    #     # Non-streaming response
    #     resp = self.client.chat.completions.create(
    #         model=self.model,
    #         messages=messages,
    #         temperature=temperature
    #     )
    #     return resp.choices[0].message.content