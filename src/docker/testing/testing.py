import sys
import requests

def test_data_status():
    endpoints = [
        "gateway/status",
        "data/status",
        "data/update",
        "training/status",
        "training/train",
        "prediction/status",
        "prediction/test",
        "prediction/call",
        "scoring/status",
        "scoring/label_prediction",
        "scoring/update_f1_score"
    ]

    for endpoint in endpoints:
        url = f"http://gateway:8001/{endpoint}"
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an exception if the status code is not 200
            sys.stdout.write(f"Test {url}: PASSED with status code {response.status_code}\n")
        except requests.RequestException as e:
            sys.stdout.write(f"Test {url}: FAILED - {e}\n")

test_data_status()
