import requests


def test_gateway_status():
    response = requests.get("http://gateway:8001/gateway/status")
    assert response.status_code == 200
    message = "Test /gateway/status: PASSED"
    print(message)
