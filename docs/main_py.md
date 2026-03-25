# `cli/main.py` - Modern Python Command Line Interfaces

This script serves up the human interaction terminal application allowing us to leverage everything we built simply.

## Key Technologies Used:
1. **`typer`**: A super fast and intuitive framework wrapping CLI architectures around standard Python types natively.
2. **`requests`**: Easily submits synchronous HTTP POST and GET commands directly querying our Node application endpoints.
3. **`rich`**: Helps visually paint beautiful tables and colored logs directly to console outputs instead of dull white texts.

## Core Implementations:

### REST Wrappers (`create_log`, `get_logs`)
- Uses Python's native `requests.post()` and `requests.get()` formatting parameters effectively into dictionary JSON mappings routing straight into the Node REST backend. 

### AI Automation Wrappers (`analyze_errors`, `fix_issue`, `auto_fix`)
- Provides CLI sugar-coating by generating explicit contextual "Objectives" formatted in plain english (e.g., `"Fetch the latest logs... then automatically fix the source code"`).
- Since MCP and `openai` function asynchronously, it invokes the entire objective via `asyncio.run(run_agent(objective))`. This hands off execution context gracefully to the underlying `DebugAgent`.
