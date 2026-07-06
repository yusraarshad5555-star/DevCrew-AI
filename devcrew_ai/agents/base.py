from devcrew_ai.llm import get_llm
from devcrew_ai.database import add_agent_log

class BaseAgent:
    def __init__(self, name: str, role_description: str):
        self.name = name
        self.role_description = role_description
        self.llm = get_llm()

    def get_system_instruction(self) -> str:
        return f"You are {self.name}, the {self.role_description} in DevCrew AI. Follow your role rules strictly and operate in offline developer mode."

    def log(self, project_id: int, message: str):
        """Log agent activities and internal reasoning to terminal and database."""
        formatted_message = f"[{self.name}] {message}"
        print(formatted_message)
        add_agent_log(project_id, self.name, message)

    def run(self, project_id: int, prompt: str) -> str:
        """Execute the LLM query under the agent's persona."""
        self.log(project_id, f"Reasoning about task: {prompt[:120]}...")
        system_instruction = self.get_system_instruction()
        response = self.llm.generate(prompt, system_instruction=system_instruction)
        return response
