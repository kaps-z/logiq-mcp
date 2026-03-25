# MCP Log Intelligence System

A production-grade polyglot application that demonstrates the Model Context Protocol (MCP) using a Node.js log service, a Python MCP server with AI tools, and an AI-driven CLI for debugging.

## Architecture

- **Node.js**: A log generation service (Express + better-sqlite3) exposing REST APIs (`POST /logs`, `GET /logs`).
- **Python MCP Server**: Exposes MCP tools (`fetch_logs`, `analyze_logs`, `fix_issue`, `restart_service`) via JSON-RPC over `stdio`.
- **AI Agent (CLI)**: A Python CLI application to interact with logs and run an autonomous AI agent that leverages OpenAI and MCP to reason, debug, and fix issues.
- **Docker**: Used to simulate services that the `restart_service` tool can interact with.
- **SQLite**: The central shared database.

## Setup Instructions

### Prerequisites
- Node.js > 18
- Python > 3.10
- Docker (for testing the restart_service tool)
- OpenAI API Key

### 1. Database & Node Service Setup
```bash
cd node-service
npm install
npm run dev
```

### 2. Python Tools
In a new terminal:
```bash
cd python-mcp
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. CLI Setup
In a new terminal:
```bash
cd cli
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
export OPENAI_API_KEY="your-api-key"
```

### 4. Docker Test setup
```bash
cd docker
docker-compose up -d
```

## Example Usage

With the Node service running, you can use the CLI tool to manage logs and debug using the AI agent.

```bash
# In the cli directory

# 1. Create a log
python main.py create-log ERROR "Failed to connect to test_service database. Connection Refused." "test_service"

# 2. Get logs
python main.py get-logs

# 3. Analyze errors using AI Agent over MCP
python main.py analyze-errors --service test_service

# 4. Fix issues (will suggest fixes and attempt to restart container)
python main.py fix-issue --service test_service
```
