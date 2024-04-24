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
    st.markdown("<h1 style='text-align:center;'>SHIELD</h1></br><h6 style='text-align:center;'><em>Safety Hazard Identification and Emergency Law Deployment</em></h6>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;'>SHIELD est une application Python alimentée par l'IA qui utilise l'apprentissage automatique pour prédire les niveaux de priorité des accidents de la route, aidant les forces de l'ordre à optimiser les ressources et à maximiser l'impact.</p>", unsafe_allow_html=True)
    st.write("") 
    st.markdown("<p style='text-align:center;'>SHIELD est développé par <span style='color:orange;'>Fabrice Charraud, Omar Choa, Michael Deroche, Alexandre Winger</span>. <br>Cela constitue notre projet final pour le programme DataScientest Machine Learning Engineer.</p>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;'>cohort dec23_mlops // <span style='color:#6ab7ff;'>Datascientest</span></p>", unsafe_allow_html=True)

def show_features():
    st.markdown("<h1 id='features' style='text-align: center;'>Caractéristiques de l'Accident</h1>", unsafe_allow_html=True)

    # Caractéristiques
    today = st.date_input("", value=None, min_value=None, max_value=None, key=None)
    hour = st.slider("Heure", min_value=0, max_value=23, step=1)
    dep = st.slider("Département", min_value=1, max_value=100, step=1)
    place = st.slider("Lieu", min_value=0, max_value=100, step=1)
    nb_victim = st.slider("Nombre de Victimes", min_value=0, max_value=100, step=1)
    nb_vehicules = st.slider("Nombre de Véhicules", min_value=0, max_value=100, step=1)
    catu = st.slider("Catégorie d'Usager", min_value=0, max_value=10, step=1)
    sex = st.radio("Sexe", ["Homme", "Femme"], help="Sélectionner le genre")
    secu1 = st.slider("Sécurité 1", min_value=0.0, max_value=10.0, step=0.1)
    victim_age = st.slider("Âge de la Victime", min_value=0, max_value=100, step=1)
    catv = st.slider("Catégorie du Véhicule", min_value=0, max_value=10, step=1)
    obsm = st.slider("Observation Mobile", min_value=0, max_value=10, step=1)
    motor = st.slider("Motorisé", min_value=0, max_value=10, step=1)
    catr = st.slider("Catégorie de la Route", min_value=0, max_value=10, step=1)
    circ = st.slider("Circulation", min_value=0, max_value=10, step=1)
    surf = st.slider("Surface", min_value=0, max_value=10, step=1)
    situ = st.slider("Situation", min_value=0, max_value=10, step=1)
    vma = st.slider("Vitesse Maximale Autorisée", min_value=0, max_value=100, step=1)
    lum = st.slider("Luminosité", min_value=0, max_value=10, step=1)
    com = st.slider("Code Commune", min_value=1, max_value=100000, step=1)
    agg_ = st.slider("Agglomération", min_value=0, max_value=10, step=1)
    inter = st.slider("Intersection", min_value=0, max_value=10, step=1)
    atm = st.slider("Météo", min_value=0, max_value=10, step=1)
    col = st.slider("Collision", min_value=0, max_value=10, step=1)
    lat = st.slider("Latitude", min_value=0.0, max_value=90.0, step=0.001)
    long = st.slider("Longitude", min_value=0.0, max_value=180.0, step=0.001)

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
