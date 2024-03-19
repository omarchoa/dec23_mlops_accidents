# ---------------------------- Imports ----------------------------------------

# external
import datetime
from fastapi import FastAPI, Header, HTTPException
import pandas as pd
import joblib
import json
import os
from pathlib import Path
from pydantic import BaseModel
import random
from sklearn import ensemble
from sklearn.metrics import f1_score
import sys
import time
from typing import Optional
import numpy as np
import string

# internal
# add path to import datalib which is in src/data
# 3 folders upper of the current
root_path = Path(os.path.realpath(__file__)).parents[3]
sys.path.append(os.path.join(root_path, "src", "data"))
import datalib

# set commonly used paths as variables
path_data_preprocessed = os.path.join(root_path, "data", "preprocessed")
path_logs = os.path.join(root_path, "logs")

# ---------------------------- HTTP Exceptions --------------------------------
responses = {
    200: {"description": "OK"},
    401: {"description": "Identifiant ou mot de passe invalide(s)"}
}

# ---------------------------- Chargement base de données users ---------------
file_path = os.path.join(os.path.dirname(__file__), "users_db_bis.json")
with open(file_path, 'r') as file:
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
    description="API permettant l'utilisation de l'application SHIELD (Safety \
                 Hazard Identification and Emergency Law Deployment) utilisée \
                 par les forces de l'ordre pour prédire la priorité \
                 d'intervention en cas d'un accident de la route.",
    version="0.1",
    openapi_tags=[
        {'name': 'USERS',
         'description': 'Gestion des utilisateurs'},
        {'name': 'PREDICTIONS',
         'description': 'Prédictions faites par le modèle.'},
        {'name': 'UPDATE',
         'description': 'Mises à jour du modèle et des données'}
        ])

# ---------- 1. Vérification du fonctionnement de l’API: ----------------------


@api.get('/status', name="test de fonctionnement de l'API", tags=['GET'])
async def is_fonctionnal():
    """
    Vérifie que l'api fonctionne.
    """
    return {"L'api fonctionne."}

# ---------- 2. Inscription d'un utilisateur: ---------------------------------


class User(BaseModel):
    username: str
    password: str
    rights: Optional[int] = 0  # Droits par défaut: utilisateur fdo


@api.post('/register',
          name="Ajout d'un nouvel utilisateur",
          tags=['USERS'], responses=responses)
async def post_user(new_user: User, identification=Header(None)):
    """Fonction pour ajouter un nouvel utilisateur.
       Il faut être administrateur pour pouvoir ajouter un nouvel utilisateur.
       Identification: entrez votre identifiant et votre mot de passe
       au format identifiant:mot_de_passe
    """
    # Récupération des identifiants et mots de passe:
    user, psw = identification.split(":")

    # Test d'autorisation:
    if users_db[user]['rights'] == 1:

        # Test d'identification:
        if users_db[user]['password'] == psw:

            # Enregistrement du nouvel utilisateur:
            users_db[new_user.username] = {
                "username": new_user.username,
                "password": new_user.password,
                "rights": new_user.rights
            }
            update_users_db = json.dumps(users_db, indent=4)
            with open("users_db_bis.json", "w") as outfile:
                outfile.write(update_users_db)

            return {"Nouvel utilisateur ajouté!"}

        else:
            raise HTTPException(
                status_code=401,
                detail="Identifiant ou mot de passe invalide(s)")
    else:
        raise HTTPException(
                status_code=403,
                detail="Vous n'avez pas les droits d'administrateur.")


# ---------- 3. Suppresion d'un utilisateur: ----------------------------------


class OldUser(BaseModel):
    user: str


@api.delete('/remove_user',
            name="Suppression d'un utilisateur existant.",
            tags=['USERS'], responses=responses)
