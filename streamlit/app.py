import streamlit as st

def main():
    st.title('SHIELD: Prediction of Road Accident Priority Levels')

    # Menu in the sidebar
    st.sidebar.title('Menu')

    # Afficher la page correspondante en fonction de la sélection
    selected_home = st.sidebar.button("Home")
    selected_features = st.sidebar.button("Features")

    if selected_home:
        show_homepage()
    if selected_features:
        show_features()

def show_homepage():
    st.write('Welcome to SHIELD. This application allows you to predict road accident priority levels.')
    st.image("images/bouclier.png", caption='SHIELD Logo', use_column_width=True)

def show_features():
    st.markdown("<h1 id='features' style='text-align: center;'>Accident Features</h1>", unsafe_allow_html=True)
    
    # Caractéristiques
    place = st.slider("Place", min_value=0, max_value=100, step=1)
    catu = st.slider("Catu", min_value=0, max_value=10, step=1)
    sexe = st.slider("Sexe", min_value=0, max_value=1, step=1)
    secu1 = st.slider("Secu1", min_value=0.0, max_value=10.0, step=0.1)
    year_acc = st.slider("Year Acc", min_value=2000, max_value=2025, step=1)
    victim_age = st.slider("Victim Age", min_value=0, max_value=100, step=1)
    catv = st.slider("Catv", min_value=0, max_value=10, step=1)
    obsm = st.slider("Obsm", min_value=0, max_value=10, step=1)
    motor = st.slider("Motor", min_value=0, max_value=10, step=1)
    catr = st.slider("Catr", min_value=0, max_value=10, step=1)
    circ = st.slider("Circ", min_value=0, max_value=10, step=1)
    surf = st.slider("Surf", min_value=0, max_value=10, step=1)
    situ = st.slider("Situ", min_value=0, max_value=10, step=1)
    vma = st.slider("Vma", min_value=0, max_value=100, step=1)
    jour = st.slider("Jour", min_value=1, max_value=31, step=1)
    mois = st.slider("Mois", min_value=1, max_value=12, step=1)
    lum = st.slider("Lum", min_value=0, max_value=10, step=1)
    dep = st.slider("Dep", min_value=1, max_value=100, step=1)
    com = st.slider("Com", min_value=1, max_value=100000, step=1)
    agg_ = st.slider("Agg", min_value=0, max_value=10, step=1)
    inter = st.slider("Inter", min_value=0, max_value=10, step=1)
    atm = st.slider("Atm", min_value=0, max_value=10, step=1)
    col = st.slider("Col", min_value=0, max_value=10, step=1)
    lat = st.slider("Lat", min_value=0.0, max_value=90.0, step=0.001)
    long = st.slider("Long", min_value=0.0, max_value=180.0, step=0.001)
    hour = st.slider("Hour", min_value=0, max_value=23, step=1)
    nb_victim = st.slider("Number of Victims", min_value=0, max_value=100, step=1)
    nb_vehicules = st.slider("Number of Vehicles", min_value=0, max_value=100, step=1)

if __name__ == '__main__':
    main()
