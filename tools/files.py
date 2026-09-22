import os
from config import WORKSPACE_DIR

def safe_path(path: str) -> str:
    workspace = os.path.abspath(WORKSPACE_DIR)
    full = os.path.abspath(os.path.join(workspace, path))
    try:
        common = os.path.commonpath([full, workspace])
    except ValueError:
        raise ValueError("Path outside workspace")
    if common != workspace:
        raise ValueError("Path outside workspace")
    return full

def read_file(path: str) -> str:
    try:
        with open(safe_path(path), "r", encoding="utf-8") as f:
            content = f.read()
        if len(content) > 8000:
            return content[:8000] + f"\n... [truncated, total {len(content)} chars]"
        return content
    except Exception as e:
        return f"Error reading file: {e}"

def write_file(path: str, content: str) -> str:
    try:
        full = safe_path(path)
        os.makedirs(os.path.dirname(full) or WORKSPACE_DIR, exist_ok=True)
        with open(full, "w", encoding="utf-8") as f:
            f.write(content)
        return f"Wrote {len(content)} chars to {path}"
    except Exception as e:
        return f"Error writing file: {e}"

def list_files(path: str = ".") -> str:
    try:
        full = safe_path(path)
        return "\n".join(os.listdir(full)) or "(empty)"
    except Exception as e:
        return f"Error listing files: {e}"