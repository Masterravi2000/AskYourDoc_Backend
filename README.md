# AskYourDoc_Backend

## 🧠 Offline AI-Powered Document Search Engine (Backend)

AskYourDoc is a fully offline, high-performance document processing and semantic search system that transforms multiple document formats into vector embeddings and enables accurate, context-aware retrieval using FAISS.

It is designed as a **modular, scalable pipeline** that processes documents end-to-end — from upload to intelligent search — without relying on any external APIs.

---

## ✨ Features

### 📂 Multi-Format Document Support
- PDF  
- Images (OCR-based)  
- PPTX  
- TXT  
- XLS / XLSX  

### ⚡ High-Performance Processing
- Parallel file processing (threaded pipeline)  
- Real-time file detection using watchdog  
- Batch processing support  

### 🧠 Semantic Search
- Embedding-based retrieval (not keyword-based)  
- Context-aware results  
- High accuracy retrieval  

### 📦 Efficient Storage
- FAISS vector database (in-memory)  
- Batch-based disk persistence  
- Metadata tracking  

### 📴 Fully Offline System
- No external APIs  
- Local processing & storage  
- Privacy-focused  

---

## 🧠 How It Works (High Level)

1. User uploads documents  
2. Files are automatically detected  
3. Text is extracted  
4. Cleaned & normalized  
5. Chunked  
6. Embedded  
7. Stored in FAISS  
8. Query returns relevant results  

---

## 🏗️ Architecture Overview


Upload → Extract → Clean → Normalize → Chunk → Embed → FAISS → Search


---

## 📁 Project Structure

```
AskYourDoc_Backend/
│
├── app/
│ ├── controllers/
│ │ ├── uploadPDF/
│ │ │ └── controller.py
│ │ ├── uploadIMAGES/
│ │ │ └── controller.py
│ │ ├── uploadPPTX/
│ │ │ └── controller.py
│ │ ├── uploadTXT/
│ │ │ └── controller.py
│ │ ├── uploadXLS/
│ │ │ └── controller.py
│ │
│ ├── fileProcessors/
│ │ ├── pdfProcessor.py
│ │ ├── imageProcessor.py
│ │ ├── pptxProcessor.py
│ │ ├── txtProcessor.py
│ │ ├── xlsProcessor.py
│ │
│ ├── utils/
│ │ └── text_cleaner.py
│ │
│ ├── chunking/
│ │ └── chunker.py
│ │
│ ├── embedding/
│ │ └── embedder.py
│ │
│ ├── vectorstore/
│ │ └── faiss_store.py
│ │
│ ├── workers/
│ │ └── file_watcher.py
│ │
│ ├── routes/
│ │ └── search_routes.py
│ │
│ ├── search/
│ │ └── search.py
│ │
│ ├── main.py
│ └── status_store.py
│
├── docs/
│ ├── pdf/
│ ├── images/
│ ├── pptx/
│ ├── txt/
│ ├── xls/
│
├── venv/
├── README.md
└── requirements.txt

```
---

## 🛠️ Tech Stack

- **FastAPI** – API framework  
- **Python (async + threading)**  
- **PyMuPDF, pytesseract, python-pptx, pandas**  
- **sentence-transformers (MiniLM)**  
- **FAISS (vector DB)**  

---

## ⚙️ Pipeline Breakdown

### 1. 📤 Upload
- Multi-file support  
- Duplicate prevention  
- Organized storage  

### 2. ⚙️ Processing
- Watchdog-based automation  
- Parallel execution  
- File-type-specific extraction  

### 3. 🧹 Cleaning
- Centralized utility  
- Text normalization  

### 4. ✂️ Chunking
- Sentence-aware splitting  
- Metadata preserved  

### 5. 🧠 Embedding
- Local model (MiniLM)  
- Fast vector generation  

### 6. 📦 FAISS Storage
- In-memory search  
- Metadata mapping  

### 7. 🔄 Batching
- Optimized disk writes  
- Persistent storage  

---

## 🔍 Query Flow


User Query → Embedding → FAISS → Top Matches → Response


---

## 📊 Performance

| Stage       | Complexity |
|------------|-----------|
| Upload     | O(n)      |
| Processing | O(n)      |
| Chunking   | O(n)      |
| Embedding  | O(n)      |
| Search     | ~O(log n) |

---

## ⚠️ Edge Cases Handled

- Corrupted files  
- Unsupported formats  
- Empty content  
- OCR failures  
- Partial processing failures  

---

## 📦 Storage Behavior

- Local filesystem  
- Organized by file type  
- RAM + disk hybrid  
- Batch persistence  

---

## 🧠 Design Principles

- Modular architecture  
- Separation of concerns  
- Fault-tolerant  
- Offline-first  
- Scalable  

---

## 🚀 Setup

```bash
git clone <your-repo>
cd AskYourDoc_Backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app/main.py


🚀 Usage
Upload files
Wait for processing
Query system
Get semantic results


🎯 Status
✅ Pipeline complete
✅ Accurate retrieval
✅ Offline system
✅ Production-ready backend


🔮 Future Improvements
Re-ranking
Threshold tuning
Frontend integration
Advanced caching


👤 Author
Ravi Sharma
Full Stack developer