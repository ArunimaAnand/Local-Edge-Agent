import asyncio

from src.agent import Agent
from src.tools import tools, tool_descriptions

def main():
    # set the system prompt and instructions for the agent
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

    agent = Agent(
        tools=tools,
        instructions=system_prompt + instructions
    )

    print("Type 'exit' or 'quit' to end the chat.")
    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in {"exit", "quit"}:
            print("Goodbye!")
            break
        result = asyncio.run(agent.run(user_input))
        print(f"Agent: {result}")

if __name__ == "__main__":
    main()