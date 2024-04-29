# imports
from io import StringIO

import pandas as pd
import plotly.express as px
import requests
import streamlit as st


# define scoring label prediction function
def scoring_label_prediction():

    ## display label prediction page text
    st.markdown(
        "<h1 id='features' style='text-align: center;'>Valider ou corriger une prédiction</h1>",
        unsafe_allow_html=True,
    )

    ## get input data
    accident_reference = st.text_input("Référence de l'accident")
    accident_gravity = st.radio("Gravité de l'accident", ("Grave", "Non grave"))

    ## convert input data to format expected by api gateway and `scoring` microservice
    y_true = 1 if accident_gravity == "Grave" else 0
    input_data_label_pred = {"request_id": accident_reference, "y_true": y_true}

    ## get authentication string from session state
    authentication_string = st.session_state["authentication_string"]

    ## when user clicks on action button
    if st.button("Soumettre la correction") == True:

        ### send input data and authentication string to `scoring` microservice via api gateway
        response = requests.post(
            url="http://gateway:8001/scoring/label-prediction",
            json=input_data_label_pred,
            headers=authentication_string,
        )

        ### display `scoring` microservice response
        if "Merci" in response.text:
            st.success(response.text)
        elif "Veuillez" in response.text:
            st.error(response.text)


# define scoring plot f1 scores function
def scoring_plot_f1_scores():

    ## display plot f1 scores page text
    st.markdown(
        "<h1 id='graph' style='text-align: center;'>Graphique de Prédiction</h1>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<p style='text-align:left;'>Afficher un graphique où chaque nouvelle prédiction ajoute un point à une courbe illustrant l'amélioration des performances au fil du temps.</p>",
        unsafe_allow_html=True,
    )

    ## get authentication string from session state
    authentication_string = st.session_state["authentication_string"]

    ## send authentication string to `scoring` microservice via api gateway
    response = requests.get(
        url="http://gateway:8001/scoring/get-f1-scores",
        headers=authentication_string,
    )

    ## convert `scoring` microservice response to pandas dataframe
    response_stream = response.json()
    data_string = StringIO(response_stream)
    df = pd.read_table(filepath_or_buffer=data_string, sep=";")
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="s", origin="1970-01-01")
    df.set_index(keys="timestamp", inplace=True)

    ## plot dataframe data as plotly line chart
    fig = px.line(
        df, x=df.index, y="f1-score", labels={"x": "Timestamp", "y": "F1-score"}
    )
    st.plotly_chart(fig)
