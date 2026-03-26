import asyncio
import os
import json
from dotenv import load_dotenv
from typing import Optional
from openai import AsyncOpenAI
from mcp.client.stdio import stdio_client, StdioServerParameters
from mcp.client.session import ClientSession
from contextlib import AsyncExitStack
import mcp.types as types

env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env')
load_dotenv(env_path)

openai_client = AsyncOpenAI(
    api_key=os.environ.get("GROQ_API_KEY", "dummy-key"),
    base_url="https://api.groq.com/openai/v1"
)

class DebugAgent:
    def __init__(self, server_script: str):
        python_exe = os.path.abspath(os.path.join(os.path.dirname(__file__), '../python-mcp/venv/bin/python3'))
        self.server_parameters = StdioServerParameters(
            command=python_exe,
            args=[server_script],
            env={**os.environ}
        )
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()

    async def __aenter__(self):
        streams = await self.exit_stack.enter_async_context(stdio_client(self.server_parameters))
        self.read, self.write = streams
        self.session = await self.exit_stack.enter_async_context(ClientSession(self.read, self.write))
        await self.session.initialize()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.exit_stack.aclose()

    async def run(self, objective: str):
        print(f"Agent Objective: {objective}")
        
        # Get available tools from MCP server
        tools_response = await self.session.list_tools()
        
        # Convert MCP tools to OpenAI tool format
        openai_tools = []
        for tool in tools_response.tools:
            openai_tools.append({
                "type": "function",
                "function": {
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": tool.inputSchema
                }
            })

        messages = [
            {
                "role": "system", 
                "content": (
                    "You are an autonomous AI debugging agent. You use tools to fetch logs, analyze them, find fixes, and restart services if necessary. "
                    "CRITICAL: You MUST call one tool at a time, wait to receive the actual text result of that tool, and THEN call the next tool. "
                    "NEVER pass un-evaluated variables or placeholders like '<fetch_logs_result>' as arguments into a tool."
                )
            },
            {"role": "user", "content": objective}
        ]

        while True:
            response = await openai_client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=messages,
                tools=openai_tools
            )
            
            message = response.choices[0].message
            # Append message to conversation
            messages.append(message)
            
            if message.tool_calls:
                for tool_call in message.tool_calls:
                    print(f"--> Calling tool: {tool_call.function.name} with args {tool_call.function.arguments}")
                    args = json.loads(tool_call.function.arguments)
                    
                    try:
                        result = await self.session.call_tool(
                            tool_call.function.name,
                            arguments=args
                        )
                        result_text = "\n".join([c.text for c in result.content if c.type == "text"])
                    except Exception as e:
                        result_text = f"Error calling tool: {e}"
                        
                    print(f"<-- Tool Result: {result_text}")
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": result_text
                    })
            else:
                print("Final Response:", message.content)
                break
