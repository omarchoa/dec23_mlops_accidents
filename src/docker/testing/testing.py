import requests
import time


header_admin = {"identification": "admin:4dmin"}
payload_new_user = {"username": "antoine", "password": "jussieu", "rights": 0}
payload_old_user = {"user": "antoine"}
payload_year_range = {"start_year": 2021, "end_year": 2021}
payload_input_data = {
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


def test_gateway_status():
    # time.sleep(5)
    response = requests.get(url="http://gateway:8001/gateway/status")
    assert response.status_code == 200
    message = "Test /gateway/status: PASSED"
    print(message)


def test_users_status():
    # time.sleep(5)
    response = requests.get(url="http://gateway:8001/users/status")
    assert response.status_code == 200
    message = "Test /users/status: PASSED"
    print(message)


def test_users_register():
    # time.sleep(5)
    response = requests.post(
        url="http://gateway:8001/users/register",
        json=payload_new_user,
        headers=header_admin,
    )
    assert response.status_code == 200
    message = "Test /users/register: PASSED"
    print(message)


def test_users_remove():
    # time.sleep(5)
    response = requests.delete(
        url="http://gateway:8001/users/remove",
        json=payload_old_user,
        headers=header_admin,
    )
    assert response.status_code == 200
    message = "Test /users/remove: PASSED"
    print(message)


def test_data_download_prep_status():
    # time.sleep(5)
    response = requests.get(url="http://gateway:8001/data-download-prep/status")
    assert response.status_code == 200
    message = "Test /data-download-prep/status: PASSED"
    print(message)


def test_data_download_prep_run():
    # time.sleep(5)
    response = requests.post(
        url="http://gateway:8001/data-download-prep/run",
        json=payload_year_range,
        headers=header_admin,
    )
    assert response.status_code == 200
    message = "Test /data-download-prep/run: PASSED"
    print(message)


def test_training_status():
    # time.sleep(5)
    response = requests.get(url="http://gateway:8001/training/status")
    assert response.status_code == 200
    message = "Test /training/status: PASSED"
    print(message)


def test_training_train():
    # time.sleep(5)
    response = requests.get(
        url="http://gateway:8001/training/train", headers=header_admin
    )
    assert response.status_code == 200
    message = "Test /training/train: PASSED"
    print(message)


def test_prediction_status():
    # time.sleep(5)
    response = requests.get(url="http://gateway:8001/prediction/status")
    assert response.status_code == 200
    message = "Test /prediction/status: PASSED"
    print(message)


def test_prediction_test():
    # time.sleep(5)
    response = requests.get(
        url="http://gateway:8001/prediction/test",
        headers=header_admin,
    )
    assert response.status_code == 200
    message = "Test /prediction/test: PASSED"
    print(message)


def test_prediction_call():
    # time.sleep(5)
    response = requests.post(
        url="http://gateway:8001/prediction/call",
        json=payload_input_data,
        headers=header_admin,
    )
    assert response.status_code == 200
    message = "Test /prediction/call: PASSED"
    print(message)
