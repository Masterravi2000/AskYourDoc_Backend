from fastapi import FastAPI
import threading
from app.controllers.uploadFile.uploadPDF.upload_pdf_route import router as upload_pdf_router
from app.controllers.uploadFile.uploadIMAGES.upload_images_route import router as upload_images_router
from app.controllers.uploadFile.uploadPPTX.upload_pptx_route import router as upload_pptx_router
from app.controllers.uploadFile.uploadTXT.upload_txt_route import router as upload_txt_router
from app.controllers.uploadFile.uploadXLS.upload_xls_route import router as upload_xls_router
from app.controllers.search.search_routes import router as search_router
from app.controllers.status.status_route import router as status_router
from app.features.workers.file_watcher import start_watching
import app.features.workers.file_watcher as file_watcher
from app.features.workers.worker_pool import start_worker_pool

app = FastAPI()

@app.on_event("startup")
def startup_event():
    
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

@app.get("/status")
def get_status():
    return {"status": "ready" if file_watcher.WATCHER_READY else "loading"}