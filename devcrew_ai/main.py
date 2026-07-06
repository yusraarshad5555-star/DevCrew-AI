from fastapi import FastAPI, HTTPException, BackgroundTasks, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
import os

from devcrew_ai.config import DB_PATH, WORKSPACE_DIR
from devcrew_ai.database import (
    init_db,
    create_project,
    get_project,
    get_all_projects,
    get_tasks_for_project,
    get_logs_for_project,
    get_project_memories,
    get_all_vector_memories,
    get_artifacts_for_project,
    delete_project_data
)
from devcrew_ai.schema import (
    ProjectCreate,
    ProjectResponse,
    TaskResponse,
    LogResponse,
    MemoryResponse,
    ArtifactResponse
)
from devcrew_ai.workflow import WorkflowRunner
from devcrew_ai.memory.local_similarity import search_local_memories

# Initialize FastAPI App
app = FastAPI(
    title="DevCrew AI Backend API",
    description="Offline-ready local multi-agent software engineering automation system API.",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure Database is initialized on startup
@app.on_event("startup")
def startup_event():
    init_db()

@app.get("/")
def read_root():
    return {
        "status": "online",
        "message": "Welcome to the DevCrew AI Backend Server.",
        "config": {
            "database": str(DB_PATH),
            "workspace": str(WORKSPACE_DIR)
        }
    }

# Create and Start a new project run
@app.post("/api/projects", response_model=ProjectResponse, status_code=201)
def start_project_run(project_input: ProjectCreate, background_tasks: BackgroundTasks):
    try:
        project_id = create_project(project_input.name, project_input.description)
        project = get_project(project_id)
        
        # Launch the workflow in a separate background thread/task
        runner = WorkflowRunner(project_id)
        background_tasks.add_task(runner.run)
        
        return project
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to start project execution: {e}")

# List all projects
@app.get("/api/projects", response_model=List[ProjectResponse])
def list_projects():
    return get_all_projects()

# Get specific project status
@app.get("/api/projects/{project_id}", response_model=ProjectResponse)
def get_project_status(project_id: int):
    project = get_project(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

# Get tasks list for a project
@app.get("/api/projects/{project_id}/tasks", response_model=List[TaskResponse])
def get_project_tasks(project_id: int):
    return get_tasks_for_project(project_id)

# Get live agent logs
@app.get("/api/projects/{project_id}/logs", response_model=List[LogResponse])
def get_project_logs(project_id: int):
    return get_logs_for_project(project_id)

# Get generated artifacts (files)
@app.get("/api/projects/{project_id}/artifacts", response_model=List[ArtifactResponse])
def get_project_artifacts(project_id: int):
    return get_artifacts_for_project(project_id)

# Get memories with optional query search
@app.get("/api/projects/{project_id}/memories")
def get_memories(project_id: int, query: Optional[str] = None):
    # If a search query is provided, perform local vector/text similarity search
    if query:
        # Get raw vector memories stored in SQLite
        vector_mems = get_all_vector_memories(project_id)
        # Search using TF-IDF similarity matcher
        results = search_local_memories(query, vector_mems, top_k=5)
        return {"search_query": query, "matches": results}
    
    # Otherwise, return structured key-value memories
    return {"memories": get_project_memories(project_id)}

# Delete project data
@app.delete("/api/projects/{project_id}")
def delete_project(project_id: int):
    project = get_project(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    try:
        delete_project_data(project_id)
        # Clean workspace directory if it exists
        project_name = project["name"]
        workspace_path = WORKSPACE_DIR / project_name
        # Note: We won't recursively delete files here to avoid safe command boundaries,
        # but the database records are fully purged.
        return {"status": "success", "message": f"Project {project_id} deleted."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete project: {e}")
