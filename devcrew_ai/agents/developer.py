import os
from devcrew_ai.agents.base import BaseAgent
from devcrew_ai.database import add_artifact
from devcrew_ai.config import WORKSPACE_DIR

class DeveloperAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Developer Agent",
            role_description="Senior Software Engineer who writes clean, modular, production-ready Python code following SOLID principles."
        )

    def write_file(self, project_id: int, project_name: str, file_path: str, file_desc: str, project_requirements: str) -> str:
        self.log(project_id, f"Coding file: '{file_path}' ({file_desc})")
        
        prompt = f"""
Write the code for file path: '{file_path}'
File description: {file_desc}
Overall project requirements: {project_requirements}

Write clean, robust, working, and offline-compatible Python code.
Do NOT write markdown wrap blocks in your code output if possible, or keep code blocks simple.
Provide ONLY the raw code contents.
"""
        code_content = self.run(project_id, prompt)
        
        # Clean markdown code blocks if the LLM output wrapped them
        cleaned_code = code_content.strip()
        if cleaned_code.startswith("```python"):
            cleaned_code = cleaned_code[9:]
        elif cleaned_code.startswith("```"):
            cleaned_code = cleaned_code[3:]
            
        if cleaned_code.endswith("```"):
            cleaned_code = cleaned_code[:-3]
            
        cleaned_code = cleaned_code.strip()
        
        # Write to physical file
        target_dir = WORKSPACE_DIR / project_name
        full_file_path = target_dir / file_path
        os.makedirs(full_file_path.parent, exist_ok=True)
        
        with open(full_file_path, "w", encoding="utf-8") as f:
            f.write(cleaned_code)
            
        self.log(project_id, f"Successfully wrote code to {file_path}.")
        
        # Determine file type
        file_type = "code"
        if "test" in file_path.lower():
            file_type = "tests"
        
        # Save to artifacts database
        add_artifact(
            project_id=project_id,
            filename=os.path.basename(file_path),
            content=cleaned_code,
            filepath=file_path,
            type=file_type
        )
        
        return cleaned_code
