# `python-mcp/mcp_server.py` - Understanding the Model Context Protocol Server

This file sets up a **Model Context Protocol (MCP)** backend. MCP is a standard format letting AI Agents connect to external environments (like your database or local files) easily.

## Key Technologies Used:
- **`mcp.server.Server`**: The core application engine.
- **`stdio_server`**: Instead of hosting a standard REST API over typical web ports (like `8080`), we host our MCP server over the application's "Standard Input/Output" (`stdio`). The client literally hooks into this python script by launching it as a subprocess and sending strictly formatted JSON messages through standard shell pipelines.

## Code Walkthrough:

### 1. `app = Server("logiq-mcp-server")`
Simply names and initializes our MCP server instance.

### 2. `@app.list_tools()`
When the AI client first connects, it asks the server: "What can you do?"
This function replies with a structured list of `types.Tool` objects. Each tool declares its `name`, `description`, and a specific JSON schema of properties it expects.
* **Why this format?**: This exact format is inherently compatible with OpenAI's feature called "Function Calling", making it ridiculously easy to connect the AI's "brain" to these tools.

### 3. `@app.call_tool(name, arguments)`
When the AI actually decides to use a tool, it fires an event here.
We evaluate the `name` (e.g. `if name == "fetch_logs":`) and then execute the actual backend Python logic by taking the raw parameters out of `arguments` and mapping them to our python functions. Finally, it returns a `types.TextContent` object containing the tool execution results.

### 4. `asyncio.run(main())`
Since MCP handles a lot of concurrent I/O mapping across processes, it relies on Python's `asyncio` loop rather than running sequentially.
