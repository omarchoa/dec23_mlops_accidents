# >>>>>>>> IMPORTS <<<<<<<<


import json
import os

import requests
from fastapi import FastAPI, Header, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel


# >>>>>>>> CLASS DECLARATIONS <<<<<<<<


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


# >>>>>>>> USER DATABASE <<<<<<<<
## delete once connection to mariadb database in users microservice is implemented


## path_users_db = os.path.join("src", "docker", "bdd", "users_db_bis.json")  ### for local debugging
path_users_db = os.path.join(
    "home", "shield", "users", "users_db_bis.json"
)  ### for container deployment
with open(path_users_db, "r") as file:
    users_db = json.load(file)


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
    return JSONResponse(response)


# ---------- Inscription d'un utilisateur: ---------------------------------


# class User(BaseModel):
#     username: str
#     password: str
#     rights: Optional[int] = 0  # Droits par défaut: utilisateur fdo


# @api.post('/register',
#           name="Ajout d'un nouvel utilisateur",
#           tags=['USERS'], responses=responses)
# async def post_user(new_user: User, identification=Header(None)):
#     """Fonction pour ajouter un nouvel utilisateur.
#        Il faut être administrateur pour pouvoir ajouter un nouvel utilisateur.
#        Identification: entrez votre identifiant et votre mot de passe
#        au format identifiant:mot_de_passe
#     """
#     # Récupération des identifiants et mots de passe:
#     user, psw = identification.split(":")

#     # Test d'autorisation:
#     if users_db[user]['rights'] == 1:

#         # Test d'identification:
#         if users_db[user]['password'] == psw:

#             # Enregistrement du nouvel utilisateur:
#             users_db[new_user.username] = {
#                 "username": new_user.username,
#                 "password": new_user.password,
#                 "rights": new_user.rights
#             }
#             update_users_db = json.dumps(users_db, indent=4)
#             with open(path_users_db, "w") as outfile:
#                 outfile.write(update_users_db)

#             return {"Nouvel utilisateur ajouté!"}

#         else:
#             raise HTTPException(
#                 status_code=401,
#                 detail="Identifiant ou mot de passe invalide(s)")
#     else:
#         raise HTTPException(
#                 status_code=403,
#                 detail="Vous n'avez pas les droits d'administrateur.")


# ---------- Suppresion d'un utilisateur: ----------------------------------


# class OldUser(BaseModel):
#     user: str


# @api.delete('/remove_user',
#             name="Suppression d'un utilisateur existant.",
#             tags=['USERS'], responses=responses)
# async def remove_user(old_user: OldUser, identification=Header(None)):
#     """Fonction pour supprimer un nouvel utilisateur.
#        Il faut être administrateur pour pouvoir supprimer un nouvel utilisateur.
#        Identification: entrez votre identifiant et votre mot de passe
#        au format identifiant:mot_de_passe
#     """
#     # Récupération des identifiants et mots de passe:
#     user, psw = identification.split(":")

#     # Test d'autorisation:
#     if users_db[user]['rights'] == 1:

#         # Test d'identification:
#         if users_db[user]['password'] == psw:

#             # Suppression de l'ancien utilisateur:
#             try:
#                 users_db.pop(old_user.user)
#                 update_users_db = json.dumps(users_db, indent=4)
#                 with open(path_users_db, "w") as outfile:
#                     outfile.write(update_users_db)
#                 return {"Utilisateur supprimé!"}

#             except KeyError:
#                 return "L'utilisateur spécifié n'existe pas."

#         else:
#             raise HTTPException(
#                 status_code=401,
#                 detail="Identifiant ou mot de passe invalide(s)")
#     else:
#         raise HTTPException(
#                 status_code=403,
#                 detail="Vous n'avez pas les droits d'administrateur.")


# >>>>>>>> MICROSERVICES - DATA <<<<<<<<


@api.get(
    path="/data/status",
    tags=["MICROSERVICES - Data"],
    name="check data microservice API status",
)
async def data_status():
    response = requests.get(url="http://data:8003/status")
    if response.status_code == 200:  ### 200: success
        response_clean = str(response.content)[3:-2]  ### strip unnecessary characters
        return JSONResponse(content=response_clean)
    else:
        raise HTTPException(status_code=400, detail="Bad request.")


@api.post(path="/data/update", tags=["MICROSERVICES - Data"], name="update data")
async def data_update(year_range: YearRange, identification=Header(None)):

    ## auth challenge check
    username, password = identification.split(":")
    if users_db[username]["rights"] == 1:  ### 1: admin
        if users_db[username]["password"] == password:

            ## microservice call
            params = {
                "start_year": year_range.start_year,
                "end_year": year_range.end_year,
            }
            response = requests.post(url="http://data:8003/update", json=params)

            ## microservice response
            if response.status_code == 200:  ### 200: success
                response_clean = str(response.content)[
                    3:-2
                ]  ### strip unnecessary characters
                return JSONResponse(content=response_clean)
            else:
                raise HTTPException(status_code=400, detail="Bad request.")

        ## auth challenge failure
        else:
            raise HTTPException(status_code=401, detail="Invalid credentials.")
    else:
        raise HTTPException(
            status_code=403, detail="Administrator privileges required."
        )


# >>>>>>>> MICROSERVICES - TRAINING <<<<<<<<


