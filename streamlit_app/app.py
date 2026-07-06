import streamlit as st
import requests
import time
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Backend URL config
BACKEND_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="DevCrew AI — Autonomous Engineering Board",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Premium Styling injection
st.markdown("""
<style>
    /* Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&family=JetBrains+Mono:wght@300;400;700&display=swap');
    
    /* Core Layout Styles */
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
    }
    
    /* Custom Header Gradient */
    .header-gradient {
        background: linear-gradient(135deg, #FF3366 0%, #7000FF 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        font-size: 3rem;
        margin-bottom: 0.2rem;
        letter-spacing: -1px;
    }
    
    .subtitle-text {
        font-size: 1.1rem;
        color: #8892B0;
        margin-bottom: 2rem;
        font-weight: 300;
    }
    
    /* Glassmorphic Container Cards */
    .glass-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.2);
        backdrop-filter: blur(8px);
        -webkit-backdrop-filter: blur(8px);
    }
    
    .agent-active-badge {
        background: linear-gradient(90deg, #7000FF 0%, #00C4FF 100%);
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 50px;
        font-weight: 600;
        font-size: 0.85rem;
        display: inline-block;
    }
    
    .status-running {
        color: #00FFCC;
        font-weight: bold;
        animation: pulse 1.5s infinite;
    }
    
    .status-completed {
        color: #00FF66;
        font-weight: bold;
    }
    
    .status-failed {
        color: #FF3366;
        font-weight: bold;
    }
    
    @keyframes pulse {
        0% { opacity: 0.4; }
        50% { opacity: 1; }
        100% { opacity: 0.4; }
    }
    
    /* Console Terminal Look */
    .terminal-container {
        font-family: 'JetBrains Mono', monospace;
        background-color: #0E1117;
        border: 1px solid #1F2937;
        border-radius: 8px;
        padding: 1rem;
        height: 380px;
        overflow-y: auto;
        font-size: 0.9rem;
        line-height: 1.4;
        color: #E2E8F0;
    }
    
    .terminal-line {
        margin-bottom: 0.5rem;
        border-left: 3px solid #7000FF;
        padding-left: 8px;
    }
</style>
""", unsafe_allow_html=True)

# Main Title Header
st.markdown('<div class="header-gradient">DevCrew AI</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle-text">Autonomous Multi-Agent Offline Software Engineering Board</div>', unsafe_allow_html=True)

# Sidebar - Project Selector & Configuration
st.sidebar.markdown("## ⚙️ Configuration")

# Safe API Connection Check
backend_online = False
try:
    health_resp = requests.get(f"{BACKEND_URL}/")
    if health_resp.status_code == 200:
        backend_online = True
except Exception:
    backend_online = False

if backend_online:
    st.sidebar.success("🟢 Backend Service: Online")
else:
    st.sidebar.error("🔴 Backend Service: Offline. Start backend using `uvicorn devcrew_ai.main:app`")

# Load environment configuration details
llm_provider = os.getenv("LLM_PROVIDER", "mock")
ollama_model = os.getenv("OLLAMA_MODEL", "qwen2.5-coder:7b")

st.sidebar.markdown(f"**LLM Mode:** `{llm_provider}`")
if llm_provider == "ollama":
    st.sidebar.markdown(f"**Ollama Model:** `{ollama_model}`")

st.sidebar.markdown("---")
st.sidebar.markdown("## 📂 Projects List")

# Fetch all projects
projects = []
if backend_online:
    try:
        projects = requests.get(f"{BACKEND_URL}/api/projects").json()
    except Exception as e:
        st.sidebar.error(f"Error loading projects: {e}")

project_options = {f"#{p['id']}: {p['name']}": p['id'] for p in projects}

# Project selection dropdown
selected_project_label = st.sidebar.selectbox(
    "Active Workspace",
    options=list(project_options.keys()),
    index=0 if project_options else None,
    help="Select a previous project workspace to view tasks, logs, and deliverables."
)

active_project_id = project_options[selected_project_label] if selected_project_label else None

# Action buttons in sidebar
if active_project_id:
    if st.sidebar.button("🗑️ Delete Workspace Data", use_container_width=True):
        try:
            requests.delete(f"{BACKEND_URL}/api/projects/{active_project_id}")
            st.toast("Workspace data cleared.")
            time.sleep(0.5)
            st.rerun()
        except Exception as e:
            st.sidebar.error(f"Failed to delete: {e}")

