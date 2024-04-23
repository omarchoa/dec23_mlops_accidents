import streamlit as st

def main():  
    
    selected_home = st.sidebar.button("Home")
    selected_features = st.sidebar.button("Features")

    # Determine which page to display based on the selected button
    if selected_home:
        st.session_state.selected_page = "Home"
    elif selected_features:
        st.session_state.selected_page = "Features"

    # Display the corresponding page
    if "selected_page" not in st.session_state:
        st.session_state.selected_page = "Home"  # Default to Home page

    if st.session_state.selected_page == "Home":
        show_homepage()
    elif st.session_state.selected_page == "Features":
        show_features()

def show_homepage():
    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        st.image("/mount/src/dec23_mlops_accidents/streamlit/images/bouclier.png")
    st.write("")  # Ajouter un espace vertical pour créer une nouvelle ligne
    st.markdown("<h1 style='text-align:center;'>Welcome to SHIELD</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;'>This application allows you to predict road accident priority levels.</p>", unsafe_allow_html=True)
    
def show_features():
    st.markdown("<h1 id='features' style='text-align: center;'>Accident Features</h1>", unsafe_allow_html=True)

    # Features
    today = st.date_input("", value=None, min_value=None, max_value=None, key=None)
    hour = st.slider("Hour", min_value=0, max_value=23, step=1)
    dep = st.slider("Dep", min_value=1, max_value=100, step=1)
    place = st.slider("Place", min_value=0, max_value=100, step=1)
    nb_victim = st.slider("Number of Victims", min_value=0, max_value=100, step=1)
    nb_vehicules = st.slider("Number of Vehicles", min_value=0, max_value=100, step=1)
    catu = st.slider("Catu", min_value=0, max_value=10, step=1)

    # Display "Sexe" as clickable words
    st.write("Sexe:")
    male_clicked = st.markdown("Male()", unsafe_allow_html=True)
    female_clicked = st.markdown("Female()", unsafe_allow_html=True)
    
    sexe = st.selectbox("Sexe", options=["Male", "Female"], help="Select gender")
    sexe = st.selectbox("Sexe", options=["Male", "Female"])
    secu1 = st.slider("Secu1", min_value=0.0, max_value=10.0, step=0.1)
    victim_age = st.slider("Victim Age", min_value=0, max_value=100, step=1)
    catv = st.slider("Catv", min_value=0, max_value=10, step=1)
    obsm = st.slider("Obsm", min_value=0, max_value=10, step=1)
    motor = st.slider("Motor", min_value=0, max_value=10, step=1)
    catr = st.slider("Catr", min_value=0, max_value=10, step=1)
    circ = st.slider("Circ", min_value=0, max_value=10, step=1)
    surf = st.slider("Surf", min_value=0, max_value=10, step=1)
    situ = st.slider("Situ", min_value=0, max_value=10, step=1)
    vma = st.slider("Vma", min_value=0, max_value=100, step=1)
    lum = st.slider("Lum", min_value=0, max_value=10, step=1)
    com = st.slider("Com", min_value=1, max_value=100000, step=1)
    agg_ = st.slider("Agg", min_value=0, max_value=10, step=1)
    inter = st.slider("Inter", min_value=0, max_value=10, step=1)
    atm = st.slider("Atm", min_value=0, max_value=10, step=1)
    col = st.slider("Col", min_value=0, max_value=10, step=1)
    lat = st.slider("Lat", min_value=0.0, max_value=90.0, step=0.001)
    long = st.slider("Long", min_value=0.0, max_value=180.0, step=0.001)

    st.write("")  # Add vertical space to create a new line
    if st.button("Validate"):
        # Perform processing here
        pass
        
if __name__ == '__main__':
    main()
