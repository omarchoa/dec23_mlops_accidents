# imports
from io import StringIO

import pandas as pd
import plotly.express as px
import requests
import streamlit as st


# define scoring label prediction function
def label_prediction():

    ## display page title
    st.title("Valider ou corriger une prédiction")

    ## get input data
    accident_reference = st.text_input(label="Référence de la prédiction")
    accident_gravity = st.radio("Gravité de l'accident", ("Grave", "Non grave"))

    ## convert input data to format expected by api gateway and `scoring` microservice
    y_true = 1 if accident_gravity == "Grave" else 0
    input_data_label_pred = {"request_id": accident_reference, "y_true": y_true}

    ## get authentication string from session state
    authentication_string = st.session_state["authentication_string"]

    ## when user clicks on action button
    if st.button("Envoyer") == True:

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


# define scoring get f1 scores helper function
def get_f1_scores_helper():

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

    ## return dataframe
    return df


# define scoring get latest f1 score function
def get_latest_f1_score():

    ## display page title
    st.title(body="Récupérer le dernier F1 score")

    ## get authentication string from session state
    authentication_string = st.session_state["authentication_string"]

    ## send authentication string to `scoring` microservice via api gateway
    response = requests.get(
        url="http://gateway:8001/scoring/get-latest-f1-score",
        headers=authentication_string,
    )

    ## convert `scoring` microservice response to pandas dataframe
    response_stream = response.json()
    data_string = StringIO(response_stream)
    st.write(data_string.read())


# define scoring get f1 scores function
def get_f1_scores():

    ## display page title
    st.title(body="Récupérer tous les F1 scores")

    ## get f1 scores dataframe
    df = get_f1_scores_helper()

    ## display dataframe
    st.dataframe(df)


# define scoring plot f1 scores function
def plot_f1_scores():

    ## display page title
    st.title(body="Visualiser l'évolution des F1 scores")

    ## get f1 scores dataframe
    df = get_f1_scores_helper()

    ## plot dataframe data as plotly line chart
    fig = px.line(
        df,
        x=df.index,
        y="f1-score",
        labels={"timestamp": "Timestamp", "f1-score": "F1-score"},
    )
    st.plotly_chart(fig)
