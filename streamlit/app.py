import streamlit as st

def main():
    st.title('SHIELD : Safety Hazard Identification and Emergency Law Deployment')

    # Collecte des caractéristiques
    st.sidebar.title('Caractéristiques de l\'accident')
    feature1 = st.sidebar.text_input('Caractéristique 1')
    feature2 = st.sidebar.text_input('Caractéristique 2')
    # etc pour les autres caractéristiques

if __name__ == '__main__':
    main()
