"""State file helpers for an incremental load.

load_state(path) -> dict   (missing file -> {"watermark": None}; always has "watermark")
save_state(path, state)    atomic JSON write; creates parent directories
"""
