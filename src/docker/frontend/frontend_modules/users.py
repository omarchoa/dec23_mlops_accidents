# imports
import requests
import streamlit as st

# get all users from `database` microservice via `users` microservice and api gateway
response = requests.get(url="http://gateway:8001/users/all")
users_db = response.json()


# define authentication function
def authenticate(username, password):
    if username in users_db and users_db[username]["pwd"] == password:
        return True
    else:
        return False


# define authorization function
def authorize(username, feature):
    if username in users_db and feature in users_db[username]["features"]:
        return True
    else:
        return False


# define login function
def login():

    ## display login page text
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
