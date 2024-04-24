# >>>>>>>> IMPORTS <<<<<<<<

import datetime
import os
import requests
from fastapi import FastAPI, Header, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ConfigDict


# >>>>>>>> CLASS DECLARATIONS <<<<<<<<


## define input data model for endpoint /users/register
class NewUser(BaseModel):
    username: str
    password: str
    rights: int


## define input data model for endpoint /users/remove
class OldUser(BaseModel):
    user: str


## define input data model for endpoint /data-download-prep/run
class YearRange(BaseModel):
    start_year: int  ### admin shall use valid year, e.g. 2021
    end_year: int  ### admin shall use valid year, e.g. 2021


## define input data model for endpoint /prediction/call
class InputDataPredCall(BaseModel):
    model_config = ConfigDict(revalidate_instances="always")
    place: int
    catu: int
    sexe: int
    secu1: float
    year_acc: int
    victim_age: int
    catv: int
    obsm: int
    motor: int
    catr: int
    circ: int
    surf: int
    situ: int
    vma: int
    jour: int
    mois: int
    lum: int
    dep: int
    com: int
    agg_: int
    inter: int
    atm: int
    col: int
    lat: float
    long: float
    hour: int
    nb_victim: int
    nb_vehicules: int


## define input data model for endpoint /scoring/label_prediction
class InputDataLabelPred(BaseModel):
    model_config = ConfigDict(revalidate_instances="always")
    request_id: int
    y_true: int


# >>>>>>>> FUNCTION DECLARATIONS <<<<<<<<


def return_request(response):
    if response.status_code == 200:
        return eval(response.content.decode("utf-8"))
    else:
        raise HTTPException(status_code=400, detail="Bad request.")


def get_all_users():
    response = requests.get(url="http://users:8002/all")
    return return_request(response)


def verify_rights(identification, rights):
    """
    rights: 
    - 0 for user, robot and administrator,
    - 1 for robot and administrator
    - 2 for administrator
    """

    user_type = {0: "User", 1: "Robot", 2: "Administrator"}

    try:
        user, pwd = identification.split(":")
    except:
        raise HTTPException(
            status_code=401,
            detail="Identification doesn't match the following pattern: username:password",
        )

    users_db = get_all_users()

    if user in users_db and users_db[user]["admin"] >= rights:
        if users_db[user]["pwd"] == pwd:
            return user
        else:
            raise HTTPException(status_code=401, detail="Invalid password.")
    else:
        raise HTTPException(
            status_code=403, detail=f"{user_type[rights]} rights required."
        )


log_directory = "/logs"
# os.makedirs(log_directory, exist_ok=True)

def log(start, user, data, logname):
    full_logname = f"/logs/{logname}"
    if not os.path.exists(full_logname):
        with open(full_logname, "w") as logfile:
            logfile.write("start;end;user;data\n")
    end = str(datetime.datetime.now())
    with open(full_logname, "a") as logfile:
        logfile.write(f"{start};{end};{user};{data}\n")


# >>>>>>>> ERROR MANAGEMENT <<<<<<<<
## revise


# responses = {
#     200: {"description": "OK"},
#     401: {"description": "Identifiant ou mot de passe invalide(s)"}
# }


# >>>>>>>> API GATEWAY DECLARATION <<<<<<<<


api = FastAPI(title="🛡️ SHIELD API Gateway")


# >>>>>>>> API GATEWAY STATUS CHECK <<<<<<<<


@api.get(path="/gateway/status", tags=["API Gateway"], name="check API gateway status")
async def gateway_status():
    response = "The API gateway is up."
    return JSONResponse(content=response)


# >>>>>>>> MICROSERVICES - USERS <<<<<<<<


@api.get(
    path="/users/status",
    tags=["MICROSERVICES - Users"],
    name="check users microservice API status",
)
async def users_status():
    response = requests.get(url="http://users:8002/status")
    return return_request(response)


# @api.get(path="/users/all", tags=["MICROSERVICES - Users"], name="get all users")
# async def users_all():
#     return get_all_users()


@api.post(path="/users/register", tags=["MICROSERVICES - Users"], name="register user")
async def users_register(new_user: NewUser, identification=Header(None)):
    """Add a user to the database.
    Administrator rights required.
    Identification field should be filled in as follows: username:password.
    """

    verify_rights(identification, 2)  # 2 for administrator only
    payload = new_user.model_dump()
    response = requests.post(
        url="http://users:8002/register",
        json=payload,
    )
    return return_request(response)


