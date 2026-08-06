from fastapi.responses import FileResponse
import os
from app.services.stats.stats_service import increment_download

def download_file(file_name: str, file_type: str) :
    folder = "images" if file_type == "image" else file_type
    file_path = os.path.join("docs", folder, file_name)
    
    if not os.path.exists(file_path):
        raise FileNotFoundError("File not found")
    
    #increment download
    increment_download()
        
    return FileResponse(
        path=file_path,
        filename=file_name,
        media_type="application/octet-stream"
    )
    