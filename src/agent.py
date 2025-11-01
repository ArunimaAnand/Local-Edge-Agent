import asyncio
import os
import re
import yaml

from typing import List
from src.model import ModelInterface
from src.tools import Tool

class Agent:
    def __init__(
        self,
        tools: List[Tool],
        identity: str
    ):
        # temporarily read in the configuration for the agent
        # TODO: scope the configuration to only read the agent vars into a dict
        with open("config.yaml", "r") as f:
            config = yaml.safe_load(f)

        # model used by the agent
        self.model = ModelInterface()

        # tools available to the agent
        self.tools = {tool.name: tool for tool in tools}

        # system instructions for the agent
        self.core_identity = identity

        # long term memory of the agent
        self.long_memory = ""
        self._max_long_memory = config.get("LONG_MEMORY_SIZE", 5096) # tokens

        # short term history of the agent
        self.short_memory = []
        self._max_short_memory = config.get("SHORT_MEMORY_SIZE", 20) # messages

        # set-up transcript for debugging/analysis/oversight
        # write directly to a new file in transcripts for each session
        # file name is timestamped + transcript as so: transcripts/transcript_<timestamp>.txt
        self.transcript_file = f"transcripts/transcript_{self._get_timestamp()}.txt"

    def run(self) -> None:
        """Run the agent loop."""
        print("Type 'exit' or 'quit' to end the chat.")

        # setup the transcript file
        with open(self.transcript_file, "w") as f:
            f.write("Agent Transcript\n")
            f.write("================\n\n")
        
        # interaction loop
        while True:
            user_input = input("You: ").strip()
            if user_input.lower() in {"exit", "quit"}:
                print("Goodbye!")
                break
            result = asyncio.run(self.chat_completion(user_input))
            print(f"Agent: {result}")

            # log the interaction to the transcript file
            with open(self.transcript_file, "a") as f:
                f.write(f"You: {user_input}\n\n")
                f.write(f"Agent: {result}\n\n")

        # close the transcript file, deleting if empty
        if os.path.getsize(self.transcript_file) == 0:
            os.remove(self.transcript_file)
        else:
            with open(self.transcript_file, "a") as f:
                f.write("================\n\n")

    ###
    # When building a prompt for the model, include:
    # 1. The core identity/instructions of the agent
    # 2. The long-term memory of the agent, summarized as a page that is regularly updated as messages drop off the short-term history
    # 3. The recent short-term history of interactions
    # 4. The current user input

    def _build_prompt(self, user_input: str) -> List[dict]:
        """Build a prompt for the model, including identity, memory, and recent interactions."""
        messages = [{"role": "system", "content": self.core_identity}]

        if self.long_memory:
            messages.append({"role": "system", "content": f"Long-Term Memory:\n{self.long_memory}"})

        if self.short_memory:
            messages.append({"role": "system", "content": "Recent Interactions:"})
            for message in self.short_memory:
                role = message["role"]
                content = message["content"]
                messages.append({"role": "system", "content": f"{role.capitalize()}: {content}"})

        messages.append({"role": "user", "content": user_input})

        print(f"Input Messages: {messages}")  # Debugging output

        return messages
    
    def _handle_memory(self, user_input: str, assistant_response: str) -> None:
        """Update the agent's memory with the latest interaction."""
        print("Updating memory...")
        # add to short-term memory
        self.short_memory.append({"role": "user", "content": user_input})
        self.short_memory.append({"role": "assistant", "content": assistant_response})

        # trim short-term memory if it exceeds max size
        popped_messages = []
        while len(self.short_memory) > self._max_short_memory:
            popped_messages.append(self.short_memory.pop(0))  # remove oldest message

        # update long-term memory when messages are popped from short-term memory
        if popped_messages:
            # build the summary prompt
            instruction_content = (
                "Use the following messages to update the long-term memory summary of an agent."
                "This will replace the existing long-term memory summary, so combine the old and new information."
                "The long-term memory should broadly capture the agent context over time in a concise manner."
                "You will receive the existing long-term memory summary in <long> tags, a series of messages that have just dropped off the short-term history in <messages> tags, and the short term-memory in <short> tags."
                "Use this information to create an updated long-term memory summary without duplicating the short-term memory."
                "Keep the size of the summary approximately 5096 tokens or less."
            )

            # collapse the memory messages into the prompt
            summary_content = f"<long>{self.long_memory}</long>\n<messages>"
            for msg in popped_messages:
                summary_content += f"<{msg['role']}>{msg['content']}</{msg['role']}>\n"
            summary_content += "</messages>\n<short>"
            for msg in self.short_memory:
                summary_content += f"<{msg['role']}>{msg['content']}</{msg['role']}>\n"
            summary_content += "</short>"

            # combine the instruction and content
            instruction_content += "\n\n" + summary_content

            summary_prompt = [
                {"role": "system", "content": instruction_content},
            ]
            # get the summary from the model
            summary = self.model.chat_completion(summary_prompt)
            
            # replace the long-term memory with the new summary
            self.long_memory = summary.strip()

        print("Memory updated.")

    async def chat_completion(
        self,
        user_input: str,
    ) -> str:
        # history = [
        #     {"role": "system", "content": self.core_identity},
        #     {"role": "user", "content": user_input}
        # ]
        messages = self._build_prompt(user_input)

        tool_call_pattern = re.compile(r"^(\w+)\((.*)\)$", re.DOTALL)

        # call the model with the initial request and check for tool calls
        response = self.model.chat_completion(messages)
        match = tool_call_pattern.match(response.strip())
        
        if match:
            # call tool if a tool call is found
            name, arg = match.groups()
            tool = self.tools.get(name)
            if tool:
                # Handle tools with or without arguments
                result = tool.run(arg) if arg else tool.run("")
                # history.append({"role": "assistant", "content": response})
                # history.append({"role": "tool", "content": result})
                # return result.strip()
        else:
            # Not a tool call: treat as final answer
            # history.append({"role": "assistant", "content": response})
            result = response
        result = result.strip()
        
        # update memory with the interaction
        self._handle_memory(user_input, result)
        
        # print the new memory states for debugging
        print("Long-Term Memory:", self.long_memory)
        print("Short-Term Memory:", self.short_memory)

        return result
        
    def _get_timestamp(self) -> str:
        from datetime import datetime
        now = datetime.now()
        return now.strftime("%Y%m%d_%H%M%S")