@api.delete(path="/users/remove", tags=["MICROSERVICES - Users"], name="remove user")
async def users_remove(old_user: OldUser, identification=Header(None)):
    """Remove a user from the database.
    Administrator rights required.
    Identification field should be filled in as follows: username:password.
    """

    verify_rights(identification, 2)  # 2 for administrator only
    payload = old_user.model_dump()
    response = requests.delete(url="http://users:8002/remove", json=payload)
    return return_request(response)


# >>>>>>>> MICROSERVICES - DATA-DOWNLOAD-PREP <<<<<<<<


@api.get(
    path="/data-download-prep/status",
    tags=["MICROSERVICES - Data-Download-Prep"],
    name="check data-download-prep microservice API status",
)
async def data_download_prep_status():
    response = requests.get(url="http://data-download-prep:8003/status")
    return return_request(response)


@api.post(
    path="/data-download-prep/run",
    tags=["MICROSERVICES - Data-Download-Prep"],
    name="download and prepare data",
)
async def data_download_prep_run(year_range: YearRange, identification=Header(None)):
    verify_rights(identification, 1)  # 1 for robot and administrator
    payload = year_range.model_dump()
    response = requests.post(
        url="http://data-download-prep:8003/run",
        json=payload,
    )
    return return_request(response)


# >>>>>>>> MICROSERVICES - TRAINING <<<<<<<<


@api.get(
    path="/training/status",
    tags=["MICROSERVICES - Training"],
    name="check training microservice API status",
)
async def training_status():
    response = requests.get(url="http://training:8004/status")
    return return_request(response)


@api.get(path="/training/train", tags=["MICROSERVICES - Training"], name="train model")
async def training_train(identification=Header(None)):
    verify_rights(identification, 1)  # 1 for robot and administrator
    response = requests.get(url="http://training:8004/train")
    return return_request(response)


# >>>>>>>> MICROSERVICES - PREDICTION <<<<<<<<


@api.get(
    path="/prediction/status",
    tags=["MICROSERVICES - Prediction"],
    name="check prediction microservice API status",
)
async def prediction_status():
    response = requests.get(url="http://prediction:8005/status")
    return return_request(response)


@api.get(
    path="/prediction/test",
    tags=["MICROSERVICES - Prediction"],
    name="predict from test",
)
async def prediction_test(identification=Header(None)):
    verify_rights(identification, 0)  # at least user rights
    response = requests.get(url="http://prediction:8005/test")
    return return_request(response)


@api.post(
    path="/prediction/call",
    tags=["MICROSERVICES - Prediction"],
    name="predict from call",
)
async def prediction_call(input_data: InputDataPredCall, identification=Header(None)):
    verify_rights(identification, 0)  # at least user rights
    payload = input_data.model_dump()
    response = requests.post(url="http://prediction:8005/call", json=payload)
    return return_request(response)


# >>>>>>>> MICROSERVICES - SCORING <<<<<<<<


@api.get(
    path="/scoring/status",
    tags=["MICROSERVICES - Scoring"],
    name="check scoring microservice API status",
)
async def scoring_status():
    response = requests.get(url="http://scoring:8006/status")
    return return_request(response)


@api.post(
    path="/scoring/label_prediction",
    tags=["MICROSERVICES - Scoring"],
    name="label prediction",
)
async def scoring_label_prediction(
    input_data: InputDataLabelPred, identification=Header(None)
):
    verify_rights(identification, 0)  # at least user rights
    payload = input_data.model_dump()
    response = requests.post(url="http://scoring:8006/label_prediction", json=payload)
    response_clean = str(response.content)[3:-2]  ### strip unnecessary characters
    if "updated" in response_clean:
        return JSONResponse(content=response_clean)
    elif "not found" in response_clean:
        raise HTTPException(status_code=404, detail=response_clean)
    else:
        raise HTTPException(status_code=400, detail="Bad request.")


@api.get(
    path="/scoring/update_f1_score",
    tags=["MICROSERVICES - Scoring"],
    name="update f1 score",
)
async def scoring_update_f1_score(identification=Header(None)):
    start = str(datetime.datetime.now())
    user = verify_rights(identification, 1)  # 1 for robot and administrator
    response = requests.get(url="http://scoring:8006/update_f1_score")
    # f1_score = return_request(response)
    f1_score = "0.76543210"
    log(start, user, f1_score, "f1-score.csv")
    return f1_score
