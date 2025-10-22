import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app.search_tools import SearchTool

print("Initializing hybrid search...")

tool = SearchTool(repo_owner="Bloceducare", repo_name="Web3bridge-Web3-Cohort-XIII")

print("Performing hybrid search for 'smart contracts'...\n")

results = tool.hybrid_search("smart contracts", num_results=3)

if not results:
    print("No results found.")
else:
    for i, r in enumerate(results, 1):
        print(f"\nResult {i}:")
        print(f"File: {r.get('filename', 'unknown')}")
        snippet = r.get('content', '') or r.get('section', '')
        print(f"Snippet: {snippet[:200]}")


