# wait for `gateway` microservice to go online
sleep 5

# download and prepare 2021 accident data
curl -X 'POST' \
  'http://gateway:8001/data-download-prep/run' \
  -H 'accept: application/json' \
  -H 'identification: robot:Autom@t' \
  -H 'Content-Type: application/json' \
  -d '{
  "start_year": 2021,
  "end_year": 2021
}'

# train model
curl -X 'GET' \
  'http://gateway:8001/training/train' \
  -H 'accept: application/json' \
  -H 'identification: robot:Autom@t'

# perform sample prediction
curl -X 'POST' \
  'http://gateway:8001/prediction/call' \
  -H 'accept: application/json' \
  -H 'identification: robot:Autom@t' \
  -H 'Content-Type: application/json' \
  -d '{
  "place": 10,
  "catu": 3,
  "sexe": 1,
  "secu1": 0.0,
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

# save sample prediction request id as environmental variable
REQUEST_ID=$(head -n 1 /home/shield/logs/preds_call.jsonl | jq -r '.request_id' | tr -d '"')

# label sample prediction
curl -X 'POST' \
  'http://gateway:8001/scoring/label-prediction' \
  -H 'accept: application/json' \
  -H 'identification: robot:Autom@t' \
  -H 'Content-Type: application/json' \
  -d '{
  "request_id": '${REQUEST_ID}',
  "y_true": 1
}'