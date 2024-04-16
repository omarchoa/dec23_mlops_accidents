import requests

def test_data_status(endpoint):
    url = f"http://gateway:8001/{endpoint}"
    response = requests.get(url)
    assert response.status_code == 200
    print(f"Test {url}: PASSED")

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
    test_data_status(endpoint)
