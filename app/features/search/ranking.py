from typing import List

def rank_results(query: str, results: List[dict]) -> List[dict] :
    """
    Reorders the filtered results based on relevance.
    """
    ranked_results = []
    
    for result in results :
        content = result["content"]
        # now compare the query against the content and assign a priority
        if query.lower() == content.lower():
            priority = 1
        elif query.lower() in content.lower():
            priority = 2
        else:
            priority = 3
        #now append both priority and result into the ranked_results variable
        ranked_results.append((priority, result))
        
    # now short the results  by priority
    ranked_results.sort(key=lambda x: (x[0], x[1]["score"]))
    
    final_result = []
    
    for _, result in ranked_results:
        final_result.append(result)
    
    return final_result