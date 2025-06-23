# MLflow + MinIO + Kubeflow Pipeline Integration (v3.1.0)   

This guide explains how to:

- Install MinIO via Helm with NodePort access
- Configure `mc` CLI to verify MinIO
- Upgrade and run MLflow v3.1.0 with MinIO
- Update your Kubeflow pipeline to register models with MLflow
- Execute the pipeline end-to-end

---

## 1. Install MinIO Using Helm

### Step-by-Step

#### Install Helm (Linux):

```bash
curl https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3 | bash
```

## Add MinIO Helm Repo and Install:

```bash
helm repo add minio https://charts.min.io/
helm repo update

helm upgrade --install minio minio/minio \
  --namespace default \
  --create-namespace \
  --set mode=standalone \
  --set accessKey=myminio \
  --set secretKey=myminio123 \
  --set persistence.enabled=false \
  --set buckets[0].name=mlflow-artifacts \
  --set service.type=NodePort \
  --set consoleService.type=NodePort \
  --set resources.requests.memory=128Mi \
  --set resources.limits.memory=256Mi
```

#### Fetch Access & Secret Keys:

```bash
kubectl get secret minio -o jsonpath="{.data.rootUser}" | base64 --decode
echo
kubectl get secret minio -o jsonpath="{.data.rootPassword}" | base64 --decode
echo
```
#### Setup MinIO Client (`mc`) and Verify:

```bash
wget https://dl.min.io/client/mc/release/linux-amd64/mc
chmod +x mc
sudo mv mc /usr/local/bin/
```

Add your MinIO endpoint:

```bash
mc alias set local http://<minio-node-ip>:<node-port> AWS_ACCESS_KEY_ID AWS_SECRET_ACCESS_KEY
```

Then check if it works:

```bash
mc ls localminio
```

You should see:

```
[2025-06-20 18:00:00 UTC]     0B mlflow-artifacts/
```

---

# 1. MLflow v3.1.0 Setup

You need to **update your Dockerfile and MLflow deployment YAML** to match the **actual MinIO credentials**:

```Dockerfile
FROM python:3.10-slim

WORKDIR /app

RUN pip install --no-cache-dir \
    mlflow[extras]==3.1.0 \
    boto3
```

**MLflow Deployment YAML File:**

```yaml
containers:
  - name: mlflow
    image: edquest/mlflow-ui:v3 # <---Update here your latest image --->
    command: ["mlflow"]
    args:
      - server
      - --host=0.0.0.0
      - --port=5000
      - --backend-store-uri=/mnt/mlflow-artifacts
      - --default-artifact-root=s3://mlflow-artifacts # <-- update here default-artifact-root path-->
    env:
      - name: MLFLOW_S3_ENDPOINT_URL
        value: http://minio:9000
      - name: AWS_ACCESS_KEY_ID 
        value: <AWS_ACCESS_KEY_ID> # Fetch actual MinIO access key that are active inside your deployment.
      - name: AWS_SECRET_ACCESS_KEY 
        value: <AWS_SECRET_ACCESS_KEY> # Fetch actual MinIO secret key that are active inside your deployment.
    volumeMounts:
      - name: mlflow-artifact
        mountPath: /mnt/mlflow-artifacts
```
Then apply the changes:

```bash
kubectl apply -f mlflow-ui-deployment.yaml
```

## Final Checklist

- MLflow upgraded to v3.1.0
- MinIO set up with NodePort
- S3 settings configured in MLflow 
- Run successfully tracked in MLflow

---
