from typing import List, Dict, Any

import asyncio
import httpx
import json
import requests
import sys

class AnythingLLMClient:
    def __init__(self, config: Dict[str, Any]):
        # general configuration
        self.api_key = config.get("ANYTHINGLLM_API_KEY", None)
        self.stream_timeout = config.get("ANYTHINGLLM_STREAM_TIMEOUT", 30)
        self.workspace = config.get("ANYTHINGLLM_WORKSPACE", "default")
        
        # configure the url
        base_url = config.get("ANYTHINGLLM_URL", "http://localhost:3001/api/v1")
        self.chat_url = f"{base_url}/workspace/{self.workspace}"

        self.headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": "Bearer " + self.api_key
        }  

    def chat(self, message: str) -> str:
        """
        Send a chat request to the model server and return the response
        
        Inputs:
        - message: The message to send to the chatbot
        """
        data = {
            "message": message,
            "mode": "chat",
            "sessionId": "example-session-id",
            "attachments": []
        }

        blocking_chat_url = f"{self.chat_url}/chat"
        chat_response = requests.post(
            blocking_chat_url,
            headers=self.headers,
            json=data
        )

        try:
            return chat_response.json()['textResponse']
        except ValueError:
            return "Response is not valid JSON"
        except Exception as e:
            return f"Chat request failed. Error: {e}"
        
    def streaming_chat(self, message: str) -> None:
        """
        Wrapper to run the asynchronous streaming chat.
        """
        asyncio.run(self._streaming_chat_async(message))

    async def _streaming_chat_async(self, message: str) -> None:
        """
        Stream chat responses asynchronously from the model server and display them in real-time.
        Buffers incomplete JSON chunks until a full chunk (terminated by newline) is collected.
        """

        data = {
            "message": message,
            "mode": "chat",
            "sessionId": "example-session-id",
            "attachments": []
        }

        buffer = ""
        try:
            async with httpx.AsyncClient(timeout=self.stream_timeout) as client:
                async with client.stream("POST", F"{self.chat_url}/stream-chat", headers=self.headers, json=data) as response:
                    print("Agent: ", end="")
                    async for chunk in response.aiter_text():
                        if chunk:
                            buffer += chunk
                            # Process each complete line
                            while "\n" in buffer:
                                line, buffer = buffer.split("\n", 1)
                                if line.startswith("data: "):
                                    line = line[len("data: "):]
                                try:
                                    parsed_chunk = json.loads(line.strip())
                                    print(parsed_chunk.get("textResponse", ""), end="", flush=True)

                                    if parsed_chunk.get("close", False):
                                        print("")
                                except json.JSONDecodeError:
                                    # The line is not a complete JSON; wait for more data.
                                    continue
                                except Exception as e:
                                    # generic error handling, quit for debug
                                    print(f"Error processing chunk: {e}")
                                    sys.exit()
        except httpx.RequestError as e:
            print(f"Streaming chat request failed. Error: {e}")

def concat_messages(messages: List[Dict[str, str]]) -> str:
    """Concatenate a list of message dictionaries into a single string."""
    result = []
    for msg in messages:
        role = msg.get('role', '')
        content = msg.get('content', '')
        if role and content:
            result.append(f"{role}: {content}")
    return "\n".join(result)

def setup_anythingllm_client(
    config: Dict[str, Any]
) -> AnythingLLMClient:
    return AnythingLLMClient(config)

def anythingllm_chat_completion(
    client: AnythingLLMClient,
    messages: List[Dict[str, str]],
    temperature: float = 0.7,
    stream: bool = False
) -> Any:
    """Send messages to the AnythingLLM language model and get a response."""
    if stream:
        return client.streaming_chat(concat_messages(messages))
    else:
        return client.chat(concat_messages(messages))
