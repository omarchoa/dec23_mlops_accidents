# ---------------------------- Imports ----------------------------------------
from fastapi import FastAPI, Header, HTTPException
import pandas as pd
import json
import random
import joblib

from typing import Optional
from pydantic import BaseModel

# ---------------------------- HTTP Exceptions --------------------------------
responses = {
    200: {"description": "OK"},
    401: {"description": "Identifiant ou mot de passe invalide(s)"}
}
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


@api.get('/', name="test de fonctionnement de l'API", tags=['GET'])
async def is_fonctionnal():
    """
    Vérifie que l'api fonctionne.
    """
    return {"L'api fonctionne."}

# ---------- 2. Inscription d'un utilisateur: ---------------------------------


class NewUser(BaseModel):
    user: str
    psw: str
    rights: Optional[int] = 0  # Droits par défaut: utilisateur fdo


users_db = open("users_db.json", 'r')
users_passwords_db = json.load(users_db)


@api.post('/register',
          name="Ajout d'un nouvel utilisateur",
          tags=['USERS'], responses=responses)
async def post_user(new_user: NewUser, identification=Header(None)):
    """Fonction pour ajouter un nouvel utilisateur.
       Il faut être administrateur pour pouvoir ajouter un nouvel utilisateur.
       Identification: entrez votre identifiant et votre mot de passe
       au format identifiant:mot_de_passe
    """
    # Récupération des identifiants et mots de passe:
    user, psw = identification.split(":")

    # Test d'autorisation:
    if users_passwords_db[user][1] == 1:

        # Test d'identification:
        if users_passwords_db[user][0] == psw:

            # Enregistrement du nouvel utilisateur:
            users_passwords_db[new_user.user] = [new_user.psw, new_user.rights]
            users_db = json.dumps(users_passwords_db)
            with open("users_db.json", "w") as outfile:
                outfile.write(users_db)
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


users_db = open("users_db.json", 'r')
users_passwords_db = json.load(users_db)


@api.delete('/remove_user',
            name="Suppression d'un utilisateur existant.",
            tags=['USERS'], responses=responses)
async def remove_user(old_user: OldUser, identification=Header(None)):
    """Fonction pour ajouter un nouvel utilisateur.
       Il faut être administrateur pour pouvoir ajouter un nouvel utilisateur.
       Identification: entrez votre identifiant et votre mot de passe
       au format identifiant:mot_de_passe
    """
    # Récupération des identifiants et mots de passe:
    user, psw = identification.split(":")

    # Test d'autorisation:
    if users_passwords_db[user][1] == 1:

        # Test d'identification:
        if users_passwords_db[user][0] == psw:

            # Suppression de l'ancien utilisateur:
            try:
                users_passwords_db.pop(old_user.user)
                users_db = json.dumps(users_passwords_db)
                with open("users_db.json", "w") as outfile:
                    outfile.write(users_db)
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
    if users_passwords_db[user][0] == psw:

        # Chargement du modèle:
        rdf = joblib.load("../../models/trained_model.joblib")

        # Chargement des données test:
        X_test = pd.read_csv("../../../data/preprocessed/X_test.csv")

        # Prédiction d'une donnée aléatoire:
        i = random.choice(X_test.index)
        pred = rdf.predict(X_test.iloc[[i]])

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
    if users_passwords_db[user][0] == psw:

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
async def get_train():
    """Fonction pour entrainer le modèle.
    """

# ---------- 7. Mise à jour de la base de données -----------------------------


@api.get('/update_data',
         name='Mise à jour des données accidents',
         tags=['UPDATE'])
async def get_update_data():
    """Fonction pour mettre à jour les données accidents.
    """
