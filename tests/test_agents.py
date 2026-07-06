import unittest
import os
import tempfile
from unittest.mock import patch

import tempfile
import os

# Set DB_PATH to a temporary file instead of :memory: so multiple connection opens share tables
db_fd, temp_db_path = tempfile.mkstemp(suffix=".db")
os.close(db_fd)
os.environ["DB_PATH"] = temp_db_path
os.environ["LLM_PROVIDER"] = "mock"

from devcrew_ai.database import init_db, create_project, get_tasks_for_project, get_logs_for_project
from devcrew_ai.llm import get_llm
from devcrew_ai.agents.base import BaseAgent
from devcrew_ai.agents.planner import PlannerAgent

class TestAgentsAndWorkflow(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Initialize memory database
        init_db()

    @classmethod
    def tearDownClass(cls):
        if os.path.exists(temp_db_path):
            try:
                os.remove(temp_db_path)
            except Exception as e:
                print(f"Error removing temp test DB: {e}")

    def setUp(self):
        self.project_id = create_project("TestApp", "Create a basic math calculator app")

    def test_mock_llm_provider(self):
        llm = get_llm()
        resp = llm.generate("Hello", system_instruction="Planner Agent")
        # Planner response should contain tasks JSON array
        self.assertIn("tasks", resp)

    def test_base_agent_logging(self):
        agent = BaseAgent(name="Test Agent", role_description="Test Role")
        agent.log(self.project_id, "This is a unit test log entry.")
        
        # Verify it got saved in SQLite logs table
        logs = get_logs_for_project(self.project_id)
        self.assertEqual(len(logs), 1)
        self.assertEqual(logs[0]["agent_name"], "Test Agent")
        self.assertEqual(logs[0]["log_text"], "This is a unit test log entry.")

    def test_planner_agent_tasks_insertion(self):
        planner = PlannerAgent()
        tasks = planner.plan_project(self.project_id, "Create a basic math calculator app")
        
        # Should create tasks in database
        db_tasks = get_tasks_for_project(self.project_id)
        self.assertEqual(len(db_tasks), len(tasks))
        self.assertEqual(db_tasks[0]["name"], tasks[0]["name"])
        self.assertEqual(db_tasks[0]["assigned_to"], tasks[0]["assigned_to"])

    def test_manager_delivery_approved(self):
        from devcrew_ai.agents.manager import ManagerAgent
        manager = ManagerAgent()
        
        # Mock logging or clear existing logs to isolate test
        res = manager.deliver_project(self.project_id, "test_workspace_approved", approved=True)
        self.assertEqual(res, "SUCCESS")
        
        logs = get_logs_for_project(self.project_id)
        # Verify the success messages are in the logs
        delivery_ready_logged = any("DevCrew AI project delivery ready!" in log["log_text"] for log in logs)
        self.assertTrue(delivery_ready_logged)
        
    def test_manager_delivery_unresolved(self):
        from devcrew_ai.agents.manager import ManagerAgent
        manager = ManagerAgent()
        
        res = manager.deliver_project(self.project_id, "test_workspace_failed", approved=False)
        self.assertEqual(res, "UNRESOLVED")
        
        logs = get_logs_for_project(self.project_id)
        # Verify the failure/unresolved messages are in the logs
        unresolved_logged = any("Project finished with unresolved issues." in log["log_text"] for log in logs)
        delivery_ready_logged = any("DevCrew AI project delivery ready!" in log["log_text"] for log in logs)
        self.assertTrue(unresolved_logged)
        self.assertFalse(delivery_ready_logged)

if __name__ == "__main__":
    unittest.main()
