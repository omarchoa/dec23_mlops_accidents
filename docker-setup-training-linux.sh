# script to setup docker environment on linux for standalone execution of training microservice


# build dummy microservice image
docker image build -f ./src/docker/dummy/dummy.Dockerfile -t omarchoa/shield:dummy .

# push dummy microservice image
docker image push omarchoa/shield:dummy

# build training microservice image
docker image build -f ./src/docker/training/training.Dockerfile -t omarchoa/shield:training .

# push training microservice image
docker image push omarchoa/shield:training

# create shield network
docker network create shield

# create data volume
docker volume create data

# populate data volume
docker cp ./data /var/lib/docker/volumes/data/_data/

# create logs volume
docker volume create logs

# create models volume
docker volume create models

# launch docker-compose
docker-compose -f docker-compose-training.yml up