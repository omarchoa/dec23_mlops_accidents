# imports
import streamlit as st
from frontend_modules import (
    data_download_prep,
    home,
    prediction,
    scoring,
    training,
    users,
    utilities,
)


# define button actions function
def button_actions():

    ## home
    if st.session_state["page"] == "home":
        home.home()

    ## logout
    if st.session_state["page"] == "logout":
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

    ## status
    if st.session_state["page"] == "status":
        utilities.status()

    ## logs
    if st.session_state["page"] == "logs":
        utilities.logs()

    ## lineage
    if st.session_state["page"] == "lineage":
        utilities.lineage()

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

    ## scoring update f1 score
    if st.session_state["page"] == "scoring_update_f1_score":
        scoring.update_f1_score()

    ## scoring get latest f1 score
    if st.session_state["page"] == "scoring_get_latest_f1_score":
        scoring.get_latest_f1_score()

    ## scoring get f1 scores
    if st.session_state["page"] == "scoring_get_f1_scores":
        scoring.get_f1_scores()

    ## scoring plot f1 scores
    if st.session_state["page"] == "scoring_plot_f1_scores":
        scoring.plot_f1_scores()
