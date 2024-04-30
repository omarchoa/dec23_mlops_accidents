import requests
import streamlit as st


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
