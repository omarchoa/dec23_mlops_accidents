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
        "<h1 style='text-align: center;'> \
            SHIELD \
        </h1> \
        <h6 style='text-align: center;'> \
            <em> \
                Safety Hazard Identification and Emergency Law Deployment \
            </em> \
        </h6>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<p style='text-align:center;'> \
            SHIELD est une application Python qui utilise l'apprentissage automatique pour prédire les niveaux de priorité des accidents de la route, aidant ainsi les forces de l'ordre à optimiser leurs ressources et à maximiser leur impact. \
        </p>",
        unsafe_allow_html=True,
    )
    st.write("")
    st.markdown(
        "<p style='text-align:center;'> \
            SHIELD est développée par \
            <a href='https://github.com/FCharraud' style='color:orange;'> Fabrice Charraud </a>, \
            <a href='https://github.com/omarchoa' style='color:orange;'> Omar Choa </a>, \
            <a href='https://github.com/miklderoche' style='color:orange;'> Michael Deroche </a> et \
            <a href='https://github.com/alexandrewinger' style='color:orange;'> Alexandre Winger</a>. \
            <br> \
            Elle constitue notre projet final pour la <a href='https://datascientest.com/formation-ml-ops' style='color:#6ab7ff;'> formation MLOps de DataScientest </a>. \
        </p>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<p style='text-align:center;'> \
            dec23_mlops // <a href='https://datascientest.com/' style='color:#6ab7ff;'> DataScientest </a> \
        </p>",
        unsafe_allow_html=True,
    )
