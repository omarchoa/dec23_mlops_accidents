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