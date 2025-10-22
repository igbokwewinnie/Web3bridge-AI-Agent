import os 
from dotenv import load_dotenv
import asyncio
from app.search_agent import init_agent
from app.logs import log_interaction_to_file

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

# Agent setup (use your repo info)
repo_owner = "Bloceducare"
repo_name = "Web3bridge-Web3-Cohort-XIII"

# Initialize your agent
agent = init_agent(repo_owner, repo_name)

async def main():
    # Simulate a user query
    user_query = "Explain what a smart contract is"
    
    # Run the agent
    response = await agent.run(user_query)
    
    # Log the interaction
    log_file = log_interaction_to_file(agent, response.new_messages(), source='user')
    
    print(f" Log saved to: {log_file}")
    print("Sample log entry:")
    with open(log_file, "r", encoding="utf-8") as f:
        import json
        data = json.load(f)
        print(json.dumps(data, indent=2)[:500])  # Print first 500 chars

# Run async main
asyncio.run(main())
