# >>>>>>>> IMPORTS <<<<<<<<


import streamlit as st
from frontend_modules.home import home
from frontend_modules.prediction import predict
from frontend_modules.scoring import label_prediction, plot_f1_scores
from frontend_modules.users import authorize, login


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
        label_prediction()
    elif selected_page == "Graphique":
        plot_f1_scores()

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
