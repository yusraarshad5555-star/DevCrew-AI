from pydantic import BaseModel, Field
from typing import List, Optional

class ProjectCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="Name of the project")
    description: str = Field(..., min_length=5, description="Project specifications and requirements")

class ProjectResponse(BaseModel):
    id: int
    name: str
    description: str
    status: str
    created_at: str

class TaskResponse(BaseModel):
    id: int
    project_id: int
    name: str
    description: str
    assigned_to: str
    status: str
    dependencies: str
    output: Optional[str] = None
    updated_at: str

class LogResponse(BaseModel):
    id: int
    project_id: int
    agent_name: str
    log_text: str
    timestamp: str

class MemoryResponse(BaseModel):
    id: int
    project_id: int
    key: str
    value: str
    category: str
    created_at: str

class ArtifactResponse(BaseModel):
    id: int
    project_id: int
    filename: str
    content: str
    filepath: str
    type: str
    created_at: str
