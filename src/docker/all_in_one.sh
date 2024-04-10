docker system prune -af
# docker container prune -f
docker image build -f ./src/docker/bdd/Dockerfile ./src/docker/bdd -t dummyfcd/bdd_container:0.0.1
# docker image rm dummyfcd/data_container:0.0.1
docker image build -f ./src/docker/data/Dockerfile ./src/docker/data -t dummyfcd/data_container:0.0.1
# docker image rm dummyfcd/gateway_container:0.0.1
docker image build -f ./src/docker/gateway/Dockerfile ./src/docker/gateway -t dummyfcd/gateway_container:0.0.1
docker-compose -f src/docker/docker-compose.yml up
