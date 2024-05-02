import pandas as pd

catu = {
    "Conducteur": 1,
    "Passager": 2,
    "Piéton": 3,
}

sexe = {
    "Masculin": 1,
    "Féminin": 2,
}

secu1 = {
    "Non renseigné": -1,
    "Aucun équipement": 0,
    "Ceinture": 1,
    "Casque": 2,
    "Dispositif enfants": 3,
    "Gilet réfléchissant": 4,
    "Airbag (2RM/3RM)": 5,
    "Gants (2RM/3RM)": 6,
    "Gants + Airbag (2RM/3RM)": 7,
    "Non déterminable": 8,
    "Autre": 9,
}

catv = {
    "Indeterminable": 0,
    "Bicyclette": 1,
    "Cyclomoteur <50cm3": 2,
    "Voiturette (Quadricycle à moteur carrossé)": 3,
    "Référence inutilisée depuis 2006 (scooter immatriculé)": 4,
    "Référence inutilisée depuis 2006 (motocyclette)": 5,
    "Référence inutilisée depuis 2006 (side-car)": 6,
    "VL seul": 7,
    "Référence inutilisée depuis 2006 (VL + caravane)": 8,
    "Référence inutilisée depuis 2006 (VL + remorque)": 9,
    "VU seul 1,5T <= PTAC <= 3,5T avec ou sans remorque": 10,
    "Référence inutilisée depuis 2006 (VU (10) + caravane)": 11,
    "Référence inutilisée depuis 2006 (VU (10) + remorque)": 12,
    "PL seul 3,5T <PTCA <= 7,5T": 13,
    "PL seul > 7,5T": 14,
    "PL > 3,5T + remorque": 15,
    "Tracteur routier seul": 16,
    "Tracteur routier + semi-remorque": 17,
    "Référence inutilisée depuis 2006 (transport en commun)": 18,
    "Référence inutilisée depuis 2006 (tramway)": 19,
    "Engin spécial": 20,
    "Tracteur agricole": 21,
    "Scooter < 50 cm3": 30,
    "Motocyclette > 50 cm3 et <= 125 cm3": 31,
    "Scooter > 50 cm3 et <= 125 cm3": 32,
    "Motocyclette > 125 cm3": 33,
    "Scooter > 125 cm3": 34,
    "Quad léger <= 50 cm3 (Quadricycle à moteur non carrossé)": 35,
    "Quad lourd > 50 cm3 (Quadricycle à moteur non carrossé)": 36,
    "Autobus": 37,
    "Autocar": 38,
    "Train": 39,
    "Tramway": 40,
    "3RM <= 50 cm3": 41,
    "3RM > 50 cm3 <= 125 cm3": 42,
    "3RM > 125 cm3": 43,
    "EDP à moteur": 50,
    "EDP sans moteur": 60,
    "VAE": 80,
    "Autre véhicule": 99,
}

obsm = {
    "Non renseigné": -1,
    "Aucun": 0,
    "Piéton": 1,
    "Véhicule": 2,
    "Véhicule sur rail": 4,
    "Animal domestique": 5,
    "Animal sauvage": 6,
    "Autre": 9,
}

motor = {
    "Non renseigné": -1,
    "Inconnue": 0,
    "Hydrocarbures": 1,
    "Hybride électrique": 2,
    "Electrique": 3,
    "Hydrogène": 4,
    "Humaine": 5,
    "Autre": 6,
}

catr = {
    "Autoroute": 1,
    "Route nationale": 2,
    "Route Départementale": 3,
    "Voie Communales": 4,
    "Hors réseau public": 5,
    "Parc de stationnement ouvert à la circulation publique": 6,
    "Routes de métropole urbaine": 7,
    "Autre": 9,
}

circ = {
    "Non renseigné": -1,
    "A sens unique": 1,
    "Bidirectionnelle": 2,
    "A chaussées séparées": 3,
    "Avec voies d’affectation variable": 4,
}

surf = {
    "Non renseigné": -1,
    "Normale": 1,
    "Mouillée": 2,
    "Flaques": 3,
    "Inondée": 4,
    "Enneigée": 5,
    "Boue": 6,
    "Verglacée": 7,
    "Corps gras – huile": 8,
    "Autre": 9,
}

situ = {
    "Non renseigné": -1,
    "Aucun": 0,
    "Sur chaussée": 1,
    "Sur bande d’arrêt d’urgence": 2,
    "Sur accotement": 3,
    "Sur trottoir": 4,
    "Sur piste cyclable": 5,
    "Sur autre voie spéciale": 6,
    "Autres": 8,
}

lum = {
    "Plein jour": 1,
    "Crépuscule ou aube": 2,
    "Nuit sans éclairage public": 3,
    "Nuit avec éclairage public non allumé": 4,
    "Nuit avec éclairage public allumé": 5,
}

# départements
columns = ["DEP", "LIBELLE"]
df = pd.read_csv(
    filepath_or_buffer="/home/shield/frontend/frontend_modules/codes_insee_departements_2023.csv",
    usecols=columns,
)
dep = {
    key: value
    for line in df.set_index("DEP").T.to_dict("records")
    for key, value in line.items()
}
for key in dep:
    dep[key] = key + " - " + dep[key]
corse = {"2A": "201", "2B": "202"}

# communes
columns = ["COM", "LIBELLE"]
df = pd.read_csv(
    filepath_or_buffer="/home/shield/frontend/frontend_modules/codes_insee_communes_2023.csv",
    usecols=columns,
)
com = {
    key: value
    for line in df.set_index("COM").T.to_dict("records")
    for key, value in line.items()
}
for key in com:
    com[key] = key + " - " + com[key]

agg_ = {
    "Hors agglomération": 1,
    "En agglomération": 2,
}

inter = {
    "Hors intersection": 1,
    "Intersection en X": 2,
    "Intersection en T": 3,
    "Intersection en Y": 4,
    "Intersection à plus de 4 branches": 5,
    "Giratoire": 6,
    "Place": 7,
    "Passage à niveau": 8,
    "Autre intersection": 9,
}

atm = {
    "Non renseigné": -1,
    "Normale": 1,
    "Pluie légère": 2,
    "Pluie forte": 3,
    "Neige - grêle": 4,
    "Brouillard - fumée": 5,
    "Vent fort - tempête": 6,
    "Temps éblouissant": 7,
    "Temps couvert": 8,
    "Autre": 9,
}

col = {
    "Non renseigné": -1,
    "Deux véhicules - frontale": 1,
    "Deux véhicules – par l’arrière": 2,
    "Deux véhicules – par le coté": 3,
    "Trois véhicules et plus – en chaîne": 4,
    "Trois véhicules et plus - collisions multiples": 5,
    "Autre collision": 6,
    "Sans collision": 7,
}