async def remove_user(old_user: OldUser, identification=Header(None)):
    """Fonction pour supprimer un nouvel utilisateur.
       Il faut être administrateur pour pouvoir supprimer un nouvel utilisateur.
       Identification: entrez votre identifiant et votre mot de passe
       au format identifiant:mot_de_passe
    """
    # Récupération des identifiants et mots de passe:
    user, psw = identification.split(":")

    # Test d'autorisation:
    if users_db[user]['rights'] == 1:

        # Test d'identification:
        if users_db[user]['password'] == psw:

            # Suppression de l'ancien utilisateur:
            try:
                users_db.pop(old_user.user)
                update_users_db = json.dumps(users_db, indent=4)
                with open("users_db_bis.json", "w") as outfile:
                    outfile.write(update_users_db)
                return {"Utilisateur supprimé!"}

            except KeyError:
                return "L'utilisateur spécifié n'existe pas."

        else:
            raise HTTPException(
                status_code=401,
                detail="Identifiant ou mot de passe invalide(s)")
    else:
        raise HTTPException(
                status_code=403,
                detail="Vous n'avez pas les droits d'administrateur.")


# ---------- 4. Prédictions de priorité à partir des données test: ------------

@api.get('/predict_from_test',
         name="Effectue une prediction à partir d'un échantillon test.",
         tags=['PREDICTIONS'],
         responses=responses)
async def get_pred_from_test(identification=Header(None)):
    """Fonction pour effectuer une prédiction à partir d'une donnée
        issue de l'échantillon de test.
        Identification: entrez votre identifiant et votre mot de passe
        au format identifiant:mot_de_passe
    """
    # Récupération des identifiants et mots de passe:
    user, psw = identification.split(":")

    # Test d'identification:
    if users_db[user]['password'] == psw:

        # Chargement du modèle:
        rdf = joblib.load("../../models/trained_model.joblib")

        # Chargement des données test:
        path_X_test = os.path.join(path_data_preprocessed, "X_test.csv")
        path_y_test = os.path.join(path_data_preprocessed, "y_test.csv")
        X_test = pd.read_csv(path_X_test)
        y_test = pd.read_csv(path_y_test)

        # Prédiction d'une donnée aléatoire:
        i = random.choice(X_test.index)
        pred_time_start = time.time()
        pred = rdf.predict(X_test.iloc[[i]])
        pred_time_end = time.time()

        # Prédiction générale de y
        y_pred = rdf.predict(X_test)
        y_true = y_test

        # Calcul du F1 score macro average
        f1_score_macro_average = f1_score(y_true=y_true,
                                          y_pred=y_pred,
                                          average="macro")

        # Préparation des métadonnées pour exportation
        metadata_dictionary = {
            "request_id": "".join(random.choices(string.digits, k=16)),
            "time_stamp": str(datetime.datetime.now()),
            "user_name": user,
            "response_status_code": 200,
            "input_features": X_test.iloc[[i]].to_dict(orient="records")[0],
            "output_prediction": int(pred[0]),
            "verified_prediction": None,
            "f1_score_macro_average": f1_score_macro_average,
            "prediction_time": pred_time_end - pred_time_start
            }
        metadata_json = json.dumps(obj=metadata_dictionary)

        # Exportation des métadonnées
        path_log_file = os.path.join(path_logs, "pred_test.jsonl")
        with open(path_log_file, "a") as file:
            file.write(metadata_json + "\n")

        # Réponse:
        priority = pred[0]
        if priority == 1:
            return "L'intervention est prioritaire."
        else:
            return "L'intervention n'est pas prioritaire."

    else:
        raise HTTPException(
            status_code=401,
            detail="Identifiant ou mot de passe invalide(s)"
        )

# ---------- 5. Prédictions de priorité à partir de données saisies: ----------


class InputData(BaseModel):
    place: Optional[int] = 10
    catu: Optional[int] = 3
    sexe: Optional[int] = 1
    secu1: Optional[float] = 0.0
    year_acc: Optional[int] = 2021
    victim_age: Optional[int] = 60
    catv: Optional[int] = 2
    obsm: Optional[int] = 1
    motor: Optional[int] = 1
    catr: Optional[int] = 3
    circ: Optional[int] = 2
    surf: Optional[int] = 1
    situ: Optional[int] = 1
    vma: Optional[int] = 50
    jour: Optional[int] = 7
    mois: Optional[int] = 12
    lum: Optional[int] = 5
    dep: Optional[int] = 77
    com: Optional[int] = 77317
    agg_: Optional[int] = 2