# Layout columns: Main display area splits
tab1, tab2, tab3 = st.tabs(["🚀 Launch Board", "📊 Workflow Execution", "📦 Deliverables Explorer"])

# --- TAB 1: LAUNCH BOARD ---
with tab1:
    st.markdown("### Create New Agentic Project")
    
    with st.form("new_project_form"):
        proj_name = st.text_input("Project Name", placeholder="e.g., WeatherApp", help="Letters and numbers only. No spaces.")
        proj_desc = st.text_area(
            "Software Requirements & Objective", 
            placeholder="Describe the software you want DevCrew AI to build. E.g.,\nCreate a local weather forecast app that mock reads data from cities.json and displays details in a command line interface. Implement full unit test suites.",
            height=200
        )
        
        submit_btn = st.form_submit_button("🚀 Start DevCrew Workflow", use_container_width=True)
        
        if submit_btn:
            if not proj_name.isalnum():
                st.error("Project Name must be alpha-numeric only (no spaces or special characters).")
            elif len(proj_desc) < 5:
                st.error("Please provide a more detailed requirement description.")
            elif not backend_online:
                st.error("Cannot launch project. FastAPI Backend Server is offline.")
            else:
                try:
                    payload = {"name": proj_name, "description": proj_desc}
                    response = requests.post(f"{BACKEND_URL}/api/projects", json=payload)
                    
                    if response.status_code == 201:
                        new_proj = response.json()
                        st.success(f"Success! Project #{new_proj['id']} created. Running multi-agent workflow...")
                        # Save in session state and switch to tab 2
                        st.session_state["active_project_id"] = new_proj["id"]
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error(f"Error starting project: {response.text}")
                except Exception as e:
                    st.error(f"Request failed: {e}")

    st.markdown("""
    #### 💡 Supported Offline Workflows
    Because this DevCrew AI node is configured to run **100% offline**, it utilizes smart local rule templates to model agent decisions and generate real code. Recommended prompts to test:
    - `Offline double-precision math calculator with unit testing`
    - `SQLite based task CRUD to-do list manager`
    - `Local news tag and link parser web scraper simulator`
    - `Offline weather forecast city index service`
    """)

