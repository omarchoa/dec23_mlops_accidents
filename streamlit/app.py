import streamlit as st
    
# Fonction pour l'authentification utilisateur
def authenticate_user(username, password):
    # Authentification de l'utilisateur
    if username == "user" and password == "user":
        return "user"
    elif username == "admin" and password == "admin":
        return "admin"
    else:
        return None

# Page de connexion
def login_page():
    st.header("Connexion")

    # Champs de saisie pour le nom d'utilisateur et le mot de passe
    username = st.text_input("Nom d'utilisateur")
    password = st.text_input("Mot de passe", type="password")

    # Bouton de connexion
    if st.button("Se connecter"):
        # Authentification de l'utilisateur
        user_type = authenticate_user(username, password)
        if user_type == "user":
            st.success("Connexion réussie en tant qu'utilisateur.")
            return "user"
        elif user_type == "admin":
            st.success("Connexion réussie en tant qu'administrateur.")
            return "admin"
        else:
            st.error("Nom d'utilisateur ou mot de passe incorrect.")
    return None

# Fonction principale
def main():
    user_type = login_page()  # Authentifier l'utilisateur

    if user_type == "user":
        st.write("Bienvenue, utilisateur !")
        # Votre code pour la section utilisateur
    elif user_type == "admin":
        st.write("Bienvenue, administrateur !")
        # Votre code pour la section administrateur

    # Afficher le reste du frontend
    if user_type:
        show_frontend(user_type)

def show_frontend(user_type):
    selected_page = st.sidebar.radio("Navigation", ["Accueil", "Ajouter un accident", "Rectifier un accident", "Graphique de Prédiction"])

    # Afficher la page sélectionnée
    if selected_page == "Accueil":
        show_homepage()
    elif selected_page == "Ajouter un accident":
        show_features()
    elif selected_page == "Rectifier un accident":
        show_feedback_features()
    elif selected_page == "Graphique de Prédiction":
        show_graph()

def show_homepage():
    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        st.image("/mount/src/dec23_mlops_accidents/streamlit/images/bouclier.png")
    st.write("") 
    st.markdown("<h1 style='text-align:center;'>SHIELD</h1><h6 style='text-align:center;'><em>Safety Hazard Identification and Emergency Law Deployment</em></h6>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;'>SHIELD est une application Python alimentée par l'IA qui utilise l'apprentissage automatique pour prédire les niveaux de priorité des accidents de la route, aidant les forces de l'ordre à optimiser les ressources et à optimiser les ressources des forces de l'ordre.</p>", unsafe_allow_html=True)
    st.write("") 
    st.markdown("<p style='text-align:center;'>SHIELD est développé par <span style='color:orange;'>Fabrice Charraud, Omar Choa, Michael Deroche, Alexandre Winger</span>. <br>Ce frontend streamlit constitue notre projet final pour le programme DataScientest Machine Learning Engineer.</p>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;'>dec23_mlops // <span style='color:#6ab7ff;'>Datascientest</span></p>", unsafe_allow_html=True)

