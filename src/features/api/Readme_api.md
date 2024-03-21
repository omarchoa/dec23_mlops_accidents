
# 1. Test / : vérification du fonctionnement de l’API:

Sous Linux:
curl -X 'GET' 'http://127.0.0.1:8000/' -H 'accept: application/json'

Sous Windows:
curl.exe -X 'GET' 'http://127.0.0.1:8000/' -H 'accept: application/json'

# 2. Test /register: inscription d'un nouvel utilisateur:

Sous Linux:
curl -X 'POST' \
  'http://127.0.0.1:8000/register' \
  -H 'accept: application/json' \
  -H 'identification: admin:4dmin' \
  -H 'Content-Type: application/json' \
  -d '{
  "user": "sherlock",
  "psw": "BakerStr33t",
  "rights": 0
}'

Sous Windows:

# 3. Test /remove_user: suppression d'un utilisateur existant:

Sous Linux:
curl -X 'DELETE' \
  'http://127.0.0.1:8000/remove_user' \
  -H 'accept: application/json' \
  -H 'identification: admin:4dmin' \
  -H 'Content-Type: application/json' \
  -d '{
  "user": "sherlock"
}'

# 4. Test /predict_from_test: prédiction à partir d'un échantillon test

Sous Linux:
curl -X 'GET' \
  'http://127.0.0.1:8000/predict_from_test' \
  -H 'accept: application/json' \
  -H 'identification: fdo:c0ps'

# 5. Test /predict_from_call: prédiction à partir du relevé d'un appel
Par défaut, les données du fichier test_features.json sont utilisées.

Sous Linux:
curl -X 'POST' \
  'http://127.0.0.1:8000/predict_from_call' \
  -H 'accept: application/json' \
  -H 'identification: policierA:sherif' \
  -H 'Content-Type: application/json' \
  -d '{
  "place": 10,
  "catu": 3,
  "sexe": 1,
  "secu1": 0,
  "year_acc": 2021,
  "victim_age": 60,
  "catv": 2,
  "obsm": 1,
  "motor": 1,
  "catr": 3,
  "circ": 2,
  "surf": 1,
  "situ": 1,
  "vma": 50,
  "jour": 7,
  "mois": 12,
  "lum": 5,
  "dep": 77,
  "com": 77317,
  "agg_": 2,
  "inter": 1,
  "atm": 0,
  "col": 6,
  "lat": 48.6,
  "long": 2.89,
  "hour": 17,
  "nb_victim": 2,
  "nb_vehicules": 1
}'

# 6. Test /train: A FAIRE

# 7. Test /update_data: A FAIRE