# imports
import streamlit as st
from frontend_modules import (
    data_download_prep,
    home,
    prediction,
    scoring,
    status,
    training,
    users,
)


# define button actions function
def button_actions():

    ## home
    if st.session_state["page"] == "home":
        home.home()

    ## status
    if st.session_state["page"] == "status":
        status.status()

    ## logout
    if st.session_state["page"] == "logout":
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

    ## users all
    if st.session_state["page"] == "users_all":
        users.all()

    ## users register
    if st.session_state["page"] == "users_register":
        users.register()

    ## users remove
    if st.session_state["page"] == "users_remove":
        users.remove()

    ## data download prep run
    if st.session_state["page"] == "data_download_prep_run":
        data_download_prep.run()

    ## training train
    if st.session_state["page"] == "training_train":
        training.train()

    ## prediction test
    if st.session_state["page"] == "prediction_test":
        prediction.test()

    ## prediction call
    if st.session_state["page"] == "prediction_call":
        prediction.call()

    ## scoring label prediction
    if st.session_state["page"] == "scoring_label_prediction":
        scoring.label_prediction()

    ## scoring get f1 scores
    if st.session_state["page"] == "scoring_get_f1_scores":
        scoring.get_f1_scores()

    ## scoring plot f1 scores
    if st.session_state["page"] == "scoring_plot_f1_scores":
        scoring.plot_f1_scores()
