import strawberry
from models import  Container
from typing import List
import docker
from nvitop import MigDevice
client = docker.from_env()
mig = MigDevice.all()

def get_gpu_status():
     gpu_status = []
     for  gpu in mig:
          total = gpu.memory_total_human()
          free = gpu.memory_free_human()
          used = gpu.memory_used_human()
          gpu, device = gpu.index
          gpu_status.append(dict( gpu=gpu, device=device, total=total, free=free, used=used))
     return gpu_status
## python filter type to dict

def get_containers(ws = False):
    containers = []
    gpu_status = get_gpu_status()
    for index, container in enumerate(client.containers.list(all=True)):
          if container.image.tags[0] in ["tf2:0.05", "tf1:0.01"]:
                cnt = dict(index=index, id=container.short_id, name=container.name, status=container.status)
                if ws:
                    containers.append(dict(**cnt, **gpu_status[27-index]))
                else:
                    containers.append(Container(**cnt, **gpu_status[27-index]))
    return containers  

@strawberry.field
def resolve_container_list(self) -> List[Container]:
    return get_containers()
