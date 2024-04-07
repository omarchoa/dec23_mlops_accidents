# script to setup docker environment on linux for standalone execution of scoring microservice


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
docker cp ./data /var/lib/docker/volumes/data/_data/

# create logs volume
docker volume create logs

# populate logs volume
docker cp ./logs /var/lib/docker/volumes/logs/_data/

# create models volume
docker volume create models

# launch docker-compose
docker-compose -f docker-compose-scoring.yml up