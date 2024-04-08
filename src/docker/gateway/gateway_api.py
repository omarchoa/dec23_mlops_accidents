# ---------------------------- Imports ----------------------------------------

# external
# import datetime
from fastapi import FastAPI, Header, HTTPException
from fastapi.responses import JSONResponse
# import pandas as pd
# import joblib
import json
import os
# from pathlib import Path
from pydantic import BaseModel
# import random
import requests
# from sklearn import ensemble
# from sklearn.metrics import f1_score
import socket
# import sys
# import time
# from typing import Optional
# import numpy as np
# import string


# define input data model for endpoint /predict_from_call
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


# define input data model for endpoint /label_prediction
class InputDataLabelPred(BaseModel):
    request_id: int = 6012919476848551
    y_true: int = 1


# internal
# add path to import datalib which is in src/data
# 3 folders upper of the current
# root_path = Path(os.path.realpath(__file__)).parents[3]
# sys.path.append(os.path.join(root_path, "src", "data"))
# import datalib

# set commonly used paths as variables
# path_data_preprocessed = os.path.join(root_path, "data", "preprocessed")
# path_X_train = os.path.join(path_data_preprocessed, "X_train.csv")
# path_y_train = os.path.join(path_data_preprocessed, "y_train.csv")
# path_X_test = os.path.join(path_data_preprocessed, "X_test.csv")
# path_y_test = os.path.join(path_data_preprocessed, "y_test.csv")
# path_logs = os.path.join(root_path, "logs")
# path_db_preds_unlabeled = os.path.join(path_logs, "preds_call.jsonl")
# path_db_preds_labeled = os.path.join(path_logs, "preds_labeled.jsonl")
# path_trained_model = os.path.join(root_path, "src", "models", "trained_model.joblib")
# path_new_trained_model = os.path.join(root_path, "src", "models", "new_trained_model.joblib")
path_users_db = os.path.join("home", "shield", "users", "users_db_bis.json")

# ---------------------------- HTTP Exceptions --------------------------------
# responses = {
#     200: {"description": "OK"},
#     401: {"description": "Identifiant ou mot de passe invalide(s)"}
# }

# ---------------------------- Load users database-----------------------------
# with open(path_users_db, 'r') as file:
#     users_db = json.load(file)
with open(path_users_db, 'r') as file:
    users_db = json.load(file)

# ---------------------------- API --------------------------------------------

# DONE 1. / : vérification du fonctionnement de l’API
# DONE 2. /register : inscription de l’utilisateur.
# DONE 3. /remove_user : suppression d'un utilisateur.
#    /login : identification de l’utilisateur.
#             -> inutile? cela se fait via la requête non?
# DONE 4. /predict_from_test : prédiction de la priorité de l'intervention
# à partir d'échantillon issu de X_test
# DONE 5. /predict_from_call : prédiction de la priorité de l'intervention
# à partir d'entrée manuelle
# 6. /train : entraîner le modèle avec de nouvelles données.
# 7. /update_data : mettre à jour la base de données avec de nouvelles données
#                   sur les accidents.


api = FastAPI(
    title="🛡️ SHIELD",
    description="API using the SHIELD application (Safety \
                 Hazard Identification and Emergency Law Deployment) used  \
                 by the police to predict the priority of intervention\
                 in the event of a road accident.",
    version="0.1",
    openapi_tags=[
        {'name': 'USERS', 'description': 'Users management.'},
        {'name': 'UPDATE', 'description': 'Update data'}
    ]
)

# ---------- 1. Vérification du fonctionnement de l’API: ----------------------


@api.get('/status', name="Check whether the gateway API is running", tags=['GET'])
async def is_fonctionnal():
    """
    Check whether the gateway API is running
    """
    return {"The gateway API is running"}

# ---------- 2. Inscription d'un utilisateur: ---------------------------------


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


# ---------- 3. Suppresion d'un utilisateur: ----------------------------------


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


# >>>>>>>> MICROSERVICE: TRAINING <<<<<<<<


@api.get(path="/train", tags=["TRAINING"], name="train")
async def train(identification=Header(None)):

    ## auth challenge check
    username, password = identification.split(":")
    if users_db[username]["rights"] == 1: ### 1: admin
        if users_db[username]["password"] == password:

            ## microservice call
            response = requests.get(url="http://training:8004/train")

            ## microservice response
            if response.status_code == 200: ### 200: success
                response_clean = str(response.content)[3:-2] ### strip unnecessary characters
                return JSONResponse(response_clean)
            else:
                raise HTTPException(
                    status_code=400,
                    detail="Bad request."
                )

    ## auth challenge failure
        else:
            raise HTTPException(
                status_code=401,
                detail="Invalid credentials."
                )
    else:
        raise HTTPException(
                status_code=403,
                detail="Administrator privileges required."
                )


# >>>>>>>> MICROSERVICE: PREDICTION <<<<<<<<


@api.get(path="/predict_from_test", tags=["PREDICTION"], name="predict from test")
async def predict_from_test(identification=Header(None)):

    ## auth challenge check
    username, password = identification.split(":")
    if users_db[username]["password"] == password:

        ## microservice call
        response = requests.get(url="http://prediction:8005/predict_from_test")

        ## microservice response
        if response.status_code == 200: ### 200: success
            response_clean = str(response.content)[3:-2] ### strip unnecessary characters
            return JSONResponse(response_clean)
        else:
            raise HTTPException(
                status_code=400,
                detail="Bad request."
            )

    ## auth challenge failure
    else:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials."
            )


