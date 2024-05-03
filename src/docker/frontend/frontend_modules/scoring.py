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
    reference = st.text_input(label="Référence de la prédiction")
    priority = st.radio(
        "Caractère de l'intervention", ("Prioritaire", "Non prioritaire")
    )

    ## convert input data to format expected by api gateway and `scoring` microservice
    y_true = 1 if priority == "Prioritaire" else 0
    input_data_label_pred = {"request_id": reference, "y_true": y_true}

    ## get authentication string from session state
    authentication_string = st.session_state["authentication_string"]

    ## when user clicks on action button
    if st.button("Envoyer") == True:

        ### display processing message
        with st.status(label="Mise à jour de la prédiction en cours...") as status:

            #### send input data and authentication string to `scoring` microservice, /label-prediction endpoint via api gateway
            response = requests.post(
                url="http://gateway:8001/scoring/label-prediction",
                json=input_data_label_pred,
                headers=authentication_string,
            )

            #### send authentication string to `scoring` microservice, /update-f1-score endpoint via api gateway
            requests.get(
                url="http://gateway:8001/scoring/update-f1-score",
                headers=authentication_string,
            )

            #### display complete message
            status.update(
                label="Mise à jour de la prédiction terminée.", state="complete"
            )

        ### display `scoring` microservice, /label-prediction endpoint response
        if "Merci" in response.text:
            st.success(response.text)
        elif "Veuillez" in response.text:
            st.error(response.text)


# define scoring update f1 score function
def update_f1_score():

    ## display page title
    st.title("Mettre à jour le F1 score")

    ## get authentication string from session state
    authentication_string = st.session_state["authentication_string"]

    ## display action message
    st.write("Cliquez sur le bouton ci-dessous pour mettre à jour le F1 score.")

    ## when user clicks on action button
    if st.button(label="Valider") == True:

        ### display processing message
        with st.status(label="Mise à jour du F1 score en cours...") as status:

            #### send authentication string to `scoring` microservice via api gateway
            response = requests.get(
                url="http://gateway:8001/scoring/update-f1-score",
                headers=authentication_string,
            )

            #### display complete message
            status.update(label="Mise à jour du F1 score terminée.", state="complete")

        ### display `scoring` microservice response
        st.success(body=f"F1 score {response.text} enregistré avec succès.")


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

    ## get f1 scores dataframe
    df = get_f1_scores_helper()

    ## compute delta between latest and second latest f1 scores
    latest_f1_score = df["f1-score"].iloc[-1]
    if df.shape[0] == 1:
        delta = 0
    else:
        second_latest_f1_score = df["f1-score"].iloc[-2]
        delta = latest_f1_score - second_latest_f1_score

    ## display latest f1 score
    st.metric(label="F1 score", value=latest_f1_score, delta=delta)


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
        labels={"timestamp": "Timestamp", "f1-score": "F1 score"},
    )
    st.plotly_chart(fig)
