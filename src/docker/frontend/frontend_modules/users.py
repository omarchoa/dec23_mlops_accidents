# imports
import pandas as pd
import requests
import streamlit as st

# get all users from `database` microservice via `users` microservice and api gateway
response = requests.get(url="http://gateway:8001/users/all")
users_db = response.json()


# define authenticate function
def authenticate(username, password):
    if username in users_db and users_db[username]["pwd"] == password:
        return True
    else:
        return False


# define authorize function
def authorize(username, feature):
    if username in users_db and feature in users_db[username]["features"]:
        return True
    else:
        return False


# define login function
def login():

    ## display page text
    st.markdown(
        "<h1 style='text-align: center;'>SHIELD</h1><h6 style='text-align: center;'><em>Safety Hazard Identification and Emergency Law Deployment</em></h6>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<p style='text-align: center;'>Application web pour la prédiction et la gestion des accidents de la route.</p>",
        unsafe_allow_html=True,
    )

    ## get user credentials
    username = st.text_input("Nom d'utilisateur")
    password = st.text_input("Mot de passe", type="password")

    ## when user clicks on action button
    if st.button("Connexion") == True:

        ## authenticate user, and if successful
        if authenticate(username, password) == True:

            ### from credentials, create authentication string to send with requests to api gateway
            authentication_string = {"identification": f"{username}:{password}"}

            ### save variables in session state for later reuse
            st.session_state["authentication_string"] = authentication_string
            st.session_state["authenticated"] = True
            st.session_state["username"] = username
            st.session_state["admin"] = users_db[username]["admin"]

            ### clear page
            st.empty()

            ### rerun page to display authenticated content
            st.rerun()


# define users all function
def users_all():

    ## display page title
    st.title("Visualiser tous les utilisateurs")

    ## get all users from `database` microservice via `users` microservice and api gateway
    response = requests.get(url="http://gateway:8001/users/all")
    users_db = response.json()

    ## convert users_db to pandas dataframe
    df = pd.DataFrame(users_db).T

    ## reorganize columns
    df["Nom d'utilisateur"] = df.index
    df.reset_index(inplace=True, drop=True)

    df["Mot de passe"] = df["pwd"]

    df["Droits"] = df["admin"].apply(
        lambda x: (
            "Administrateur" if x == 2 else ("Robot" if x == 1 else "Utilisateur")
        )
    )

    ## display results
    st.dataframe(df[["Nom d'utilisateur", "Mot de passe", "Droits"]])


# define users register function
def users_register():

    ## display page title
    st.title("Ajouter un utilisateur")

    ## get input data
    username = st.text_input("Nom d'utilisateur")
    password = st.text_input("Mot de passe", type="password")
    rights = st.selectbox("Droits", ["Utilisateur", "Robot", "Administrateur"])

    ## when user clicks on action button
    if st.button("Ajouter") == True:

        ### convert rights to integer
        if rights == "Utilisateur":
            rights = 0
        elif rights == "Robot":
            rights = 1
        else:
            rights = 2

        ### convert input data to format expected by api gateway and `users` microservice
        new_user = {
            "username": username,
            "password": password,
            "rights": rights,
        }

        ### get authentication string from session state
        authentication_string = st.session_state["authentication_string"]

        ### send input data to `database` microservice via `users` microservice and api gateway
        response = requests.post(
            url="http://gateway:8001/users/register",
            json=new_user,
            headers=authentication_string,
        )

        ### display response
        st.success(response.text)


# define users remove function
def users_remove():

    ## display page title
    st.title("Supprimer un utilisateur")

    ## get input data
    username = st.text_input("Nom d'utilisateur")

    ## when user clicks on action button
    if st.button("Supprimer") == True:

        ### convert input data to format expected by api gateway and `users` microservice
        old_user = {"username": username}

        ### get authentication string from session state
        authentication_string = st.session_state["authentication_string"]

        ### send input data to `database` microservice via `users` microservice and api gateway
        response = requests.delete(
            url="http://gateway:8001/users/remove",
            json=old_user,
            headers=authentication_string,
        )

        ### display response
        st.success(response.text)
