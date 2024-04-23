import requests
import time


def test_gateway_status():
    time.sleep(10)
    response = requests.get("http://gateway:8001/gateway/status")
    assert response.status_code == 200
    message = "Test /gateway/status: PASSED"
    print(message)


def test_data_download_prep_status():
    time.sleep(10)
    response = requests.get("http://gateway:8001/data-download-prep/status")
    assert response.status_code == 200
    message = "Test /data-download-prep/status: PASSED"
    print(message)
