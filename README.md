# 🚀 DevCrew AI
### Autonomous Multi-Agent Software Engineering Team

> An offline, autonomous multi-agent AI system that plans, designs, develops, tests, reviews, and documents software projects using specialized AI agents powered by a local LLM (Ollama).

---

## 📖 Overview

DevCrew AI is an autonomous software engineering system that simulates a complete software development team.

Instead of relying on a single AI assistant, DevCrew AI coordinates multiple specialized agents that collaborate to transform software requirements into a working project.

The entire system runs locally using Ollama, ensuring privacy, offline execution, and zero API costs.

This project was developed as part of the **Kaggle 5-Day AI Agents: Intensive Vibe Coding Capstone Project**.

---

# 🎯 Problem Statement

Modern software development involves many repetitive tasks including:

- Understanding requirements
- Planning implementation
- Researching technologies
- Designing architecture
- Writing code
- Running tests
- Reviewing code quality
- Creating documentation

Developers often switch between multiple tools to complete these tasks.

DevCrew AI automates this workflow by allowing specialized AI agents to collaborate just like a real software engineering team.

---

# 💡 Solution

DevCrew AI receives a software requirement from the user and automatically executes a complete development workflow.

The system:

- Understands project requirements
- Creates a development plan
- Researches best practices
- Designs project architecture
- Generates source code
- Executes automated tests
- Reviews generated code
- Produces project documentation

All of this happens without requiring cloud APIs.

---

# 🏗️ System Architecture

```
                User Request
                     │
                     ▼
             Manager Agent
                     │
                     ▼
             Planner Agent
                     │
                     ▼
            Research Agent
                     │
                     ▼
           Architect Agent
                     │
                     ▼
           Developer Agent
                     │
                     ▼
            Testing Agent
                     │
                     ▼
            Reviewer Agent
                     │
                     ▼
        Documentation Agent
                     │
                     ▼
          Generated Project
```

---

# 🤖 Multi-Agent Workflow

## 👨‍💼 Manager Agent

- Accepts user requirements
- Coordinates all agents
- Tracks workflow progress
- Delivers final project

---

## 📋 Planner Agent

- Analyzes requirements
- Breaks work into tasks
- Assigns responsibilities

---

## 🔍 Research Agent

- Suggests technologies
- Recommends best practices
- Stores findings in project memory

---

## 🏛️ Architect Agent

- Designs project structure
- Generates folder layout
- Plans software architecture

---

## 💻 Developer Agent

- Writes source code
- Creates project files
- Revises code based on reviewer feedback

---

## 🧪 Testing Agent

- Runs automated unit tests
- Detects failures
- Reports execution results

---

## ✅ Reviewer Agent

- Reviews generated code
- Detects implementation issues
- Requests improvements

---

## 📚 Documentation Agent

- Generates README
- Creates setup instructions
- Documents the final project

---

# ✨ Features

- Multi-Agent Collaboration
- Autonomous Planning
- Project Memory
- Offline Execution
- Local LLM Integration
- Automated Code Generation
- Automated Testing
- Code Review Loop
- README Generation
- SQLite Project Database
- Streamlit Dashboard
- FastAPI Backend

---

# 🛠️ Technologies Used

## AI

- Ollama
- Qwen2.5-Coder
- Multi-Agent Architecture

## Backend

- Python 3
- FastAPI
- SQLite

## Frontend

- Streamlit

## Development

- Uvicorn
- unittest
- Pydantic

---

# 📂 Project Structure

```
devcrew_ai/
│
├── agents/
│   ├── Manager
│   ├── Planner
│   ├── Research
│   ├── Architect
│   ├── Developer
│   ├── Testing
│   ├── Reviewer
│   └── Documentation
│
├── llm/
├── memory/
├── tools/
│
streamlit_app/
tests/
generated_projects/
```

---

# 🔄 Workflow

1. User enters project requirements
2. Manager initializes workflow
3. Planner creates execution plan
4. Research Agent gathers information
5. Architect designs project
6. Developer writes code
7. Testing Agent executes tests
8. Reviewer validates implementation
9. Documentation Agent creates README
10. Manager delivers project

---

# 🔒 Security

- Offline execution
- No external API calls
- No API keys required
- Local SQLite database
- Local LLM inference
- Private project generation

---

# 🚀 Getting Started

 ## Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/DevCrew-AI.git

cd DevCrew-AI
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Install Ollama

Download:

https://ollama.com

Pull the model:

```bash
ollama pull qwen2.5-coder:3b
```

or

```bash
ollama pull qwen2.5-coder:7b
```

---

## Configure

Create a `.env` file

```env
LLM_PROVIDER=ollama

OLLAMA_MODEL=qwen2.5-coder:3b
```

---

## Start Backend

```bash
python -m uvicorn devcrew_ai.main:app --host 127.0.0.1 --port 8000
```

---

## Start Dashboard

```bash
streamlit run streamlit_app/app.py
```

Open

```
http://localhost:8501
```

---

# 📸 Screenshots

<img width="1893" height="1005" alt="Image" src="https://github.com/user-attachments/assets/6e12bd07-69f3-487d-ae22-59317eaf2b4c" />

---

# 🎥 Demo

A complete demonstration video is available in the Kaggle submission.

<img width="1894" height="1006" alt="Image" src="https://github.com/user-attachments/assets/62b49945-ab61-4e47-9e12-c34d1bd18249" />

# 📈 Future Improvements

- Google ADK Integration
- MCP Server Support
- Docker Deployment
- GitHub Pull Request Automation
- CI/CD Pipeline
- Multi-language Code Generation
- RAG Knowledge Base
- Long-Term Agent Memory

---

# 📄 License

MIT License

---

# 👨‍💻 Author

**Yusra Arshad**

Build with focus and hardwork for Ai Engineering & Multiagent system

---

# ⭐ Acknowledgements

Built as part of the

**Kaggle 5-Day AI Agents: Intensive Vibe Coding Course with Google**

Special thanks to the Kaggle and Google teams for providing the learning resources and inspiration behind this project.
