from kfp.components import InputPath

def deploy(model_input: InputPath(str)):
    import os
    import shutil

    # Simulate deployment by printing
    print(f"Deploying model from {model_input}")
    # Here you can add KServe YAML apply logic or use `kserve` CLI if available


# def deploy(model_path: InputPath(str)):
#     import os
#     import shutil

#     os.makedirs("/mnt/models", exist_ok=True)
#     shutil.copy(model_path, "/mnt/models/model.joblib")
#     print("Copied model to /mnt/models for KServe")

#     # Save KServe YAML
#     with open("kserve.yaml", "w") as f:
#         f.write("""
# apiVersion: serving.kserve.io/v1beta1
# kind: InferenceService
# metadata:
#   name: icecream-model
# spec:
#   predictor:
#     sklearn:
#       storageUri: "pvc://model-pvc"
#       resources:
#         requests:
#           cpu: 100m
#           memory: 256Mi
# """)
#     print("KServe YAML written.")
