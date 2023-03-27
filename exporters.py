from influxdb_client import  Point, InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS
import docker
import time
import datetime
from nvitop import MigDevice


SLEEP = 5
DOCKER_BUCKET = "docker"
GPU_BUCKET = "gpu"
ORGANIZATION = "my-org"
TOKEN = "BwsRD6-_mbeV8IQUJjcAKJuj2pZir0pp9Cy1bezT3z0MJ5fkqD5wmhY_l5cnCbYLlgxsy0L8GkuJ0PM_n-sk6Q=="
URL = "http://localhost:8076"


docker_client = docker.from_env()

client = InfluxDBClient(url=URL, token=TOKEN, org=ORGANIZATION)
buckets_api = client.buckets_api()
write_api = client.write_api(write_options=SYNCHRONOUS)

#buckets_api.delete_bucket(buckets_api.find_bucket_by_name(BUCKET))
# if (buckets_api.find_bucket_by_name(DOCKER_BUCKET) == None):
#     buckets_api.create_bucket(bucket_name=DOCKER_BUCKET, org=ORGANIZATION) 
    
def update_docker():
    points = []
    index = 'a'
    for container in docker_client.containers.list(all=True):
            if (container.status == "running" and container.image.tags[0] in ["tf2:0.05", "tf1:0.01"]):
                point = Point("docker_stat").tag("index", index).tag("id", container.short_id).field("status", True)
            elif (container.image.tags[0] in ["tf2:0.05", "tf1:0.01"]):
                point = Point("docker_stat").tag("index", index).tag("id", container.short_id).field("status", False)
            else: continue
            points.append(point)
            index = chr(ord(index) + 1)
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