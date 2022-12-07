from kubernetes import client, config
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import json
import time

# config.load_kube_config()
config.load_incluster_config()


def insert_into_db():
    v1=client.CoreV1Api()

    api = client.CustomObjectsApi()
    resource = api.list_namespaced_custom_object(group="metrics.k8s.io",version="v1beta1", namespace="default", plural="pods", label_selector="app=cassandra")
    max_cpu_per_pod = 500
    max_mem_per_pod = 1024
    no_pods = 0
    sum_of_cpu = 0
    sum_of_mem = 0
    for pod in resource["items"]:
        no_pods = no_pods + 1
        ncpu = int(pod['containers'][0]['usage']['cpu'][:-1])
        mcpu = ncpu/1000000
        sum_of_cpu = sum_of_cpu + mcpu
        kmem = int(pod['containers'][0]['usage']['memory'][:-2])
        mmem = kmem/1024
        sum_of_mem = sum_of_mem + mmem
       
    total_cpu = no_pods * 500
    total_mem = no_pods * 1024
    avg_cpu = (sum_of_cpu/total_cpu) * 100
    avg_mem = (sum_of_mem/total_mem) * 100
    print ("avg cpu utilization", avg_cpu)
    print ("avg mem utilization", avg_mem)

    bucket = "cassandra"

    influx_client = InfluxDBClient(url="http://influxdb:8086", token="0ksKGCfE6ypKYbW0WnOV", org="primary")

    write_api = influx_client.write_api(write_options=SYNCHRONOUS)

    p = Point("resources").field(avg_cpu, avg_mem).tag("nodes", no_pods)

    write_api.write(bucket=bucket, record=p)


if __name__ == "__main__":
    while (1):
        insert_into_db()
        time.sleep(2)
