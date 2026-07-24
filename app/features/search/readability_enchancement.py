from typing import List

def enchance_readability(query: str, results: List[dict]) -> List[dict]:
    """
    Extracts a concise snippet around the matched query
    to improve search result readability.
    """
    enchanced_results = []
    
    for result in results:
        content = result["content"]
        
        # Find the starting index of the query
        start_index = content.lower().find(query.lower())
        
        # if not found then keep the original content
        if start_index == -1:
            result["content"] = content
            enchanced_results.append(result)
            continue
        
        # 50 characters before and after the match
        snippet_start = max(0, start_index - 50)
        snippet_end = min(len(content), start_index + len(query) + 50)
        
        snippet = content[snippet_start:snippet_end]
        
        # Replace full content with snippet
        result["content"] = snippet
        
        enchanced_results.append(result)
        
    
    return enchanced_results