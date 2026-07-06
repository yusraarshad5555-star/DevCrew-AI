from devcrew_ai.agents.base import BaseAgent
from devcrew_ai.database import add_project_memory

class ManagerAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Manager Agent",
            role_description="Engineering Manager who coordinates timelines, defines requirements, and delivers the final software product."
        )

    def analyze_requirements(self, project_id: int, project_name: str, requirements: str):
        self.log(project_id, f"Initializing project '{project_name}'.")
        self.log(project_id, f"Analyzing user specifications: '{requirements}'")
        
        # Save requirements to memory
        add_project_memory(project_id, "Raw Requirements", requirements, "requirement")
        
        prompt = f"Decompose requirements for project: {project_name}. Requirements: {requirements}"
        response = self.run(project_id, prompt)
        
        self.log(project_id, "Requirements analysis complete. Project state saved. Invoking Planner.")
        return response

    def deliver_project(self, project_id: int, workspace_path: str, approved: bool):
        self.log(project_id, "Conducting final deployment review.")
        if approved:
            self.log(project_id, f"All tasks completed successfully. Project files located at: {workspace_path}")
            self.log(project_id, "DevCrew AI project delivery ready!")
            return "SUCCESS"
        else:
            self.log(project_id, "Project finished with unresolved issues.")
            return "UNRESOLVED"