# variable d'origine 'int' renommée ici en 'inter' (pour 'intersection')
# pour éviter les conflits avec le type 'int'.
    inter: Optional[int] = 1
    atm: Optional[int] = 0
    col: Optional[int] = 6
    lat: Optional[float] = 48.60
    long: Optional[float] = 2.89
    hour: Optional[int] = 17
    nb_victim: Optional[int] = 2
    nb_vehicules: Optional[int] = 1


@api.post('/predict_from_call',
          name="Effectue une prediction à partir de saisie opérateur.",
          tags=['PREDICTIONS'],
          responses=responses)
async def post_pred_from_call(data: InputData, identification=Header(None)):
    """Fonction pour effectuer une prédiction à partir d'une saisie effectuée
       par un agent des FdO.
       Identification: entrez votre identifiant et votre mot de passe
       au format identifiant:mot_de_passe
    """
    # Récupération des identifiants et mots de passe:
    user, psw = identification.split(":")

    # Test d'identification:
    if users_db[user]['password'] == psw:

        # Chargement du modèle:
        rdf = joblib.load("../../models/trained_model.joblib")

        # Chargement des données test:
        test = pd.DataFrame.from_dict(dict(data), orient='index').T
        test.rename(columns={"inter": "int"}, inplace=True)

        # Prédiction :
        pred = rdf.predict(test)

        # Réponse:
        priority = pred[0]
        if priority == 1:
            return "L'intervention est prioritaire."
        else:
            return "L'intervention n'est pas prioritaire."

    else:
        raise HTTPException(
            status_code=401,
            detail="Identifiant ou mot de passe invalide(s)"
        )


# ---------- 6. Entraîner le modèle avec de nouvelles données: ----------------


@api.get('/train',
         name='Entrainement du modèle',
         tags=['UPDATE'])
async def get_train(identification=Header(None)):
    """Fonction pour entrainer le modèle.
    """
# Récupération des identifiants et mots de passe:
    user, psw = identification.split(":")

    # Test d'autorisation:
    if users_db[user]['rights'] == 1:

        # Test d'identification:
        if users_db[user]['password'] == psw:

            # Chargement des données:
            path_X_train = os.path.join(path_data_preprocessed, "X_train.csv")
            path_y_train = os.path.join(path_data_preprocessed, "y_train.csv")
            X_train = pd.read_csv(path_X_train)
            y_train = pd.read_csv(path_y_train)
            y_train = np.ravel(y_train)

            rf_classifier = ensemble.RandomForestClassifier(n_jobs=-1)

            # Entrainement du modèle:
            train_time_start = time.time()
            rf_classifier.fit(X_train, y_train)
            train_time_end = time.time()

            # Préparation des métadonnées pour exportation
            metadata_dictionary = {
                "request_id": "".join(random.choices(string.digits, k=16)),
                "time_stamp": str(datetime.datetime.now()),
                "user_name": user,
                "response_status_code": 200,
                "estimator_type": str(type(rf_classifier)),
                "estimator_parameters": rf_classifier.get_params(),
                "feature_importances": dict(zip(X_train.columns.to_list(),
                                                list(rf_classifier.feature_importances_))),
                "train_time": train_time_end - train_time_start
                }
            metadata_json = json.dumps(obj=metadata_dictionary)

            # Exportation des métadonnées
            path_log_file = os.path.join(path_logs, "train.jsonl")
            with open(path_log_file, "a") as file:
                file.write(metadata_json + "\n")

            # Sauvegarde du modèle:
            # Sauvegarde dans new_trained_model.joblib dans un premier temps
            # TODO: Versioning du modèle
            model_filename = '../../models/new_trained_model.joblib'
            joblib.dump(rf_classifier, model_filename)
            return {"Modèle ré-entrainé et sauvegardé!"}

        else:
            raise HTTPException(
                status_code=401,
                detail="Identifiant ou mot de passe invalide(s)")
    else:
        raise HTTPException(
                status_code=403,
                detail="Vous n'avez pas les droits d'administrateur.")

# ---------- 7. Mise à jour de la base de données -----------------------------


