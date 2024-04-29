# imports
import streamlit as st


# define home function
def home():

    ## display app logo
    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        st.image("/home/shield/frontend/frontend_images/bouclier.png")

    ## display home page text
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
