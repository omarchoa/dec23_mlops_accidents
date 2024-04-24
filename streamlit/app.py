import streamlit as st

def main():  
    
    selected_home = st.sidebar.button("Accueil")
    selected_features = st.sidebar.button("Caractéristiques")
    selected_graph = st.sidebar.button("Graphique de Prédiction")

    # Déterminer quelle page afficher en fonction du bouton sélectionné
    if selected_home:
        st.session_state.selected_page = "Accueil"
    elif selected_features:
        st.session_state.selected_page = "Caractéristiques"
    elif selected_graph:
        st.session_state.selected_page = "Graphique"

    # Afficher la page correspondante
    if "selected_page" not in st.session_state:
        st.session_state.selected_page = "Accueil"  # Par défaut, afficher la page d'accueil

    if st.session_state.selected_page == "Accueil":
        show_homepage()
    elif st.session_state.selected_page == "Caractéristiques":
        show_features()
    elif st.session_state.selected_page == "Graphique":
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
    st.markdown("<h1 id='features' style='text-align: center;'>Caractéristiques de l'Accident</h1>", unsafe_allow_html=True)

    # Caractéristiques
    jour_accident = st.date_input("Jour de l'accident", value=None, min_value=None, max_value=None, key=None)
    heure_accident = st.slider("Heure de l'accident", min_value=0, max_value=23, step=1)
    departement = st.text_input("Département (Code INSEE)")
    place_occupée = st.slider("Place occupée dans le véhicule", min_value=0, max_value=10, step=1, help="10 – Piéton (non applicable)")
    nombre_victimes = st.slider("Nombre de victimes", min_value=0, max_value=100, step=1)
    nombre_vehicules = st.text_input("Nombre de véhicules impliqués")
    categorie_usager = st.select_slider("Catégorie d'usager", options={1: "Conducteur", 2: "Passager", 3: "Piéton"})
    sexe_usager = st.select_slider("Sexe de l'usager", options={1: "Masculin", 2: "Féminin"})
    equipement_securite = st.select_slider("Équipement de sécurité", options={-1: "Non renseigné", 0: "Aucun équipement", 1: "Ceinture", 2: "Casque", 3: "Dispositif enfants", 4: "Gilet réfléchissant", 5: "Airbag (2RM/3RM)", 6: "Gants (2RM/3RM)", 7: "Gants + Airbag (2RM/3RM)", 8: "Non déterminable", 9: "Autre"})
    age_victime = st.slider("Âge de la ou des victimes", min_value=0, max_value=100, step=1)
    
