import threading

_status_store = {}
_lock = threading.Lock()

def set_status(filename: str, status: str, error: str = None):
    with _lock:
        _status_store[filename] = {
            "status": status,
            "error": error
        }

def get_status(filename: str):
    with _lock:
        return _status_store.get(filename, {"status": "not_found", "error": None})

def get_all_status():
    with _lock:
        return _status_store.copy()

def delete_status(filename: str):
    with _lock:
        if filename in _status_store:
            del _status_store[filename]