from typing import List, Any
from app.ingest import index_data

class SearchTool:
    def __init__(self, repo_owner: str, repo_name: str):
        print(f"Loading and indexing repository: {repo_owner}/{repo_name}")
        self.index = index_data(repo_owner, repo_name, chunk=True)
        print("Index built successfully!")

    def hybrid_search(self, query: str, num_results: int = 5) -> List[Any]:
        """

        Perform a hybrid (semantic + keyword) search on the repository index.

        Args:
            query (str): The search query string.
        num_results (int): Number of top results to return.

        Returns:
            List[Any]: A list of search results with similarity scores.
            
    """
    
        print(f"Performing hybrid search for '{query}'...\n")
        results = self.index.search(query, num_results=num_results)

        for i, r in enumerate(results, start=1):
            print(f"Result {i}:")
            print(f"File: {r.get('filename', 'unknown file')}")
            snippet = r.get('content', '')[:200]
            print(f"Snippet: {snippet}\n")

        return results
