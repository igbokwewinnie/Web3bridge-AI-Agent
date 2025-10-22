import os
from dotenv import load_dotenv
import asyncio
from . import ingest, search_agent, logs

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")



REPO_OWNER = "Bloceducare"
REPO_NAME = "Web3bridge-Web3-Cohort-XIII"

def initialize_index():
    print(f"Starting Web3Bridge Agent for {REPO_OWNER}/{REPO_NAME}")
    index = ingest.index_data(REPO_OWNER, REPO_NAME, chunk=True)
    print("Index built successfully!")
    return index

def initialize_agent(index):
    print("Initializing agent...")
    agent = search_agent.init_agent(REPO_OWNER, REPO_NAME)
    print("Agent initialized successfully!")
    return agent

def main():
    index = initialize_index()
    agent = initialize_agent(index)

    print("\nReady to answer questions! Type 'stop' to exit.\n")

    while True:
        question = input("Your question: ")
        if question.strip().lower() == "stop":
            print("Goodbye!")
            break

        print("Processing your question...")
        # Run the agent asynchronously
        response = asyncio.run(agent.run(user_prompt=question))
        logs.log_interaction_to_file(agent, response.new_messages())

        # Print the agent's output
        print("\nResponse:\n", response.output)
        print("\n" + "="*50 + "\n")


if __name__ == "__main__":
    main()