# imports
import streamlit as st
from frontend_modules.home import home
from frontend_modules.prediction import prediction_call, prediction_test
from frontend_modules.scoring import scoring_label_prediction
from frontend_modules.status import status


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

    ## prediction test
    if st.session_state["page"] == "prediction_test":
        prediction_test()

    ## prediction call
    if st.session_state["page"] == "prediction_call":
        prediction_call()

    ## scoring label prediction
    if st.session_state["page"] == "scoring_label_prediction":
        scoring_label_prediction()
