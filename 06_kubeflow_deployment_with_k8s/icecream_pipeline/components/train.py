

def train(input_csv_path: str, model_path: str):

    import pandas as pd
    import joblib
    import mlflow
    import mlflow.sklearn
    from sklearn.linear_model import LinearRegression
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
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    model = LinearRegression()
    model.fit(X_train, y_train)

    # Save model locally
    joblib.dump(model, model_path)

    # Log to MLflow
    with mlflow.start_run():
        mlflow.log_param("model_type", "LinearRegression")
        mlflow.log_param("input_data", input_csv_path)
        mlflow.log_artifact(model_path, artifact_path="models")
     
        mlflow.sklearn.log_model(
        sk_model=model,
        artifact_path="sklearn-model",
        registered_model_name="ice_cream_model_pipeline"
    )
        print(f"Model saved and logged to MLflow at {model_path}")
        
    
