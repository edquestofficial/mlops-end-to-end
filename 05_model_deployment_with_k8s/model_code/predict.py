import json
import requests
import time

# Load input data
with open("ice_cream_data.json", "r") as f:
    input_data = f.read()

url = "http://10.96.219.175:80/invocations"
headers = {"Content-Type": "application/json"}

while True:
    try:
        response = requests.post(url, headers=headers, data=input_data)
        print("Response:", response.json())
    except Exception as e:
        print("Error:", e)
    # time.sleep(1)