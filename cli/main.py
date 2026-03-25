import typer
import requests
import json
import asyncio
from rich.console import Console
from rich.table import Table
import os

from agent import DebugAgent

app = typer.Typer(help="CLI for MCP Log Intelligence System")
console = Console()

API_URL = "http://localhost:3000/api"

@app.command()
def create_log(level: str, message: str, service: str, metadata: str = None, correlation_id: str = None):
    """Create a new log entry via Node.js API."""
    data = {
        "level": level,
        "message": message,
        "service": service,
    }
    if metadata:
        try:
            data["metadata"] = json.loads(metadata)
        except json.JSONDecodeError:
            console.print("[red]Error: metadata must be valid JSON string[/red]")
            raise typer.Exit(1)
            
    if correlation_id:
        data["correlation_id"] = correlation_id
        
    try:
        response = requests.post(f"{API_URL}/logs", json=data)
        response.raise_for_status()
        console.print(f"[green]Log created successfully![/green] ID: {response.json().get('id')}")
    except requests.exceptions.RequestException as e:
        console.print(f"[red]Failed to create log:[/red] {e}")

@app.command()
def get_logs(level: str = None, service: str = None, limit: int = 50):
    """Fetch logs from Node.js API."""
    params = {"limit": limit}
    if level: params["level"] = level
    if service: params["service"] = service
    
    try:
        response = requests.get(f"{API_URL}/logs", params=params)
        response.raise_for_status()
        
        logs = response.json().get("data", [])
        if not logs:
            console.print("No logs found.")
            return
            
        table = Table("ID", "Level", "Service", "Message", "Timestamp")
        for log in logs:
            table.add_row(str(log["id"]), log["level"], log["service"], log["message"], str(log["timestamp"]))
            
        console.print(table)
    except requests.exceptions.RequestException as e:
        console.print(f"[red]Failed to fetch logs:[/red] {e}")

@app.command()
def analyze_errors(service: str = None):
    """Run the AI agent to fetch logs and analyze them for issues."""
    objective = "Fetch the latest logs"
    if service:
        objective += f" for the service '{service}'"
    objective += " then analyze them to detect issues. Tell me if any issues exist."
    
    asyncio.run(run_agent(objective))

@app.command()
def fix_issue(service: str = None):
    """Run the AI agent to completely debug and fix any detected issues."""
    objective = "Analyze the latest errors"
    if service:
        objective += f" for '{service}'"
    objective += ", figure out the issue, get fix steps, and if it requires a restart, restart the service using the restart_service tool."
    
    asyncio.run(run_agent(objective))

@app.command()
def auto_fix(service: str, file_path: str):
    """Run the AI agent to automatically fix source code based on logs."""
    absolute_path = os.path.abspath(file_path)
    objective = f"Fetch the latest ERROR/WARN logs for '{service}'. Then use those logs and the file at '{absolute_path}' to automatically fix the source code by calling the fix_code_based_on_logs tool. Provide the final summary of changes."
    
    asyncio.run(run_agent(objective))

async def run_agent(objective: str):
    server_script = os.path.abspath(os.path.join(os.path.dirname(__file__), '../python-mcp/mcp_server.py'))
    try:
        async with DebugAgent(server_script) as agent:
            await agent.run(objective)
    except Exception as e:
        console.print(f"[red]Agent execution failed:[/red] {e}")

if __name__ == "__main__":
    app()
