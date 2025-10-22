from app.search_tools import SearchTool
from pydantic_ai import Agent

SYSTEM_PROMPT_TEMPLATE = """
You are a Web3 technical assistant trained on materials from the Web3Bridge Cohort XIII program.
You help learners understand Solidity, Hardhat, smart contracts, dApps, and blockchain development.

Use the hybrid search tool to retrieve accurate information from the course materials before answering.
Always cite the source file at the end like this:
*Source:* [filename](https://github.com/{repo_owner}/{repo_name}/blob/main/{{filename}})

If no relevant material is found, provide a general but helpful explanation.
"""

def init_agent(repo_owner, repo_name):
    system_prompt = SYSTEM_PROMPT_TEMPLATE.format(repo_owner=repo_owner, repo_name=repo_name)

    search_tool = SearchTool(repo_owner, repo_name)

    agent = Agent(
        name="web3bridge_agent",
        system_prompt=system_prompt,
        tools=[search_tool.hybrid_search],
        model="groq:llama-3.1-8b-instant"
    )

    return agent
