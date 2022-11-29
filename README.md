# Kind command to initialize a kubernetes cluster
```
kind create cluster --name mycluster
```

# NFS server setup
1. Spawn a node on virtual box and install nfs server on it. Follow this [link](https://www.tecmint.com/install-nfs-server-on-ubuntu/) to set up.
2. Once that is ready you need to setup the nfs provisioner with the help of [this](https://github.com/kubernetes-sigs/nfs-subdir-external-provisioner/blob/master/charts/nfs-subdir-external-provisioner/README.md) link. In this case the nfs server is hosted at `10.0.0.20`. So the command would be
```
$ helm repo add nfs-subdir-external-provisioner https://kubernetes-sigs.github.io/nfs-subdir-external-provisioner/
$ helm install nfs-subdir-external-provisioner nfs-subdir-external-provisioner/nfs-subdir-external-provisioner \
    --set nfs.server=10.0.0.20 \
    --set nfs.path=/mnt/nfs_share
```

# Metrics server
We are using kubernetes default metrics server
To install the metrics server we can download the file below.
```
wget https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml
```
Add the `--kubelet-insecure-tls` parameter to the command line of the deployment

# How to get inside cqlsh
1. Create a pod from the openjdk image.
2. Install python on it.
3. Set the environment variable `CQLSH_HOST` to any one node in the cluster and `CQLSH_PORT` to 9042 which is the default port.

# Cassandra stress working command
```
./cassandra-stress write no-warmup n=1 cl=QUORUM -schema keyspace="myspace" -node 10.244.0.20
```
