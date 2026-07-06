import sqlite3
import json
from datetime import datetime
from devcrew_ai.config import DB_PATH

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create projects table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS projects (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT,
        status TEXT NOT NULL DEFAULT 'initialized', -- 'initialized', 'running', 'completed', 'failed'
        created_at TEXT NOT NULL
    )
    """)
    
    # Create tasks table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        project_id INTEGER NOT NULL,
        name TEXT NOT NULL,
        description TEXT,
        assigned_to TEXT NOT NULL, -- agent name
        status TEXT NOT NULL DEFAULT 'pending', -- 'pending', 'in_progress', 'completed', 'failed'
        dependencies TEXT, -- JSON array of task IDs or Names
        output TEXT,
        updated_at TEXT NOT NULL,
        FOREIGN KEY (project_id) REFERENCES projects(id)
    )
    """)
    
    # Create agent_logs table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS agent_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        project_id INTEGER NOT NULL,
        agent_name TEXT NOT NULL,
        log_text TEXT NOT NULL,
        timestamp TEXT NOT NULL,
        FOREIGN KEY (project_id) REFERENCES projects(id)
    )
    """)
    
    # Create project_memory table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS project_memory (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        project_id INTEGER NOT NULL,
        key TEXT NOT NULL,
        value TEXT NOT NULL,
        category TEXT NOT NULL, -- 'decision', 'technology', 'requirement', 'rule'
        created_at TEXT NOT NULL,
        FOREIGN KEY (project_id) REFERENCES projects(id)
    )
    """)
    
    # Create vector_memory table (stored as text for local similarity matching)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS vector_memory (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        project_id INTEGER NOT NULL,
        text TEXT NOT NULL,
        category TEXT NOT NULL,
        created_at TEXT NOT NULL,
        FOREIGN KEY (project_id) REFERENCES projects(id)
    )
    """)
    
    # Create artifacts table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS artifacts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        project_id INTEGER NOT NULL,
        filename TEXT NOT NULL,
        content TEXT NOT NULL,
        filepath TEXT NOT NULL,
        type TEXT NOT NULL, -- 'code', 'plan', 'docs', 'tests'
        created_at TEXT NOT NULL,
        FOREIGN KEY (project_id) REFERENCES projects(id)
    )
    """)
    
    conn.commit()
    conn.close()
    print("[Database] Initialized tables successfully.")

# Project operations
def create_project(name, description):
    conn = get_db_connection()
    cursor = conn.cursor()
    now = datetime.now().isoformat()
    cursor.execute(
        "INSERT INTO projects (name, description, status, created_at) VALUES (?, ?, 'initialized', ?)",
        (name, description, now)
    )
    project_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return project_id

def update_project_status(project_id, status):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE projects SET status = ? WHERE id = ?", (status, project_id))
    conn.commit()
    conn.close()

def get_project(project_id):
    conn = get_db_connection()
    row = conn.execute("SELECT * FROM projects WHERE id = ?", (project_id,)).fetchone()
    conn.close()
    return dict(row) if row else None

def get_all_projects():
    conn = get_db_connection()
    rows = conn.execute("SELECT * FROM projects ORDER BY id DESC").fetchall()
    conn.close()
    return [dict(row) for row in rows]

# Task operations
def create_task(project_id, name, description, assigned_to, dependencies=None):
    conn = get_db_connection()
    cursor = conn.cursor()
    now = datetime.now().isoformat()
    deps_str = json.dumps(dependencies) if dependencies else "[]"
    cursor.execute(
        "INSERT INTO tasks (project_id, name, description, assigned_to, status, dependencies, updated_at) VALUES (?, ?, ?, ?, 'pending', ?, ?)",
        (project_id, name, description, assigned_to, deps_str, now)
    )
    task_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return task_id

def update_task_status(task_id, status, output=None):
    conn = get_db_connection()
    cursor = conn.cursor()
    now = datetime.now().isoformat()
    if output is not None:
        cursor.execute(
            "UPDATE tasks SET status = ?, output = ?, updated_at = ? WHERE id = ?",
            (status, output, now, task_id)
        )
    else:
        cursor.execute(
            "UPDATE tasks SET status = ?, updated_at = ? WHERE id = ?",
            (status, now, task_id)
        )
    conn.commit()
    conn.close()

