# `python-mcp/tools/db_tools.py` - Understanding SQLite logic in Python

This file implements the Python side of our database bridge. In our polyglot application, while Node.js manages inserting data, Python handles reading that data for the AI agent.

## Key Code Breakdowns:

### `fetch_logs(level, service, limit)`
- **`sqlite3.connect(DB_PATH)`**: Python's native wrapper to interact with SQLite. Opening a connection lets us run queries.
- **`conn.row_factory = sqlite3.Row`**: By default, Python's SQLite returns database results as completely naked lists (e.g., `["ERROR", "Timeout"]`). By adding a `Row` factory, the results behave like Python dictionaries, letting us access columns by name (e.g., `row["level"]`), making life significantly easier.
- **Query Building**:
  - `query = "SELECT * FROM logs WHERE 1=1"`: Just like in Node.js, this lets us safely glue together dynamic `AND` statements later.
  - `params.append(level.upper())`: Normalizing standard terms ensures that "error" matches "ERROR" properly.
- **Safe Execution**:
  - `cursor.execute(query, params)`: This ensures parameters are sanitized against SQL injection before running.
- **Returning JSON**: We serialize the list of row dictionaries globally into a pure JSON string. This way, strings traveling out over MCP are fully readable by external clients or the AI.
