import docker
import json

def restart_service(container_name: str) -> str:
    try:
        client = docker.from_env()
        container = client.containers.get(container_name)
        container.restart()
        return json.dumps({"status": "success", "message": f"Container {container_name} restarted successfully."})
    except docker.errors.NotFound:
        return json.dumps({"error": f"Container {container_name} not found."})
    except Exception as e:
        return json.dumps({"error": str(e)})
