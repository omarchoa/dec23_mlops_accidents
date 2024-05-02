# imports
import requests
import streamlit as st
from frontend_modules import prediction_dictionaries as dicts


# define prediction test function
def test():

    ## display page text
    st.title(body="Effectuer une prédiction test")

    ## get authentication string from session state
    authentication_string = st.session_state["authentication_string"]

    ## display action message
    st.write("Cliquez sur le bouton ci-dessous pour effectuer une prédiction test.")

    ## when user clicks on action button
    if st.button(label="Valider") == True:

        ### display processing message
        with st.status(label="Prédiction en cours...") as status:

            #### send authentication string to `prediction` microservice via api gateway
            response = requests.get(
                url="http://gateway:8001/prediction/test",
                headers=authentication_string,
            )

            #### display complete message
            status.update(label="Prédiction terminée.", state="complete")

        ### display `prediction` microservice response
        if "non" in response.text:
            st.success(response.text)
        else:
            st.warning(response.text)


# define prediction call function
def call():

    ## display page text
    st.title(body="Effectuer une prédiction réelle")

    ## get input data for fiche baac, rubrique caractéristiques
    st.header(body="Caractéristiques")
    date_accident = st.date_input(
        label="Date de l'accident",
        value="today",
    )
    heure_accident = st.time_input(
        label="Heure de l'accident",
        value="now",
        step=3600,
    )
    lumiere = st.selectbox(
        label="Conditions d’éclairage dans lesquelles l'accident s'est produit",
        options=dicts.lum.keys(),
    )
    departement = st.selectbox(
        label="Département",
        options=dicts.dep.values(),
        placeholder="Sélectionnez un département",
    )
    commune = st.selectbox(
        label="Commune",
        options=[com for com in dicts.com.values() if com[:2] == departement[:2]],
        placeholder="Sélectionnez une commune",
    )
    localisation = st.selectbox(
        label="Localisation",
        options=dicts.agg_.keys(),
    )
    intersection = st.selectbox(
        label="Intersection",
        options=dicts.inter.keys(),
    )
    conditions_atmospheriques = st.selectbox(
        label="Conditions atmosphériques",
        options=dicts.atm.keys(),
    )
    type_collision = st.selectbox(
        label="Type de collision",
        options=dicts.col.keys(),
    )
    latitude = st.number_input(
        label="Latitude",
        min_value=-90.0,
        max_value=90.0,
        step=0.001,
    )
    longitude = st.number_input(
        label="Longitude",
        min_value=-180.0,
        max_value=180.0,
        step=0.001,
    )

    ## get input data for fiche baac, rubrique lieux
    st.header(body="Lieux")
    categorie_route = st.selectbox(
        label="Catégorie de route",
        options=dicts.catr.keys(),
    )
    regime_circulation = st.selectbox(
        label="Régime de circulation",
        options=dicts.circ.keys(),
    )
    etat_surface = st.selectbox(
        label="État de la surface",
        options=dicts.surf.keys(),
    )
    situation_accident = st.selectbox(
        label="Situation de l’accident",
        options=dicts.situ.keys(),
    )
    vitesse_max_autorisee = st.number_input(
        label="Vitesse maximale autorisée sur le lieu et au moment de l’accident",
        min_value=0,
        max_value=300,
        step=1,
    )

    ## get input data for fiche baac, rubrique véhicules
    st.header(body="Véhicules")
    categorie_vehicule = st.selectbox(
        label="Catégorie du véhicule",
        options=dicts.catv.keys(),
    )
    obstacle_mobile = st.selectbox(
        label="Obstacle mobile heurté",
        options=dicts.obsm.keys(),
    )
    type_motorisation = st.selectbox(
        label="Type de motorisation du véhicule",
        options=dicts.motor.keys(),
    )
    nombre_vehicules = st.number_input(
        label="Nombre de véhicules impliqués",
        min_value=0,
        max_value=100,
        step=1,
    )

    ## get input data for fiche baac, rubrique usagers
    st.header(body="Usagers")
    place_occupee = st.slider(
        label="Place occupée dans le véhicule par l'usager au moment de l'accident",
        min_value=0,
        max_value=10,
        step=1,
        help="Le détail est donné par l’illustration ci-dessous. Pour un piéton, sélectionnez « 10 ».",
    )
    st.image(
        image="/home/shield/frontend/frontend_images/place_occupee.png",
        # caption="Illustration des places occupées dans un véhicule",
        use_column_width=True,
    )
    categorie_usager = st.selectbox(
        label="Catégorie d'usager",
        options=dicts.catu.keys(),
    )
    sexe_usager = st.selectbox(
        label="Sexe de l'usager",
        options=dicts.sexe.keys(),
    )
    age_usager = st.number_input(
        label="Âge de l'usager",
        min_value=0,
        max_value=100,
        step=1,
    )
    equipement_securite = st.selectbox(
        label="Équipement de sécurité présent et utilisé",
        options=dicts.secu1.keys(),
    )
    nombre_usagers = st.number_input(
        label="Nombre d'usagers impliqués",
        min_value=0,
        max_value=25,
        step=1,
    )

    st.write("")

    ## when user clicks on action button
    if st.button(label="Valider") == True:

        ## replace corsica codes
        if departement in dicts.corse.keys():
            departement = dicts.corse[departement]

        ## convert input data to format expected by api gateway and `prediction` microservice
        input_data_pred_call = {
            "place": int(place_occupee),
            "catu": int(dicts.catu[categorie_usager]),
            "sexe": int(dicts.sexe[sexe_usager]),
            "secu1": float(dicts.secu1[equipement_securite]),
            "year_acc": int(date_accident.year),
            "victim_age": int(age_usager),
            "catv": int(dicts.catv[categorie_vehicule]),
            "obsm": int(dicts.obsm[obstacle_mobile]),
            "motor": int(dicts.motor[type_motorisation]),
            "catr": int(dicts.catr[categorie_route]),
            "circ": int(dicts.circ[regime_circulation]),
            "surf": int(dicts.surf[etat_surface]),
            "situ": int(dicts.situ[situation_accident]),
            "vma": int(vitesse_max_autorisee),
            "jour": int(date_accident.day),
            "mois": int(date_accident.month),
            "lum": int(dicts.lum[lumiere]),
            "dep": int(departement.split(" ")[0]),
            "com": int(commune.split(" ")[0]),
            "agg_": int(dicts.agg_[localisation]),
            "inter": int(dicts.inter[intersection]),
            "atm": int(dicts.atm[conditions_atmospheriques]),
            "col": int(dicts.col[type_collision]),
            "lat": float(latitude),
            "long": float(longitude),
            "hour": int(heure_accident.hour),
            "nb_victim": int(nombre_usagers),
            "nb_vehicules": int(nombre_vehicules),
        }

        ## get authentication string from session state
        authentication_string = st.session_state["authentication_string"]

        ### display processing message
        with st.status(label="Prédiction en cours...") as status:

            #### send input data and authentication string to `prediction` microservice via api gateway
            response = requests.post(
                url="http://gateway:8001/prediction/call",
                json=input_data_pred_call,
                headers=authentication_string,
            )

            #### display complete message
            status.update(label="Prédiction terminée.", state="complete")

        ### display `prediction` microservice response
        if "non" in response.text:
            st.success(response.text)
        else:
            st.warning(response.text)
