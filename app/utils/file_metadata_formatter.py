from datetime import datetime


def format_file_size(size: int) -> str:
    if size < 1024:
        return f"{size} B"
    elif size < 1024 * 1024:
        return f"{size / 1024:.2f} KB"
    elif size < 1024 * 1024 * 1024:
        return f"{size / (1024 * 1024):.2f} MB"
    else:
        return f"{size / (1024 * 1024 * 1024):.2f} GB"


def format_datetime(timestamp: float) -> str:
    if timestamp > 1e10:  # milliseconds
        timestamp /= 1000
    return datetime.fromtimestamp(timestamp).strftime("%d %b %Y")