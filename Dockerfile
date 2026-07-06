FROM python:3.12-slim

WORKDIR /app

# Install system dependencies if any
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY devcrew_ai/ devcrew_ai/
COPY streamlit_app/ streamlit_app/

# Environment defaults
ENV LLM_PROVIDER=mock
ENV BACKEND_HOST=0.0.0.0
ENV BACKEND_PORT=8000
ENV WORKSPACE_DIR=/app/generated_projects
ENV DB_PATH=/app/devcrew_ai.db

EXPOSE 8000
EXPOSE 8501

# Copy startup scripts if needed or default to running app
CMD ["uvicorn", "devcrew_ai.main:app", "--host", "0.0.0.0", "--port", "8000"]
