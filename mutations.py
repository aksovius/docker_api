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

@strawberry.mutation
def resolve_stop_all_container(self)-> bool:
    for container in client.containers.list():
        if container.image.tags == ['tf2:0.05']:
            container.stop()
            print("Stoped container: ", container.short_id)
    return True

@strawberry.mutation
def resolve_start_containers(self, number: int)-> bool:
    def get_current():
        current = 0
        for container in client.containers.list(all=True):
            if container.image.tags == ['tf2:0.05'] and container.status == 'running':
                current += 1
        return current
    current = get_current()
    print(f"Current containers: {current}")
    for container in client.containers.list(all=True):
        if container.image.tags == ['tf2:0.05'] and container.status == 'exited':
            print(current)
            if current < number:
                container.start()
                current += 1
                print("Started container: ", container.short_id)
            else : break
    return True