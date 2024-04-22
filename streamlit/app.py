import streamlit as st

def main():
    st.title('SHIELD: Prediction of Road Accident Priority Levels')

    # Menu in the sidebar
    st.sidebar.title('Menu')
    selected_page = st.sidebar.radio('Select a page', ['Home', 'Features'])

    # Display the corresponding page based on the selection
    if selected_page == 'Home':
        show_homepage()
    elif selected_page == 'Features':
        show_features()

def show_homepage():
    st.write('Welcome to SHIELD. This application allows you to predict road accident priority levels.')

def show_features():
    st.markdown("<h1 style='text-align: center;'>Accident Features</h1>", unsafe_allow_html=True)
    feature1 = st.text_input('Feature 1')
    feature2 = st.text_input('Feature 2')

if __name__ == '__main__':
    main()