class UpdateData(BaseModel):
    start_year: int
    end_year: int


@api.post('/update_data', name='Mise à jour des données accidents', tags=['UPDATE'])
async def update_data(update_data: UpdateData, identification=Header(None)):
    """Fonction pour mettre à jour les données accidents.
    """
    # Récupération des identifiants et mots de passe:
    user, psw = identification.split(":")

    # Test d'autorisation:
    if users_db[user]['rights'] == 1:

        # Test d'identification:
        if users_db[user]['password'] == psw:
            # download, clean and preprocess data => X_train.csv, X_test.csv, y_train.csv, y_test.csv files
            exec_time_start = time.time()
            data = datalib.Data(update_data.start_year, update_data.end_year, root_path)
            exec_time_end = time.time()

            # Préparation des métadonnées pour exportation
            metadata_dictionary = {
                "request_id": "".join(random.choices(string.digits, k=16)),
                "time_stamp": str(datetime.datetime.now()),
                "user_name": user,
                "response_status_code": 200,
                "start_year": update_data.start_year,
                "end_year": update_data.end_year,
                "execution_time": exec_time_end - exec_time_start
                }
            metadata_json = json.dumps(obj=metadata_dictionary)

            # Exportation des métadonnées
            path_log_file = os.path.join(path_logs, "update_data.jsonl")
            with open(path_log_file, "a") as file:
                file.write(metadata_json + "\n")

        else:
            raise HTTPException(
                status_code=401,
                detail="Identifiant ou mot de passe invalide(s)")
    else:
        raise HTTPException(
                status_code=403,
                detail="Vous n'avez pas les droits d'administrateur.")

# -------- 8. Labellisation d'une prédiction enregistrée --------


class Prediction(BaseModel):
    """Modèle pour la labellisation d'une prédiction enregistrée"""

    request_id: int
    """Référence de la prédiction"""

    y_true: int
    """Label de la prédiction"""


@api.post('/label', name="Labellisation d'une prédiction enregistrée", tags=['PREDICTIONS'])
async def post_label(prediction: Prediction, identification=Header(None)):
    """Fonction qui labellise une prédiction enregistrée à partir du retour utilisateur

    Paramètres :
        prediction (class Prediction)
        identification (str) : identifiants utilisateur selon le format nom_d_utilisateur:mot_de_passe

    Lève :
        HTTPException401 : identifiants non valables
        HTTPException404 : enregistrement non existant

    Retourne :
        str : confirmation de la mise à jour de l'enregistrement
    """
    # Récupération des identifiants
    user, psw = identification.split(":")

    # Test d'identification
    if users_db[user]['password'] == psw:

        ## Chargement de la base de données de prédictions
        path_db_predictions = os.path.join(path_logs, "pred_test.jsonl") ### TODO Remplacer "pred_test.jsonl" par "pred_call.jsonl" une fois ce dernier prêt
        with open(path_db_predictions, "r") as file:
            db_predictions = [json.loads(line) for line in file]

        ## Extraction de l'enregistrement correspondant au request_id reçu
        record_exists = "no"
        record_to_update = {}
        for record in db_predictions:
            if int(record["request_id"]) == prediction.request_id:
                record_exists = "yes"
                record_to_update = record

                ## Mise à jour du champ verified_prediction avec la valeur de y_true
                record_to_update["verified_prediction"] = prediction.y_true

                ## Mise à jour de la base de données de prédictions
                metadata_json = json.dumps(obj=record_to_update)
                path_db_predictions = os.path.join(path_logs, "feedback.jsonl") ### TODO Remplacer "feedback.jsonl" par "pred_call.jsonl" une fois ce dernier prêt, et en écrasant l'enregistrement concerné
                with open(path_db_predictions, "a") as file:
                    file.write(metadata_json + "\n")

        if record_exists == "yes":
            return {"Enregistrement mis à jour. Merci pour votre retour."}
        else:
            raise HTTPException(status_code=404, detail="Aucun enregistrement trouvé. Merci de fournir une référence (request_id) valable.")

    else:
        raise HTTPException(status_code=401, detail="Identifiants non valables.")
