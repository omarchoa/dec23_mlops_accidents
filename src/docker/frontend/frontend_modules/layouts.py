# imports
import streamlit as st
from frontend_modules import navigation


# define admin function
def admin():

    ## set home page as landing page
    if "page" not in st.session_state:
        st.session_state["page"] = "home"

    ## display home section
    st.sidebar.header(body="Accueil")
    if st.sidebar.button(label="Accueil"):
        st.session_state["page"] = "home"
    if st.sidebar.button(label="État du système"):
        st.session_state["page"] = "status"
    if st.sidebar.button(label="Déconnexion"):
        st.session_state["page"] = "logout"

    ## display users section
    st.sidebar.header(body="Utilisateurs")
    if st.sidebar.button(
        label="Visualiser tous les utilisateurs"
    ):  ### for debugging purposes only
        st.session_state["page"] = "users_all"
    if st.sidebar.button(label="Ajouter un utilisateur"):
        st.session_state["page"] = "users_register"
    if st.sidebar.button(label="Supprimer un utilisateur"):
        st.session_state["page"] = "users_remove"

    ## display data section
    st.sidebar.header(body="Données")
    if st.sidebar.button(label="Télécharger et préparer des données"):
        st.session_state["page"] = "data_download_prep_run"

    ## display modeling section
    st.sidebar.header(body="Modélisation")
    if st.sidebar.button(label="Entraîner le modèle"):
        st.session_state["page"] = "training_train"

    ## display prediction section
    st.sidebar.header(body="Prédiction")
    if st.sidebar.button(label="Effectuer une prédiction test"):
        st.session_state["page"] = "prediction_test"
    if st.sidebar.button(label="Effectuer une prédiction réelle"):
        st.session_state["page"] = "prediction_call"

    ## display scoring section
    st.sidebar.header(body="Évaluation")
    if st.sidebar.button(label="Valider ou corriger une prédiction"):
        st.session_state["page"] = "scoring_label_prediction"
    if st.sidebar.button(label="Mettre à jour le F1 score"):
        st.session_state["page"] = "scoring_update_f1_score"
    if st.sidebar.button(label="Récupérer le dernier F1 score"):
        st.session_state["page"] = "scoring_get_latest_f1_score"
    if st.sidebar.button(label="Récupérer tous les F1 scores"):
        st.session_state["page"] = "scoring_get_f1_scores"
    if st.sidebar.button(label="Visualiser l'évolution des F1 scores"):
        st.session_state["page"] = "scoring_plot_f1_scores"

    ## execute button actions
    navigation.button_actions()


# define non admin function
def non_admin():

    ## set home page as landing page
    if "page" not in st.session_state:
        st.session_state["page"] = "home"

    ## display home section
    st.sidebar.header(body="Accueil")
    if st.sidebar.button(label="Accueil"):
        st.session_state["page"] = "home"
    if st.sidebar.button(label="Déconnexion"):
        st.session_state["page"] = "logout"

    ## display prediction section
    st.sidebar.header(body="Prédiction")
    if st.sidebar.button(label="Effectuer une prédiction test"):
        st.session_state["page"] = "prediction_test"
    if st.sidebar.button(label="Effectuer une prédiction réelle"):
        st.session_state["page"] = "prediction_call"

    ## display scoring section
    st.sidebar.header(body="Évaluation")
    if st.sidebar.button(label="Valider ou corriger une prédiction"):
        st.session_state["page"] = "scoring_label_prediction"

    ## execute button actions
    navigation.button_actions()
