import threading

_status_store = {}
_lock = threading.Lock()

def set_status(fileId: str, filename: str, status: str, error: str = None):
    with _lock:
        _status_store[fileId] = {
            "fileId": fileId,
            "filename": filename,
            "status": status,
            "error": error
        }

def get_status(fileId: str):
    with _lock:
        print(fileId)
        print(_status_store)
        return _status_store.get(fileId, {"status": "not_found", "error": None})

def get_all_status():
    with _lock:
        return _status_store.copy()

def delete_status(fileId: str):
    with _lock:
        if fileId in _status_store:
            del _status_store[fileId]