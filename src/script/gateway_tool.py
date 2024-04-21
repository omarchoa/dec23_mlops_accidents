import requests
import sys

if len(sys.argv) > 2:
    print(f"""This script get the status of services and initiates data for prediction according to 2021 accidents.\n
Usage: python3 {sys.argv[0]} [IP_gateway_address]
- IP_gateway_address: IP address of the host of gateway API""")
    sys.exit(1)
try:
    IP_gateway_address = sys.argv[1]
except:
    IP_gateway_address = "127.0.0.1"

URI = f"http://{IP_gateway_address}:8001"

print("""You can select multiple choice by separating them by a space charactere :

    1 - get gateway API status
    2 - get users API status
    3 - get data-download-prep API status
    4 - get training API status
    5 - get prediction API status
    6 - download and preprocess data of 2021 year
    7 - train data
""")


choice = input("Your choice: ")
print("")
choice_list = choice.split(" ")

def return_request(response):
    if response.status_code == 200:
        return eval(response.content.decode("utf-8"))
    else:
        return response.status_code

def get_gateway_status():
    response = requests.get(url=f"{URI}/gateway/status")
    return return_request(response)


def get_users_status():
    response = requests.get(url=f"{URI}/users/status")
    return return_request(response)


def get_data_download_prep_status():
    response = requests.get(url=f"{URI}/data-download-prep/status")
    return return_request(response)


def get_training_status():
    response = requests.get(url=f"{URI}/training/status")
    return return_request(response)


def get_prediction_status():
    response = requests.get(url=f"{URI}/prediction/status")
    return return_request(response)


def data_download_prep_run():
    response = requests.post(
        url=f"{URI}/data-download-prep/run",
        headers={"identification": "robot:Autom@t"},
        json={"start_year": 2021, "end_year": 2021}
    )
    return return_request(response)


# def get_all():
#     response = requests.get(url=f"{URI}/users/all")
#     print(return_request(response))


def training_train():
    response = requests.get(
        url=f"{URI}/training/train",
        headers={"identification": "robot:Autom@t"},
    )
    return return_request(response)

function_dictionary = {
    "1": get_gateway_status,
    "2": get_users_status,
    "3": get_data_download_prep_status,
    "4": get_training_status,
    "5": get_prediction_status,
    "6": data_download_prep_run,
    "7": training_train,
}

for choice in choice_list:
    try:
        print(f"{choice}: {function_dictionary[choice]()}")
    except Exception as err:
        print(err)
        sys.exit(1)
