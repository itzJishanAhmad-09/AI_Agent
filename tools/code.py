import os
import sys
import tempfile
import subprocess
from config import WORKSPACE_DIR

def run_code(code: str, timeout: int = 10) -> str:
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".py", delete=False, dir=WORKSPACE_DIR
    ) as f:
        f.write(code)
        tmp_path = f.name

    try:
        env = os.environ.copy()
        env["PYTHONIOENCODING"] = "utf-8"
        result = subprocess.run(
            [sys.executable, "-I", "-S", tmp_path],
            capture_output=True,
            text=True,
            timeout=timeout,
            env=env,
            cwd=WORKSPACE_DIR,
        )
        output = result.stdout
        if result.stderr:
            output += "\n[stderr]\n" + result.stderr
        return output or "(no output)"
    except subprocess.TimeoutExpired:
        return f"Error: code timed out after {timeout}s"
    except Exception as e:
        return f"Error running code: {e}"
    finally:
        try:
            os.unlink(tmp_path)
        except Exception:
            pass