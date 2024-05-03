import json
import time

import requests

from config import paths

header_admin = {"identification": "admin:4dmin"}
payload_new_user = {"username": "antoine", "password": "jussieu", "rights": 0}
payload_old_user = {"username": "antoine"}
payload_year_range = {"start_year": 2021, "end_year": 2021}
payload_input_data_pred_call = {
    "place": 10,
    "catu": 3,
    "sexe": 1,
    "secu1": 0.0,
    "year_acc": 2021,
    "victim_age": 60,
    "catv": 2,
    "obsm": 1,
    "motor": 1,
    "catr": 3,
    "circ": 2,
    "surf": 1,
    "situ": 1,
    "vma": 50,
    "jour": 7,
    "mois": 12,
    "lum": 5,
    "dep": 77,
    "com": 77317,
    "agg_": 2,
    "inter": 1,
    "atm": 0,
    "col": 6,
    "lat": 48.6,
    "long": 2.89,
    "hour": 17,
    "nb_victim": 2,
    "nb_vehicules": 1,
}
delay = 5


def test_gateway_status():
    time.sleep(delay)
    response = requests.get(url="http://gateway:8001/gateway/status")
    assert response.status_code == 200
    message = "Test /gateway/status: PASSED"
    print(message)


def test_users_status():
    time.sleep(delay)
    response = requests.get(url="http://gateway:8001/users/status")
    assert response.status_code == 200
    message = "Test /users/status: PASSED"
    print(message)


def test_users_all():
    time.sleep(delay)
    response = requests.get(url="http://gateway:8001/users/all")
    assert response.status_code == 200
    message = "Test /users/all: PASSED"
    print(message)


def test_users_register():
    time.sleep(delay)
    response = requests.post(
        url="http://gateway:8001/users/register",
        json=payload_new_user,
        headers=header_admin,
    )
    assert response.status_code == 200
    message = "Test /users/register: PASSED"
    print(message)


def test_users_remove():
    time.sleep(delay)
    response = requests.delete(
        url="http://gateway:8001/users/remove",
        json=payload_old_user,
        headers=header_admin,
    )
    assert response.status_code == 200
    message = "Test /users/remove: PASSED"
    print(message)


def test_data_download_prep_status():
    time.sleep(delay)
    response = requests.get(url="http://gateway:8001/data-download-prep/status")
    assert response.status_code == 200
    message = "Test /data-download-prep/status: PASSED"
    print(message)


def test_data_download_prep_run():
    time.sleep(delay)
    response = requests.post(
        url="http://gateway:8001/data-download-prep/run",
        json=payload_year_range,
        headers=header_admin,
    )
    assert response.status_code == 200
    message = "Test /data-download-prep/run: PASSED"
    print(message)


def test_training_status():
    time.sleep(delay)
    response = requests.get(url="http://gateway:8001/training/status")
    assert response.status_code == 200
    message = "Test /training/status: PASSED"
    print(message)


def test_training_train():
    time.sleep(delay)
    response = requests.get(
        url="http://gateway:8001/training/train", headers=header_admin
    )
    assert response.status_code == 200
    message = "Test /training/train: PASSED"
    print(message)


def test_training_retrain():
    time.sleep(delay)
    response = requests.get(
        url="http://gateway:8001/training/retrain", headers=header_admin
    )
    assert response.status_code == 200
    message = "Test /training/retrain: PASSED"
    print(message)


def test_prediction_status():
    time.sleep(delay)
    response = requests.get(url="http://gateway:8001/prediction/status")
    assert response.status_code == 200
    message = "Test /prediction/status: PASSED"
    print(message)


def test_prediction_test():
    time.sleep(delay)
    response = requests.get(
        url="http://gateway:8001/prediction/test",
        headers=header_admin,
    )
    assert response.status_code == 200
    message = "Test /prediction/test: PASSED"
    print(message)


def test_prediction_call():
    time.sleep(delay)
    response = requests.post(
        url="http://gateway:8001/prediction/call",
        json=payload_input_data_pred_call,
        headers=header_admin,
    )
    assert response.status_code == 200
    message = "Test /prediction/call: PASSED"
    print(message)


def test_scoring_status():
    time.sleep(delay)
    response = requests.get(url="http://gateway:8001/scoring/status")
    assert response.status_code == 200
    message = "Test /scoring/status: PASSED"
    print(message)


def test_scoring_label_prediction():
    time.sleep(delay)

    with open(paths.LOGS_PREDS_CALL, "r") as file:
        line_string = file.readline().strip("\n")
        line_json = json.loads(line_string)

    payload_input_data_label_pred = {
        "request_id": int(line_json["request_id"]),
        "y_true": 1,
    }

    response = requests.post(
        url="http://gateway:8001/scoring/label-prediction",
        json=payload_input_data_label_pred,
        headers=header_admin,
    )

    assert response.status_code == 200

    message = "Test /scoring/label_prediction: PASSED"

    print(message)


def test_scoring_update_f1_score():
    time.sleep(delay)
    response = requests.get(
        url="http://gateway:8001/scoring/update-f1-score",
        headers=header_admin,
    )
    assert response.status_code == 200
    message = "Test /scoring/update_f1_score: PASSED"
    print(message)


def test_scoring_get_f1_scores():
    time.sleep(delay)
    response = requests.get(
        url="http://gateway:8001/scoring/get-f1-scores",
        headers=header_admin,
    )
    assert response.status_code == 200
    message = "Test /scoring/update_f1_score: PASSED"
    print(message)


def test_scoring_get_latest_f1_score():
    time.sleep(delay)
    response = requests.get(
        url="http://gateway:8001/scoring/get-latest-f1-score",
        headers=header_admin,
    )
    assert response.status_code == 200
    message = "Test /scoring/get_latest_f1_score: PASSED"
    print(message)


def test_frontend_status():
    time.sleep(delay)
    response = requests.get(
        url="http://frontend:8501/",
    )
    assert response.status_code == 200
    message = "Test /frontend/status: PASSED"
    print(message)
