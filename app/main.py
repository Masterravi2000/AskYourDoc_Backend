from fastapi import FastAPI
import threading
from app.controllers.uploadFile.uploadPDF.upload_pdf_route import router as upload_pdf_router
from app.controllers.uploadFile.uploadIMAGES.upload_images_route import router as upload_images_router
from app.controllers.uploadFile.uploadPPTX.upload_pptx_route import router as upload_pptx_router
from app.controllers.uploadFile.uploadTXT.upload_txt_route import router as upload_txt_router
from app.controllers.uploadFile.uploadXLS.upload_xls_route import router as upload_xls_router
from app.controllers.search.search_routes import router as search_router
from app.controllers.status.status_route import router as status_router
from app.controllers.download.download_routes import router as download_route
from app.controllers.stats.stats_route import router as stats_route
from app.controllers.recent_searches.recent_searches_route import router as recent_search_router

from app.features.workers.file_watcher import start_watching
import app.features.workers.file_watcher as file_watcher
from app.features.workers.worker_pool import start_worker_pool
from fastapi.middleware.cors import CORSMiddleware
from app.repositories.stats_repository import initialize_stats_table
from app.repositories.recent_search_repository import initialize_recent_searches_table

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.on_event("startup")
def startup_event():
    
    # Start Sqlite and create stats tables
    initialize_stats_table()
    
    # Start Sqlite and create recent search tables
    initialize_recent_searches_table()
    
    # Start worker threads
    start_worker_pool()
    
    # Start watcing in background
    threading.Thread(target=start_watching, daemon=True).start()

@app.get("/")
def home():
    return {"message": "Nexdoc Backend is live!"}

app.include_router(upload_pdf_router, prefix="/api")
app.include_router(upload_images_router, prefix="/api")
app.include_router(upload_pptx_router, prefix="/api")
app.include_router(upload_txt_router, prefix="/api")
app.include_router(upload_xls_router, prefix="/api")
app.include_router(search_router, prefix="/api")
app.include_router(status_router, prefix="/api")
app.include_router(download_route, prefix="/api")
app.include_router(stats_route, prefix="/api")
app.include_router(recent_search_router, prefix="/api")

@app.get("/status")
def get_status():
    return {"status": "ready" if file_watcher.WATCHER_READY else "loading"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)