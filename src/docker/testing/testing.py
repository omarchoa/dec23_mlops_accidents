import sys
import json
import requests

def test_endpoint(method, url, data=None, headers=None):
    try:
        if method == "GET":
            response = requests.get(url)
        elif method == "POST":
            response = requests.post(url, json=data, headers=headers)

        response.raise_for_status()  # Raise an exception if the status code is not 200
        sys.stdout.write(f"Test {url}: PASSED with status code {response.status_code}\n")
    except requests.RequestException as e:
        sys.stdout.write(f"Test {url}: FAILED - {e}\n")

def test_endpoints():
    endpoints = {
        "GET": [
            "gateway/status",
            "data/status",
            "training/status",
            "prediction/status",
            "scoring/status",
            "scoring/label_prediction"
        ],
        "POST": [
            {"url": "data/update", "data": {"key": "value"}, "headers": {"Content-Type": "application/json"}},
            {"url": "training/train", "data": {"key": "value"}, "headers": {"Content-Type": "application/json"}},
            {"url": "prediction/test", "data": {"key": "value"}, "headers": {"Content-Type": "application/json"}},
            {"url": "prediction/call", "data": {"key": "value"}, "headers": {"Content-Type": "application/json"}},
            {"url": "scoring/update_f1_score", "data": {"key": "value"}, "headers": {"Content-Type": "application/json"}}
        ]
    }

    for method, urls in endpoints.items():
        for endpoint in urls:
            if method == "GET":
                url = f"http://gateway:8001/{endpoint}"
                test_endpoint(method, url)
            elif method == "POST":
                url = f"http://gateway:8001/{endpoint['url']}"
                data = endpoint.get('data', {})
                headers = endpoint.get('headers', {})
                test_endpoint(method, url, data=data, headers=headers)

test_endpoints()
