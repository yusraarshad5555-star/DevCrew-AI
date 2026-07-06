import json
from devcrew_ai.agents.base import BaseAgent
from devcrew_ai.database import create_task

class PlannerAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Planner Agent",
            role_description="System Planner who breaks down requirements into structured, sequenced software tasks."
        )

    def plan_project(self, project_id: int, requirements: str):
        self.log(project_id, "Formulating step-by-step project plan.")
        
        prompt = f"""
Analyze these requirements and output a structured JSON plan containing a list of tasks.
Format the output as a valid JSON object with a single key "tasks", which contains an array of tasks.
Each task must have:
- "name": Brief name of task.
- "description": What needs to be done.
- "agent": Which agent should do it (choose from: "Research Agent", "Architect Agent", "Developer Agent", "Testing Agent", "Reviewer Agent", "Documentation Agent").

Requirements:
{requirements}

Return ONLY valid JSON. No markdown blocks.
"""
        response = self.run(project_id, prompt)
        
        # Parse JSON
        try:
            # Strip markdown code blocks if present
            cleaned_resp = response.strip()
            if cleaned_resp.startswith("```"):
                # find first { and last }
                start = cleaned_resp.find("{")
                end = cleaned_resp.rfind("}")
                if start != -1 and end != -1:
                    cleaned_resp = cleaned_resp[start:end+1]
                    
            plan_data = json.loads(cleaned_resp)
            tasks = plan_data.get("tasks", [])
            
            self.log(project_id, f"Successfully parsed {len(tasks)} tasks from LLM plan.")
            
            created_tasks = []
            for task in tasks:
                task_id = create_task(
                    project_id=project_id,
                    name=task["name"],
                    description=task["description"],
                    assigned_to=task["agent"]
                )
                created_tasks.append({
                    "id": task_id,
                    "name": task["name"],
                    "description": task["description"],
                    "assigned_to": task["agent"]
                })
                self.log(project_id, f"Registered Task #{task_id}: '{task['name']}' assigned to '{task['agent']}'")
                
            return created_tasks
            
        except Exception as e:
            self.log(project_id, f"Error parsing planner JSON: {e}. Fallback to default checklist.")
            # Fallback checklist if JSON fails
            fallback_tasks = [
                ("Research Stack", "Research libraries and best practices.", "Research Agent"),
                ("Design Architecture", "Design modular folder layout.", "Architect Agent"),
                ("Generate Code", "Write the application code files.", "Developer Agent"),
                ("Run Validation", "Write and execute unit tests.", "Testing Agent"),
                ("Review Quality", "Audit and refine code logic.", "Reviewer Agent"),
                ("Generate Documentation", "Create README.md and installation logs.", "Documentation Agent")
            ]
            created_tasks = []
            for name, desc, agent in fallback_tasks:
                task_id = create_task(project_id, name, desc, agent)
                created_tasks.append({"id": task_id, "name": name, "description": desc, "assigned_to": agent})
            return created_tasks
