docker system prune -af
docker image build -f ./src/docker/bdd/Dockerfile ./src/docker/bdd -t dummyfcd/bdd_container:0.0.1
docker image build -f ./src/docker/data/Dockerfile ./src/docker/data -t dummyfcd/data_container:0.0.1
docker-compose -f src/docker/docker-compose.yml up
