import requests
import streamlit as st

# Données des utilisateurs
response = requests.get(url="http://gateway:8001/users/all")
users_db = response.json()
for key, value in users_db.items():
    if value["admin"] == 0:  ## standard user
        value["roles"] = ["accueil", "ajout_accident"]
    if value["admin"] == 2:  ## admin
        value["roles"] = [
            "accueil",
            "ajout_accident",
            "correction_accident",
            "graphique",
        ]


# Fonction de vérification des identifiants de connexion
def authenticate(username, password):
    if username in users_db:
        if users_db[username]["pwd"] == password:
            return True
    return False


# Fonction de vérification des autorisations
def has_role(username, role):
    if username in users_db and role in users_db[username]["roles"]:
        return True
    return False


# Fonction principale
def main():
    # État de la session pour l'authentification
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False

    # Vérifier si l'utilisateur est déjà authentifié
    if st.session_state["authenticated"]:
        main_authenticated()
    else:
        show_login_page()


def show_login_page():
    st.markdown(
        "<h1 style='text-align: center;'>SHIELD</h1><h6 style='text-align: center;'><em>Safety Hazard Identification and Emergency Law Deployment</em></h6>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<p style='text-align: center;'>Application web pour la prédiction et la gestion des accidents de la route.</p>",
        unsafe_allow_html=True,
    )

    # Champs de saisie de connexion
    username = st.text_input("Nom d'utilisateur")
    password = st.text_input("Mot de passe", type="password")
    if st.button("Se connecter"):
        if authenticate(username, password):
            ## À partir des identifiants, créer la chaîne d'authentification à passer à la passerelle `gateway`
            authentication_string = {"identification": f"{username}:{password}"}

            ## La sauvegarder avec d'autres variables dans l'état de session pour une utilisation ultérieure dans d'autres fonctions
            st.session_state["authentication_string"] = authentication_string
            st.session_state["authenticated"] = True
            st.session_state["username"] = username

            ## Effacer le contenu de la page
            st.empty()

            ## Forcer le rerun de la page pour afficher le contenu authentifié
            st.experimental_rerun()


