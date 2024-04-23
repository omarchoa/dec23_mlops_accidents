# use latest alpine image
FROM alpine:latest

# install dependencies
RUN apk update && \
    apk upgrade && \
    apk add --no-cache python3 && \
    apk add --no-cache py3-pip
COPY ./src/docker/testing/testing_requirements.txt \
    /home/shield/testing/testing_requirements.txt
RUN pip3 install -r /home/shield/testing/testing_requirements.txt \
    --break-system-packages

# copy microservice script file
COPY ./src/docker/testing/testing.py \
    /home/shield/testing/testing.py

# run container
CMD tail -f /dev/null