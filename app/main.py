from fastapi import FastAPI
import os
from app.controllers.uploadPDF.controller import router as upload_pdf_router
from app.controllers.uploadIMAGES.controller import router as upload_images_router
from app.controllers.uploadPPTX.controller import router as upload_pptx_router
from app.controllers.uploadTXT.controller import router as upload_txt_router
from app.controllers.uploadXLS.controller import router as upload_xls_router

app = FastAPI()

@app.get("/")
def home():
    return {"message": "AskYourDoc Backend is live!"}

app.include_router(upload_pdf_router, prefix="/api")
app.include_router(upload_images_router, prefix="/api")
app.include_router(upload_pptx_router, prefix="/api")
app.include_router(upload_txt_router, prefix="/api")
app.include_router(upload_xls_router, prefix="/api")

@app.get("/status")
def get_status():
    from app.workers.file_watcher import WATCHER_READY
    return {"status": "ready" if WATCHER_READY else "loading"}