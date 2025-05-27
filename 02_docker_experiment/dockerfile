FROM python:3.10-slim

WORKDIR /app

COPY linear_regression_model.pkl .

COPY requirements.txt . 

RUN pip install -r requirements.txt

COPY . .

EXPOSE 5005

CMD ["python", "app.py"]