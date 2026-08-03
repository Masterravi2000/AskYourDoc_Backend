import lancedb
import pyarrow as pa
import os
from app.repositories.status_store_repository import set_status

db = lancedb.connect("NexDoc_DB")

schema = pa.schema([
    pa.field("id", pa.string(), nullable=False),
    pa.field("vector", pa.list_(pa.float32(), 384), nullable=False),
    pa.field("text", pa.string(), nullable=False),
    
    pa.field("file_name", pa.string(), nullable=True),
    pa.field("file_type", pa.string(), nullable=True),
    pa.field("sheet_name", pa.string(), nullable=True),
    pa.field("page_number", pa.int32(), nullable=True),
    pa.field("slide_number", pa.int32(), nullable=True),
    pa.field("line_start", pa.int32(), nullable=True),
    pa.field("line_end", pa.int32(), nullable=True),
    pa.field("file_size", pa.int64(), nullable=True),
    pa.field("created_on", pa.float64(), nullable=True),
    pa.field("last_modified", pa.float64(), nullable=True),
])

table = db.create_table(
    "documents",
    schema=schema,
    exist_ok=True
)

def insert_embeddings(fileId: str, records):
    flattened_records = []
    
    # start = time.perf_counter()
    filename = records[0]["metadata"]["file_name"]
    set_status(fileId, filename, "storing")

    for record in records:
        metadata = record["metadata"]

        flattened_records.append({
            "id": record["id"],
            "vector": record["vector"],
            "text": record["text"],

            "file_name": metadata.get("file_name"),
            "file_type": metadata.get("file_type"),
            "sheet_name": metadata.get("sheet_name"),
            "page_number": metadata.get("page_number"),
            "slide_number": metadata.get("slide_number"),
            "line_start": metadata.get("line_start"),
            "line_end": metadata.get("line_end"),
            "file_size": metadata.get("file_size"),
            "created_on": metadata.get("created_on"),
            "last_modified": metadata.get("last_modified"),
        })

    table.add(flattened_records)
    
    # print(f"[LanceDB Storage] Completed in {time.perf_counter() - start:.3f} sec")
    
def inspect_vector_db():
    print("Total records available on LanceDB - ", table.count_rows())
    # print("Example of an record - ", table.to_arrow().to_pylist()[:3])

def clear_lancedb():
    table.delete("true")
