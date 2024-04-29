# imports
import frontend_modules.prediction_dictionaries as dicts
import requests
import streamlit as st


# define predict function
def predict():

    ## display prediction page text
    st.markdown(
        "<h1 id='features' style='text-align: center;'>Ajouter un accident</h1>",
        unsafe_allow_html=True,
    )

    ## get input data
    jour_accident = st.date_input(
        "Jour de l'accident",
        value=None,
        min_value=None,
        max_value=None,
        key=None,
    )
    heure_accident = st.slider(
        "Heure de l'accident",
        min_value=0,
        max_value=23,
        step=1,
    )
    departement = st.text_input("Département (Code INSEE)")
    place_occupée = st.slider(
        "Place occupée dans le véhicule",
        min_value=0,
        max_value=10,
        step=1,
        help="10 – Piéton (non applicable)",
    )
    nombre_victimes = st.slider(
        "Nombre de victimes",
        min_value=0,
        max_value=25,
        step=1,
    )
    nombre_vehicules = st.text_input("Nombre de véhicules impliqués")
    categorie_usager = st.selectbox(
        "Catégorie d'usager",
        options=dicts.catu.keys(),
    )
    sexe_usager = st.selectbox(
        "Sexe de l'usager",
        options=dicts.sexe.keys(),
    )
    equipement_securite = st.selectbox(
        "Équipement de sécurité",
        options=dicts.secu1.keys(),
    )
    age_victime = st.slider(
        "Âge de la ou des victimes",
        min_value=0,
        max_value=100,
        step=1,
    )
    categorie_vehicule = st.selectbox(
        "Catégorie du véhicule",
        options=dicts.catv.keys(),
    )
    obstacle_mobile = st.selectbox(
        "Obstacle mobile heurté",
        options=dicts.obsm.keys(),
    )
    type_motorisation = st.selectbox(
        "Type de motorisation du véhicule",
        options=dicts.motor.keys(),
    )
    categorie_route = st.selectbox(
        "Catégorie de route",
        options=dicts.catr.keys(),
    )
    regime_circulation = st.selectbox(
        "Régime de circulation",
        options=dicts.circ.keys(),
    )
    etat_surface = st.selectbox(
        "État de la surface",
        options=dicts.surf.keys(),
    )
    situation_accident = st.selectbox(
        "Situation de l’accident",
        options=dicts.situ.keys(),
    )
    vitesse_max_autorisee = st.slider(
        "Vitesse maximale autorisée",
        min_value=0,
        max_value=300,
        step=1,
    )
    lumiere = st.selectbox(
        "Lumière",
        options=dicts.lum.keys(),
    )
    commune = st.text_input("Commune (Code INSEE)")
    localisation = st.selectbox(
        "Localisation",
        options=dicts.agg_.keys(),
    )
    intersection = st.selectbox(
        "Intersection",
        options=dicts.inter.keys(),
    )
    conditions_atmospheriques = st.selectbox(
        "Conditions atmosphériques",
        options=dicts.atm.keys(),
    )
    type_collision = st.selectbox(
        "Type de collision",
        options=dicts.col.keys(),
    )
    latitude = st.slider(
        "Latitude",
        min_value=-90.0,
        max_value=90.0,
        step=0.001,
    )
    longitude = st.slider(
        "Longitude",
        min_value=-180.0,
        max_value=180.0,
        step=0.001,
    )

    st.write("")

    ## convert input data to format expected by api gateway and `prediction` microservice
    input_data_pred_call = {
        "place": int(place_occupée),
        "catu": int(dicts.catu[categorie_usager]),
        "sexe": int(dicts.sexe[sexe_usager]),
        "secu1": float(dicts.secu1[equipement_securite]),
        "year_acc": int(jour_accident.year),
        "victim_age": int(age_victime),
        "catv": int(dicts.catv[categorie_vehicule]),
        "obsm": int(dicts.obsm[obstacle_mobile]),
        "motor": int(dicts.motor[type_motorisation]),
        "catr": int(dicts.catr[categorie_route]),
        "circ": int(dicts.circ[regime_circulation]),
        "surf": int(dicts.surf[etat_surface]),
        "situ": int(dicts.situ[situation_accident]),
        "vma": int(vitesse_max_autorisee),
        "jour": int(jour_accident.day),
        "mois": int(jour_accident.month),
        "lum": int(dicts.lum[lumiere]),
        "dep": int(departement),
        "com": int(commune),
        "agg_": int(dicts.agg_[localisation]),
        "inter": int(dicts.inter[intersection]),
        "atm": int(dicts.atm[conditions_atmospheriques]),
        "col": int(dicts.col[type_collision]),
        "lat": float(latitude),
        "long": float(longitude),
        "hour": int(heure_accident),
        "nb_victim": int(nombre_victimes),
        "nb_vehicules": int(nombre_vehicules),
    }

    ## get authentication string from session state
    authentication_string = st.session_state["authentication_string"]

    ## when user clicks on action button
    if st.button("Valider") == True:

        ### send input data and authentication string to `prediction` microservice via api gateway
        response = requests.post(
            url="http://gateway:8001/prediction/call",
            json=input_data_pred_call,
            headers=authentication_string,
        )

        ### display `prediction` microservice response
        if "non" in response.text:
            st.success(response.text)
        else:
            st.warning(response.text)
