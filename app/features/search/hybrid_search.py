from typing import List

def hybrid_filter(query: str, results: List[dict]) -> List[dict]:
    """
    Filters LanceDB results by verifying that the query
    actually exists inside the retrieved chunk.
    """
    filtered_results = []
    
    for result in results :
        content = result["content"]
        
        # now findout the query in the given result content and append only those results whos content had the matching query/word
        if query.lower() in content.lower():
            filtered_results.append(result)
    
    return filtered_results
    