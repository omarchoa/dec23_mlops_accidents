#!/bin/bash

# Fichier utilisé pour la conteneurisation de notre appli SHIELD.

# Création du volume:
docker volume create --name shield_volume

# -------------- 1. Image Import Data -----------------------------------------

# Création de l'image depuis la racine:
docker image build  -f ./src/data/import_data.Dockerfile -t shield_import_data .

# Lancement depuis la racine: 
docker run --rm --mount type=volume,src=shield_volume,dst=/home/volume shield_import_data

# -------------- 2. Image Make Dataset -----------------------------------------

# Création de l'image depuis la racine:
docker image build  -f ./src/data/make_dataset.Dockerfile -t shield_make_dataset .

# Lancement depuis la racine: 
docker run --rm --mount type=volume,src=shield_volume,dst=/home/volume shield_make_dataset


# -------------- Image 3. Create users db ---------------------------------------

# Création de l'image depuis la racine:
docker image build  -f ./src/data/create_users_db/Dockerfile -t shield_create_users_db_image .

# Lancement depuis la racine: 

docker run --mount type=volume,src=shield_volume,dst=/home/volume shield_create_users_db_image


# -------------- Image 4. Train Model ---------------------------------------

# Création de l'image depuis la racine:
docker image build  -f ./src/models/model.Dockerfile -t shield_train_model_image .

# Lancement depuis la racine: 

docker run --mount type=volume,src=shield_volume,dst=/home/volume shield_train_model_image

# --------------- Image 5. API ---------------------------------------------------
# Création de l'image `api`: 
docker image build  -f ./src/features/api/Dockerfile -t shield_api_image .

# Lancement du conteneur à partir de l'image:
docker run -p 8010:8000 --rm --mount type=volume,src=shield_volume,dst=/home/volume/ shield_api_image

# Test de l'api dans un autre terminal:
curl.exe -X GET -i http://127.0.0.1:8010/status

# L'autre voie ne fonctionne pas, malgré beaucoup d'essais et d'investigation:
curl.exe -X GET -i http://172.17.0.2:8000/status
# curl: (28) Failed to connect to 172.17.0.2 port 8000 after 21042 ms: Couldn't connect to server

