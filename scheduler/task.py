"""
task.py
Script to manage the deployment of machine learning models to a prediction API.
"""

import os
import pickle
import random
import requests
import logging
from sklearn.metrics import classification_report

# Configuration
API_URL = 'http://iris-api-new:8000'
MODELS_DIR = '/app/models/'
DATA_DIR = '/app/data/'
HEADERS = {'Content-Type': 'application/json'}

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def send_request(url, data, headers, method='GET'):
    try:
        if method == 'GET':
            response = requests.request('GET', url, json=data, headers=headers)
        elif method == 'POST':
            response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        return response
    except requests.RequestException as e:
        logging.error(f'Request to {url} failed: {e}')
        return None

def deploy_model(model_name):
    url = f"{API_URL}/load"
    data = {"model_name": model_name}
    response = send_request(url, data, HEADERS, method='POST')
    if response and response.status_code == 200:
        logging.info("Model deployed successfully!")
        logging.info(response.json())
    else:
        logging.error(f"Model deployment failed: {response.status_code}")

def select_and_evaluate_model():
    models = os.listdir(MODELS_DIR)
    model_name = fetch_current_model_name()

    if model_name in models:
        models.remove(model_name)

    random_model_name = random.choice(models)
    selected_model_path = os.path.join(MODELS_DIR, random_model_name)
    test_data, test_labels = load_test_data()

    selected_model = pickle.load(open(selected_model_path, 'rb'))
    predictions = selected_model.predict(test_data)
    report = classification_report(test_labels, predictions)

    logging.info(f"Selected model: {random_model_name}")
    logging.info(f"Classification Report:\n{report}")

    return random_model_name

def fetch_current_model_name():
    url = f"{API_URL}/predict"
    data = {
        "sepallength": 1.1,
        "sepalwidth": 1.2,
        "petallength": 1.3,
        "petalwidth": 1.4
    }
    response = send_request(url, data, HEADERS, method='GET')
    if response:
        response_data = response.json()
        return response_data.get('model')
    return None

def load_test_data():
    test_data = pickle.load(open(os.path.join(DATA_DIR, 'test-data.p'), 'rb'))
    test_labels = pickle.load(open(os.path.join(DATA_DIR, 'test-labels.p'), 'rb'))
    return test_data, test_labels

if __name__ == '__main__':
    logging.info("Starting model selection and evaluation...")
    new_model_name = select_and_evaluate_model()
    if new_model_name:
        deploy_model(new_model_name)
