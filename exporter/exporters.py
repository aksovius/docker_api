from influxdb_client import  Point, InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS
import docker
import time
import datetime
from nvitop import MigDevice
import os
os.environ.get("HOST", "0.0.0.0")
SLEEP = 5
DOCKER_BUCKET = "docker"
GPU_BUCKET = "gpu"
ORGANIZATION = "my-org"
TOKEN = "BwsRD6-_mbeV8IQUJjcAKJuj2pZir0pp9Cy1bezT3z0MJ5fkqD5wmhY_l5cnCbYLlgxsy0L8GkuJ0PM_n-sk6Q=="
URL = "http://172.17.0.1:8076"


docker_client = docker.from_env()

client = InfluxDBClient(url=URL, token=TOKEN, org=ORGANIZATION)
buckets_api = client.buckets_api()
write_api = client.write_api(write_options=SYNCHRONOUS)

#buckets_api.delete_bucket(buckets_api.find_bucket_by_name(BUCKET))
# if (buckets_api.find_bucket_by_name(DOCKER_BUCKET) == None):
#     buckets_api.create_bucket(bucket_name=DOCKER_BUCKET, org=ORGANIZATION) 
    
def update_docker():
    points = []
    #index = 'a'
    for container in docker_client.containers.list(all=True):
            if (container.status == "running" and container.name.startswith("sandbox")):
                #point = Point("docker_stat").tag("index", index).tag("name", container.name).field("status", True)
                point = Point("docker_stat").tag("name", container.name).field("status", True) 
            elif (container.name.startswith("sandbox")):
                #point = Point("docker_stat").tag("index", index).tag("name", container.name).field("status", False)
                point = Point("docker_stat").tag("name", container.name).field("status", False)
            else: continue
            points.append(point)
            #index = chr(ord(index) + 1)
    write_api.write(bucket=DOCKER_BUCKET, record=points)
    print("Write docker state at {0}".format(datetime.datetime.fromtimestamp(time.time()).strftime('%c')))
   
 
    
def update_gpu():
    points = []
    mig = MigDevice.all()
    for gpu in mig:
        point = Point("gpu_loading").tag("index", gpu.index).field("GPU", gpu.memory_used())
        points.append(point)
    write_api.write(bucket=GPU_BUCKET, record=points)
    print("Write GPU at {0}".format(datetime.datetime.fromtimestamp(time.time()).strftime('%c')))
    
 
    
while True:
    try:
        update_docker()
        update_gpu()
        time.sleep(SLEEP)
    except KeyboardInterrupt:
        print("Stoping")
        break