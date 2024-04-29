# imports
import streamlit as st
from frontend_modules.navigation import button_actions


# define admin function
def admin():

    ## display home section
    st.sidebar.header(body="Accueil")
    button_home = st.sidebar.button(label="Accueil")
    button_status = st.sidebar.button(label="État du système")
    button_logout = st.sidebar.button(label="Déconnexion")

    ## display users section
    st.sidebar.header(body="Utilisateurs")
    st.sidebar.button(
        label="Visualiser tous les utilisateurs", key="users_all"
    )  ### for debugging purposes only
    st.sidebar.button(label="Ajouter un utilisateur", key="users_register")
    st.sidebar.button(label="Supprimer un utilisateur", key="users_remove")

    ## display data section
    st.sidebar.header(body="Données")
    st.sidebar.button(
        label="Télécharger et préparer des données", key="data_download_prep_run"
    )

    ## display modeling section
    st.sidebar.header(body="Modélisation")
    st.sidebar.button(label="Entraîner le modèle", key="training_train")

    ## display prediction section
    st.sidebar.header(body="Prédiction")
    st.sidebar.button(label="Effectuer une prédiction test", key="prediction_test")
    st.sidebar.button(label="Effectuer une prédiction réelle", key="prediction_call")

    ## display scoring section
    st.sidebar.header(body="Évaluation")
    st.sidebar.button(
        label="Valider ou corriger une prédiction",
        key="scoring_label_prediction",
    )
    st.sidebar.button(label="Mettre à jour le F1 score", key="scoring_update_f1_score")
    st.sidebar.button(
        label="Récupérer le dernier F1 score", key="scoring_get_latest_f1_score"
    )
    st.sidebar.button(label="Récupérer tous les F1 scores", key="scoring_get_f1_scores")
    st.sidebar.button(
        label="Visualiser l'évolution des F1 scores",
        key="scoring_plot_f1_scores",
    )

    ## save button actions to session state
    st.session_state["button_home"] = button_home
    st.session_state["button_status"] = button_status
    st.session_state["button_logout"] = button_logout

    ## execute button actions
    button_actions()


# define non admin function
def non_admin():

    ## display home section
    st.sidebar.header(body="Accueil")
    button_home = st.sidebar.button(label="Accueil", key="home")
    button_logout = st.sidebar.button(label="Déconnexion", key="logout")

    ## display prediction section
    st.sidebar.header(body="Prédiction")
    st.sidebar.button(label="Effectuer une prédiction test", key="prediction_test")
    st.sidebar.button(label="Effectuer une prédiction réelle", key="prediction_call")

    ## display scoring section
    st.sidebar.header(body="Évaluation")
    st.sidebar.button(
        label="Valider ou corriger une prédiction",
        key="scoring_label_prediction",
    )

    ## save button actions to session state
    st.session_state["button_home"] = button_home
    st.session_state["button_logout"] = button_logout

    ## execute button actions
    button_actions()
