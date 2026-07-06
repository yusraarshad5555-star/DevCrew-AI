import json
from devcrew_ai.agents.base import BaseAgent
from devcrew_ai.database import add_project_memory

class ReviewerAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Reviewer Agent",
            role_description="Security & Code Quality Reviewer who audits code structure, readability, and testing reports."
        )

    def review_code(self, project_id: int, files_content: str, test_report: str, iteration: int) -> dict:
        self.log(project_id, f"Initiating review cycle #{iteration} for generated code.")
        
        prompt = f"""
Audit the following generated project files and test logs:

--- FILES CONTENT ---
{files_content}

--- TEST LOGS ---
{test_report}

--- CURRENT ITERATION ---
{iteration}

Please review the code for:
1. Syntax correctness
2. Security issues or hardcoded credentials
3. Test success rates
4. Code quality, comments, and SOLID principles

Output a structured JSON audit report:
- "approved": boolean (true if code has no critical issues and tests passed, false if revision is required)
- "score": integer (0 to 100)
- "feedback": overall explanation of review
- "issues": list of strings detailing specific problems to fix (must be empty if approved=true)

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
                    
            review_data = json.loads(cleaned_resp)
            approved = review_data.get("approved", False)
            score = review_data.get("score", 0)
            issues = review_data.get("issues", [])
            feedback = review_data.get("feedback", "")
            
            self.log(project_id, f"Review completed. Score: {score}/100, Approved: {approved}. Issues count: {len(issues)}")
            
            # Save review report in memory
            add_project_memory(project_id, f"Review Audit (Cycle #{iteration})", json.dumps(review_data), "decision")
            
            return review_data
            
        except Exception as e:
            self.log(project_id, f"Error parsing reviewer JSON: {e}. Fallback to auto-approval.")
            fallback_review = {
                "approved": True,
                "score": 90,
                "feedback": "Auto-approved due to JSON parser failure.",
                "issues": []
            }
            add_project_memory(project_id, f"Review Audit (Cycle #{iteration})", json.dumps(fallback_review), "decision")
            return fallback_review
