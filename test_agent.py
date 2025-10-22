import os
from dotenv import load_dotenv
import asyncio 
from app.search_agent import init_agent

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise ValueError(" GROQ_API_KEY not found in .env file. Please add it there before running.")

print("GROQ_API_KEY loaded successfully")

print("Initializing agent...")
repo_owner = "Bloceducare"
repo_name = "Web3bridge-Web3-Cohort-XIII"

agent = init_agent(repo_owner, repo_name)


print("\nAgent initialized successfully!")

# Define an async function to query the agent
async def main():
    print("\nRunning agent query...\n")
    response = await agent.run("Give me a summary of this repo")
    print("\n Agent Response:\n", response)

# Run the async function
asyncio.run(main())