# imports
import requests
import streamlit as st


# define training train function
def train():

    ## display page title
    st.title(body="Entraîner le modèle")

    ## get authentication string from session state
    authentication_string = st.session_state["authentication_string"]

    ## display action message
    st.write("Cliquez sur le bouton ci-dessous pour entraîner le modèle.")

    ## when user clicks on action button
    if st.button(label="Valider") == True:

        ### display processing message
        with st.status(label="Entraînement du modèle en cours...") as status:

            #### send authentication string to `training` microservice via api gateway
            response = requests.get(
                url="http://gateway:8001/training/train",
                headers=authentication_string,
            )

            #### display complete message
            status.update(label="Entraînement du modèle terminé.", state="complete")

        ### display `training` microservice response
        st.success(response.text)