def get_tasks_for_project(project_id):
    conn = get_db_connection()
    rows = conn.execute("SELECT * FROM tasks WHERE project_id = ? ORDER BY id ASC", (project_id,)).fetchall()
    conn.close()
    return [dict(row) for row in rows]

# Agent log operations
def add_agent_log(project_id, agent_name, log_text):
    conn = get_db_connection()
    cursor = conn.cursor()
    now = datetime.now().isoformat()
    cursor.execute(
        "INSERT INTO agent_logs (project_id, agent_name, log_text, timestamp) VALUES (?, ?, ?, ?)",
        (project_id, agent_name, log_text, now)
    )
    conn.commit()
    conn.close()

def get_logs_for_project(project_id):
    conn = get_db_connection()
    rows = conn.execute("SELECT * FROM agent_logs WHERE project_id = ? ORDER BY id ASC", (project_id,)).fetchall()
    conn.close()
    return [dict(row) for row in rows]

# Project memory operations
def add_project_memory(project_id, key, value, category):
    conn = get_db_connection()
    cursor = conn.cursor()
    now = datetime.now().isoformat()
    cursor.execute(
        "INSERT INTO project_memory (project_id, key, value, category, created_at) VALUES (?, ?, ?, ?, ?)",
        (project_id, key, value, category, now)
    )
    conn.commit()
    conn.close()

def get_project_memories(project_id, category=None):
    conn = get_db_connection()
    if category:
        rows = conn.execute(
            "SELECT * FROM project_memory WHERE project_id = ? AND category = ? ORDER BY id DESC",
            (project_id, category)
        ).fetchall()
    else:
        rows = conn.execute(
            "SELECT * FROM project_memory WHERE project_id = ? ORDER BY id DESC",
            (project_id,)
        ).fetchall()
    conn.close()
    return [dict(row) for row in rows]

# Vector/text memory operations
def add_vector_memory(project_id, text, category):
    conn = get_db_connection()
    cursor = conn.cursor()
    now = datetime.now().isoformat()
    cursor.execute(
        "INSERT INTO vector_memory (project_id, text, category, created_at) VALUES (?, ?, ?, ?)",
        (project_id, text, category, now)
    )
    conn.commit()
    conn.close()

def get_all_vector_memories(project_id):
    conn = get_db_connection()
    rows = conn.execute("SELECT * FROM vector_memory WHERE project_id = ?", (project_id,)).fetchall()
    conn.close()
    return [dict(row) for row in rows]

# Artifact operations
def add_artifact(project_id, filename, content, filepath, type):
    conn = get_db_connection()
    cursor = conn.cursor()
    now = datetime.now().isoformat()
    cursor.execute(
        "INSERT INTO artifacts (project_id, filename, content, filepath, type, created_at) VALUES (?, ?, ?, ?, ?, ?)",
        (project_id, filename, content, filepath, type, now)
    )
    conn.commit()
    conn.close()

def get_artifacts_for_project(project_id):
    conn = get_db_connection()
    rows = conn.execute("SELECT * FROM artifacts WHERE project_id = ? ORDER BY id ASC", (project_id,)).fetchall()
    conn.close()
    return [dict(row) for row in rows]

# Delete a project (useful for resets)
def delete_project_data(project_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM artifacts WHERE project_id = ?", (project_id,))
    cursor.execute("DELETE FROM vector_memory WHERE project_id = ?", (project_id,))
    cursor.execute("DELETE FROM project_memory WHERE project_id = ?", (project_id,))
    cursor.execute("DELETE FROM agent_logs WHERE project_id = ?", (project_id,))
    cursor.execute("DELETE FROM tasks WHERE project_id = ?", (project_id,))
    cursor.execute("DELETE FROM projects WHERE id = ?", (project_id,))
    conn.commit()
    conn.close()
