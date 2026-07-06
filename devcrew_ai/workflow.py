import json
import time
import traceback
from typing import List, Dict, Any
from devcrew_ai.database import (
    get_tasks_for_project,
    update_task_status,
    update_project_status,
    get_artifacts_for_project,
    add_project_memory,
    get_project
)
from devcrew_ai.config import WORKSPACE_DIR
from devcrew_ai.agents.manager import ManagerAgent
from devcrew_ai.agents.planner import PlannerAgent
from devcrew_ai.agents.research import ResearchAgent
from devcrew_ai.agents.architect import ArchitectAgent
from devcrew_ai.agents.developer import DeveloperAgent
from devcrew_ai.agents.testing import TestingAgent
from devcrew_ai.agents.reviewer import ReviewerAgent
from devcrew_ai.agents.documentation import DocumentationAgent

class WorkflowRunner:
    def __init__(self, project_id: int):
        self.project_id = project_id
        
        # Initialize agents
        self.manager = ManagerAgent()
        self.planner = PlannerAgent()
        self.research = ResearchAgent()
        self.architect = ArchitectAgent()
        self.developer = DeveloperAgent()
        self.tester = TestingAgent()
        self.reviewer = ReviewerAgent()
        self.doc_writer = DocumentationAgent()

    def run(self):
        """Execute the full 10-step multi-agent software engineering workflow."""
        try:
            update_project_status(self.project_id, "running")
            project = get_project(self.project_id)
            if not project:
                print(f"[Workflow] Project ID {self.project_id} not found in DB.")
                return
                
            project_name = project["name"]
            requirements = project["description"]
            
            print(f"[Workflow] Starting execution workflow for project '{project_name}' (ID: {self.project_id})")
            
            # --- STAGE 1: UNDERSTAND REQUIREMENTS ---
            print("[Workflow] STAGE 1: Requirements Analysis...")
            self.manager.analyze_requirements(self.project_id, project_name, requirements)
            
            # --- STAGE 2: CREATE PROJECT PLAN ---
            print("[Workflow] STAGE 2: Planning Decompositions...")
            tasks = self.planner.plan_project(self.project_id, requirements)
            
            # Helper to map task in database to its status and update it
            def find_and_start_task(agent_name: str) -> int:
                project_tasks = get_tasks_for_project(self.project_id)
                for t in project_tasks:
                    if t["assigned_to"] == agent_name and t["status"] == "pending":
                        update_task_status(t["id"], "in_progress")
                        return t["id"]
                return -1

            def get_task_id_for_agent(agent_name: str) -> int:
                project_tasks = get_tasks_for_project(self.project_id)
                for t in project_tasks:
                    if t["assigned_to"] == agent_name:
                        return t["id"]
                return -1

            def complete_task(task_id: int, output: str = ""):
                if task_id != -1:
                    update_task_status(task_id, "completed", output)

            def fail_task(task_id: int, output: str = ""):
                if task_id != -1:
                    update_task_status(task_id, "failed", output)

            # --- STAGE 3: RESEARCH TECHNOLOGIES ---
            print("[Workflow] STAGE 3: Tech Stack Research...")
            tid = find_and_start_task("Research Agent")
            research_report = self.research.conduct_research(self.project_id, requirements)
            complete_task(tid, research_report)
            
            # --- STAGE 4: DESIGN ARCHITECTURE ---
            print("[Workflow] STAGE 4: Architectural Design...")
            tid = find_and_start_task("Architect Agent")
            layout = self.architect.design_architecture(self.project_id, requirements, research_report)
            complete_task(tid, json.dumps(layout))
            
            # --- STAGE 5: GENERATE CODE ---
            print("[Workflow] STAGE 5: Developer Coding...")
            dev_tid = find_and_start_task("Developer Agent")
            files_to_create = layout.get("files", [])
            
            generated_files = []
            for file_info in files_to_create:
                path = file_info["path"]
                desc = file_info["description"]
                code = self.developer.write_file(self.project_id, project_name, path, desc, requirements)
                generated_files.append({"path": path, "code": code})
                time.sleep(0.5)  # Slight throttle for logs visibility
                
            complete_task(dev_tid, f"Generated {len(generated_files)} files in workspace.")
            
            # Iterate review-refine loops (maximum 2 times)
            iteration = 1
            max_reviewer_iterations = 2
            review_approved = False
            review_feedback = ""
            
            test_results = {}
            
            while iteration <= max_reviewer_iterations and not review_approved:
                # --- STAGE 6: RUN VALIDATION (TESTING) ---
                print(f"[Workflow] STAGE 6: Validation (Iteration #{iteration})...")
                test_tid = find_and_start_task("Testing Agent")
                test_results = self.tester.run_tests(self.project_id, project_name)
                
                # Check database to see if we need to create/update task for testing
                test_task_id = test_tid if test_tid != -1 else get_task_id_for_agent("Testing Agent")
                if test_task_id != -1:
                    update_task_status(test_task_id, "in_progress")
                    complete_task(test_task_id, test_results["output_log"])
                
                # --- STAGE 7: REVIEW QUALITY (REVIEWER) ---
                print(f"[Workflow] STAGE 7: Quality Review (Iteration #{iteration})...")
                rev_tid = find_and_start_task("Reviewer Agent")
                reviewer_task_id = rev_tid if rev_tid != -1 else get_task_id_for_agent("Reviewer Agent")
                if reviewer_task_id != -1:
                    update_task_status(reviewer_task_id, "in_progress")
                
                # Combine files contents for review
                files_content_str = ""
                for gf in generated_files:
                    files_content_str += f"\n=== File: {gf['path']} ===\n{gf['code']}\n"
                    
                review_report = self.reviewer.review_code(
                    project_id=self.project_id,
                    files_content=files_content_str,
                    test_report=test_results["output_log"],
                    iteration=iteration
                )
                
                review_approved = review_report.get("approved", False)
                review_feedback = review_report.get("feedback", "")
                complete_task(reviewer_task_id, json.dumps(review_report))
                
                # --- STAGE 8: IMPROVE SOLUTION (REFINEMENT) ---
                if not review_approved and iteration < max_reviewer_iterations:
                    print(f"[Workflow] STAGE 8: Refinement Cycle #{iteration}...")
                    self.developer.log(self.project_id, f"Reviewer rejected. Issues: {review_report.get('issues', [])}. Rewriting code...")
                    
                    # Update Developer Agent task to in-progress for refinement
                    update_task_status(dev_tid, "in_progress")
                    
                    # Ask developer agent to regenerate/fix files based on issues
                    refined_files = []
                    for file_info in files_to_create:
                        path = file_info["path"]
                        desc = f"{file_info['description']}. Please resolve these issues: {', '.join(review_report.get('issues', []))}."
                        code = self.developer.write_file(self.project_id, project_name, path, desc, f"{requirements}\nFix notes: {review_feedback}")
                        refined_files.append({"path": path, "code": code})
                        
                    generated_files = refined_files
                    complete_task(dev_tid, f"Refinement completed (Iteration #{iteration}). Re-writing files.")
                    iteration += 1
                else:
                    # Approved or max iterations reached
                    if not review_approved:
                        print("[Workflow] WARNING: Review not approved but reached max refinement limit.")
                    break
            
            # --- STAGE 9: GENERATE DOCUMENTATION ---
            print("[Workflow] STAGE 9: Generating System Documentation...")
            doc_tid = find_and_start_task("Documentation Agent")
            files_list = [f["path"] for f in files_to_create]
            readme_content = self.doc_writer.write_readme(self.project_id, project_name, requirements, files_list)
            complete_task(doc_tid, "README.md created.")
            
            # --- STAGE 10: DELIVER FINAL RESULT ---
            print("[Workflow] STAGE 10: Project Delivery...")
            manager_tid = find_and_start_task("Manager Agent")
            target_workspace = WORKSPACE_DIR / project_name
            self.manager.deliver_project(self.project_id, str(target_workspace), review_approved)
            
            # If manager task completed successfully, update status
            manager_task_id = manager_tid if manager_tid != -1 else get_task_id_for_agent("Manager Agent")
            if manager_task_id != -1:
                update_task_status(manager_task_id, "completed", "Delivery Success.")
            
            update_project_status(self.project_id, "completed")
            print(f"[Workflow] Project '{project_name}' completed successfully!")
            
        except Exception as e:
            tb = traceback.format_exc()
            print(f"[Workflow Error] Run failed: {e}\n{tb}")
            update_project_status(self.project_id, "failed")
            # Log failure to project log
            try:
                self.manager.log(self.project_id, f"CRITICAL CRASH in workflow: {e}\n{tb}")
            except:
                pass
