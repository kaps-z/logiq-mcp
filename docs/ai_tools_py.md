# `python-mcp/tools/ai_tools.py` - Deep Dive into the Autonomous Functions

This file houses the specialized AI functionalities powering our debugging tools. It essentially calls out to OpenAI from *inside* the backend to perform logical transformations on logs and code.

## Key Concepts Utilized:
- **`AsyncOpenAI`**: The asynchronous openAI API client ensuring our python backend doesn't freeze or block MCP transactions while we wait several seconds for ChatGPT to generate heavy source code edits.
- **Structured Outputs** (`response_format={"type": "json_object"}`): This guarantees that the LLM sends back perfectly parseable JSON structure rather than erratic markdown conversation blocks, which allows the code to easily parse items programmatically via `json.loads()`.

## Core Functions:

### `analyze_logs(logs)` and `fix_issue(issue_type)`
- Operates primarily by taking inputs (like raw server data) and feeding them directly into prompt templates.
- Explicitly demands answers in JSON format indicating confident scores and actionable steps.

### `fix_code_based_on_logs(logs, file_path)`
This function is highly dangerous and powerful—it autonomously overwrites physical source code.
1. **File Reading**: Uses pure Python `open(file_path)` to extract the literal string text of the targeted module.
2. **Backups with `shutil`**: Protects the user by copying `file.js` to a backup file dynamically tagged with timestamps. Handled entirely via standard python module `shutil.copy2` (which preserves core file metadata).
3. **Synthesis**: Sends both the raw file contents and the error logs back to the `gpt` agent telling it to rewrite the code.
4. **Writing the Update**: Opens the file sequentially backward in write mode (`"w"`) wiping it clean and applying the AI's patched solution.
5. **Auditing**: Opens `audit.log` natively in append mode (`"a"`) so it doesn't overwrite prior edits, leaving permanent trail metrics regarding the operation's outcome so developers can see what was handled quietly in the background!
