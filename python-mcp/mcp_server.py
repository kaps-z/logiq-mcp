import asyncio
import os
from dotenv import load_dotenv

from mcp.server import Server
from mcp.server.stdio import stdio_server
import mcp.types as types

from tools.db_tools import fetch_logs
from tools.ai_tools import analyze_logs, fix_issue, fix_code_based_on_logs
from tools.docker_tools import restart_service

load_dotenv()

app = Server("logiq-mcp-server")

@app.list_tools()
async def list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="fetch_logs",
            description="Fetch logs from the SQLite DB. Filters: level, service, limit.",
            inputSchema={
                "type": "object",
                "properties": {
                    "level": {"type": "string", "description": "Log level (INFO, WARN, ERROR)"},
                    "service": {"type": "string", "description": "Service name to filter"},
                    "limit": {"type": "integer", "description": "Max number of logs to return"}
                }
            }
        ),
        types.Tool(
            name="analyze_logs",
            description="Analyze a list of logs using LLM to detect issues.",
            inputSchema={
                "type": "object",
                "properties": {
                    "logs": {"type": "string", "description": "JSON string of logs to analyze"}
                },
                "required": ["logs"]
            }
        ),
        types.Tool(
            name="fix_issue",
            description="Provide actionable fix steps for an issue type.",
            inputSchema={
                "type": "object",
                "properties": {
                    "issue_type": {"type": "string", "description": "Type of the issue identified"}
                },
                "required": ["issue_type"]
            }
        ),
        types.Tool(
            name="restart_service",
            description="Restart a Docker container.",
            inputSchema={
                "type": "object",
                "properties": {
                    "container_name": {"type": "string", "description": "Name of the docker container to restart"}
                },
                "required": ["container_name"]
            }
        ),
        types.Tool(
            name="read_file",
            description="Read the contents of a file from the local filesystem.",
            inputSchema={
                "type": "object",
                "properties": {
                    "file_path": {"type": "string", "description": "Absolute path to the file"}
                },
                "required": ["file_path"]
            }
        ),
        types.Tool(
            name="fix_code_based_on_logs",
            description="Automatically analyze logs and source code, generate fixes, backup original file, write fixed code, and create an audit log.",
            inputSchema={
                "type": "object",
                "properties": {
                    "logs": {"type": "string", "description": "Recent log entries to analyze"},
                    "file_path": {"type": "string", "description": "Absolute path to the source code file to fix"}
                },
                "required": ["logs", "file_path"]
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    try:
        if name == "fetch_logs":
            result = fetch_logs(
                level=arguments.get("level"),
                service=arguments.get("service"),
                limit=arguments.get("limit", 50)
            )
            return [types.TextContent(type="text", text=result)]
        
        elif name == "analyze_logs":
            result = await analyze_logs(arguments["logs"])
            return [types.TextContent(type="text", text=result)]
            
        elif name == "fix_issue":
            result = await fix_issue(arguments["issue_type"])
            return [types.TextContent(type="text", text=result)]
            
        elif name == "restart_service":
            result = restart_service(arguments["container_name"])
            return [types.TextContent(type="text", text=result)]
            
        elif name == "read_file":
            try:
                with open(arguments["file_path"], "r", encoding="utf-8") as f:
                    content = f.read()
                return [types.TextContent(type="text", text=content)]
            except Exception as e:
                return [types.TextContent(type="text", text=f"Error reading file: {e}")]
                
        elif name == "fix_code_based_on_logs":
            result = await fix_code_based_on_logs(arguments["logs"], arguments["file_path"])
            return [types.TextContent(type="text", text=result)]
            
        else:
            raise ValueError(f"Unknown tool: {name}")
            
    except Exception as e:
        return [types.TextContent(type="text", text=f"Tool error: {str(e)}")]

async def main():
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())

if __name__ == "__main__":
    asyncio.run(main())
