import asyncio

from src.agent import Agent
from src.tools import tools, tool_descriptions

def main():
    # built the agent identity with the system prompt and instructions
    #    - system prompt: tell the agent who it is and what it can do
    #   - instructions: explain how to use the tools
    system_prompt = "You are a tool-calling agent that may use tools by responding according to their instructions.\n"
    instructions = (
        "You may use the following tools to assist with user queries.\n"
        "Avoid using tools if the user query can be answered without them.\n"
        "Here are the tools you can use:\n"
        f"{tool_descriptions}\n"
        "When you decide to use a tool, respond with the format:\n"
        "'ToolName(arg)' where ToolName is the name of the tool and arg is the argument to pass to the tool.\n"
        "If the tool does not require an argument, use 'ToolName()'.\n"
        "Only use one tool per response.\n"
    )
    agent_identity = system_prompt + instructions

    # build the agent for the session
    agent = Agent(
        tools=tools,
        identity=agent_identity
    )

    # run the agent interaction loop
    agent.run()

if __name__ == "__main__":
    main()