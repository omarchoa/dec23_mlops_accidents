import requests
import time


header_admin = {"identification": "admin:4dmin"}
payload_new_user = {"username": "antoine", "password": "jussieu", "rights": 0}
payload_old_user = {"user": "antoine"}
payload_year_range = {"start_year": 2021, "end_year": 2021}


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
