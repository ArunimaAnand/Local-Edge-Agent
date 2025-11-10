from datetime import datetime
from typing import Callable
from googlesearch import search

class Tool:
    def __init__(self, name: str, func: Callable[[str], str], description: str):
        self.name = name
        self.func = func
        self.description = description

    def run(self, arg: str) -> str:
        return self.func(arg) if arg != "" else self.func()

# Example prompt to use the time tool: "What time is it?"
def time_tool() -> str:
    now = datetime.now()
    return f"The current time is {now.strftime('%I:%M%p').lstrip('0').lower()} on {now.strftime('%d %B %Y')}"

def web_search_tool(query: str) -> str:
    """
    Performs a web search using Google and returns formatted results.
    
    Args:
        query: The search query string
        
    Returns:
        A formatted string with search results including titles, URLs, and descriptions
    """
    try:
        results = search(query, advanced=True, num_results=5)
        
        if not results:
            return "No search results found."
        
        output = f"Search results for '{query}':\n\n"
        for i, result in enumerate(results, 1):
            output += f"{i}. {result.title}\n"
            output += f"   URL: {result.url}\n"
            if result.description:
                output += f"   {result.description}\n"
            output += "\n"
        
        return output.strip()
    except Exception as e:
        return f"Error performing web search: {str(e)}"

# Define available tools
tools = [
    Tool(
        "Time",
        time_tool,
        "Prints the current date and time. Usage: return 'Time()'"
    ),
    Tool(
        "WebSearch",
        web_search_tool,
        "Searches the web for information. Usage: return 'WebSearch(\"your query here\")'"
    )
]
# Build tool descriptions for the instructions
tool_descriptions = "\n".join(
    f"- {tool.name}: {tool.description}" for tool in tools
)