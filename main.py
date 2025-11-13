import asyncio
import yaml

from src.agent import Agent
from src.tools import tools, tool_descriptions

def agent_identity() -> str:
    """Build the agent identity with system prompt and instructions."""
    system_prompt = "You are a tool-calling agent that may use tools by responding according to their instructions.\n"
    instructions = (
        "You may use the following tools to assist with user queries.\n"
        "Avoid using tools if the user query can be answered without them.\n"
        "Here are the tools you can use:\n"
        f"{tool_descriptions}\n"
        "When you decide to use a tool, respond with the format:"
        "'ToolName(arg)' where ToolName is the name of the tool and arg is the argument to pass to the tool."
        "If the tool does not require an argument, use 'ToolName()'.\n"
        "Only use one tool per response.\n"
    )
    return system_prompt + instructions

def main():
    config = yaml.safe_load(open("config.yaml"))

    retriever = None
    if config.get("RETRIEVAL_ENABLED", False):
        from src.retrieval.vector_store import VectorStore
        from src.retrieval.embedding import Embeddings
        from sentence_transformers import SentenceTransformer
        
        embeddings = Embeddings(SentenceTransformer(config.get("EMBEDDING_MODEL", "all-MiniLM-L6-v2")))
        vector_store = VectorStore(
            index_path=config.get("FAISS_INDEX_PATH", "faiss_index.index"),
            metadata_path=config.get("METADATA_PATH", "metadata.jsonl")
        )
        retriever = {
            "vector_store": vector_store,
            "embeddings": embeddings,
            "top_k": config.get("RETRIEVAL_TOP_K", 5)
        }

    agent = Agent(
        tools=tools,
        identity=agent_identity()
    )
    agent.run()

if __name__ == "__main__":
    main()