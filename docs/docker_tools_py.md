# `python-mcp/tools/docker_tools.py` - Interacting with Container APIs

It's common for developers to want dynamic recovery systems. This tool allows the MCP server to directly orchestrate and restart broken containers automatically.

## Key Technologies Used:
1. **`import docker`**: The official Python Docker SDK.

## Core Code Overview:

### `restart_service(container_name)`
- **`docker.from_env()`**: This magically reads the host system's standard Docker environment configurations (acting through the underlying local docker socket) making authentication easy.
- **`client.containers.get(container_name)`**: Fetches the targeted docker object directly from the daemon.
- **`.restart()`**: Issues a standard stop-and-start network signal essentially mimicking the action of literally typing `docker restart <name>` in the terminal.
- **Error catching**: explicitly traps `docker.errors.NotFound` so if an AI agent tries to reboot a container that does not exist, our server doesn't brutally crash and will politely inform the agent it failed via JSON.
