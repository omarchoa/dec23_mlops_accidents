# script to setup docker environment on linux for standalone execution of prediction microservice


# build dummy microservice image
docker image build -f ./src/docker/dummy/dummy.Dockerfile -t omarchoa/shield:dummy .

# push dummy microservice image
docker image push omarchoa/shield:dummy

# build prediction microservice image
docker image build -f ./src/docker/prediction/prediction.Dockerfile -t omarchoa/shield:prediction .

# push prediction microservice image
docker image push omarchoa/shield:prediction

# create shield network
docker network create shield

# create data volume
docker volume create data

# populate data volume
docker cp ./data /var/lib/docker/volumes/data/_data/

# create models volume
docker volume create models

# launch docker-compose
docker-compose -f docker-compose-prediction.yml up