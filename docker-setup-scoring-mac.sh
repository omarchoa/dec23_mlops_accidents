# script to setup docker environment on mac for standalone execution of scoring microservice


# build dummy microservice image
docker image build -f ./src/docker/dummy/dummy.Dockerfile -t omarchoa/shield:dummy .

# push dummy microservice image
docker image push omarchoa/shield:dummy

# build scoring microservice image
docker image build -f ./src/docker/scoring/scoring.Dockerfile -t omarchoa/shield:scoring .

# push scoring microservice image
docker image push omarchoa/shield:scoring

# create shield network
docker network create shield

# create data volume
docker volume create data

# populate data volume
docker container run -d --rm --name dummy -v data:/home/shield/data omarchoa/shield:dummy
docker cp ./data dummy:/home/shield
docker container stop dummy

# create logs volume
docker volume create logs

# populate logs volume
docker container run -d --rm --name dummy -v logs:/home/shield/logs omarchoa/shield:dummy
docker cp ./logs dummy:/home/shield
docker container stop dummy

# create models volume
docker volume create models

# launch docker-compose
docker-compose -f docker-compose-scoring.yml up