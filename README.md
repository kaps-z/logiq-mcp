# MCP Log Intelligence System

A production-grade polyglot application that demonstrates the Model Context Protocol (MCP) using a Node.js log service, a Python MCP server with AI tools, an AI-driven CLI, and an **Interactive React UI** for log generation and autonomous AI debugging.

## Architecture

- **React Frontend (`logiq-ui`)**: A premium, dynamic Vite application where users can inject test logs, view real-time log tables, and interactively request and approve AI-generated code fixes.
- **Node.js**: A log generation service (Express + better-sqlite3) exposing REST APIs (`POST /logs`, `GET /logs`).
- **Python MCP Server**: Exposes MCP tools (`fetch_logs`, `analyze_logs`, `fix_issue`, `restart_service`, `read_file`, `fix_code_based_on_logs`) via JSON-RPC.
- **Python AI API (`api.py`)**: A FastAPI application bridging the React frontend to the AI agent, allowing interactive code generation and patching.
- **AI Agent (CLI)**: A Python CLI application to interact with logs and run autonomous AI agent loops natively.
- **SQLite**: The central shared database.

## Setup Instructions

### Prerequisites
- Node.js > 18
- Python > 3.10
- Docker (for testing the restart_service tool)
- Groq API Key configured in your `.env`

### 1. Database & Node Service Setup (Port 3000)
```bash
cd node-service
npm install
npm run dev
```

### 2. Global Environment Config
In the main project root folder, copy the example template:
```bash
cp .env.example .env
```
Now edit that `.env` file to insert your specific `GROQ_API_KEY`.

### 3. Python Tools & AI API (Port 8000)
In a new terminal:
```bash
cd python-mcp
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn api:app --host 0.0.0.0 --port 8000
```

### 4. React Frontend UI (Port 5173)
In a new terminal:
```bash
cd logiq-ui
npm install
npm run dev
```

### 5. Docker Test setup (Optional)
```bash
cd docker
docker-compose up -d
```

## Example Usage

### Using the React UI
Navigate to `http://localhost:5173`. You can immediately:
1. Simulate errors by injecting customized logs via the left-hand panel.
2. Click **AI Debug** on any `ERROR` row.
3. Review the AI's step-by-step reasoning and side-by-side code diff.
4. Click **Approve & Apply File Patch** to securely backup the original code and overwrite it with the fix!

### Using the CLI
```bash
cd cli
source venv/bin/activate

# Run interactive AI Agent analysis
python3 main.py analyze-errors --service auth-service

# Autonomously fix known source code
python3 main.py auto-fix auth-service ./auth-service/db.js
```
