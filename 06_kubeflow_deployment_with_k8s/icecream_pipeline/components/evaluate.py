import pandas as pd
import joblib
import json
import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

def evaluate(model_path: str, input_csv_path: str):
    
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
