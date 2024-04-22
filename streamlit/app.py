import streamlit as st

def main():
    st.title('SHIELD: Prédiction des niveaux de priorité des accidents de la route')

    st.sidebar.title('Menu')
    page1 = st.sidebar.text_input('Page 1')

    st.markdown('<style>div.Widget.row-widget.stRadio > div{flex-direction: row;}</style>', unsafe_allow_html=True)

    st.markdown("<h1 style='text-align: center;'>Caractéristiques de l'accident</h1>", unsafe_allow_html=True)
    feature1 = st.text_input('Caractéristique 1')
    feature2 = st.text_input('Caractéristique 2')

if __name__ == '__main__':
    main()
