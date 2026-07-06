import json
from devcrew_ai.agents.base import BaseAgent
from devcrew_ai.database import add_project_memory, add_vector_memory

class ArchitectAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Architect Agent",
            role_description="System Architect who structures project folders, databases, module interfaces, and API schemas."
        )

    def design_architecture(self, project_id: int, requirements: str, research_report: str) -> dict:
        self.log(project_id, "Formulating application architecture.")
        
        prompt = f"""
Based on requirements: {requirements}
And research: {research_report}

Output a structured JSON architecture layout containing:
- "directories": A list of relative subdirectories to create.
- "files": A list of files to generate. Each file must be an object with:
    - "path": Relative path of the file (e.g. "src/calculator.py").
    - "description": Short description of the file's contents.
- "database_schema": Description of any database schema, if needed.

Return ONLY valid JSON.
"""
        response = self.run(project_id, prompt)
        
        try:
            cleaned_resp = response.strip()
            if cleaned_resp.startswith("```"):
                start = cleaned_resp.find("{")
                end = cleaned_resp.rfind("}")
                if start != -1 and end != -1:
                    cleaned_resp = cleaned_resp[start:end+1]
                    
            layout = json.loads(cleaned_resp)
            self.log(project_id, f"Architecture design finalized: {len(layout.get('files', []))} target files planned.")
            
            # Save architecture decisions in memory
            add_project_memory(project_id, "Directory Layout", json.dumps(layout.get("directories", [])), "decision")
            add_project_memory(project_id, "Database Schema Design", str(layout.get("database_schema", "None")), "decision")
            add_project_memory(project_id, "Target Files Configuration", json.dumps(layout.get("files", [])), "decision")
            
            add_vector_memory(project_id, f"Architecture decision: Directory layout is {layout.get('directories')}", "architect")
            add_vector_memory(project_id, f"Architecture decision: Database schema is {layout.get('database_schema')}", "architect")
            
            return layout
            
        except Exception as e:
            self.log(project_id, f"Error parsing architect JSON: {e}. Fallback to default layout.")
            fallback_layout = {
                "directories": ["src", "tests"],
                "files": [
                    {"path": "src/app.py", "description": "Core application logic"},
                    {"path": "tests/test_app.py", "description": "Unit tests for application"}
                ],
                "database_schema": "None"
            }
            add_project_memory(project_id, "Target Files Configuration", json.dumps(fallback_layout["files"]), "decision")
            return fallback_layout
