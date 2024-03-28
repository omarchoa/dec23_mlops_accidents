docker system prune -af
docker rm $(docker ps -a -q)
docker rmi $(docker image ls -q)
docker image build . -t dummyfcd/bdd_container:0.0.1
docker image ls -a

docker-compose up