@api.post(path="/predict_from_call", tags=["PREDICTION"], name="predict from call")
async def predict_from_call(input_data: InputDataPredCall, identification=Header(None)):

    ## auth challenge check
    username, password = identification.split(":")
    if users_db[username]["password"] == password:

        ## microservice call
        payload = input_data.model_dump()
        response = requests.post(url="http://prediction:8005/predict_from_call", json=payload)

        ## microservice response
        if response.status_code == 200: ### 200: success
            response_clean = str(response.content)[3:-2] ### strip unnecessary characters
            return JSONResponse(response_clean)
        else:
            raise HTTPException(
                status_code=400,
                detail="Bad request."
            )

    ## auth challenge failure
    else:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials."
            )


# >>>>>>>> MICROSERVICE: SCORING <<<<<<<<


@api.post(path="/label_prediction", tags=["SCORING"], name="label prediction")
async def label_prediction(input_data: InputDataLabelPred, identification=Header(None)):

    ## auth challenge check
    username, password = identification.split(":")
    if users_db[username]["password"] == password:

        ## microservice call
        payload = input_data.model_dump()
        response = requests.post(url="http://scoring:8006/label_prediction", json=payload)

        ## microservice response
        response_clean = str(response.content)[3:-2] ### strip unnecessary characters
        if "updated" in response_clean:
            return JSONResponse(response_clean)
        elif "not found" in response_clean:
            raise HTTPException(
                status_code=404,
                detail=response_clean
            )
        else:
            raise HTTPException(
                status_code=400,
                detail="Bad request."
            )

    ## auth challenge failure
    else:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials."
            )


@api.get(path="/update_f1_score", tags=["SCORING"], name="update f1 score")
async def update_f1_score(identification=Header(None)):

    ## auth challenge check
    username, password = identification.split(":")
    if users_db[username]["rights"] == 1: ### 1: admin
        if users_db[username]["password"] == password:

            ## microservice call
            response = requests.get(url="http://scoring:8006/update_f1_score")

            ## microservice response
            if response.status_code == 200: ### 200: success
                response_clean = str(response.content)[3:-2] ### strip unnecessary characters
                return JSONResponse(response_clean)
            else:
                raise HTTPException(
                    status_code=400,
                    detail="Bad request."
                )

    ## auth challenge failure
        else:
            raise HTTPException(
                status_code=401,
                detail="Invalid credentials."
                )
    else:
        raise HTTPException(
                status_code=403,
                detail="Administrator privileges required."
                )


# ---------- 7. Mise à jour de la base de données -----------------------------
@api.get('/data_api_status', name="check data API status", tags=['GET'])
async def requests_test():
    response = requests.get(url='http://data_container:8000/status')
    if response.status_code == 200:
        return {response.text}
    else:
        return {"url unknown"}


class YearRange(BaseModel):
    start_year: int  # admin shall use valid year e.g 2021
    end_year: int    # admin shall use valid year e.g 2021


@api.post('/update_data', name='Update accident data', tags=['UPDATE'])
async def update_data(year_range: YearRange, identification=Header(None)):
    user, pwd = identification.split(":")
    if users_db[user]['rights'] == 1:
        if users_db[user]['password'] == pwd:
            params = {
                "start_year": year_range.start_year,
                "end_year": year_range.end_year
            }
            response = requests.post(url='http://data_container:8000/update_data', json=params)
            if response.status_code == 200:
                return {"Data updated"}
            else:
                return {"Request in error"}
        else:
            raise HTTPException(
                status_code=401,
                detail="Invalid login or password.")
    else:
        raise HTTPException(
                status_code=403,
                detail="You do not have administrator rights.")


# @api.post('/update_data', name='Mise à jour des données accidents', tags=['UPDATE'])
# async def update_data(update_data: UpdateData, identification=Header(None)):
#     """Fonction pour mettre à jour les données accidents.
#     """
#     # Récupération des identifiants et mots de passe:
#     user, psw = identification.split(":")

#     # Test d'autorisation:
#     if users_db[user]['rights'] == 1:

#         # Test d'identification:
#         if users_db[user]['password'] == psw:
#             # download, clean and preprocess data => X_train.csv, X_test.csv, y_train.csv, y_test.csv files
#             exec_time_start = time.time()
#             data = datalib.Data(update_data.start_year, update_data.end_year, root_path)
#             exec_time_end = time.time()

#             # Préparation des métadonnées pour exportation
#             metadata_dictionary = {
#                 "request_id": "".join(random.choices(string.digits, k=16)),
#                 "time_stamp": str(datetime.datetime.now()),
#                 "user_name": user,
#                 "response_status_code": 200,
#                 "start_year": update_data.start_year,
#                 "end_year": update_data.end_year,
#                 "execution_time": exec_time_end - exec_time_start
#                 }
#             metadata_json = json.dumps(obj=metadata_dictionary)

#             # Exportation des métadonnées
#             path_log_file = os.path.join(path_logs, "update_data.jsonl")
#             with open(path_log_file, "a") as file:
#                 file.write(metadata_json + "\n")

#         else:
#             raise HTTPException(
#                 status_code=401,
#                 detail="Identifiant ou mot de passe invalide(s)")
#     else:
#         raise HTTPException(
#                 status_code=403,
#                 detail="Vous n'avez pas les droits d'administrateur.")