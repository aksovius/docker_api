from strawberry.file_uploads import Upload
import strawberry
import docker
from influxdb_client import  Point, InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS
from typing import List
from models import ContainerInput
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId

client = docker.from_env()

# write container status on remove. w/ot status not updated on remove
DOCKER_BUCKET = "docker"
GPU_BUCKET = "gpu"
ORGANIZATION = "my-org"
TOKEN = "BwsRD6-_mbeV8IQUJjcAKJuj2pZir0pp9Cy1bezT3z0MJ5fkqD5wmhY_l5cnCbYLlgxsy0L8GkuJ0PM_n-sk6Q=="
URL = "http://localhost:8076"
MONITORING_URL = "localhost:27017"

mongo_client = AsyncIOMotorClient(MONITORING_URL)
db_mongo = mongo_client.health

db_client = InfluxDBClient(url=URL, token=TOKEN, org=ORGANIZATION)
buckets_api = db_client.buckets_api()
write_api = db_client.write_api(write_options=SYNCHRONOUS)

async def get_user_password(userId): 
    user = await db_mongo.users.find_one({"_id": ObjectId(userId)})
    return user.get('password')

async def run_container(name, port, gpu, device, userDir, userId):
    password = await get_user_password(userId)
    print("password: " + password)
    container = client.containers.run(
                'tf2:1.0', 
                detach=True, 
                ports={'8080/tcp': port}, 
                volumes={'/home/gil/Desktop/colab/': {'bind': '/home/user/workdir/data', 'mode': 'ro'}, 
                        '/home/gil/Desktop/alexander/code-server/user_dir': {'bind': '/home/user/workdir/example', 'mode': 'ro'},
                        '/etc/timezone': {'bind': '/etc/timezone', 'mode': 'ro'}, 
                        '/etc/localtime': {'bind': '/etc/localtime', 'mode': 'ro'},
                        '/home/gil/Desktop/alexander/code-server/tf_docker/config.yaml': {'bind': '/home/user/.config/code-server/config.yaml', 'mode': 'ro'},
                        '/home/gil/Desktop/users_data/'+ userDir : {'bind': '/home/user/workdir/my_data', 'mode': 'rw'}
                        }, 
                shm_size='1g', 
                environment=['TZ=Asia/Seoul', 'HASHED_PASSWORD='+ password], 
                remove=False, 
                name=name,
                device_requests=[{'DeviceIDs': [f'{gpu}:{device}'],
                                'Capabilities': [['gpu']],
                                }], 
                command='code-server',
                entrypoint='bash')
    point = Point("docker_stat").tag("name", name).field("status", True)
    write_api.write(bucket=DOCKER_BUCKET, record=point)
    print("Run: " + container.short_id  + " gpu: " + str(gpu) + " device: " + str(device))
    return True

@strawberry.mutation
async def resolve_stop_container(self, name: str)-> bool:
    print(name)
    container = client.containers.get(name)
    if(container):
        try:
            container.remove(force=True)
            point = Point("docker_stat").tag("name", name).field("status", False)
            write_api.write(bucket=DOCKER_BUCKET, record=point)
            print(f"Container {container.short_id} removed")
        except Exception as e:
            print(e)
    return True

@strawberry.mutation
async def resolve_start_container(self, name:str, port:int, gpu:int, device:int, userDir:str, userId: str)-> bool:
    try: await run_container(name, port, gpu, device, userDir, userId)
    except Exception as e:
        print(e)
    return True
    

@strawberry.mutation
async def resolve_reload_container(self, id:str)-> bool:
    await get_user_password("642fb32c45b7ee16b417d410")
    # container = client.containers.get(id)
    # container.reload()
    # print(f"Container {container.short_id} reloaded")
    return True

@strawberry.mutation
async def resolve_stop_all_container(self)-> bool:
    for container in client.containers.list():
        if container.name.startswith("sandbox"):
            container.remove(force=True)
            point = Point("docker_stat").tag("name", container.name).field("status", False)
            write_api.write(bucket=DOCKER_BUCKET, record=point)
            print(container.name, "removed")
    return True

@strawberry.mutation
async def resolve_start_containers(self, containers:List[ContainerInput])-> bool:
    for container in containers:
        print("name: ", container.name, container.port, container.gpu, container.device, container.userDir)
        try:
            run_container(name=container.name, port=container.port, gpu=container.gpu, device=container.device, userDir=container.userDir)
        except Exception as e:
            print(e)
    return True
