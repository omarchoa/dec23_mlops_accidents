from fastapi import FastAPI, Header, HTTPException
from fastapi.responses import JSONResponse
import json
import os
from pydantic import BaseModel
import requests


def return_request(response):
    if response.status_code == 200:
        return eval(response.content.decode('utf-8'))
    else:
        raise HTTPException(status_code=400, detail="Bad request.")


def get_users_db():
    response = requests.get(url='http://users_container:8002/users_db')
    return return_request(response)


def verify_rights(identification, rights):
    """
    rights: 0 for user, 1 for administrator
    """
    user_type = {
        0 : "User",
        1 : "Administrator"
    }
    try:
        user, pwd = identification.split(":")
    except:
        raise HTTPException(status_code=401, detail="Identification doesn't match the following pattern: user:password")

    users_db = get_users_db()

    if user in users_db and users_db[user]['admin'] == rights:
        if users_db[user]['pwd'] == pwd:
            return user
        else:
            raise HTTPException(status_code=401, detail="Invalid password")
    else:
        raise HTTPException(status_code=403, detail=f"{user_type[rights]} rights are required")


## define input data model for /update_data endpoint in data microservice
class YearRange(BaseModel):
    start_year: int  ### admin shall use valid year, e.g. 2021
    end_year: int  ### admin shall use valid year, e.g. 2021


## define input data model for /predict_from_call endpoint in prediction microservice
class InputDataPredCall(BaseModel):
    place: int = 10
    catu: int = 3
    sexe: int = 1
    secu1: float = 0.0
    year_acc: int = 2021
    victim_age: int = 60
    catv: int = 2
    obsm: int = 1
    motor: int = 1
    catr: int = 3
    circ: int = 2
    surf: int = 1
    situ: int = 1
    vma: int = 50
    jour: int = 7
    mois: int = 12
    lum: int = 5
    dep: int = 77
    com: int = 77317
    agg_: int = 2
    inter: int = 1
    atm: int = 0
    col: int = 6
    lat: float = 48.60
    long: float = 2.89
    hour: int = 17
    nb_victim: int = 2
    nb_vehicules: int = 1


## define input data model for /label_prediction endpoint in scoring microservice
class InputDataLabelPred(BaseModel):
    request_id: int = 6012919476848551
    y_true: int = 1


# >>>>>>>> ERROR MANAGEMENT <<<<<<<<
responses = {
    200: {"description": "OK"},
    401: {"description": "Identifiant ou mot de passe invalide(s)"}
}


api = FastAPI(title="🛡️ SHIELD API Gateway")


@api.get(path="/gateway/status", tags=["API Gateway"], name="check API gateway status")
async def gateway_status():
    """check API gateway status"""
    return "The gateway API is up."


@api.get('/users_db', name="Get all database users", tags=['GET'])
async def check():
    return get_users_db()


class User(BaseModel):
    username: str
    password: str
    rights: int  # Default rights (e.g: fdo), for admin rights != 0


@api.get('/users/status', name="Check whether the users API is running", tags=['USERS'])
async def is_users_fonctionnal():
    response = requests.get(url='http://users_container:8002/status')
    return return_request(response)


@api.post('/users/register', name="Add a user in the database", tags=['USERS'])
async def post_user(new_user: User, identification=Header(None)):
    """Add a user in the database
    Administrator rights are required to add a new user.
    Identification field shall be fill as following: identifier:password.
    """
    verify_rights(identification, 1)  # 1 for admin
    response = requests.post(
        url='http://users_container:8002/register',
        json={
            "username": new_user.username,
            "password": new_user.password,
            "rights": new_user.rights
        }
    )
    return return_request(response)


class OldUser(BaseModel):
    user: str