def main_authenticated():
    # Affichage des pages accessibles après authentification
    # Afficher les options de menu en fonction des rôles de l'utilisateur
    selected_home = (
        st.sidebar.button("Accueil", key="accueil")
        if has_role(st.session_state["username"], "accueil")
        else None
    )
    selected_features = (
        st.sidebar.button("Ajouter un accident", key="ajout_accident")
        if has_role(st.session_state["username"], "ajout_accident")
        else None
    )
    selected_feedback_features = (
        st.sidebar.button("Rectifier un accident", key="rectifier_accident")
        if has_role(st.session_state["username"], "correction_accident")
        else None
    )
    selected_graph = (
        st.sidebar.button("Graphique", key="graphique")
        if has_role(st.session_state["username"], "graphique")
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
        show_homepage()
    elif selected_page == "Ajouter un accident":
        show_features()
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


def show_homepage():
    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        st.image("/home/shield/frontend/images/bouclier.png")

    st.markdown(
        "<h1 style='text-align: center;'>SHIELD</h1><h6 style='text-align: center;'><em>Safety Hazard Identification and Emergency Law Deployment</em></h6>",
        unsafe_allow_html=True,
    )

    st.markdown(
        "<p style='text-align:center;'>SHIELD est une application Python alimentée par l'IA qui utilise l'apprentissage automatique pour prédire les niveaux de priorité des accidents de la route, aidant les forces de l'ordre à optimiser les ressources et à optimiser les ressources des forces de l'ordre.</p>",
        unsafe_allow_html=True,
    )
    st.write("")
    st.markdown(
        "<p style='text-align:center;'>SHIELD est développé par <span style='color:orange;'>Fabrice Charraud, Omar Choa, Michael Deroche, Alexandre Winger</span>. <br>Ce frontend streamlit constitue notre projet final pour le programme DataScientest Machine Learning Engineer.</p>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<p style='text-align:center;'>dec23_mlops // <span style='color:#6ab7ff;'>Datascientest</span></p>",
        unsafe_allow_html=True,
    )


def show_features():
    st.markdown(
        "<h1 id='features' style='text-align: center;'>Ajouter un accident</h1>",
        unsafe_allow_html=True,
    )

    # Caractéristiques de l'accident

    ## Correspondances
    dict_catu = {
        "Conducteur": 1,
        "Passager": 2,
        "Piéton": 3,
    }
    dict_sexe = {
        "Masculin": 1,
        "Féminin": 2,
    }
    dict_secu1 = {
        "Non renseigné": -1,
        "Aucun équipement": 0,
        "Ceinture": 1,
        "Casque": 2,
        "Dispositif enfants": 3,
        "Gilet réfléchissant": 4,
        "Airbag (2RM/3RM)": 5,
        "Gants (2RM/3RM)": 6,
        "Gants + Airbag (2RM/3RM)": 7,
        "Non déterminable": 8,
        "Autre": 9,
    }
    dict_catv = {
        "Indeterminable": 0,
        "Bicyclette": 1,
        "Cyclomoteur <50cm3": 2,
        "Voiturette (Quadricycle à moteur carrossé)": 3,
        "Référence inutilisée depuis 2006 (scooter immatriculé)": 4,
        "Référence inutilisée depuis 2006 (motocyclette)": 5,
        "Référence inutilisée depuis 2006 (side-car)": 6,
        "VL seul": 7,
        "Référence inutilisée depuis 2006 (VL + caravane)": 8,
        "Référence inutilisée depuis 2006 (VL + remorque)": 9,
        "VU seul 1,5T <= PTAC <= 3,5T avec ou sans remorque": 10,
        "Référence inutilisée depuis 2006 (VU (10) + caravane)": 11,
        "Référence inutilisée depuis 2006 (VU (10) + remorque)": 12,
        "PL seul 3,5T <PTCA <= 7,5T": 13,
        "PL seul > 7,5T": 14,
        "PL > 3,5T + remorque": 15,
        "Tracteur routier seul": 16,
        "Tracteur routier + semi-remorque": 17,
        "Référence inutilisée depuis 2006 (transport en commun)": 18,
        "Référence inutilisée depuis 2006 (tramway)": 19,
        "Engin spécial": 20,
        "Tracteur agricole": 21,
        "Scooter < 50 cm3": 30,
        "Motocyclette > 50 cm3 et <= 125 cm3": 31,
        "Scooter > 50 cm3 et <= 125 cm3": 32,
        "Motocyclette > 125 cm3": 33,
        "Scooter > 125 cm3": 34,
        "Quad léger <= 50 cm3 (Quadricycle à moteur non carrossé)": 35,
        "Quad lourd > 50 cm3 (Quadricycle à moteur non carrossé)": 36,
        "Autobus": 37,
        "Autocar": 38,
        "Train": 39,
        "Tramway": 40,
        "3RM <= 50 cm3": 41,
        "3RM > 50 cm3 <= 125 cm3": 42,
        "3RM > 125 cm3": 43,
        "EDP à moteur": 50,
        "EDP sans moteur": 60,
        "VAE": 80,
        "Autre véhicule": 99,
    }
    dict_obsm = {
        "Non renseigné": -1,
        "Aucun": 0,
        "Piéton": 1,
        "Véhicule": 2,
        "Véhicule sur rail": 4,
        "Animal domestique": 5,
        "Animal sauvage": 6,
        "Autre": 9,
    }
    dict_motor = {
        "Non renseigné": -1,
        "Inconnue": 0,
        "Hydrocarbures": 1,
        "Hybride électrique": 2,
        "Electrique": 3,
        "Hydrogène": 4,
        "Humaine": 5,
        "Autre": 6,
    }
    dict_catr = {
        "Autoroute": 1,
        "Route nationale": 2,
        "Route Départementale": 3,
        "Voie Communales": 4,
        "Hors réseau public": 5,
        "Parc de stationnement ouvert à la circulation publique": 6,
        "Routes de métropole urbaine": 7,
        "Autre": 9,
    }
    dict_circ = {
        "Non renseigné": -1,
        "A sens unique": 1,
        "Bidirectionnelle": 2,
        "A chaussées séparées": 3,
        "Avec voies d’affectation variable": 4,
    }
    dict_surf = {
        "Non renseigné": -1,
        "Normale": 1,
        "Mouillée": 2,
        "Flaques": 3,
        "Inondée": 4,
        "Enneigée": 5,
        "Boue": 6,
        "Verglacée": 7,
        "Corps gras – huile": 8,
        "Autre": 9,
    }
    dict_situ = {
        "Non renseigné": -1,
        "Aucun": 0,
        "Sur chaussée": 1,
        "Sur bande d’arrêt d’urgence": 2,
        "Sur accotement": 3,
        "Sur trottoir": 4,
        "Sur piste cyclable": 5,
        "Sur autre voie spéciale": 6,
        "Autres": 8,
    }
    dict_lum = {
        "Plein jour": 1,
        "Crépuscule ou aube": 2,
        "Nuit sans éclairage public": 3,
        "Nuit avec éclairage public non allumé": 4,
        "Nuit avec éclairage public allumé": 5,
    }
    dict_agg_ = {
        "Hors agglomération": 1,
        "En agglomération": 2,
    }
    dict_inter = {
        "Hors intersection": 1,
        "Intersection en X": 2,
        "Intersection en T": 3,
        "Intersection en Y": 4,
        "Intersection à plus de 4 branches": 5,
        "Giratoire": 6,
        "Place": 7,
        "Passage à niveau": 8,
        "Autre intersection": 9,
    }
    dict_atm = {
        "Non renseigné": -1,
        "Normale": 1,
        "Pluie légère": 2,
        "Pluie forte": 3,
        "Neige - grêle": 4,
        "Brouillard - fumée": 5,
        "Vent fort - tempête": 6,
        "Temps éblouissant": 7,
        "Temps couvert": 8,
        "Autre": 9,
    }
    dict_col = {
        "Non renseigné": -1,
        "Deux véhicules - frontale": 1,
        "Deux véhicules – par l’arrière": 2,
        "Deux véhicules – par le coté": 3,
        "Trois véhicules et plus – en chaîne": 4,
        "Trois véhicules et plus - collisions multiples": 5,
        "Autre collision": 6,
        "Sans collision": 7,
    }

    ## Saisie
    jour_accident = st.date_input(
        "Jour de l'accident",
        value=None,
        min_value=None,
        max_value=None,
        key=None,
    )
    heure_accident = st.slider(
        "Heure de l'accident",
        min_value=0,
        max_value=23,
        step=1,
    )
    departement = st.text_input("Département (Code INSEE)")
    place_occupée = st.slider(
        "Place occupée dans le véhicule",
        min_value=0,
        max_value=10,
        step=1,
        help="10 – Piéton (non applicable)",
    )
    nombre_victimes = st.slider(
        "Nombre de victimes",
        min_value=0,
        max_value=25,
        step=1,
    )
    nombre_vehicules = st.text_input("Nombre de véhicules impliqués")
    categorie_usager = st.selectbox(
        "Catégorie d'usager",
        options=dict_catu.keys(),
    )
    sexe_usager = st.selectbox(
        "Sexe de l'usager",
        options=dict_sexe.keys(),
    )
    equipement_securite = st.selectbox(
        "Équipement de sécurité",
        options=dict_secu1.keys(),
    )
    age_victime = st.slider(
        "Âge de la ou des victimes",
        min_value=0,
        max_value=100,
        step=1,
    )
    categorie_vehicule = st.selectbox(
        "Catégorie du véhicule",
        options=dict_catv.keys(),
    )
    obstacle_mobile = st.selectbox(
        "Obstacle mobile heurté",
        options=dict_obsm.keys(),
    )
    type_motorisation = st.selectbox(
        "Type de motorisation du véhicule",
        options=dict_motor.keys(),
    )
    categorie_route = st.selectbox(
        "Catégorie de route",
        options=dict_catr.keys(),
    )
    regime_circulation = st.selectbox(
        "Régime de circulation",
        options=dict_circ.keys(),
    )
    etat_surface = st.selectbox(
        "État de la surface",
        options=dict_surf.keys(),
    )
    situation_accident = st.selectbox(
        "Situation de l’accident",
        options=dict_situ.keys(),
    )
    vitesse_max_autorisee = st.slider(
        "Vitesse maximale autorisée",
        min_value=0,
        max_value=300,
        step=1,
    )
    lumiere = st.selectbox(
        "Lumière",
        options=dict_lum.keys(),
    )
    commune = st.text_input("Commune (Code INSEE)")
    localisation = st.selectbox(
        "Localisation",
        options=dict_agg_.keys(),
    )
    intersection = st.selectbox(
        "Intersection",
        options=dict_inter.keys(),
    )
    conditions_atmospheriques = st.selectbox(
        "Conditions atmosphériques",
        options=dict_atm.keys(),
    )
    type_collision = st.selectbox(
        "Type de collision",
        options=dict_col.keys(),
    )
    latitude = st.slider(
        "Latitude",
        min_value=-90.0,
        max_value=90.0,
        step=0.001,
    )
    longitude = st.slider(
        "Longitude",
        min_value=-180.0,
        max_value=180.0,
        step=0.001,
    )

    ## Conversion
    input_data_pred_call = {
        "place": int(place_occupée),
        "catu": int(dict_catu[categorie_usager]),
        "sexe": int(dict_sexe[sexe_usager]),
        "secu1": float(dict_secu1[equipement_securite]),
        "year_acc": int(jour_accident.year),
        "victim_age": int(age_victime),
        "catv": int(dict_catv[categorie_vehicule]),
        "obsm": int(dict_obsm[obstacle_mobile]),
        "motor": int(dict_motor[type_motorisation]),
        "catr": int(dict_catr[categorie_route]),
        "circ": int(dict_circ[regime_circulation]),
        "surf": int(dict_surf[etat_surface]),
        "situ": int(dict_situ[situation_accident]),
        "vma": int(vitesse_max_autorisee),
        "jour": int(jour_accident.day),
        "mois": int(jour_accident.month),
        "lum": int(dict_lum[lumiere]),
        "dep": int(departement),
        "com": int(commune),
        "agg_": int(dict_agg_[localisation]),
        "inter": int(dict_inter[intersection]),
        "atm": int(dict_atm[conditions_atmospheriques]),
        "col": int(dict_col[type_collision]),
        "lat": float(latitude),
        "long": float(longitude),
        "hour": int(heure_accident),
        "nb_victim": int(nombre_victimes),
        "nb_vehicules": int(nombre_vehicules),
    }

    st.write("")

    ## Prédiction
    if st.button("Valider"):
        ### Récupérer la chaîne d'authentification à partir de l'état de session
        authentication_string = st.session_state["authentication_string"]

        ### Appeler le microservice `prediction` en lui passant les données d'entrée et la chaîne d'authentification
        response = requests.post(
            url="http://gateway:8001/prediction/call",
            json=input_data_pred_call,
            headers=authentication_string,
        )

        ### Afficher la réponse du microservice `prediction`
        st.write(response.text)


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
            url="http://scoring:8006/label-prediction",
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
    # Générer les valeurs x
    x_values = list(range(1, 21))

    # Calculer les valeurs y comme des nombres progressivement croissants
    y_values = [i**2 for i in x_values]

    # Afficher la courbe en utilisant line_chart de Streamlit
    st.line_chart({"x": x_values, "y": y_values})


if __name__ == "__main__":
    main()
