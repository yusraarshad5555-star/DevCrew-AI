import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Base directory
BASE_DIR = Path("c:/Capstone project")

# LLM config
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "mock").lower()
OLLAMA_API_URL = os.getenv("OLLAMA_API_URL", "http://localhost:11434/api/generate")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5-coder:7b")

# Backend server config
BACKEND_HOST = os.getenv("BACKEND_HOST", "127.0.0.1")
BACKEND_PORT = int(os.getenv("BACKEND_PORT", "8000"))

# Database and file path config
DB_PATH = Path(os.getenv("DB_PATH", str(BASE_DIR / "devcrew_ai.db")))
WORKSPACE_DIR = Path(os.getenv("WORKSPACE_DIR", str(BASE_DIR / "generated_projects")))

# Ensure directories exist
WORKSPACE_DIR.mkdir(parents=True, exist_ok=True)
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

print(f"[Config] LLM Provider: {LLM_PROVIDER}")
print(f"[Config] DB Path: {DB_PATH}")
print(f"[Config] Workspace: {WORKSPACE_DIR}")
