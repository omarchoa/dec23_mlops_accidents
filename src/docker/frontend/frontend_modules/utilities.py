import pandas as pd
import requests
import streamlit as st
from frontend_modules import scoring


def status():
    st.title("État du système")

    component_list = [
        "gateway",
        "users",
        "data-download-prep",
        "training",
        "prediction",
        "scoring",
    ]

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Composant")

    with col2:
        st.subheader("État")

    for microservice in component_list:
        response = requests.get(url=f"http://gateway:8001/{microservice}/status")
        with col1:
            st.code(microservice)
        if response.status_code == 200:
            with col2:
                st.success("Disponible")
        else:
            with col2:
                st.error("Non disponible")


def logs():
    st.title("Journalisation")

    log_file_directory_01 = "/home/shield/logs/"
    log_file_directory_02 = "/home/shield/logs_gateway/"

    log_file_name_list = [
        "data-download-prep",
        "train",
        "preds_test",
        "preds_call",
        "preds_labeled",
        "f1_scores",
        "crontab",
        "retrain",
    ]

    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs(log_file_name_list)

    # data-download-prep.jsonl
    with tab1:
        log_file = log_file_directory_01 + log_file_name_list[0] + ".jsonl"
        df = pd.read_json(log_file, lines=True)
        df["request_id"] = df["request_id"].astype(str)
        st.dataframe(df)

    # train.jsonl
    with tab2:
        log_file = log_file_directory_01 + log_file_name_list[1] + ".jsonl"
        df = pd.read_json(log_file, lines=True)

        df_estimator_parameters = pd.json_normalize(df["estimator_parameters"])
        df_feature_importances = pd.json_normalize(df["feature_importances"])
        df = df.drop(columns=["estimator_parameters", "feature_importances"])
        df = df.join(df_estimator_parameters.add_prefix("estim_param_"))
        df = df.join(df_feature_importances.add_prefix("feat_impt_"))

        df["request_id"] = df["request_id"].astype(str)
        st.dataframe(df)

    # preds_*.jsonl
    tabs = [tab3, tab4, tab5]
    log_files = [
        log_file_directory_01 + log_file_name_list[i] + ".jsonl" for i in range(2, 5)
    ]
    for tab, log_file in zip(tabs, log_files):
        with tab:
            df = pd.read_json(log_file, lines=True)

            df_input_features = pd.json_normalize(df["input_features"])
            df = df.drop(columns=["input_features"])
            df = df.join(df_input_features.add_prefix("input_feat_"))

            df["request_id"] = df["request_id"].astype(str)
            st.dataframe(df)

    # f1 scores
    with tab6:
        df = scoring.get_f1_scores_helper()
        st.dataframe(df)

    # crontab.csv
    with tab7:
        log_file = log_file_directory_02 + log_file_name_list[6] + ".csv"
        with open(log_file, "r") as file:
            file_content = file.read()
        st.code(file_content, language="csv")

    # training.csv
    with tab8:
        log_file = log_file_directory_02 + "training" + ".csv"
        with open(log_file, "r") as file:
            file_content = file.read()
        st.code(file_content, language="csv")
