\# Campus Notice Board - CTE412 Practical (student 02230151)



Rolling, Recreate and Blue/Green releases of a small Python API on a local kind cluster,

with an availability monitor that measures failed requests during every release.



\## Software versions



\- OS: Microsoft Windows 11 Home Single Language

\- Docker: Docker version 29.8.0, build 88096ef

\- kind: kind v0.33.0 go1.26.7 windows/amd64

\- kubectl: Client Version: v1.36.1 | Kustomize Version: v5.8.1

\- Cluster Kubernetes: v1.37.0

\- App: Python 3.12 on python:3.12-alpine; monitor: busybox:1.36



\## Rebuild the final state from an empty machine (PowerShell, run from the repo root)



1\. Create the cluster (1 control-plane + 2 workers, host 127.0.0.1:30090 -> NodePort 30090):



```

kind create cluster --name cte412-02230151 --config cluster/kind-cluster.yaml

```



2\. Build the three images (no registry is used):



```

docker build --build-arg APP\_VERSION=1.0.0 --build-arg STUDENT\_ID=02230151 -t notice-board:02230151-1.0.0 ./app

docker build --build-arg APP\_VERSION=1.1.0 --build-arg STUDENT\_ID=02230151 -t notice-board:02230151-1.1.0 ./app

docker build --build-arg APP\_VERSION=1.2.0-broken --build-arg BROKEN=true --build-arg STUDENT\_ID=02230151 -t notice-board:02230151-1.2.0-broken ./app

```



3\. Load the images into the cluster nodes:



```

kind load docker-image notice-board:02230151-1.0.0 notice-board:02230151-1.1.0 notice-board:02230151-1.2.0-broken --name cte412-02230151

docker pull busybox:1.36

docker save --platform linux/amd64 busybox:1.36 -o busybox.tar

kind load image-archive busybox.tar --name cte412-02230151

```



4\. Namespace first, then quota, limit range and the availability monitor:



```

kubectl apply -f manifests/base/namespace.yaml

kubectl apply -f manifests/base/

kubectl config set-context --current --namespace=nb-02230151

```



5\. Objects of the final state (blue/green Deployments, Services, flag ConfigMap; production on green):



```

kubectl apply -f manifests/bluegreen/

kubectl rollout status deployment/notice-board-blue

kubectl rollout status deployment/notice-board-green

```



6\. Check: `curl.exe http://127.0.0.1:30090/version`, then `bash scripts/summarise.sh <monitor-log>`.



\## Clean-up



```

kubectl config set-context --current --namespace=default

kind delete cluster --name cte412-02230151

```



\## Layout



cluster/  app/  manifests/{base,rolling,bluegreen}/  scripts/summarise.sh  evidence/  report/p06-report.md

