# script to setup docker environment on linux for standalone execution of training, prediction, and scoring microservices


# build images
docker image build -f ./src/docker/gateway/gateway.Dockerfile -t omarchoa/shield:gateway .
docker image build -f ./src/docker/dummy/dummy.Dockerfile -t omarchoa/shield:dummy .
docker image build -f ./src/docker/training/training.Dockerfile -t omarchoa/shield:training .
docker image build -f ./src/docker/prediction/prediction.Dockerfile -t omarchoa/shield:prediction .
docker image build -f ./src/docker/scoring/scoring.Dockerfile -t omarchoa/shield:scoring .

# create network
docker network create shield

# create volumes
docker volume create --name data
docker volume create --name logs
docker volume create --name models
docker volume create --name users

# populate volumes
sudo docker cp ./data \
    /var/lib/docker/volumes/data/_data/
sudo docker cp ./logs \
    /var/lib/docker/volumes/logs/_data/
sudo docker cp ./models \
    /var/lib/docker/volumes/models/_data/
sudo docker cp ./src/docker/bdd/users_db_bis.json \
    /var/lib/docker/volumes/users/_data/

# launch docker-compose
docker-compose -f docker-compose.yml up