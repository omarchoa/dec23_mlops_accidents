# script to setup docker environment on mac for standalone execution of training, prediction, and scoring microservices


# create network
docker network create shield

# create volumes
docker volume create --name data
docker volume create --name logs
docker volume create --name models
docker volume create --name users

# populate volumes
docker container run -d --rm --name dummy \
    -v data:/home/shield/data \
    -v logs:/home/shield/logs \
    -v models:/home/shield/models \
    -v users:/home/shield/users \
    omarchoa/shield:dummy
sudo docker cp ./data dummy:/home/shield
sudo docker cp ./logs dummy:/home/shield
sudo docker cp ./models dummy:/home/shield
sudo docker cp ./src/docker/bdd/users_db_bis.json \
    dummy:/home/shield/users
docker container stop dummy

# launch docker-compose
docker-compose -f docker-compose.yml up