@api.get(
    path="/training/status",
    tags=["MICROSERVICES - Training"],
    name="check training microservice API status",
)
async def training_status():
    response = requests.get(url="http://training:8004/status")
    if response.status_code == 200:  ### 200: success
        response_clean = str(response.content)[3:-2]  ### strip unnecessary characters
        return JSONResponse(content=response_clean)
    else:
        raise HTTPException(status_code=400, detail="Bad request.")


@api.get(path="/training/train", tags=["MICROSERVICES - Training"], name="train model")
async def training_train(identification=Header(None)):

    ## auth challenge check
    username, password = identification.split(":")
    if users_db[username]["rights"] == 1:  ### 1: admin
        if users_db[username]["password"] == password:

            ## microservice call
            response = requests.get(url="http://training:8004/train")

            ## microservice response
            if response.status_code == 200:  ### 200: success
                response_clean = str(response.content)[
                    3:-2
                ]  ### strip unnecessary characters
                return JSONResponse(content=response_clean)
            else:
                raise HTTPException(status_code=400, detail="Bad request.")

        ## auth challenge failure
        else:
            raise HTTPException(status_code=401, detail="Invalid credentials.")
    else:
        raise HTTPException(
            status_code=403, detail="Administrator privileges required."
        )


# >>>>>>>> MICROSERVICES - PREDICTION <<<<<<<<


@api.get(
    path="/prediction/status",
    tags=["MICROSERVICES - Prediction"],
    name="check prediction microservice API status",
)
async def prediction_status():
    response = requests.get(url="http://prediction:8005/status")
    if response.status_code == 200:  ### 200: success
        response_clean = str(response.content)[3:-2]  ### strip unnecessary characters
        return JSONResponse(content=response_clean)
    else:
        raise HTTPException(status_code=400, detail="Bad request.")


@api.get(
    path="/prediction/test",
    tags=["MICROSERVICES - Prediction"],
    name="predict from test",
)
async def prediction_test(identification=Header(None)):

    ## auth challenge check
    username, password = identification.split(":")
    if users_db[username]["password"] == password:

        ## microservice call
        response = requests.get(url="http://prediction:8005/test")

        ## microservice response
        if response.status_code == 200:  ### 200: success
            response_clean = str(response.content)[
                3:-2
            ]  ### strip unnecessary characters
            return JSONResponse(content=response_clean)
        else:
            raise HTTPException(status_code=400, detail="Bad request.")

    ## auth challenge failure
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials.")


@api.post(
    path="/prediction/call",
    tags=["MICROSERVICES - Prediction"],
    name="predict from call",
)
async def prediction_call(input_data: InputDataPredCall, identification=Header(None)):

    ## auth challenge check
    username, password = identification.split(":")
    if users_db[username]["password"] == password:

        ## microservice call
        payload = input_data.model_dump()
        response = requests.post(url="http://prediction:8005/call", json=payload)

        ## microservice response
        if response.status_code == 200:  ### 200: success
            response_clean = str(response.content)[
                3:-2
            ]  ### strip unnecessary characters
            return JSONResponse(content=response_clean)
        else:
            raise HTTPException(status_code=400, detail="Bad request.")

    ## auth challenge failure
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials.")


# >>>>>>>> MICROSERVICES - SCORING <<<<<<<<


@api.get(
    path="/scoring/status",
    tags=["MICROSERVICES - Scoring"],
    name="check scoring microservice API status",
)
async def scoring_status():
    response = requests.get(url="http://scoring:8006/status")
    if response.status_code == 200:  ### 200: success
        response_clean = str(response.content)[3:-2]  ### strip unnecessary characters
        return JSONResponse(content=response_clean)
    else:
        raise HTTPException(status_code=400, detail="Bad request.")


@api.post(
    path="/scoring/label_prediction",
    tags=["MICROSERVICES - Scoring"],
    name="label prediction",
)
async def scoring_label_prediction(
    input_data: InputDataLabelPred, identification=Header(None)
):

    ## auth challenge check
    username, password = identification.split(":")
    if users_db[username]["password"] == password:

        ## microservice call
        payload = input_data.model_dump()
        response = requests.post(
            url="http://scoring:8006/label_prediction", json=payload
        )

        ## microservice response
        response_clean = str(response.content)[3:-2]  ### strip unnecessary characters
        if "updated" in response_clean:
            return JSONResponse(content=response_clean)
        elif "not found" in response_clean:
            raise HTTPException(status_code=404, detail=response_clean)
        else:
            raise HTTPException(status_code=400, detail="Bad request.")

    ## auth challenge failure
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials.")


@api.get(
    path="/scoring/update_f1_score",
    tags=["MICROSERVICES - Scoring"],
    name="update f1 score",
)
async def scoring_update_f1_score(identification=Header(None)):

    ## auth challenge check
    username, password = identification.split(":")
    if users_db[username]["rights"] == 1:  ### 1: admin
        if users_db[username]["password"] == password:

            ## microservice call
            response = requests.get(url="http://scoring:8006/update_f1_score")

            ## microservice response
            if response.status_code == 200:  ### 200: success
                response_clean = str(response.content)[
                    3:-2
                ]  ### strip unnecessary characters
                return JSONResponse(content=response_clean)
            else:
                raise HTTPException(status_code=400, detail="Bad request.")

        ## auth challenge failure
        else:
            raise HTTPException(status_code=401, detail="Invalid credentials.")
    else:
        raise HTTPException(
            status_code=403, detail="Administrator privileges required."
        )
