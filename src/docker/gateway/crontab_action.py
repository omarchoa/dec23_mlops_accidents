import datetime

import requests

threshold = 0.74
URI = "http://0.0.0.0:8001"  # gateway
log_filename = "/logs/crontab.csv"
retraining = False


def format_timestamp(timestamp):
    return timestamp.strftime("%Y-%m-%d %H:%M:%S")


def log(start, comment):
    with open(log_filename, "a") as log_file:
        log_file.write(f"{format_timestamp(start)}: {comment}\n")


start = datetime.datetime.now()
response = requests.get(
    url=f"{URI}/scoring/get-latest-f1-score",
    headers={"identification": "robot:Autom@t"},
)

if response.status_code == 200:
    latest_score = eval(response.content.decode("utf-8"))
    if latest_score >= threshold:
        comment = (
            f"latest_score ({latest_score}) >= threshold ({threshold}): nothing to do"
        )
    else:
        comment = f"latest_score ({latest_score}) < threshold ({threshold}): model shall be retrained !"
        retraining = True
else:
    comment = (
        f"request status on {URI}/scoring/get-latest-f1-score: {response.status_code}"
    )

log(start, comment)

if retraining:
    start = datetime.datetime.now()
    response = requests.get(
        url=f"{URI}/training/retrain",
        headers={"identification": "robot:Autom@t"},
    )
    requests.get(
        url=f"{URI}/scoring/update-f1-score",
        headers={"identification": "robot:Autom@t"},
    )
    if response.status_code == 200:
        end = datetime.datetime.now()
        comment = f"retraining took {end - start} s"
    else:
        comment = f"retraining failed, request status on {URI}/training/retrain: {response.status_code}"
    log(start, comment)
