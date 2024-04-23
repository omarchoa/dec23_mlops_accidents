import requests
import time


admin = {"identification": "admin:4dmin"}


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
    new_user = {"username": "antoine", "password": "jussieu", "rights": 0}
    response = requests.post(
        url="http://gateway:8001/users/register", json=new_user, headers=admin
    )
    assert response.status_code == 200
    message = "Test /users/register: PASSED"
    print(message)


def test_users_remove():
    # time.sleep(5)
    old_user = {"user": "antoine"}
    response = requests.delete(
        url="http://gateway:8001/users/remove", json=old_user, headers=admin
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
