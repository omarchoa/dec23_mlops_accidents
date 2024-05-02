# imports
import requests
import streamlit as st
from frontend_modules import prediction_dictionaries as dicts
from frontend_modules import utilities


# define feature importances function
def feature_importances(model: str = "current", n: int = 5):

    ## load feature importances from logs
    feature_importances = utilities.logs_feature_importances(model)

    ## convert values to percentages
    feature_importances_percentages = (
        feature_importances / feature_importances.sum() * 100
    ).round(2)

    ## get top n features
    feature_importances_percentages_top_n = feature_importances_percentages.sort_values(
        ascending=False
    ).head(n)

    ## rename rows & columns for better human readability
    feature_importances_percentages_top_n_renamed = (
        feature_importances_percentages_top_n.rename(index=dicts.field_names)
    ).rename("Pourcentage")

    ## display top n features
    st.info(f"Les {n} caractéristiques qui ont le plus pesé dans la prédiction sont :")
    st.dataframe(feature_importances_percentages_top_n_renamed)


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

        ### display feature importances
        feature_importances(model="current", n=5)


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
        label=dicts.field_names["hour"],
        value="now",
        step=3600,
    )
    lumiere = st.selectbox(
        label=dicts.field_names["lum"],
        options=dicts.lum.keys(),
    )
    departement = st.selectbox(
        label=dicts.field_names["dep"],
        options=dicts.dep.values(),
        placeholder="Sélectionnez un département",
    )
    commune = st.selectbox(
        label=dicts.field_names["com"],
        options=[com for com in dicts.com.values() if com[:2] == departement[:2]],
        placeholder="Sélectionnez une commune",
    )
    localisation = st.selectbox(
        label=dicts.field_names["agg_"],
        options=dicts.agg_.keys(),
    )
    intersection = st.selectbox(
        label=dicts.field_names["inter"],
        options=dicts.inter.keys(),
    )
    conditions_atmospheriques = st.selectbox(
        label=dicts.field_names["atm"],
        options=dicts.atm.keys(),
    )
    type_collision = st.selectbox(
        label=dicts.field_names["col"],
        options=dicts.col.keys(),
    )
    latitude = st.number_input(
        label=dicts.field_names["lat"],
        min_value=-90.0,
        max_value=90.0,
        step=0.001,
    )
    longitude = st.number_input(
        label=dicts.field_names["long"],
        min_value=-180.0,
        max_value=180.0,
        step=0.001,
    )

    ## get input data for fiche baac, rubrique lieux
    st.header(body="Lieux")
    categorie_route = st.selectbox(
        label=dicts.field_names["catr"],
        options=dicts.catr.keys(),
    )
    regime_circulation = st.selectbox(
        label=dicts.field_names["circ"],
        options=dicts.circ.keys(),
    )
    etat_surface = st.selectbox(
        label=dicts.field_names["surf"],
        options=dicts.surf.keys(),
    )
    situation_accident = st.selectbox(
        label=dicts.field_names["situ"],
        options=dicts.situ.keys(),
    )
    vitesse_max_autorisee = st.number_input(
        label=dicts.field_names["vma"],
        min_value=0,
        max_value=300,
        step=1,
    )

    ## get input data for fiche baac, rubrique véhicules
    st.header(body="Véhicules")
    categorie_vehicule = st.selectbox(
        label=dicts.field_names["catv"],
        options=dicts.catv.keys(),
    )
    obstacle_mobile = st.selectbox(
        label=dicts.field_names["obsm"],
        options=dicts.obsm.keys(),
    )
    type_motorisation = st.selectbox(
        label=dicts.field_names["motor"],
        options=dicts.motor.keys(),
    )
    nombre_vehicules = st.number_input(
        label=dicts.field_names["nb_vehicules"],
        min_value=0,
        max_value=100,
        step=1,
    )

    ## get input data for fiche baac, rubrique usagers
    st.header(body="Usagers")
    place_occupee = st.slider(
        label=dicts.field_names["place"],
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
        label=dicts.field_names["catu"],
        options=dicts.catu.keys(),
    )
    sexe_usager = st.selectbox(
        label=dicts.field_names["sexe"],
        options=dicts.sexe.keys(),
    )
    age_usager = st.number_input(
        label=dicts.field_names["victim_age"],
        min_value=0,
        max_value=100,
        step=1,
    )
    equipement_securite = st.selectbox(
        label=dicts.field_names["secu1"],
        options=dicts.secu1.keys(),
    )
    nombre_usagers = st.number_input(
        label=dicts.field_names["nb_victim"],
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
        field_values = [
            int(place_occupee),
            int(dicts.catu[categorie_usager]),
            int(dicts.sexe[sexe_usager]),
            float(dicts.secu1[equipement_securite]),
            int(date_accident.year),
            int(age_usager),
            int(dicts.catv[categorie_vehicule]),
            int(dicts.obsm[obstacle_mobile]),
            int(dicts.motor[type_motorisation]),
            int(dicts.catr[categorie_route]),
            int(dicts.circ[regime_circulation]),
            int(dicts.surf[etat_surface]),
            int(dicts.situ[situation_accident]),
            int(vitesse_max_autorisee),
            int(date_accident.day),
            int(date_accident.month),
            int(dicts.lum[lumiere]),
            int(departement.split(" ")[0]),
            int(commune.split(" ")[0]),
            int(dicts.agg_[localisation]),
            int(dicts.inter[intersection]),
            int(dicts.atm[conditions_atmospheriques]),
            int(dicts.col[type_collision]),
            float(latitude),
            float(longitude),
            int(heure_accident.hour),
            int(nombre_usagers),
            int(nombre_vehicules),
        ]
        input_data_pred_call = dict(zip(dicts.field_names, field_values))

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

        ### display feature importances
        feature_importances(model="current", n=5)
