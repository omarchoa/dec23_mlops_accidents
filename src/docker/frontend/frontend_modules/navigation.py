# imports
import streamlit as st
from frontend_modules.home import home


# define button actions function
def button_actions():

    ## home
    if st.session_state["button_home"] == True:
        ### display home page
        home()

    ## logout
    if st.session_state["button_logout"] == True:

        ### unauthenticate user
        st.session_state["authenticated"] = False

        ### clear page
        st.empty()

        ### rerun page to display unauthenticated content
        st.rerun()
