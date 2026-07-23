import lancedb
import pyarrow as pa

db = lancedb.connect("NexDoc_DB")

schema = pa.schema([
    pa.field("id", pa.string(), nullable=False),
    pa.field("vector", pa.list_(pa.float32(), 384), nullable=False),
    pa.field("text", pa.string(), nullable=False),
    
    pa.field("file_name", pa.string(), nullable=True),
    pa.field("file_type", pa.string(), nullable=True),
    pa.field("page_number", pa.int32(), nullable=True),
    pa.field("slide_number", pa.int32(), nullable=True),
    pa.field("line_start", pa.int32(), nullable=True),
    pa.field("line_end", pa.int32(), nullable=True)
])

table = db.create_table(
    "documents",
    schema=schema,
    exist_ok=True
)

def insert_embeddings(records):
    flattened_records = []

    for record in records:
        metadata = record["metadata"]

        flattened_records.append({
            "id": record["id"],
            "vector": record["vector"],
            "text": record["text"],

            "file_name": metadata.get("file_name"),
            "file_type": metadata.get("file_type"),
            "page_number": metadata.get("page_number"),
            "slide_number": metadata.get("slide_number"),
            "line_start": metadata.get("line_start"),
            "line_end": metadata.get("line_end"),
        })

    table.add(flattened_records)