# --- TAB 2: WORKFLOW EXECUTION ---
with tab2:
    if not active_project_id:
        st.info("No active workspace selected. Select one in the sidebar or create a new project.")
    else:
        # Load active project status
        try:
            proj_data = requests.get(f"{BACKEND_URL}/api/projects/{active_project_id}").json()
            tasks_data = requests.get(f"{BACKEND_URL}/api/projects/{active_project_id}/tasks").json()
            logs_data = requests.get(f"{BACKEND_URL}/api/projects/{active_project_id}/logs").json()
            
            # Status Banner
            status = proj_data["status"]
            status_class = ""
            if status == "running":
                status_class = '<span class="status-running">🔄 RUNNING</span>'
            elif status == "completed":
                status_class = '<span class="status-completed">✅ COMPLETED</span>'
            elif status == "failed":
                status_class = '<span class="status-failed">❌ FAILED</span>'
            else:
                status_class = f"<span>{status.upper()}</span>"
                
            st.markdown(f"#### Workspace Status: {status_class}", unsafe_allow_html=True)
            st.markdown(f"**Objective**: {proj_data['description']}")
            st.markdown("---")
            
            # Create two columns for Tasks and Logs
            col_tasks, col_logs = st.columns([1, 1])
            
            with col_tasks:
                st.markdown("#### 📋 Decomposed Project Plan")
                
                if not tasks_data:
                    st.write("Planner Agent has not generated tasks yet.")
                else:
                    for task in tasks_data:
                        t_status = task["status"]
                        icon = "⏳"
                        if t_status == "in_progress":
                            icon = "🔄"
                        elif t_status == "completed":
                            icon = "✅"
                        elif t_status == "failed":
                            icon = "❌"
                            
                        with st.container():
                            st.markdown(
                                f"""
                                <div class="glass-card" style="padding: 1rem; margin-bottom: 0.8rem;">
                                    <strong>{icon} {task['name']}</strong><br/>
                                    <small style='color: #8892B0;'>Agent: {task['assigned_to']}</small><br/>
                                    <p style='margin: 0.3rem 0; font-size: 0.95rem;'>{task['description']}</p>
                                </div>
                                """,
                                unsafe_allow_html=True
                            )
                            
            with col_logs:
                # Determine active agent from logs or running task
                active_agent = "Manager Agent"
                for task in tasks_data:
                    if task["status"] == "in_progress":
                        active_agent = task["assigned_to"]
                        break
                        
                st.markdown(
                    f'#### 💬 Live Console Log <span class="agent-active-badge">Active: {active_agent}</span>',
                    unsafe_allow_html=True
                )
                
                if not logs_data:
                    st.markdown("<div class='terminal-container'>Logs initializing...</div>", unsafe_allow_html=True)
                else:
                    log_html = "<div class='terminal-container'>"
                    for log in logs_data:
                        clean_text = log['log_text'].replace('\n', '<br/>')
                        log_html += f"<div class='terminal-line'><strong>[{log['agent_name']}]</strong> <small style='color:#8892B0;'>{log['timestamp'][11:19]}</small><br/>{clean_text}</div>"
                    log_html += "</div>"
                    st.markdown(log_html, unsafe_allow_html=True)
                    
            # Memory search explorer
            st.markdown("---")
            st.markdown("#### 🧠 Local Memory Search Engine")
            st.write("Search the agent's database memory offline using keyword and text similarity:")
            
            search_col_1, search_col_2 = st.columns([3, 1])
            with search_col_1:
                search_q = st.text_input("Search query", placeholder="e.g. database schema or weather endpoint", label_visibility="collapsed")
            with search_col_2:
                search_btn = st.button("🔍 Search Memory", use_container_width=True)
                
            if search_btn and search_q:
                try:
                    search_res = requests.get(f"{BACKEND_URL}/api/projects/{active_project_id}/memories", params={"query": search_q}).json()
                    matches = search_res.get("matches", [])
                    if not matches:
                        st.warning("No memory segments matched your search query.")
                    else:
                        for match in matches:
                            st.markdown(
                                f"""
                                <div class="glass-card" style="padding: 1rem; border-left: 4px solid #00C4FF;">
                                    <strong>Category: {match['category'].upper()}</strong> (Score: {match['score']:.2f})<br/>
                                    <p style='margin-top:0.4rem;'>{match['text']}</p>
                                </div>
                                """,
                                unsafe_allow_html=True
                            )
                except Exception as e:
                    st.error(f"Search failed: {e}")
                    
            # Auto-reload if project is running
            if status == "running":
                time.sleep(2)
                st.rerun()
                
        except Exception as e:
            st.error(f"Error loading project details: {e}")

# --- TAB 3: DELIVERABLES EXPLORER ---
with tab3:
    if not active_project_id:
        st.info("No active workspace selected.")
    else:
        st.markdown("### Generated Code & Documentation Files")
        
        try:
            artifacts = requests.get(f"{BACKEND_URL}/api/projects/{active_project_id}/artifacts").json()
            
            if not artifacts:
                st.warning("No deliverables have been generated yet. Please run the workflow first.")
            else:
                col_tree, col_viewer = st.columns([1, 2])
                
                with col_tree:
                    st.markdown("#### 📂 Workspace Tree")
                    # Display clickable list of generated files
                    selected_file = None
                    file_options = {}
                    
                    for art in artifacts:
                        icon = "📄"
                        if art["type"] == "code":
                            icon = "🐍"
                        elif art["type"] == "docs":
                            icon = "📝"
                        elif art["type"] == "tests":
                            icon = "🧪"
                            
                        label = f"{icon} {art['filepath']}"
                        file_options[label] = art
                        
                    selected_label = st.radio(
                        "Select File to Inspect",
                        options=list(file_options.keys()),
                        label_visibility="collapsed"
                    )
                    
                    if selected_label:
                        selected_file = file_options[selected_label]
                        
                with col_viewer:
                    if selected_file:
                        st.markdown(f"#### 🔍 Viewing `{selected_file['filepath']}`")
                        
                        # Set syntax highlighting language
                        lang = "python"
                        ext = os.path.splitext(selected_file["filename"])[1]
                        if ext == ".md":
                            lang = "markdown"
                        elif ext == ".json":
                            lang = "json"
                        elif ext == ".html":
                            lang = "html"
                            
                        st.code(selected_file["content"], language=lang, line_numbers=True)
                        
                        # Add a download button for raw file
                        st.download_button(
                            label="📥 Download File",
                            data=selected_file["content"],
                            file_name=selected_file["filename"],
                            mime="text/plain",
                            use_container_width=True
                        )
                        
        except Exception as e:
            st.error(f"Error fetching workspace artifacts: {e}")
