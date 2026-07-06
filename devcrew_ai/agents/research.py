from devcrew_ai.agents.base import BaseAgent
from devcrew_ai.database import add_project_memory, add_vector_memory

class ResearchAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Research Agent",
            role_description="Research Engineer who compares technologies, fetches documentation, and identifies API usage patterns."
        )

    def conduct_research(self, project_id: int, requirements: str) -> str:
        self.log(project_id, "Searching documentation and offline library databases.")
        
        prompt = f"Provide a research report on the required libraries, best practices, and code design patterns for: {requirements}"
        report = self.run(project_id, prompt)
        
        # Save research reports in memory
        add_project_memory(project_id, "Technology Stack Report", report, "technology")
        add_vector_memory(project_id, f"Research Report details: {report}", "research")
        
        self.log(project_id, "Research completed. Added stack recommendations to project memory.")
        return report
