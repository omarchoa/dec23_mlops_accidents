from datetime import datetime, timedelta, timezone
from typing import Union, Optional

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

import pandas as pd
import json
import random
import joblib

# ---------------------------- HTTP Exceptions --------------------------------
responses = {
    200: {"description": "OK"},
    401: {"description": "Identifiant ou mot de passe invalide(s)"}
}

# ---------------------------- Configuration pour les tokens ------------------
SECRET_KEY = "shield_secret"  # pour la signature des tokens
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# ---------------------------- Chargement base de données users ---------------
file = open("users.json", 'r')
users_db = json.load(file)


# ---------------------------- Partie provenant de la doc FastAPI -------------
# https://fastapi.tiangolo.com/tutorial/security/

# Define a Pydantic Model that will be used in the token endpoint for the response:
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None


class User(BaseModel):
    username: str
    password: str
    hashed_password: str
    rights: Optional[int] = 0
    # email: Union[str, None] = None
    # full_name: Union[str, None] = None
    disabled: Optional[bool] = False


class UserInDB(User):
    hashed_password: str


# Pour encoder les mots de passe:
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Envoie le token sur l'endpoint /token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# Create a utility function to hash a password coming from the user:
def get_password_hash(password):
    return pwd_context.hash(password)


# And another utility to verify if a received password matches the hash stored:
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


# And another one to authenticate and return a user.
def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


# Create a utility function to generate a new access token:
def create_access_token(data: dict,
                        expires_delta: Union[timedelta, None] = None):

    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# Update get_current_user to receive the same token as before,
# but this time, using JWT tokens.
# Decode the received token, verify it, and return the current user.
# If the token is invalid, return an HTTP error right away.
async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


# ---------------------------- API --------------------------------------------
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
         'description': 'Mises à jour du modèle et des données'},
        {'name': 'TOKENS',
         'description': 'Endpoint de vérification'}
        ])


# Create a timedelta with the expiration time of the token.
# Create a real JWT access token and return it
@api.post("/token", tags=['TOKENS'])
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends()
) -> Token:
    user = authenticate_user(users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


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


# ---------- 1. Vérification du fonctionnement de l’API: ----------------------


@api.get('/status', name="test de fonctionnement de l'API", tags=['GET'])
async def is_fonctionnal():
    """
    Vérifie que l'api fonctionne.
    """
    return {"L'api fonctionne."}


# ---------- 2. Inscription d'un utilisateur: ---------------------------------


@api.post('/register',
          name="Ajout d'un nouvel utilisateur",
          tags=['USERS'], responses=responses)
async def post_user(new_user: User, current_user: User = Depends(get_current_active_user)):
    """Fonction pour ajouter un nouvel utilisateur.
       Il faut être administrateur pour pouvoir ajouter un nouvel utilisateur.
       Identification: entrez votre identifiant et votre mot de passe
       au format identifiant:mot_de_passe
    """

    # Test d'autorisation:
    if current_user.rights == 1:

        # Hashage du mot de passe fourni lors de l'inscription:
        h = pwd_context.hash(new_user.password)

        # Enregistrement du nouvel utilisateur:
        users_db[new_user.username] = {
            "username": new_user.username,
            "password": new_user.password,
            "hashed_password": h,
            "rights": new_user.rights,
            "disabled": new_user.disabled
        }
        update_users_db = json.dumps(users_db, indent=4)
        with open("users.json", "w") as outfile:
            outfile.write(update_users_db)

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
async def remove_user(old_user: OldUser, current_user: User = Depends(get_current_active_user)):
    """Fonction pour supprimer un nouvel utilisateur.
       Il faut être administrateur pour pouvoir supprimer
       un nouvel utilisateur.
       Identification: entrez votre identifiant et votre mot de passe
       au format identifiant:mot_de_passe
    """

    # Test d'autorisation:
    if current_user.rights == 1:

        # Test d'identification:
        # if users_passwords_db[user][0] == psw:

        # Suppression de l'ancien utilisateur:
        try:
            users_db.pop(old_user.user)
            update_users_db = json.dumps(users_db, indent=4)
            with open("users.json", "w") as outfile:
                outfile.write(update_users_db)
        except KeyError:
            return "L'utilisateur spécifié n'existe pas."

    else:
        raise HTTPException(
                status_code=403,
                detail="Vous n'avez pas les droits d'administrateur.")


# ---------- 4. Prédictions de priorité à partir des données test: ------------

@api.get('/predict_from_test',
         name="Effectue une prediction à partir d'un échantillon test.",
         tags=['PREDICTIONS'],
         responses=responses)
async def get_pred_from_test(current_user: User = Depends(get_current_active_user)):
    """Fonction pour effectuer une prédiction à partir d'une donnée
        issue de l'échantillon de test.
        Identification: entrez votre identifiant et votre mot de passe
        au format identifiant:mot_de_passe
    """

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
async def post_pred_from_call(data: InputData, current_user: User = Depends(get_current_active_user)):
    """Fonction pour effectuer une prédiction à partir d'une saisie effectuée
       par un agent des FdO.
       Identification: entrez votre identifiant et votre mot de passe
       au format identifiant:mot_de_passe
    """

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

# ---------- 6. Entraîner le modèle avec de nouvelles données: ----------------


@api.get('/train',
         name='Entrainement du modèle',
         tags=['UPDATE'])
async def get_train(current_user: User = Depends(get_current_active_user)):
    """Fonction pour entrainer le modèle.
    """
    # Test d'autorisation:
    if current_user.rights == 1:
        return "Entrainement"
    else:
        raise HTTPException(
                status_code=403,
                detail="Vous n'avez pas les droits d'administrateur.")

# ---------- 7. Mise à jour de la base de données -----------------------------


@api.get('/update_data',
         name='Mise à jour des données accidents',
         tags=['UPDATE'])
async def get_update_data(current_user: User = Depends(get_current_active_user)):
    """Fonction pour mettre à jour les données accidents.
    """
    # Test d'autorisation:
    if current_user.rights == 1:
        return "Mise à jour données accidents"
    else:
        raise HTTPException(
                status_code=403,
                detail="Vous n'avez pas les droits d'administrateur.")
