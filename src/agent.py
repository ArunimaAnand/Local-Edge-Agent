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
        identity: str,
        retriever: dict = None,
    ):
        # temporarily read in the configuration for the agent
        # TODO: scope the configuration to only read the agent vars into a dict
        with open("config.yaml", "r") as f:
            config = yaml.safe_load(f)

        # # # # core agent configuration # # # #
        
        self.model = ModelInterface()  # model used by the agent
        self.tools = {tool.name: tool for tool in tools}  # tools available to the agent
        self.core_identity = identity  # system instructions for the agent
        self.retriever = retriever  # context retriever (if any)
        # # # # # # # # # # # # # # # # # # # #

        # # # # agent memory management # # # #
        self.long_memory = ""
        self._max_long_memory = config.get("LONG_MEMORY_SIZE", 5096) # tokens
        self._disable_long_memory = config.get("DISABLE_LONG_MEMORY", True)

        self.short_memory = []
        self._max_short_memory = config.get("SHORT_MEMORY_SIZE", 20) # messages
        self._disable_short_memory = config.get("DISABLE_SHORT_MEMORY", False)
        # # # # # # # # # # # # # # # # # # # #

        # conversation transcripts for debugging/analysis/oversight
        self.transcript_file = f"transcripts/transcript_{self._get_timestamp()}.txt"

        # tool call pattern
        self.tool_call_pattern = re.compile(r"^(\w+)\((.*)\)$", re.DOTALL)

    def run(self) -> None:
        """Run the agent loop."""
        print("Type 'exit' or 'quit' to end the chat.")

        file_header = "Agent Transcript\n================\n\n"
        file_footer = "================\n\n"

        # setup the transcript file
        with open(self.transcript_file, "w") as f:
            f.write(file_header)
        
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
        with open(self.transcript_file, "r") as f:
            content = f.read()
        if content == file_header:
            os.remove(self.transcript_file)
        else:
            with open(self.transcript_file, "a") as f:
                f.write(file_footer)

    async def chat_completion(
        self,
        user_input: str,
    ) -> str:
        """
        Process a user input, potentially invoking tools, and manage memory.

        Args:
            user_input (str): The current input from the user.
        """
        messages = self._build_prompt(user_input)

        # call the model with the initial request and check for tool calls
        response = self.model.chat_completion(messages)
        match = self.tool_call_pattern.match(response.strip())
        
        # process the response
        result = ""
        if match:
            # call tool if a tool call is found
            name, arg = match.groups()
            tool = self.tools.get(name)
            if tool:
                result = tool.run(arg) if arg else tool.run("")
        else:
            result = response
        result = result.strip()
        
        # update memory with the interaction
        self._handle_memory(user_input, result)

        return result

    def _build_prompt(self, user_input: str) -> List[dict]:
        """
        Build a prompt for the model, including identity, memory, and recent interactions.
        
        1. The core identity/instructions of the agent
        2. The long-term memory of the agent, summarized as a page that is regularly updated as messages drop off the short-term history
        3. The recent short-term history of interactions
        4. The current user input

        Args:
            user_input (str): The current input from the user.

        """
        
        # start with the core identity
        messages = [{"role": "system", "content": self.core_identity}]

        # then include the long-term memory for broad context (if enabled)
        if not self._disable_long_memory and self.long_memory:
            messages.append({"role": "system", "content": f"Long-Term Memory:\n{self.long_memory}"})

        # next, include the short-term memory for recent events
        if self.short_memory:
            messages.append({"role": "system", "content": "Recent Interactions:"})
            for message in self.short_memory:
                role = message["role"]
                content = message["content"]
                messages.append({"role": "system", "content": f"{role.capitalize()}: {content}"})
        
        # deepen the context with retrieved documents (if retriever is set)
        # TODO: test and extend
        if self.retriever:
            retrieved_docs = self.retriever.retrieve(user_input)
            if retrieved_docs:
                retrieval_content = "Relevant Documents:\n"
                for i, doc in enumerate(retrieved_docs, 1):
                    retrieval_content += f"Document {i} (Source: {doc.get('source', 'unknown')}):\n{doc.get('text', '')}\n\n"
                messages.append({"role": "system", "content": retrieval_content.strip()})

        # finally, add the current user input
        messages.append({"role": "user", "content": user_input})
        return messages
    
    def _handle_memory(self, user_input: str, assistant_response: str) -> None:
        """
        Update the agent's short-term and long-term memory based on the latest interaction.

        Args:
            user_input (str): The latest input from the user.
            assistant_response (str): The latest response from the agent.
        """
        if self._disable_short_memory:
            pass

        self.short_memory.append({"role": "user", "content": user_input})
        self.short_memory.append({"role": "assistant", "content": assistant_response})

        popped_messages = []
        while len(self.short_memory) > self._max_short_memory:
            popped_messages.append(self.short_memory.pop(0))

        # handle long memory update
        if popped_messages and not self._disable_long_memory:
            # Flatten messages for readability
            popped_messages_text = "\n".join(
                f"{msg['role'].capitalize()}: {msg['content']}" for msg in popped_messages
            )
            short_memory_text = "\n".join(
                f"{msg['role'].capitalize()}: {msg['content']}" for msg in self.short_memory
            )

            instruction_content = (
                "Update the long-term memory summary for this agent.\n"
                "Previous summary:\n"
                f"{self.long_memory}\n\n"
                "Messages that just dropped off short-term memory:\n"
                f"{popped_messages_text}\n\n"
                "Current short-term memory:\n"
                f"{short_memory_text}\n\n"
                "Please write a concise English summary that includes important context from all of the above, "
                "without duplicating short-term memory. Respond in English only."
            )

            summary_prompt = [
                {"role": "system", "content": instruction_content},
            ]
            summary = self.model.chat_completion(summary_prompt)
            self.long_memory = summary.strip()
        
    def _get_timestamp(self) -> str:
        """Get a timestamp string for filenames."""
        from datetime import datetime
        now = datetime.now()
        return now.strftime("%Y%m%d_%H%M%S")