def map_categorie_vehicule(index):
    categories = {
        "00": "Indéterminable",
        "01": "Bicyclette",
        "02": "Cyclomoteur <50cm3",
        "03": "Voiturette (Quadricycle à moteur carrossé)",
        "04": "Référence inutilisée depuis 2006 (scooter immatriculé)",
        "05": "Référence inutilisée depuis 2006 (motocyclette)",
        "06": "Référence inutilisée depuis 2006 (side-car)",
        "07": "VL seul",
        "08": "Référence inutilisée depuis 2006 (VL + caravane)",
        "09": "Référence inutilisée depuis 2006 (VL + remorque)",
        "10": "VU seul 1,5T <= PTAC <= 3,5T avec ou sans remorque",
        "11": "Référence inutilisée depuis 2006 (VU (10) + caravane)",
        "12": "Référence inutilisée depuis 2006 (VU (10) + remorque)",
        "13": "PL seul 3,5T <PTCA <= 7,5T",
        "14": "PL seul > 7,5T",
        "15": "PL > 3,5T + remorque",
        "16": "Tracteur routier seul",
        "17": "Tracteur routier + semi-remorque",
        "18": "Référence inutilisée depuis 2006 (transport en commun)",
        "19": "Référence inutilisée depuis 2006 (tramway)",
        "20": "Engin spécial",
        "21": "Tracteur agricole",
        "30": "Scooter < 50 cm3",
        "31": "Motocyclette > 50 cm3 et <= 125 cm3",
        "32": "Scooter > 50 cm3 et <= 125 cm3",
        "33": "Motocyclette > 125 cm3",
        "34": "Scooter > 125 cm3",
        "35": "Quad léger <= 50 cm3 (Quadricycle à moteur non carrossé)",
        "36": "Quad lourd > 50 cm3 (Quadricycle à moteur non carrossé)",
        "37": "Autobus",
        "38": "Autocar",
        "39": "Train",
        "40": "Tramway",
        "41": "3RM <= 50 cm3",
        "42": "3RM > 50 cm3 <= 125 cm3",
        "43": "3RM > 125 cm3",
        "50": "EDP à moteur",
        "60": "EDP sans moteur",
        "80": "VAE",
        "99": "Autre véhicule"
    }
    
    categorie_vehicule = st.select_slider("Catégorie du véhicule", options={i: map_categorie_vehicule(i) for i in range(100)})
    obstacle_mobile = st.select_slider("Obstacle mobile heurté", options={-1: "Non renseigné", 0: "Aucun", 1: "Piéton", 2: "Véhicule", 4: "Véhicule sur rail", 5: "Animal domestique", 6: "Animal sauvage", 9: "Autre"})
    type_motorisation = st.select_slider("Type de motorisation du véhicule", options={-1: "Non renseigné", 0: "Inconnue", 1: "Hydrocarbures", 2: "Hybride électrique", 3: "Electrique", 4: "Hydrogène", 5: "Humaine", 6: "Autre"})
    categorie_route = st.select_slider("Catégorie de route", options={1: "Autoroute", 2: "Route nationale", 3: "Route Départementale", 4: "Voie Communales", 5: "Hors réseau public", 6: "Parc de stationnement ouvert à la circulation publique", 7: "Routes de métropole urbaine", 9: "Autre"})
    regime_circulation = st.select_slider("Régime de circulation", options={-1: "Non renseigné", 1: "A sens unique", 2: "Bidirectionnelle", 3: "A chaussées séparées", 4: "Avec voies d’affectation variable"})
    etat_surface = st.select_slider("État de la surface", options={-1: "Non renseigné", 1: "Normale", 2: "Mouillée", 3: "Flaques", 4: "Inondée", 5: "Enneigée", 6: "Boue", 7: "Verglacée", 8: "Corps gras – huile", 9: "Autre"})
    situation_accident = st.select_slider("Situation de l’accident", options={-1: "Non renseigné", 0: "Aucun", 1: "Sur chaussée", 2: "Sur bande d’arrêt d’urgence", 3: "Sur accotement", 4: "Sur trottoir", 5: "Sur piste cyclable", 6: "Sur autre voie spéciale", 8: "Autres"})
    vitesse_max_autorisee = st.slider("Vitesse maximale autorisée", min_value=0, max_value=300, step=1)
    lumiere = st.select_slider("Lumière", options={1: "Plein jour", 2: "Crépuscule ou aube", 3: "Nuit sans éclairage public", 4: "Nuit avec éclairage public non allumé", 5: "Nuit avec éclairage public allumé"})
    commune = st.text_input("Commune (Code INSEE)")
    localisation = st.select_slider("Localisation", options={1: "Hors agglomération", 2: "En agglomération"})
    intersection = st.select_slider("Intersection", options={1: "Hors intersection", 2: "Intersection en X", 3: "Intersection en T", 4: "Intersection en Y", 5: "Intersection à plus de 4 branches", 6: "Giratoire", 7: "Place", 8: "Passage à niveau", 9: "Autre intersection"})
    conditions_atmospheriques = st.select_slider("Conditions atmosphériques", options={-1: "Non renseigné", 1: "Normale", 2: "Pluie légère", 3: "Pluie forte", 4: "Neige - grêle", 5: "Brouillard - fumée", 6: "Vent fort - tempête", 7: "Temps éblouissant", 8: "Temps couvert", 9: "Autre"})
    type_collision = st.select_slider("Type de collision", options={-1: "Non renseigné", 1: "Deux véhicules - frontale", 2: "Deux véhicules – par l’arrière", 3: "Deux véhicules – par le coté", 4: "Trois véhicules et plus – en chaîne", 5: "Trois véhicules et plus - collisions multiples", 6: "Autre collision", 7: "Sans collision"})
    latitude = st.slider("Latitude", min_value=-90.0, max_value=90.0, step=0.001)
    longitude = st.slider("Longitude", min_value=-180.0, max_value=180.0, step=0.001)

    st.write("")  # Ajouter de l'espace vertical pour créer une nouvelle ligne
    if st.button("Valider"):
        # Effectuer le traitement ici
        pass

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
