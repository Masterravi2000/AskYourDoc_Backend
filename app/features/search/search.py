from app.features.embedding.embedder import model
from app.repositories.lancedb_repository import table
from app.features.search.hybrid_search import hybrid_filter
from app.features.search.ranking import rank_results
from app.features.search.readability_enchancement import enchance_readability
from app.utils.file_metadata_formatter  import format_file_size, format_datetime
from app.services.stats.stats_service import increment_search


def search_query(query: str, k: int = 5):
    # 🔹 Step 1: Embed query
    query_vector = model.encode(query).tolist()

    # 🔹 Step 2: Search lanceDB
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
            "file_size": format_file_size(row["file_size"]),
            "created_on": format_datetime(row["created_on"]),
            "last_modified": format_datetime(row["last_modified"]),

            "page_number": row["page_number"],
            "slide_number": row["slide_number"],

            "line_start": row["line_start"],
            "line_end": row["line_end"]
        })
        
    # increment search
    increment_search()
    
    # Step 4: Hybrid Search
    filtered_result = hybrid_filter(query, formatted_results)
    filtered_result = rank_results(query, filtered_result)
    filtered_result = enchance_readability(query, filtered_result)
    
    return filtered_result