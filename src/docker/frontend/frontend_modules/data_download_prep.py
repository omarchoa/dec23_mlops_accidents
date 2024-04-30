# imports
import requests
import streamlit as st


# define data download prep run function
def run():

    ## display page title
    st.title(body="Télécharger et préparer des données")

    ## get input data
    start_year = st.selectbox(label="Année de début", options=list(range(2005, 2023)))
    end_year = st.selectbox(label="Année de fin", options=list(range(start_year, 2023)))

    ## when user clicks on action button
    if st.button(label="Valider") == True:

        ### convert input data to format expected by api gateway and `data-download-prep` microservice
        year_range = {
            "start_year": start_year,
            "end_year": end_year,
        }

        ### get authentication string from session state
        authentication_string = st.session_state["authentication_string"]

        ### display processing message
        with st.status(
            label="Téléchargement et préparation des données en cours..."
        ) as status:

            #### send input data to `data-download-prep` microservice via api gateway
            response = requests.post(
                url="http://gateway:8001/data-download-prep/run",
                json=year_range,
                headers=authentication_string,
            )

            #### display complete message
            status.update(
                label="Téléchargement et préparation des données terminés.",
                state="complete",
            )

        ### display `data-download-prep` microservice response
        st.success(response.text)
