from influxdb_client import  Point, InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS
from nvitop import MigDevice
import time
import datetime

SLEEP = 5
BUCKET = "gpu"
ORGANIZATION = "my-org"
TOKEN = "BwsRD6-_mbeV8IQUJjcAKJuj2pZir0pp9Cy1bezT3z0MJ5fkqD5wmhY_l5cnCbYLlgxsy0L8GkuJ0PM_n-sk6Q=="
URL = "http://localhost:8076"

client = InfluxDBClient(url=URL, token=TOKEN, org=ORGANIZATION)
write_api = client.write_api(write_options=SYNCHRONOUS)
query_api = client.query_api()
try:
    while True:
        points = []
        mig = MigDevice.all()
        for gpu in mig:
            point = Point("gpu_loading").tag("index", gpu.index).field("GPU", gpu.memory_used())
            points.append(point)
        write_api.write(bucket=BUCKET, record=points)
        print("Write GPU at {0}".format(datetime.datetime.fromtimestamp(time.time()).strftime('%c')))
        time.sleep(SLEEP)
except KeyboardInterrupt:
    pass