import strawberry
import docker
client = docker.from_env()

@strawberry.mutation
def resolve_stop_container(self, id: str)-> bool:
    container = client.containers.get(id)
    container.stop()
    print(f"Container {container.short_id} stopped")
    return True

@strawberry.mutation
def resolve_start_container(self, id: str)-> bool:
    container = client.containers.get(id)
    container.start()
    print(f"Container {container.short_id} started")
    return True

@strawberry.mutation
def resolve_reload_container(self, id: str)-> bool:
    container = client.containers.get(id)
    container.reload()
    print(f"Container {container.short_id} reloaded")
    return True