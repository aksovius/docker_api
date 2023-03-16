import strawberry
from models import User, Container
from typing import List
import docker
client = docker.from_env()

def get_containers():
    containers = []
    for container in client.containers.list(all=True):
        if container.image.tags[0] in ["tf2:0.05", "tf1:0.01"]:
            containers.append(Container(id=container.short_id, name=container.name, status=container.status, image=container.image.tags[0]))
    return containers  

@strawberry.field
def resolve_user(self) -> User:
    return User(name="Patrick", age=100)
@strawberry.field
def resolve_container_list(self) -> List[Container]:
    return get_containers()