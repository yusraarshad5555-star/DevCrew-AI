import json
import re
from devcrew_ai.llm.base import BaseLLM

class MockLLM(BaseLLM):
    def generate(self, prompt: str, system_instruction: str = "") -> str:
        """
        Simulate LLM generation based on system instructions and prompt contents.
        Generates realistic plans, architecture designs, working python code, tests, and documentation.
        """
        # Determine active agent from system_instruction or prompt
        agent_role = "developer"
        inst_lower = system_instruction.lower()
        prompt_lower = prompt.lower()
        
        if "manager" in inst_lower:
            agent_role = "manager"
        elif "planner" in inst_lower:
            agent_role = "planner"
        elif "research" in inst_lower:
            agent_role = "research"
        elif "architect" in inst_lower:
            agent_role = "architect"
        elif "developer" in inst_lower:
            agent_role = "developer"
        elif "test" in inst_lower or "qa" in inst_lower:
            agent_role = "tester"
        elif "reviewer" in inst_lower:
            agent_role = "reviewer"
        elif "documentation" in inst_lower:
            agent_role = "documentation"
            
        # Determine project type
        project_type = "generic"
        if "calculator" in prompt_lower or "math" in prompt_lower:
            project_type = "calculator"
        elif "weather" in prompt_lower or "forecast" in prompt_lower:
            project_type = "weather"
        elif "scraper" in prompt_lower or "scrape" in prompt_lower or "crawler" in prompt_lower:
            project_type = "scraper"
        elif "todo" in prompt_lower or "task" in prompt_lower or "to-do" in prompt_lower:
            project_type = "todo"
            
        # Dispatch to simulated response based on agent role
        if agent_role == "manager":
            return self._sim_manager(prompt, project_type)
        elif agent_role == "planner":
            return self._sim_planner(prompt, project_type)
        elif agent_role == "research":
            return self._sim_research(prompt, project_type)
        elif agent_role == "architect":
            return self._sim_architect(prompt, project_type)
        elif agent_role == "developer":
            return self._sim_developer(prompt, project_type)
        elif agent_role == "tester":
            return self._sim_tester(prompt, project_type)
        elif agent_role == "reviewer":
            return self._sim_reviewer(prompt, project_type)
        elif agent_role == "documentation":
            return self._sim_documentation(prompt, project_type)
            
        return f"[MockLLM] Simulated response for agent '{agent_role}' on project type '{project_type}'."

    def _sim_manager(self, prompt: str, project_type: str) -> str:
        return f"""[Manager Agent]
Analyzed project requirement. The user wants to build a {project_type} application.
Targeting a clean, production-ready implementation inside the workspace.
Passing execution to the Planner Agent to decompose the tasks.
Status: Success. Initialized workspace settings."""

    def _sim_planner(self, prompt: str, project_type: str) -> str:
        tasks = []
        if project_type == "calculator":
            tasks = [
                {"name": "Research Stack", "description": "Research Python math modules and standard practices.", "agent": "Research Agent"},
                {"name": "Design Architecture", "description": "Design modular folder layout and calculator API class.", "agent": "Architect Agent"},
                {"name": "Implement Calculator Logic", "description": "Create calculator.py containing core math operations.", "agent": "Developer Agent"},
                {"name": "Implement Test Cases", "description": "Create test_calculator.py covering standard and boundary math inputs.", "agent": "Testing Agent"},
                {"name": "Review and Quality Audit", "description": "Perform static analysis, verify edge cases, code quality and test coverage.", "agent": "Reviewer Agent"},
                {"name": "Documentation Generation", "description": "Create README, CLI setup documentation, and API guides.", "agent": "Documentation Agent"}
            ]
        elif project_type == "weather":
            tasks = [
                {"name": "Research Weather APIs", "description": "Research offline mock weather API and standard requests.", "agent": "Research Agent"},
                {"name": "Design Weather App Architecture", "description": "Design directory structures, models, and interfaces.", "agent": "Architect Agent"},
                {"name": "Implement Weather Service", "description": "Create service and mock data structures in weather.py.", "agent": "Developer Agent"},
                {"name": "Implement App Tests", "description": "Create test_weather.py to validate API and offline fallbacks.", "agent": "Testing Agent"},
                {"name": "Review System Quality", "description": "Verify code readability, error handling, and security.", "agent": "Reviewer Agent"},
                {"name": "Generate User Documentation", "description": "Write project README.md, API contracts, and usage logs.", "agent": "Documentation Agent"}
            ]
        elif project_type == "scraper":
            tasks = [
                {"name": "Research Scraper Libraries", "description": "Check libraries for offline simulation and HTML parsing.", "agent": "Research Agent"},
                {"name": "Design Scraping Module", "description": "Outline structures, result models, and API interfaces.", "agent": "Architect Agent"},
                {"name": "Implement Scraper Logic", "description": "Write web_scraper.py with offline fallback HTML parsing.", "agent": "Developer Agent"},
                {"name": "Write Scraper Tests", "description": "Create test_scraper.py testing parser and error responses.", "agent": "Testing Agent"},
                {"name": "Review Scraper Quality", "description": "Validate error logging, timeout settings, and SOLID principles.", "agent": "Reviewer Agent"},
                {"name": "Write Scraper Docs", "description": "Write setup guidelines, CLI args reference, and documentation.", "agent": "Documentation Agent"}
            ]
        else:  # todo & generic
            tasks = [
                {"name": "Research Stack", "description": "Research standard libraries for task tracking and serialization.", "agent": "Research Agent"},
                {"name": "Design Directory & Database Schema", "description": "Create folder structure and SQLite schema layout.", "agent": "Architect Agent"},
                {"name": "Develop App Logic", "description": "Write todo.py containing database connection and CRUD methods.", "agent": "Developer Agent"},
                {"name": "Implement Unit Tests", "description": "Create test_todo.py with standard task lifecycle assertions.", "agent": "Testing Agent"},
                {"name": "Audit App Quality", "description": "Inspect error paths, code design patterns, and reliability.", "agent": "Reviewer Agent"},
                {"name": "Document To-Do Application", "description": "Write setup instructions, schema details, and API docs.", "agent": "Documentation Agent"}
            ]
        return json.dumps({"tasks": tasks}, indent=2)

    def _sim_research(self, prompt: str, project_type: str) -> str:
        if project_type == "calculator":
            return """[Research Report - Calculator]
Recommended Technology Stack:
- Core: Python 3.12+ (standard library only, zero external dependencies required)
- Testing: Standard `unittest` framework.
- Design: OOP class architecture with double-precision floating support.
No external network components needed. Fully offline compatible."""
        elif project_type == "weather":
            return """[Research Report - Weather Simulator]
Recommended Technology Stack:
- Core: Python 3.12+ standard library (`urllib.request` or simulated client).
- Data Source: Offline JSON database to simulate external weather APIs (prevents API key requirement and matches 100% offline goal).
- Testing: Standard `unittest` or mock requests.
- Caching: Local memory cache with dictionary."""
        elif project_type == "scraper":
            return """[Research Report - Web Scraper]
Recommended Technology Stack:
- Core: Standard library `urllib` (request parsing) or a local mock HTML engine to simulate offline page scraping.
- Parser: Regex or light HTML tag parser built in Python to avoid binary dependencies.
- Testing: `unittest` with mock offline pages."""
        else:
            return """[Research Report - CRUD Task Manager]
Recommended Technology Stack:
- Core: Python 3.12+ standard libraries.
- Storage: SQLite for lightweight, local database engine.
- Testing: Standard library `unittest` using memory database (`:memory:`) to ensure quick and isolated test runs."""

    def _sim_architect(self, prompt: str, project_type: str) -> str:
        layout = {}
        if project_type == "calculator":
            layout = {
                "directories": ["src", "tests"],
                "files": [
                    {"path": "src/calculator.py", "description": "Core calculator logic class."},
                    {"path": "tests/test_calculator.py", "description": "Unit tests for calculator operations."}
                ],
                "database_schema": "None. Static stateless calculator class."
            }
        elif project_type == "weather":
            layout = {
                "directories": ["src", "tests", "data"],
                "files": [
                    {"path": "src/weather.py", "description": "Mock weather client and data models."},
                    {"path": "data/cities.json", "description": "Offline database containing simulated cities weather information."},
                    {"path": "tests/test_weather.py", "description": "Unit tests validating weather lookup."}
                ],
                "database_schema": "JSON database storing mock city weather details."
            }
        elif project_type == "scraper":
            layout = {
                "directories": ["src", "tests", "samples"],
                "files": [
                    {"path": "src/scraper.py", "description": "Offline page parser and request handler."},
                    {"path": "samples/mock_page.html", "description": "Local test html page for offline scraping verification."},
                    {"path": "tests/test_scraper.py", "description": "Scraping results parser validations."}
                ],
                "database_schema": "None. Scraped data output to JSON file."
            }
        else:  # todo/generic
            layout = {
                "directories": ["src", "tests"],
                "files": [
                    {"path": "src/todo.py", "description": "SQLite task CRUD implementation."},
                    {"path": "tests/test_todo.py", "description": "Unit tests running against SQLite database."}
                ],
                "database_schema": "Table `tasks`: id (INTEGER PRIMARY KEY), title (TEXT), completed (INTEGER), due_date (TEXT)"
            }
        return json.dumps(layout, indent=2)

    def _sim_developer(self, prompt: str, project_type: str) -> str:
        # Check if the prompt specifically asks to write code for a specific file path
        # In developer agent, the workflow loops through files to generate. We check the path in prompt.
        path_match = re.search(r'file\s+path\s*:\s*([^\s\n]+)', prompt, re.IGNORECASE)
        file_path = path_match.group(1) if path_match else ""
        
        if "calculator.py" in file_path:
            return """class Calculator:
    \"\"\"A robust, production-quality offline calculator implementation.\"\"\"
    
    def add(self, a: float, b: float) -> float:
        return float(a + b)
        
    def subtract(self, a: float, b: float) -> float:
        return float(a - b)
        
    def multiply(self, a: float, b: float) -> float:
        return float(a * b)
        
    def divide(self, a: float, b: float) -> float:
        if b == 0:
            raise ValueError("Division by zero is not allowed.")
        return float(a / b)
        
    def power(self, base: float, exponent: float) -> float:
        return float(base ** exponent)
"""
        elif "test_calculator.py" in file_path:
            return """import unittest
from src.calculator import Calculator

class TestCalculator(unittest.TestCase):
    def setUp(self):
        self.calc = Calculator()
        
    def test_add(self):
        self.assertEqual(self.calc.add(2.5, 3.5), 6.0)
        self.assertEqual(self.calc.add(-1, 1), 0.0)
        
    def test_subtract(self):
        self.assertEqual(self.calc.subtract(5, 3), 2.0)
        
    def test_multiply(self):
        self.assertEqual(self.calc.multiply(3, 4), 12.0)
        
    def test_divide(self):
        self.assertEqual(self.calc.divide(10, 2), 5.0)
        with self.assertRaises(ValueError):
            self.calc.divide(5, 0)
            
    def test_power(self):
        self.assertEqual(self.calc.power(2, 3), 8.0)

if __name__ == "__main__":
    unittest.main()
"""
        elif "weather.py" in file_path:
            return """import json
import os
from typing import Dict, Any, Optional

class WeatherService:
    \"\"\"Offline weather query service using a local JSON database.\"\"\"
    
    def __init__(self, db_path: str = "data/cities.json"):
        self.db_path = db_path
        self._init_mock_db()
        
    def _init_mock_db(self):
        # Create directory if needed
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        if not os.path.exists(self.db_path):
            mock_data = {
                "tokyo": {"temp": 22.5, "condition": "Sunny", "humidity": 60},
                "new york": {"temp": 15.0, "condition": "Cloudy", "humidity": 75},
                "london": {"temp": 11.2, "condition": "Rainy", "humidity": 90},
                "paris": {"temp": 17.8, "condition": "Clear", "humidity": 55}
            }
            with open(self.db_path, 'w') as f:
                json.dump(mock_data, f, indent=2)
                
    def get_weather(self, city: str) -> Optional[Dict[str, Any]]:
        city = city.strip().lower()
        if not os.path.exists(self.db_path):
            return None
        with open(self.db_path, 'r') as f:
            data = json.load(f)
        return data.get(city)
"""
        elif "cities.json" in file_path:
            return """{
  "tokyo": {"temp": 22.5, "condition": "Sunny", "humidity": 60},
  "new york": {"temp": 15.0, "condition": "Cloudy", "humidity": 75},
  "london": {"temp": 11.2, "condition": "Rainy", "humidity": 90},
  "paris": {"temp": 17.8, "condition": "Clear", "humidity": 55}
}"""
        elif "test_weather.py" in file_path:
            return """import unittest
import os
import tempfile
import json
from src.weather import WeatherService

class TestWeatherService(unittest.TestCase):
    def setUp(self):
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix=".json")
        self.temp_db.close()
        # Initialize service with temporary DB
        self.service = WeatherService(db_path=self.temp_db.name)
        
    def tearDown(self):
        if os.path.exists(self.temp_db.name):
            os.remove(self.temp_db.name)
            
    def test_mock_cities(self):
        data = self.service.get_weather("Tokyo")
        self.assertIsNotNone(data)
        self.assertEqual(data["condition"], "Sunny")
        self.assertEqual(data["temp"], 22.5)
        
    def test_nonexistent_city(self):
        data = self.service.get_weather("Atlantis")
        self.assertIsNull(data) if hasattr(self, 'assertIsNull') else self.assertIsNone(data)

if __name__ == "__main__":
    unittest.main()
"""
        elif "scraper.py" in file_path:
            return """import re
from typing import Dict, List, Any

class SimpleOfflineScraper:
    \"\"\"Offline HTML page parser for extracting links and text headlines.\"\"\"
    
    def parse_headlines(self, html_content: str) -> List[str]:
        # Simple regex parser for list elements or headers
        headings = re.findall(r'<h[1-3][^>]*>(.*?)</h[1-3]>', html_content, re.IGNORECASE)
        return [h.strip() for h in headings]
        
    def parse_links(self, html_content: str) -> List[str]:
        # Simple link parser
        links = re.findall(r'href=["\'](http[s]?://[^"\']+|/[^"\']+)["\']', html_content, re.IGNORECASE)
        return [l.strip() for l in links]
"""
        elif "mock_page.html" in file_path:
            return """<!DOCTYPE html>
<html>
<head><title>Test News Page</title></head>
<body>
    <h1>Breaking Local News</h1>
    <div class="article">
        <h2>Local Tech Team Builds Offline AI Agent</h2>
        <p>A capstone project wins recognition. Read <a href="https://example.com/details">here</a>.</p>
    </div>
    <div class="article">
        <h3>Weather Forecast is Sunny</h3>
        <p>Offline simulation models run successfully. Read <a href="/weather">forecast</a>.</p>
    </div>
</body>
</html>"""
        elif "test_scraper.py" in file_path:
            return """import unittest
from src.scraper import SimpleOfflineScraper

class TestOfflineScraper(unittest.TestCase):
    def setUp(self):
        self.scraper = SimpleOfflineScraper()
        self.html = \"\"\"
        <html>
            <body>
                <h1>Main Heading</h1>
                <h2>Sub Heading</h2>
                <a href="https://google.com">Google</a>
                <a href="/about">About Us</a>
            </body>
        </html>
        \"\"\"
        
    def test_parse_headlines(self):
        headlines = self.scraper.parse_headlines(self.html)
        self.assertIn("Main Heading", headlines)
        self.assertIn("Sub Heading", headlines)
        
    def test_parse_links(self):
        links = self.scraper.parse_links(self.html)
        self.assertIn("https://google.com", links)
        self.assertIn("/about", links)

if __name__ == "__main__":
    unittest.main()
"""
        elif "todo.py" in file_path:
            return """import sqlite3
from typing import List, Tuple, Dict, Any

class TodoManager:
    \"\"\"A local SQLite to-do task tracking repository.\"\"\"
    
    def __init__(self, db_path: str = ":memory:"):
        self.db_path = db_path
        self._init_db()
        
    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(\"\"\"
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                completed INTEGER DEFAULT 0
            )
            \"\"\")
            conn.commit()
            
    def add_task(self, title: str) -> int:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO tasks (title) VALUES (?)", (title,))
            conn.commit()
            return cursor.lastrowid
            
    def complete_task(self, task_id: int):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("UPDATE tasks SET completed = 1 WHERE id = ?", (task_id,))
            conn.commit()
            
    def get_tasks(self) -> List[Dict[str, Any]]:
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            rows = cursor.execute("SELECT id, title, completed FROM tasks").fetchall()
            return [{"id": r["id"], "title": r["title"], "completed": bool(r["completed"])} for r in rows]
"""
        elif "test_todo.py" in file_path:
            return """import unittest
from src.todo import TodoManager

class TestTodoManager(unittest.TestCase):
    def setUp(self):
        self.manager = TodoManager(":memory:")
        
    def test_add_task(self):
        tid = self.manager.add_task("Write unit tests")
        self.assertEqual(tid, 1)
        tasks = self.manager.get_tasks()
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0]["title"], "Write unit tests")
        self.assertFalse(tasks[0]["completed"])
        
    def test_complete_task(self):
        tid = self.manager.add_task("Buy groceries")
        self.manager.complete_task(tid)
        tasks = self.manager.get_tasks()
        self.assertTrue(tasks[0]["completed"])

if __name__ == "__main__":
    unittest.main()
"""
        else:
            # Fallback file content if custom name requested
            return f"""# Generated file: {file_path}
# Offline local mock file
def main():
    print("Welcome to DevCrew AI generated project for {project_type}!")

if __name__ == "__main__":
    main()
"""

    def _sim_tester(self, prompt: str, project_type: str) -> str:
        return f"""[Testing Agent Report]
Unit tests have been created in the `tests/` directory for the {project_type} project.
Executing command: `python -m unittest discover -s tests` inside target path.
All test files compile. Verification complete. Passed 100% of generated test cases."""

    def _sim_reviewer(self, prompt: str, project_type: str) -> str:
        # Return a structured review, indicating if revision is needed.
        # We can simulate 1 issue in the first round, and then approve in the second round to show reflection.
        if "revision" in prompt.lower() or "revised" in prompt.lower() or "fixed" in prompt.lower() or "second review" in prompt.lower() or "feedback" in prompt.lower():
            return json.dumps({
                "approved": True,
                "score": 98,
                "feedback": "All previously identified issues are resolved. Code follows SOLID principles, has proper error handling, docstrings are present, and the test suite passes cleanly.",
                "issues": []
            }, indent=2)
        else:
            return json.dumps({
                "approved": False,
                "score": 82,
                "feedback": "Code is solid but requires minor cleanups. Missing explicit return type hints in some functions and needs additional class-level docstrings.",
                "issues": [
                    "Ensure all functions have explicit type hints.",
                    "Verify division by zero handles raising specific ValueError in Calculator class."
                ]
            }, indent=2)

    def _sim_documentation(self, prompt: str, project_type: str) -> str:
        return f"""# {project_type.capitalize()} Project - DevCrew AI Generated

This project is a clean, production-ready implementation of a {project_type} application generated by the **DevCrew AI** agent workflow.

## Directory Structure
- `src/`: Core logic modules.
- `tests/`: Isolated unittest modules.
- `README.md`: Installation and deployment guide.

## Getting Started
To run this application locally, run:
```bash
python src/{project_type}.py
```

## Running Tests
Run the test suite using standard Python unittest:
```bash
python -m unittest discover -s tests
```
"""
