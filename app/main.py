from fastapi import FastAPI
import os
from app.controllers.uploadFile.uploadPDF.upload_pdf_route import router as upload_pdf_router
from app.controllers.uploadFile.uploadIMAGES.upload_images_route import router as upload_images_router
from app.controllers.uploadFile.uploadPPTX.upload_pptx_route import router as upload_pptx_router
from app.services.uploadFiles.uploadTXT import router as upload_txt_router
from app.services.uploadFiles.uploadXLS import router as upload_xls_router
from app.features.search.search import router as search_router
from app.repositories import load_from_disk

app = FastAPI()

@app.on_event("startup")
def startup_event():
    load_from_disk()
    
    import threading
    from app.features.workers.file_watcher import start_watching
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

@app.get("/status")
def get_status():
    from app.features.workers.file_watcher import WATCHER_READY
    return {"status": "ready" if WATCHER_READY else "loading"}