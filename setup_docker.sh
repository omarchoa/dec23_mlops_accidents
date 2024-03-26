#!/bin/bash

# Fichier utilisé pour la conteneurisation de notre appli SHIELD.

# Création du volume:
docker volume create --name shield_volume

# Changement de dossier courant pour créer l'image `api`:
# cd /src

# Création de l'image `api`: prend 200s
docker image build  -f ./src/features/api/Dockerfile -t shield_api_image .

# Lancement du conteneur à partir de l'image:
docker run -p 8010:8000 --mount type=volume,src=shield_volume,dst=/home/shield shield_api_image

# Test de l'api dans un autre terminal:
curl.exe -X GET -i http://127.0.0.1:8010/status

# L'autre voie ne fonctionne pas, malgré beaucoup d'essais et d'investigation:
curl.exe -X GET -i http://172.17.0.2:8000/status
# curl: (28) Failed to connect to 172.17.0.2 port 8000 after 21042 ms: Couldn't connect to server