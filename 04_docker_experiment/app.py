from flask import Flask, request, jsonify
import numpy as np
import joblib

# Load the saved logistic regression model
model = joblib.load('linear_regression_model.pkl')

app = Flask(__name__)

@app.route('/')
def home():
    return "Linear Regression Model API is Running!"

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()

    # Validate input
    if not data or 'features' not in data:
        return jsonify({'error': 'Invalid input. Expected JSON with "features" key.'}), 400

    try:
        features = np.array(data['features']).reshape(-1, 1)  # Reshape for sklearn
        predictions = model.predict(features)

        result = {
            'predictions': predictions.tolist()
        }
        return jsonify(result)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5005)
