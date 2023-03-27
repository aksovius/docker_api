from influxdb_client import  Point, InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS
import docker
import time
import datetime

SLEEP = 5
BUCKET = "docker"
ORGANIZATION = "my-org"
TOKEN = "BwsRD6-_mbeV8IQUJjcAKJuj2pZir0pp9Cy1bezT3z0MJ5fkqD5wmhY_l5cnCbYLlgxsy0L8GkuJ0PM_n-sk6Q=="
URL = "http://localhost:8076"



client = InfluxDBClient(url=URL, token=TOKEN, org=ORGANIZATION)
buckets_api = client.buckets_api()
#buckets_api.delete_bucket(buckets_api.find_bucket_by_name(BUCKET))
if (buckets_api.find_bucket_by_name(BUCKET) == None):
    buckets_api.create_bucket(bucket_name=BUCKET, org=ORGANIZATION)

docker_client = docker.from_env()
write_api = client.write_api(write_options=SYNCHRONOUS)
query_api = client.query_api()
def update_docker():
    try:
        points = []
        index = 'a'
        for container in docker_client.containers.list(all=True):
                if (container.status == "running"):
                    point = Point("docker_stat").tag("index", index).tag("id", container.short_id).field("status", True)
                else:
                    point = Point("docker_stat").tag("index", index).tag("id", container.short_id).field("status", False)
                points.append(point)
                index = chr(ord(index) + 1)
        write_api.write(bucket=BUCKET, record=points)
        print("Write docker state at {0}".format(datetime.datetime.fromtimestamp(time.time()).strftime('%c')))
        time.sleep(SLEEP)
    except KeyboardInterrupt:
        pass