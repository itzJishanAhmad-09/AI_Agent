from .files import read_file, write_file, list_files
from .code import run_code
from .web import search_web

TOOL_MAP = {
    "read_file": read_file,
    "write_file": write_file,
    "list_files": list_files,
    "run_code": run_code,
    "search_web": search_web,
}