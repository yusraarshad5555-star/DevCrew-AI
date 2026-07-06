import os
from devcrew_ai.agents.base import BaseAgent
from devcrew_ai.database import add_artifact
from devcrew_ai.config import WORKSPACE_DIR

class DocumentationAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Documentation Agent",
            role_description="Technical Writer who details API specs, installation steps, workflows, and developer guides."
        )

    def write_readme(self, project_id: int, project_name: str, requirements: str, files_list: list) -> str:
        self.log(project_id, "Formulating system-level README and setup instructions.")
        
        prompt = f"""
Generate a comprehensive, production-ready README.md for the generated project '{project_name}'.
Requirements: {requirements}
Files written in project: {files_list}

The document should contain:
- Title and project objective
- Setup and Installation guide
- API specifications/CLI arguments usage
- Details on running unit tests
- Summary of design patterns and system architecture

Output the raw markdown document ONLY.
"""
        content = self.run(project_id, prompt)
        
        # Clean markdown code blocks if the LLM output wrapped them
        cleaned_content = content.strip()
        if cleaned_content.startswith("```markdown"):
            cleaned_content = cleaned_content[11:]
        elif cleaned_content.startswith("```"):
            cleaned_content = cleaned_content[3:]
            
        if cleaned_content.endswith("```"):
            cleaned_content = cleaned_content[:-3]
            
        cleaned_content = cleaned_content.strip()
        
        # Write to file
        target_dir = WORKSPACE_DIR / project_name
        readme_path = target_dir / "README.md"
        os.makedirs(readme_path.parent, exist_ok=True)
        
        with open(readme_path, "w", encoding="utf-8") as f:
            f.write(cleaned_content)
            
        self.log(project_id, "README.md created successfully in workspace.")
        
        # Save to artifacts database
        add_artifact(
            project_id=project_id,
            filename="README.md",
            content=cleaned_content,
            filepath="README.md",
            type="docs"
        )
        
        return cleaned_content
