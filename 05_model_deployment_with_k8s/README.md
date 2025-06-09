###### Setting up MLflow Tracking UI and Model Serving on Kubernetes and autoscaling


-- Prerequisites
   Before starting, ensure you have the following:
      A running Kubernetes cluster (Minikube, EKS, GKE, etc.)
      kubectl configured and working
      Docker installed and authenticated to your container registry

-- Step 1 - Containerize MLflow Tracking UI
    Create a Dockerfile for MLflow Tracking Server:

  Build and push the image:
    docker build -t edquest/mlflow-ui:v1.0.0 .  # Docker repo name "your-docker-user"
    docker pushedquest/mlflow-ui:v1.0.0  # push the image to docker hub repository

-- Step 2 - Deploy MLflow to Kubernetes
    Create mlflow-ui-deployment.yaml:

-- Step 3 - Expose MLflow UI
    Create mlflow-ui-service.yaml:

  Apply the resources:
    kubectl apply -f mlflow-ui-deployment.yaml
    kubectl apply -f mlflow-ui-service.yaml

-- Step 4 - Use MLflow for Tracking & Serving
    Log experiments to the Mlflow Tracking UI

#### Deploy the Model using MLflow Model Serving

-- Step 5 - Containerize MLflow Model Server
    Create a Dockerfile for MLflow Model Server:
 
  Build and push the image:
    docker build -t  edquest/ml-model-server:v1.0.0 .  # Docker repo name "your-docker-user"
    docker push  edquest/ml-model-server:v1.0.0  # push the image to docker hub repository

-- Step 6 - Deploy MLflow Model Server to Kubernetes
    Create model-deployment.yaml:

  Apply the resources:
    kubectl apply -f configmap.yml  
    kubectl apply -f model-deployment.yml  # service manifiest included in same file

-- Step 8 - Autoscale your Kubernetes pod using Horizontal Pod Autoscaler (HPA)

  Prerequisites
    1: A Kubernetes cluster (e.g., Minikube, EKS, GKE, AKS).
    2: Metrics Server installed and running in the cluster.
    3: A deployment or pod that you want to autoscale.
    4: Your application should expose resource metrics like CPU or memory.

  Step-by-Step Guide
  1. Install Metrics Server
     If not already installed, you can install it using:
     kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml

     Edit the deployment of metric server to make it running, by adding it
     # - --kubelet-insecure-tls
    
     Verify it's working:
     kubectl get deployment metrics-server -n kube-system

  2: Create the HPA
    Use the following command to create an HPA that scales based on CPU usage:
    kubectl autoscale deployment ice-cream-model-deployment --cpu-percent=50 --min=1 --max=5

    This means:
      If CPU usage exceeds 50%, Kubernetes will scale up the pods.
      It will maintain between 1 and 5 replicas.
  
  3: Check HPA Status
    kubectl get hpa

    You'll see something like:
    NAME               REFERENCE                     TARGETS   MINPODS   MAXPODS   REPLICAS   AGE
    ice-cream-model-hpa   Deployment/<deployment-name>   10%/50%   1         5         1          1m

  4: Generate Load (Optional)
     To test autoscaling, you can generate CPU load using a tool like stress or a custom script inside the pod.  

    Optional: YAML-Based HPA

      apiVersion: autoscaling/v2
      kind: HorizontalPodAutoscaler
      metadata:
        name: ice-cream-model-hpa
      spec:
        scaleTargetRef:
          apiVersion: apps/v1
          kind: Deployment
          name: <deployment-name>
        minReplicas: 1
        maxReplicas: 5
        metrics:
        - type: Resource
          resource:
            name: cpu
            target:
              type: Utilization
              averageUtilization: 50

    Apply the HPA:
    Save the above YAML to a file (e.g., ice-cream-model-hpa.yaml) and apply it:
    kubectl apply -f ice-cream-model-hpa.yaml

    
    # - --kubelet-insecure-tls
    # - --kubelet-preferred-address-types=InternalIP,Hostname,InternalDNS,ExternalDNS,ExternalIP

-- Step 9 - Deploy the model to run below command 
    curl -X POST http://<cluster-node-IP>:<nodeport>/serve-model

-- Step 10 - Test Inference
    curl -X POST http://<mlflow-model-service-ip>:<port>/invocations \
      -H "Content-Type: application/json" \
      --data @input.json

-- Step 11 - To downgrade model latest version to old version (eg. latest v5 to v3 or any other version)
   
  1: Here's a modular, function-based Bash script that:
      1. Accepts user inputs for model_name, alias, and version.
      2. Calls the API to update the alias.
      3. Fetches the MLflow tracking server IP from a running Kubernetes service.
      4. Updates the ConfigMap YAML file with the new values.
      5. Applies the updated ConfigMap and restarts the associated deployment.
      6. Includes logging for traceability.

  2:  Save the script as downgrade_model.sh.
      Make it executable:
      chmod +x latest_code/k8s/downgrade_model.sh
  3: Run it:
      ./latest_code/k8s/downgrade_model.sh.sh


For Inferencing the model with simple data:

curl -X POST http://10.102.160.124:80/invocations \
     -H "Content-Type: application/json" \
     -d '{
           "dataframe_split": {
             "columns": ["temp"],
             "data": [[33]]
           }
         }'



For Multiple inputs:

curl -X POST http://10.96.219.175:80/invocations \
     -H "Content-Type: application/json" \
     -d '{
           "dataframe_split": {
             "columns": ["temp"],
             "data": [[33], [40], [25]]
           }
         }'
 
