from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import numpy as np
import joblib


model = joblib.load('linear_regression_model.pkl')

app = FastAPI()

class PredictionRequest(BaseModel):
    features: list


@app.get("/")
def home():
    return {"message": "Linear Regression Model API is Running!"}


@app.post("/predict/")
async def predict(request: PredictionRequest):
    try:
        # Extract features and reshape for the model
        features = np.array(request.features).reshape(-1, 1)  # Reshape for sklearn

        # Predict using the model
        predictions = model.predict(features)

        result = {
            'predictions': predictions.tolist()
        }
        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

