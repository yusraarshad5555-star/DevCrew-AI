import os
from pathlib import Path
from typing import List, Dict, Any

def safe_write_file(workspace_root: Path, relative_path: str, content: str) -> Path:
    """Safely write a file ensuring directories exist and path is relative to workspace."""
    target_path = (workspace_root / relative_path).resolve()
    
    # Security check: Ensure target path is indeed inside workspace_root
    if not str(target_path).startswith(str(workspace_root.resolve())):
        raise PermissionError(f"Attempted path traversal outside workspace: {relative_path}")
        
    os.makedirs(target_path.parent, exist_ok=True)
    with open(target_path, "w", encoding="utf-8") as f:
        f.write(content)
    return target_path

def safe_read_file(workspace_root: Path, relative_path: str) -> str:
    """Safely read a file, guaranteeing path boundaries."""
    target_path = (workspace_root / relative_path).resolve()
    if not str(target_path).startswith(str(workspace_root.resolve())):
        raise PermissionError(f"Attempted path traversal outside workspace: {relative_path}")
        
    with open(target_path, "r", encoding="utf-8") as f:
        return f.read()

def list_workspace_files(workspace_root: Path) -> List[Dict[str, Any]]:
    """Recursively list all files in workspace with details."""
    files_list = []
    if not workspace_root.exists():
        return files_list
        
    for root, dirs, files in os.walk(workspace_root):
        for file in files:
            full_path = Path(root) / file
            rel_path = full_path.relative_to(workspace_root)
            
            # Skip hidden files and venv dirs
            if any(part.startswith('.') or part == 'venv' for part in rel_path.parts):
                continue
                
            files_list.append({
                "relative_path": str(rel_path),
                "name": file,
                "size": full_path.stat().st_size,
                "is_dir": False
            })
    return files_list
