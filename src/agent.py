import re
from typing import List
from src.model import ModelInterface
from src.tools import Tool

class Agent:
    def __init__(
        self,
        tools: List[Tool],
        identity: str
    ):
        # model used by the agent
        self.model = ModelInterface()

        # tools available to the agent
        self.tools = {tool.name: tool for tool in tools}

        # system instructions for the agent
        self.core_identity = identity

        # long term memory of the agent
        self.long_term_memory = []

        # short term history of the agent
        self.short_term_memory = []

        # set-up transcript for debugging/analysis/oversight
        # write directly to a new file in transcripts for each session
        # file name is timestamped + transcript as so: transcripts/transcript_<timestamp>.txt

    ###
    # When building a prompt for the model, include:
    # 1. The core identity/instructions of the agent
    # 2. The long-term memory of the agent, summarized as a page that is regularly updated as messages drop off the short-term history
    # 3. The recent short-term history of interactions
    # 4. The current user input

    async def chat_completion(
        self,
        user_input: str,
    ) -> str:
        history = [
            {"role": "system", "content": self.core_identity},
            {"role": "user", "content": user_input}
        ]
        tool_call_pattern = re.compile(r"^(\w+)\((.*)\)$", re.DOTALL)

        # call the model with the initial request
        response = self.model.chat_completion(history)
        
        # check the output for a response
        match = tool_call_pattern.match(response.strip())
        
        if match:
            # call tool if a tool call is found
            name, arg = match.groups()
            tool = self.tools.get(name)
            if tool:
                # Handle tools with or without arguments
                result = tool.run(arg) if arg else tool.run("")
                history.append({"role": "assistant", "content": response})
                history.append({"role": "tool", "content": result})
                return result.strip()
        else:
            # Not a tool call: treat as final answer
            history.append({"role": "assistant", "content": response})
            return response.strip()