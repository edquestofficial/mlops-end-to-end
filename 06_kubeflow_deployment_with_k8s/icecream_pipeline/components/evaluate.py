def evaluate(model_path: str, input_csv_path: str):
    
    import pandas as pd
    import joblib
    import json
    import numpy as np
    import mlflow
    from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
    from sklearn.model_selection import train_test_split
    import os

    # Inject your MinIO credentials here
    os.environ["AWS_ACCESS_KEY_ID"] = "YxIAgVvKESgXx4cc1Guj"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "R43tuKQAgwkaPD4t9F0OVTaJo8M66Ce3OltjqCg8"
    os.environ["MLFLOW_S3_ENDPOINT_URL"] = "http://10.111.65.79:9000" # minio service ip and port
    
    mlflow.set_tracking_uri("http://192.168.1.100:32000")  # Replace with your server IP
    mlflow.set_experiment("IceCreamPipeline")

    df = pd.read_csv(input_csv_path)
    X = df[['temp']]
    y = df['price']
    _, X_test, _, y_test = train_test_split(X, y, test_size=0.2)

    model = joblib.load(model_path)
    y_pred = model.predict(X_test)

    mae = mean_absolute_error(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test, y_pred)

    metrics = {
        "metrics": [
            {"name": "mae", "numberValue": float(mae)},
            {"name": "mse", "numberValue": float(mse)},
            {"name": "rmse", "numberValue": float(rmse)},
            {"name": "r2", "numberValue": float(r2)},
        ]
    }

    with open("/data/eval.json", "w") as f:
        json.dump(metrics, f)

    print("Evaluation metrics written to /data/eval.json")
    print(metrics)

    # Log to MLflow
    with mlflow.start_run():
        mlflow.log_metric("mae", mae)
        mlflow.log_metric("mse", mse)
        mlflow.log_metric("rmse", rmse)
        mlflow.log_metric("r2", r2)
