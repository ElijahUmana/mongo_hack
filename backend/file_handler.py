# file_handler.py

import subprocess
from pathlib import Path

# Define the root directory for all agent-generated projects.
# This is a critical security measure to sandbox the agent's actions.
WORKSPACE_DIR = Path(__file__).parent / "workspace"

def create_or_update_file(relative_path: str, content: str) -> dict:
    """
    Creates or updates a file within the sandboxed workspace directory.
    """
    # Ensure the workspace directory exists
    WORKSPACE_DIR.mkdir(parents=True, exist_ok=True)
    
    # Create the full path and resolve it to prevent directory traversal attacks
    full_path = (WORKSPACE_DIR / relative_path).resolve()

    # Security Check: Ensure the final path is still within the workspace
    if not str(full_path).startswith(str(WORKSPACE_DIR.resolve())):
        return {"status": "error", "message": "Error: Path is outside the allowed workspace."}

    try:
        # Create parent directories if they don't exist
        full_path.parent.mkdir(parents=True, exist_ok=True)
        # Write the content to the file
        full_path.write_text(content, encoding='utf-8')
        return {"status": "success", "path": str(full_path)}
    except Exception as e:
        return {"status": "error", "message": f"An error occurred: {e}"}

def run_command(command: str) -> dict:
    """
    Runs a shell command within the sandboxed workspace directory.
    """
    try:
        # Execute the command from within the workspace directory
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            cwd=WORKSPACE_DIR,  # This is crucial for sandboxing
            check=False  # Do not raise exception on non-zero exit codes
        )
        
        return {
            "status": "success",
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode
        }
    except Exception as e:
        return {"status": "error", "message": f"An error occurred: {e}"}