import requests

# API URL
url = 'http://localhost:8000/predict'

# Data to be sent as JSON
data = {
    "sepallength": 1.1,
    "sepalwidth": 1.2,
    "petallength": 1.3,
    "petalwidth": 1.4
}

# Request headers (if needed)
headers = {
    'Content-Type': 'application/json'
}

# Sending the POST request
response = requests.post(url, json=data, headers=headers)

# Checking if the request was successful
if response.status_code == 200:
    print("Request successful!")
    # Processing the response
    response_data = response.json()  # Convert response from JSON to dictionary
    print("Model name:", response_data.get('model', 'Model not found'))
else:
    print("Request failed:", response.status_code)
