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
        gpu, device = gpu.index
        index = str(gpu) +":" + str(device)
        gpu_status.append(dict(index=index))
     return gpu_status
## python filter type to dict

def get_containers(ws = False):
    containers = []
    gpu_status = get_gpu_status()
    index = 0
    for container in client.containers.list(all=True):
          if container.image.tags[0] in ["tf2:0.05", "tf1:0.01"]:
                cnt = dict(id=container.short_id, name=container.name, status=container.status)
         
                if ws:
                    containers.append(dict(**cnt, **gpu_status[27-index]))
                else:
                    containers.append(Container(**cnt, **gpu_status[27-index]))
                index += 1
    return containers  

@strawberry.field
def resolve_container_list(self) -> List[Container]:
    return get_containers()
