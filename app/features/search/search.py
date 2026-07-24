from app.features.embedding.embedder import model
from app.repositories.lancedb_repository import table
from app.features.search.hybrid_search import hybrid_filter
from app.features.search.ranking import rank_results


def search_query(query: str, k: int = 5):
    # 🔹 Step 1: Embed query
    query_vector = model.encode(query).tolist()

    # 🔹 Step 2: Search FAISS
    results = (
        table.search(query_vector)
        .limit(k)
        .to_list()
    )

    # 🔹 Step 3: Map results
    formatted_results = []
    
    for row in results:
        formatted_results.append({
            "content": row["text"],
            "score": row["_distance"],

            "file_name": row["file_name"],
            "file_type": row["file_type"],

            "page_number": row["page_number"],
            "slide_number": row["slide_number"],

            "line_start": row["line_start"],
            "line_end": row["line_end"]
        })
    
    # Step 4: Hybrid Search
    filtered_result = hybrid_filter(query, formatted_results)
    filtered_result = rank_results(query, filtered_result)
    
    return filtered_result