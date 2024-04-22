import streamlit as st

def main():
    st.title('SHIELD: Prediction of Road Accident Priority Levels')

    # Menu in the sidebar
    st.sidebar.title('Menu')
    st.sidebar.markdown("[Home](#home)", unsafe_allow_html=True)
    st.sidebar.markdown("[Features](#features)", unsafe_allow_html=True)

    # Afficher la page correspondante en fonction de la sélection
    selected_home = st.sidebar.button("Home")
    selected_features = st.sidebar.button("Features")

    if selected_home:
        show_homepage()
    if selected_features:
        show_features()

def show_homepage():
    st.write('Welcome to SHIELD. This application allows you to predict road accident priority levels.')

def show_features():
    st.markdown("<h1 id='features' style='text-align: center;'>Accident Features</h1>", unsafe_allow_html=True)
    feature1 = st.text_input('Feature 1')
    feature2 = st.text_input('Feature 2')

if __name__ == '__main__':
    main()
