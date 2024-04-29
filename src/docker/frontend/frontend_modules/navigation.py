# imports
import streamlit as st
from frontend_modules.data_download_prep import data_download_prep_run
from frontend_modules.home import home
from frontend_modules.prediction import prediction_call, prediction_test
from frontend_modules.scoring import scoring_label_prediction
from frontend_modules.status import status
from frontend_modules.users import users_all, users_register, users_remove


# define button actions function
def button_actions():

    ## home
    if st.session_state["page"] == "home":
        home()

    ## status
    if st.session_state["page"] == "status":
        status()

    ## logout
    if st.session_state["page"] == "logout":
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

    ## users all
    if st.session_state["page"] == "users_all":
        users_all()

    ## users register
    if st.session_state["page"] == "users_register":
        users_register()

    ## users remove
    if st.session_state["page"] == "users_remove":
        users_remove()

    ## data download prep run
    if st.session_state["page"] == "data_download_prep_run":
        data_download_prep_run()

    ## prediction test
    if st.session_state["page"] == "prediction_test":
        prediction_test()

    ## prediction call
    if st.session_state["page"] == "prediction_call":
        prediction_call()

    ## scoring label prediction
    if st.session_state["page"] == "scoring_label_prediction":
        scoring_label_prediction()
