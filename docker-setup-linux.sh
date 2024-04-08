# script to setup docker environment on linux for standalone execution of training, prediction, and scoring microservices


# create network
docker network create shield

# create volumes
docker volume create --name data
docker volume create --name logs
docker volume create --name models

# populate volumes
sudo docker cp ./data /var/lib/docker/volumes/data/_data/
sudo docker cp ./logs /var/lib/docker/volumes/logs/_data/
sudo docker cp ./models /var/lib/docker/volumes/models/_data/

# launch docker-compose
docker-compose -f docker-compose.yml up