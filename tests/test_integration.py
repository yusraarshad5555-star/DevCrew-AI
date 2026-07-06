import requests
import time
import sys

URL = "http://127.0.0.1:8000"

def run_integration_test():
    print("[Integration Test] Connecting to FastAPI backend...")
    try:
        r = requests.get(f"{URL}/")
        if r.status_code != 200:
            print(f"[Error] Backend is online but returned status: {r.status_code}")
            sys.exit(1)
        print("[Integration Test] Backend is online.")
    except Exception as e:
        print(f"[Error] Backend is offline or unreachable: {e}")
        sys.exit(1)
        
    payload = {
        "name": "IntegrationCalcApp",
        "description": "Create an offline double-precision math calculator with unit testing"
    }
    
    print(f"[Integration Test] Starting workflow for: '{payload['name']}'...")
    resp = requests.post(f"{URL}/api/projects", json=payload)
    if resp.status_code != 201:
        print(f"[Error] Failed to create project: {resp.text}")
        sys.exit(1)
        
    project = resp.json()
    project_id = project["id"]
    print(f"[Integration Test] Created Project ID {project_id}. Monitoring execution...")
    
    # Poll status
    max_checks = 60
    check_interval = 2
    status = "initialized"
    
    for i in range(max_checks):
        time.sleep(check_interval)
        try:
            status_data = requests.get(f"{URL}/api/projects/{project_id}").json()
            status = status_data["status"]
            print(f"[{i+1}/{max_checks}] Current Project Status: {status}")
            
            # Fetch tasks and count completions
            tasks = requests.get(f"{URL}/api/projects/{project_id}/tasks").json()
            completed_tasks = [t for t in tasks if t["status"] == "completed"]
            running_tasks = [t for t in tasks if t["status"] == "in_progress"]
            print(f"    - Tasks: {len(completed_tasks)}/{len(tasks)} completed. Currently running: {[t['name'] for t in running_tasks]}")
            
            if status in ["completed", "failed"]:
                break
        except Exception as e:
            print(f"Error checking status: {e}")
            
    if status == "completed":
        print("[Integration Test] SUCCESS! Multi-agent workflow completed successfully.")
        
        # Verify artifacts exist
        artifacts = requests.get(f"{URL}/api/projects/{project_id}/artifacts").json()
        print(f"[Integration Test] Generated files: {[a['filepath'] for a in artifacts]}")
        
        if len(artifacts) < 3:
            print("[Error] Expected at least 3 files (calculator.py, test_calculator.py, README.md)")
            sys.exit(1)
            
        print("[Integration Test] Full system integration test: PASSED.")
    else:
        print(f"[Error] Workflow execution failed or timed out. Final status: {status}")
        sys.exit(1)

if __name__ == "__main__":
    run_integration_test()
