## **Kubeflow v1.6.1 On-Prem Installation (Manual Steps)**

---

### step 1: Overview

* Kubeflow is a machine learning toolkit for Kubernetes.
* This guide shows step-by-step manual installation of **Kubeflow Pipelines v1.6.1** on an on-premises Kubernetes cluster.
* Installation uses official manifests, NodePort for access, and Local Path Provisioner for PVC support.

---

### step 2: Prerequisites

* Kubernetes cluster (v1.21+ recommended)
* `kubectl` installed and configured
* Sufficient node resources (4+ CPU, 8+ GB RAM)
* Internet access
* Port `31380` open (for NodePort access)
* Host path `/opt/local-path-provisioner` must be writable

---

## SECTION 1: PVC Setup with Local Path Provisioner

---

**Why PVC Setup is Required**

* Kubeflow components such as `minio`, `metadata`, and `pipelines` use **PersistentVolumeClaims (PVCs)** to store data.
* If no **default StorageClass** exists, these PVCs will stay in **Pending** state.
* We use **Local Path Provisioner** to dynamically provision local storage on Kubernetes nodes.

### step 3: Create Manifest Directory

```bash
mkdir -p ~/kubeflow/local-path-provisioner
```

* Creates a folder to store the local path provisioner YAML definition file.

---

### step 4: Create the Provisioner YAML File
    Save the following content as a file:

```bash
nano ~/kubeflow/local-path-provisioner/local-path-storage.yaml
```

Paste the complete YAML (from `Namespace` to `helperPod.yaml`) into the file.

---

### step 5: Apply the Provisioner YAML

```bash
kubectl apply -f ~/kubeflow/local-path-provisioner/local-path-storage.yaml
```

* Creates the local-path-storage namespace.

* Deploys the local path provisioner Deployment, RBAC resources, ConfigMap, and StorageClass.

---

### step 6: **Make StorageClass Default**

```bash
kubectl patch storageclass local-path -p \
'{"metadata": {"annotations":{"storageclass.kubernetes.io/is-default-class":"true"}}}'
```

* Marks the `local-path` StorageClass as the **default**.
* Ensures that future PVCs with no specified `storageClassName` will use this provisioner.

---

###  step 7: Verify StorageClass

```bash
kubectl get storageclass
```

* Confirms that the provisioner is correctly deployed and marked as default.

---

### step 8: Ensure Host Directory Exists

```bash
sudo mkdir -p /opt/local-path-provisioner
sudo chmod -R 777 /opt/local-path-provisioner
```

* Ensures successful volume creation by provisioner.

---

## SECTION 2: Kubeflow Pipeline Deployment

---

### step 9: **Download Kubeflow Manifests**

```bash
mkdir -p ~/kubeflow && cd ~/kubeflow
wget https://github.com/kubeflow/manifests/archive/refs/tags/v1.6.1.tar.gz
```

* Creates a working directory for Kubeflow setup.
* Downloads the v1.6.1 manifests archive from the official GitHub repository.

---

### step 10: **Extract the Manifests**

```bash
tar -xzvf v1.6.1.tar.gz
```

* Extracts the downloaded tar.gz file.
* This gives access to the `manifests-1.6.1/` directory, which contains kustomize-based YAML files for all Kubeflow components.

---

### step 11: **Remove GCP Inverse Proxy**

```bash
sed -i '/gcp\/inverse-proxy/d' manifests-1.6.1/apps/pipeline/upstream/env/dev/kustomization.yaml
```

* Removes the GCP-specific inverse proxy reference from `kustomization.yaml`.
* Ensures that only required components for on-prem installation are applied.

---

### step 12: **Create the kubeflow Namespace**

```bash
kubectl create namespace kubeflow
```

* Creates a new Kubernetes namespace called `kubeflow`.
* All Kubeflow components will be deployed inside this namespace.

---

### step 13: **Apply Cluster-Scoped Resources**

```bash
cd ~/kubeflow/manifests-1.6.1
kubectl apply -k apps/pipeline/upstream/cluster-scoped-resources
```

* Applies CRDs (CustomResourceDefinitions), ClusterRoles, and other cluster-wide resources.
* These are required by the Kubeflow Pipelines component.

---

### step 14: **Wait for CRDs to be Established**

```bash
kubectl wait --for condition=established --timeout=60s crd/applications.app.k8s.io
```

* Waits for the `Application` CRD to be fully registered.
* Prevents issues during subsequent steps that depend on this CRD.

---

### step 15: **Apply Kubeflow Pipelines Manifests**

```bash
kubectl apply -k apps/pipeline/upstream/env/dev -n kubeflow
```

* Deploys Kubeflow Pipelines components like `ml-pipeline`, `ml-pipeline-ui`, `metadata-grpc`, `cache-server`, etc.
* Uses the `dev` environment overlay provided in the manifests.
* Applies all resources under the `kubeflow` namespace.

---

### step 16: **Patch Pipeline UI as NodePort**

```bash
kubectl patch svc ml-pipeline-ui -n kubeflow \
  --type='json' \
  -p='[
    {"op":"replace","path":"/spec/type","value":"NodePort"},
    {"op":"replace","path":"/spec/ports/0/nodePort","value":31380}
  ]'
```

* Changes the `ml-pipeline-ui` service type from `ClusterIP` to `NodePort`.
* Sets the node port to `31380` so that the UI can be accessed externally via:

  ```
  http://<node-ip>:31380
  ```

---

### step 17: **Verify Deployment**

```bash
kubectl get pods -n kubeflow
kubectl get svc -n kubeflow
```

* Shows the status of all pods and services in the `kubeflow` namespace.
* Ensures that all pods are running and the `ml-pipeline-ui` service is assigned NodePort `31380`.

---

### step 18: **Access Kubeflow Pipelines UI**

```text
URL: http://<NODE-IP>:31380
```

* Open the above link in a browser.
* You should see the Kubeflow Pipelines UI.
* You can now submit, run, and monitor pipelines.

---

## Key Steps Summary
*  Set up Local Path Provisioner to enable dynamic PVC provisioning using local storage.
* `StorageClass` set as default.
*  PVCs will now auto-bind and get usable PersistentVolumes.
*  Download and extract Kubeflow v1.6.1 manifests from the official GitHub release.
*  Modify the pipeline manifest to remove GCP inverse proxy (not needed for on-prem).
*  Create the kubeflow namespace and apply cluster-scoped and pipeline-specific resources.
*  Patch the ml-pipeline-ui service to expose it via NodePort (31380).
*  Access the Kubeflow UI at http://<node-ip>:31380 and verify all pods are running.
