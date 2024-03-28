docker system prune -af
# docker rm -f $(docker ps -a -q)
docker rmi $(docker image ls -q)
docker image build . -t dummyfcd/raw_data_container:0.0.1
docker-compose up
# docker container run dummyfcd/raw_data_container:0.0.1
