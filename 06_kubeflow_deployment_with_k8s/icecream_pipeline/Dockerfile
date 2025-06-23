FROM python:3.9

# Set working directory
WORKDIR /app

# Copy component and data directories into the container
COPY components/ ./components/
COPY data/ ./data/

# Install dependencies
RUN pip install --no-cache-dir pandas scikit-learn joblib mlflow[extras]==3.1.0 boto3
   
