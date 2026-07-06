import subprocess
from pathlib import Path
from typing import Dict, Any

def execute_local_command(cwd: Path, command: list, timeout: int = 30) -> Dict[str, Any]:
    """Execute a local terminal command inside the specified directory."""
    try:
        result = subprocess.run(
            command,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        return {
            "success": result.returncode == 0,
            "exit_code": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr
        }
    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "exit_code": -1,
            "stdout": "",
            "stderr": f"Command timed out after {timeout} seconds."
        }
    except Exception as e:
        return {
            "success": False,
            "exit_code": -99,
            "stdout": "",
            "stderr": str(e)
        }
