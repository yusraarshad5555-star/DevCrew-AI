import subprocess
import os
import sys
from devcrew_ai.agents.base import BaseAgent
from devcrew_ai.config import WORKSPACE_DIR

class TestingAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Testing Agent",
            role_description="QA Engineer who writes comprehensive test cases and validates execution correctness."
        )

    def run_tests(self, project_id: int, project_name: str) -> dict:
        self.log(project_id, "Preparing test environment and launching verification runner.")
        
        project_path = WORKSPACE_DIR / project_name
        
        # Use python executable on the same path
        python_exe = sys.executable
        
        # We discover and run tests in the 'tests' directory
        command = [python_exe, "-m", "unittest", "discover", "-s", "tests"]
        
        self.log(project_id, f"Executing command: {' '.join(command)} inside {project_path}")
        
        try:
            # Run the unit tests in a subprocess
            result = subprocess.run(
                command,
                cwd=project_path,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            stdout = result.stdout
            stderr = result.stderr
            
            output_log = f"--- STDOUT ---\n{stdout}\n--- STDERR ---\n{stderr}"
            self.log(project_id, f"Test execution completed with exit code: {result.returncode}")
            
            # Simple heuristic to determine test outcome
            # Unittest outputs details on stderr. It ends with 'OK' on success or 'FAILED' on failure.
            # Example stderr: "Ran 5 tests in 0.001s\n\nOK\n" or "FAILED (failures=1)"
            passed = True
            summary = "Tests passed successfully."
            
            if "FAILED" in stderr or result.returncode != 0:
                passed = False
                summary = "Test suite detected failures or errors."
                self.log(project_id, "WARNING: Test execution failures detected!")
            else:
                self.log(project_id, "SUCCESS: All unit tests passed successfully.")
                
            return {
                "passed": passed,
                "exit_code": result.returncode,
                "stdout": stdout,
                "stderr": stderr,
                "output_log": output_log,
                "summary": summary
            }
            
        except subprocess.TimeoutExpired:
            self.log(project_id, "ERROR: Test execution timed out after 30 seconds.")
            return {
                "passed": False,
                "exit_code": -1,
                "stdout": "",
                "stderr": "Timeout expired",
                "output_log": "ERROR: Timeout expired during test discovery.",
                "summary": "Verification timed out."
            }
        except Exception as e:
            self.log(project_id, f"ERROR: Exception running tests: {e}")
            return {
                "passed": False,
                "exit_code": -99,
                "stdout": "",
                "stderr": str(e),
                "output_log": f"EXCEPTION: {e}",
                "summary": f"Failed to execute tests: {e}"
            }
def run():
    pass