@api.delete('/users/remove_user', name="Suppression d'un utilisateur existant.", tags=['USERS'])
async def remove_user(old_user: OldUser, identification=Header(None)):
    """Remove a user from the database
    Administrator rights are required to add a new user.
    Identification field shall be fill as following: identifier:password.
    """
    verify_rights(identification, 1)  # 1 for admin
    response = requests.post(
        url='http://users_container:8002/register',
        json={"user": old_user.user}
    )
    return return_request(response)


@api.get(path="/data/status", tags=["MICROSERVICES - Data"], name="check data microservice API status",
)
async def data_status():
    response = requests.get(url="http://data_container:8003/status")
    return return_request(response)


@api.post(path="/data/update", tags=["MICROSERVICES - Data"], name="update data")
async def data_update(year_range: YearRange, identification=Header(None)):

    verify_rights(identification, 1)  # 1 for admin
    
    ## microservice call
    response = requests.post(
        url="http://data_container:8003/update",
        json={
            "start_year": year_range.start_year,
            "end_year": year_range.end_year,
        }
    )
    return return_request(response)


# >>>>>>>> MICROSERVICES - TRAINING <<<<<<<<
@api.get(path="/training/status", tags=["MICROSERVICES - Training"], name="check training microservice API status",
)
async def training_status():
    response = requests.get(url="http://training:8004/status")
    return return_request(response)


@api.get(path="/training/train", tags=["MICROSERVICES - Training"], name="train model")
async def training_train(identification=Header(None)):

    verify_rights(identification, 1)  # 1 for admin

    ## microservice call
    response = requests.get(url="http://training:8004/train")

    ## microservice response
    return return_request(response)


# >>>>>>>> MICROSERVICES - PREDICTION <<<<<<<<
@api.get(path="/prediction/status", tags=["MICROSERVICES - Prediction"], name="check prediction microservice API status",
)
async def prediction_status():
    response = requests.get(url="http://prediction:8005/status")
    return return_request(response)


@api.get(path="/prediction/test", tags=["MICROSERVICES - Prediction"], name="predict from test")
async def prediction_test(identification=Header(None)):

    verify_rights(identification, 0)  # 0 for user

    ## microservice call
    response = requests.get(url="http://prediction:8005/test")

    ## microservice response
    return return_request(response)


@api.post(path="/prediction/call", tags=["MICROSERVICES - Prediction"], name="predict from call")
async def prediction_call(input_data: InputDataPredCall, identification=Header(None)):

    verify_rights(identification, 0)  # 0 for user

    ## microservice call
    payload = input_data.model_dump()
    response = requests.post(url="http://prediction:8005/call", json=payload)

    ## microservice response
    return return_request(response)


# >>>>>>>> MICROSERVICES - SCORING <<<<<<<<
# @api.get(path="/scoring/status", tags=["MICROSERVICES - Scoring"], name="check scoring microservice API status")
# async def scoring_status():
#     response = requests.get(url="http://scoring:8006/status")
#     return return_request(response)


# @api.post(path="/scoring/label_prediction", tags=["MICROSERVICES - Scoring"], name="label prediction")
# async def scoring_label_prediction(input_data: InputDataLabelPred, identification=Header(None)):

#     verify_rights(identification, 0)  # 0 for user

#     ## microservice call
#     payload = input_data.model_dump()
#     response = requests.post(
#         url="http://scoring:8006/label_prediction", json=payload
#     )

#     ## microservice response
#     response_clean = str(response.content)[3:-2]  ### strip unnecessary characters
#     if "updated" in response_clean:
#         return JSONResponse(content=response_clean)
#     elif "not found" in response_clean:
#         raise HTTPException(status_code=404, detail=response_clean)
#     else:
#         raise HTTPException(status_code=400, detail="Bad request.")


# @api.get(path="/scoring/update_f1_score", tags=["MICROSERVICES - Scoring"], name="update f1 score")
# async def scoring_update_f1_score(identification=Header(None)):

#     verify_rights(identification, 1)  # 1 for admin

#     ## microservice call
#     response = requests.get(url="http://scoring:8006/update_f1_score")

#     ## microservice response
#     return return_request(response)
