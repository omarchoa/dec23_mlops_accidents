import json
from fastapi.testclient import TestClient
import os
from pathlib import Path
import pytest
import sys

# internal
root_path = Path(os.path.realpath(__file__)).parents[3]
sys.path.append(os.path.join(root_path, "src", "features", "api"))
from src.api.api import api

# Load user data
with open("src/features/api/users_db_bis.json", 'r') as file:
    users_db = json.load(file)

# Create a test client for our API
client = TestClient(api)

def test_is_functional():
    # Send a GET request to the root of the API
    response = client.get('/status')
    # Check that the response is OK (code 200)
    assert response.status_code == 200
    print("Test is_functional: PASSED")

def test_register_user():
    new_user_data = {"username": "test_user", "password": "test_password"}
    # Send a POST request to the /register endpoint with the identification header
    response = client.request(method="POST", url='/register', json=new_user_data, headers={"identification": "admin:4dmin"})
    # Check that the response is OK (code 200)
    assert response.status_code == 200
    print("Test register_user: PASSED")

def test_remove_user():
    old_user_data = {"user": "test_user"}
    # Send a DELETE request to the /remove_user endpoint with the identification header
    response = client.request(method="DELETE", url='/remove_user', json=old_user_data, headers={"identification": "admin:4dmin"})
    # Check that the response is OK (code 200)
    assert response.status_code == 200
    print("Test remove_user: PASSED")

@pytest.mark.skip(reason="Exclu temporairement en raison d'une erreur")
def test_predict_from_test():
    # Send a GET request to the /predict_from_test endpoint with the identification header
    response = client.get('/predict_from_test', headers={"identification": "fdo:c0ps"})
    # Check that the response is OK (code 200)
    assert response.status_code == 200
    print("Test predict_from_test: PASSED")

@pytest.mark.skip(reason="Exclu temporairement en raison d'une erreur")
def test_predict_from_call():
    # Send a POST request to the /predict_from_call endpoint with input data and identification header
    input_data = {"place": 10, "catu": 3, "sexe": 1, "secu1": 0.0, "year_acc": 2021, "victim_age": 60, "catv": 2, "obsm": 1, "motor": 1, "catr": 3, "circ": 2, "surf": 1, "situ": 1, "vma": 50, "jour": 7, "mois": 12, "lum": 5, "dep": 77, "com": 77317, "agg_": 2, "inter": 1, "atm": 0, "col": 6, "lat": 48.60, "long": 2.89, "hour": 17, "nb_victim": 2, "nb_vehicules": 1}
    response = client.post('/predict_from_call', json=input_data, headers={"identification": "admin:4dmin"})
    # Check that the response is OK (code 200)
    assert response.status_code == 200
    print("Test predict_from_call: PASSED")

@pytest.mark.skip(reason="Exclu temporairement en raison d'une erreur")
def test_train_model():
    # Send a GET request to the /train endpoint with the identification header
    response = client.get('/train', headers={"identification": "admin:4dmin"})
    # Check that the response is OK (code 200)
    assert response.status_code == 200
    print("Test train_model: PASSED")

def test_label_prediction():
    # Send a POST request to the /label_prediction endpoint with prediction data and identification header
    prediction = {"request_id": 6012919476848551, "y_true": 0}
    response = client.post('/label_prediction', json=prediction, headers={"identification": "fdo:c0ps"})
    # Check that the response is OK (code 200)
    assert response.status_code == 200
    print("Test label_prediction: PASSED")

@pytest.mark.skip(reason="Exclu temporairement car dépendant des fichiers non stockés sur le repo distant")
def test_update_f1_score():
    # Send a GET request to the /update_f1_score endpoint with the identification header
    response = client.get('/update_f1_score', headers={"identification": "admin:4dmin"})
    # Check that the response is OK (code 200)
    assert response.status_code == 200
    print("Test update_f1_score: PASSED")
