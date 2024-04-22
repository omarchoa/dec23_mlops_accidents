import streamlit as st

def main():
    st.title('SHIELD: Prediction of Road Accident Priority Levels')

    # Menu in the sidebar
    st.sidebar.title('Menu')
    st.sidebar.markdown("[Home](#home)", unsafe_allow_html=True)
    st.sidebar.markdown("[Features](#features)", unsafe_allow_html=True)

    # Afficher la page correspondante en fonction de la sélection
    selected_page = st.sidebar.button("Home")

    if selected_page:
        show_homepage()

def show_homepage():
    st.write('Welcome to SHIELD. This application allows you to predict road accident priority levels.')

if __name__ == '__main__':
    main()