def show_features():
    st.markdown("<h1 id='features' style='text-align: center;'>Ajouter un accident</h1>", unsafe_allow_html=True)
   
    # Caractéristiques
    jour_accident = st.date_input("Jour de l'accident", value=None, min_value=None, max_value=None, key=None)
    heure_accident = st.slider("Heure de l'accident", min_value=0, max_value=23, step=1)
    departement = st.text_input("Département (Code INSEE)")
    place_occupée = st.slider("Place occupée dans le véhicule", min_value=0, max_value=10, step=1, help="10 – Piéton (non applicable)")
    nombre_victimes = st.slider("Nombre de victimes", min_value=0, max_value=25, step=1)
    nombre_vehicules = st.text_input("Nombre de véhicules impliqués")
    categorie_usager = st.selectbox("Catégorie d'usager", options=["Conducteur", "Passager", "Piéton"])
    sexe_usager = st.selectbox("Sexe de l'usager", options=["Masculin", "Féminin"])
    equipement_securite = st.selectbox("Équipement de sécurité", options=["Non renseigné", "Aucun équipement", "Ceinture", "Casque", "Dispositif enfants", "Gilet réfléchissant", "Airbag (2RM/3RM)", "Gants (2RM/3RM)", "Gants + Airbag (2RM/3RM)", "Non déterminable", "Autre"])
    age_victime = st.slider("Âge de la ou des victimes", min_value=0, max_value=100, step=1)
    categorie_vehicule = st.selectbox("Catégorie du véhicule", options=["Bicyclette", "Cyclomoteur <50cm3", "Voiturette (Quadricycle à moteur carrossé)", "Référence inutilisée depuis 2006 (scooter immatriculé)", "Référence inutilisée depuis 2006 (motocyclette)", "Référence inutilisée depuis 2006 (side-car)", "VL seul", "Référence inutilisée depuis 2006 (VL + caravane)", "Référence inutilisée depuis 2006 (VL + remorque)", "VU seul 1,5T <= PTAC <= 3,5T avec ou sans remorque", "Référence inutilisée depuis 2006 (VU (10) + caravane)", "Référence inutilisée depuis 2006 (VU (10) + remorque)", "PL seul 3,5T <PTCA <= 7,5T", "PL seul > 7,5T", "PL > 3,5T + remorque", "Tracteur routier seul", "Tracteur routier + semi-remorque", "Référence inutilisée depuis 2006 (transport en commun)", "Référence inutilisée depuis 2006 (tramway)", "Engin spécial", "Tracteur agricole", "Scooter < 50 cm3", "Motocyclette > 50 cm3 et <= 125 cm3", "Scooter > 50 cm3 et <= 125 cm3", "Motocyclette > 125 cm3", "Scooter > 125 cm3", "Quad léger <= 50 cm3 (Quadricycle à moteur non carrossé)", "Quad lourd > 50 cm3 (Quadricycle à moteur non carrossé)", "Autobus", "Autocar", "Train", "Tramway", "3RM <= 50 cm3", "3RM > 50 cm3 <= 125 cm3", "3RM > 125 cm3", "EDP à moteur", "EDP sans moteur", "VAE", "Autre véhicule"])
    obstacle_mobile = st.selectbox("Obstacle mobile heurté", options=["Non renseigné", "Aucun", "Piéton", "Véhicule", "Véhicule sur rail", "Animal domestique", "Animal sauvage", "Autre"])
    type_motorisation = st.selectbox("Type de motorisation du véhicule", options=["Non renseigné", "Inconnue", "Hydrocarbures", "Hybride électrique", "Electrique", "Hydrogène", "Humaine", "Autre"])
    categorie_route = st.selectbox("Catégorie de route", options=["Autoroute", "Route nationale", "Route Départementale", "Voie Communales", "Hors réseau public", "Parc de stationnement ouvert à la circulation publique", "Routes de métropole urbaine", "Autre"])
    regime_circulation = st.selectbox("Régime de circulation", options=["Non renseigné", "A sens unique", "Bidirectionnelle", "A chaussées séparées", "Avec voies d’affectation variable"])
    etat_surface = st.selectbox("État de la surface", options=["Non renseigné", "Normale", "Mouillée", "Flaques", "Inondée", "Enneigée", "Boue", "Verglacée", "Corps gras – huile", "Autre"])
    situation_accident = st.selectbox("Situation de l’accident", options=["Non renseigné", "Aucun", "Sur chaussée", "Sur bande d’arrêt d’urgence", "Sur accotement", "Sur trottoir", "Sur piste cyclable", "Sur autre voie spéciale", "Autres"])
    vitesse_max_autorisee = st.slider("Vitesse maximale autorisée", min_value=0, max_value=300, step=1)
    lumiere = st.selectbox("Lumière", options=["Plein jour", "Crépuscule ou aube", "Nuit sans éclairage public", "Nuit avec éclairage public non allumé", "Nuit avec éclairage public allumé"])
    commune = st.text_input("Commune (Code INSEE)")
    localisation = st.selectbox("Localisation", options=["Hors agglomération", "En agglomération"])
    intersection = st.selectbox("Intersection", options=["Hors intersection", "Intersection en X", "Intersection en T", "Intersection en Y", "Intersection à plus de 4 branches", "Giratoire", "Place", "Passage à niveau", "Autre intersection"])
    conditions_atmospheriques = st.selectbox("Conditions atmosphériques", options=["Non renseigné", "Normale", "Pluie légère", "Pluie forte", "Neige - grêle", "Brouillard - fumée", "Vent fort - tempête", "Temps éblouissant", "Temps couvert", "Autre"])
    type_collision = st.selectbox("Type de collision", options=["Non renseigné", "Deux véhicules - frontale", "Deux véhicules – par l’arrière", "Deux véhicules – par le coté", "Trois véhicules et plus – en chaîne", "Trois véhicules et plus - collisions multiples", "Autre collision", "Sans collision"])
    latitude = st.slider("Latitude", min_value=-90.0, max_value=90.0, step=0.001)
    longitude = st.slider("Longitude", min_value=-180.0, max_value=180.0, step=0.001)

    st.write("")  # Ajouter de l'espace vertical pour créer une nouvelle ligne
    if st.button("Valider"):
        # Effectuer le traitement ici
        gravity = determine_gravity(jour_accident, heure_accident, nombre_victimes, age_victime)
        gravity_text = translate_gravity(gravity)
        st.write(f"Gravité de l'accident : {gravity_text}")
    
def determine_gravity(jour_accident, heure_accident, nombre_victimes, age_victime):
    # Exemple de logique de détermination de la gravité fictive
    if nombre_victimes > 5:
        return 1  # Grave
    else:
        return 0  # Non grave

def translate_gravity(gravity):
    if gravity == 0:
        return "Non Grave"
    elif gravity == 1:
        return "Grave"
    else:
        return "Non déterminé"

def show_feedback_features():
    st.header("Rectifier un accident")

    # Champ pour entrer la référence de l'accident
    accident_reference = st.text_input("Référence de l'accident")

    # Sélection de la gravité de l'accident
    accident_gravity = st.radio("Gravité de l'accident", ("Grave", "Non grave"))

    # Bouton pour soumettre la correction
    if st.button("Soumettre la correction"):
        # Traitement de la correction
        if accident_reference:
            # Vous pouvez ici inclure le code pour traiter la correction de l'accident
            st.success(f"Correction soumise pour l'accident {accident_reference} avec gravité : {accident_gravity}")
        else:
            st.warning("Veuillez entrer une référence d'accident.")
    
def show_graph():
    st.markdown("<h1 id='graph' style='text-align: center;'>Graphique de Prédiction</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:left;'>Afficher un graphique où chaque nouvelle prédiction ajoute un point à une courbe illustrant l'amélioration des performances au fil du temps.</p>", unsafe_allow_html=True)
    # Générer les valeurs x
    x_values = list(range(1, 21))

    # Calculer les valeurs y comme des nombres progressivement croissants
    y_values = [i**2 for i in x_values]

    # Afficher la courbe en utilisant line_chart de Streamlit
    st.line_chart({"x": x_values, "y": y_values})
    
if __name__ == '__main__':
    main()
