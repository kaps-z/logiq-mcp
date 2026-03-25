# `cli/agent.py` - Establishing AI Orchestration & Tool Calling

A critical part of an MCP design is the **Agent**. The `DebugAgent` class acts as the user-facing side connecting OpenAI and the server context explicitly.

## Code Walkthrough:

### MCP Bootstrapping (`__aenter__` pattern)
- The agent utilizes `StdioServerParameters` specifying it should literally launch a python terminal mapping over `mcp_server.py`.
- It captures standard stream processes (`self.read, self.write`) generating a unified `ClientSession`.

### The Heartbeat of the AI: `run(objective)`
1. **Tool Ingestion**: Calls `.list_tools()` fetching all available skills the MCP provider offers. Maps these definitions securely to dictionaries explicitly supported by the OpenAI format syntax (`type: "function"`).
2. **Context Memory (`messages`)**: Sets up an array mimicking deep conversations storing initial objectives along side system instructions mapping how it behaves.
3. **The Intelligent While-Loop**:
   - Sends all existing interactions out to OpenAI `chat.completions.create`.
   - **Crucial step**: Checks if the AI triggered `.tool_calls`. When an AI identifies it lacks knowledge or needs logic resolved, it pauses replying to humans and strictly commands an invocation of local functions.
   - For every command requested, the python agent relays the execution safely using `self.session.call_tool(name, arguments)` directly translating them to our back-end MCP script.
   - Finally, appends the tool's result to the conversational memory array. Since the array is still inside the `while True:` loop, it re-queries the AI supplying the results. This allows the AI to *chain reasoning independently*.
