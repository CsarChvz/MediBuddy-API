import docker


def start_database_container():

    # Initialize Docker client
    client = docker.from_env()
    container_name = "test-db"

    # Check if the container already exists
    # If exists, stop and remove the container "test-db"
    try:
        existing_container = client.containers.get(container_name)
        print(f"Container '{container_name}' already exists. Stopping and removing it.")
        existing_container.stop()
        existing_container.remove()
        print(f"Container '{container_name}' stopped and removed")
    except docker.errors.NotFound:
        print(f"Container '{container_name}' deoes not exist.")

    container_config = {
        "name": container_name,
        "image": "postgres:16.1-alpine3.12",
        "detach": True,
        "ports": {"5432": "5434"},
        "environment": {
            "POSTGRES_USER": "postgres",
            "POSTGRES_PASSWORD": "password",
        },
    }

    container = client.containers.run(**container_config)
