# >>>>>>>> IMPORTS <<<<<<<<


from io import StringIO

import pandas as pd
import plotly.express as px
import requests
import streamlit as st
from frontend_modules.home import home
from frontend_modules.prediction import predict
from frontend_modules.users import authorize, login


def show_feedback_features():
    st.markdown(
        "<h1 id='features' style='text-align: center;'>Rectifier un accident</h1>",
        unsafe_allow_html=True,
    )

    # Champ pour entrer la référence de l'accident
    accident_reference = st.text_input("Référence de l'accident")

    # Sélection de la gravité de l'accident
    accident_gravity = st.radio("Gravité de l'accident", ("Grave", "Non grave"))

    # Bouton pour soumettre la correction
    if st.button("Soumettre la correction"):
        ## Convertir les données d'entrée au format attendu par le microservice `scoring`
        y_true = 1 if accident_gravity == "Grave" else 0
        input_data_label_pred = {"request_id": accident_reference, "y_true": y_true}

        ## Appeler le microservice `scoring` en lui passant les données d'entrée et la chaîne d'authentification
        response = requests.post(
            url="http://gateway:8001/scoring/label-prediction",
            json=input_data_label_pred,
            headers=st.session_state["authentication_string"],
        )

        ## Afficher la réponse du microservice `scoring`
        if "Merci" in response.text:
            st.success(response.text)
        elif "Veuillez" in response.text:
            st.error(response.text)


def show_graph():
    st.markdown(
        "<h1 id='graph' style='text-align: center;'>Graphique de Prédiction</h1>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<p style='text-align:left;'>Afficher un graphique où chaque nouvelle prédiction ajoute un point à une courbe illustrant l'amélioration des performances au fil du temps.</p>",
        unsafe_allow_html=True,
    )
    # Appeler le microservice `scoring` en lui passant la chaîne d'authentification
    response = requests.get(
        url="http://gateway:8001/scoring/get-f1-scores",
        headers=st.session_state["authentication_string"],
    )

    # Convertir la réponse en DataFrame
    response_stream = response.json()
    data_string = StringIO(response_stream)
    df = pd.read_table(filepath_or_buffer=data_string, sep=";")
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="s", origin="1970-01-01")
    df.set_index(keys="timestamp", inplace=True)

    # Afficher la courbe en utilisant plotly
    fig = px.line(
        df, x=df.index, y="f1-score", labels={"x": "Timestamp", "y": "F1-score"}
    )
    st.plotly_chart(fig)


def main_authenticated():
    # Affichage des pages accessibles après authentification
    # Afficher les options de menu en fonction des rôles de l'utilisateur
    selected_home = (
        st.sidebar.button("Accueil", key="accueil")
        if authorize(st.session_state["username"], "accueil")
        else None
    )
    selected_features = (
        st.sidebar.button("Ajouter un accident", key="ajout_accident")
        if authorize(st.session_state["username"], "ajout_accident")
        else None
    )
    selected_feedback_features = (
        st.sidebar.button("Rectifier un accident", key="rectifier_accident")
        if authorize(st.session_state["username"], "correction_accident")
        else None
    )
    selected_graph = (
        st.sidebar.button("Graphique", key="graphique")
        if authorize(st.session_state["username"], "graphique")
        else None
    )

    # Déterminer la page à afficher en fonction du bouton sélectionné
    selected_page = st.session_state.get("selected_page", "Accueil")

    if selected_home:
        selected_page = "Accueil"
    elif selected_features:
        selected_page = "Ajouter un accident"
    elif selected_feedback_features:
        selected_page = "Rectifier un accident"
    elif selected_graph:
        selected_page = "Graphique"

    st.session_state["selected_page"] = selected_page

    # Afficher la page correspondante
    if selected_page == "Accueil":
        home()
    elif selected_page == "Ajouter un accident":
        predict()
    elif selected_page == "Rectifier un accident":
        show_feedback_features()
    elif selected_page == "Graphique":
        show_graph()

    # Afficher le bouton de déconnexion dans la barre latérale
    if st.sidebar.button("Se déconnecter"):
        st.session_state["authenticated"] = False
        st.session_state["username"] = None
        # Effacer le contenu de la page
        st.empty()
        # Forcer le rerun de la page pour afficher le contenu non authentifié
        st.experimental_rerun()


# main function
def main():
    ## initialize authentication state
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False

    ## if user has been authenticated, grant access to corresponding content
    if st.session_state["authenticated"] == True:
        main_authenticated()
    ## else, show login page
    else:
        login()


# >>>>>>>> SCRIPT EXECUTION <<<<<<<<


# if file is run as script, run main()
if __name__ == "__main__":
    main()
