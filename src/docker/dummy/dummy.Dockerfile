# use latest alpine image
FROM alpine:latest

# install curl
RUN apk add curl

# install wget
RUN apk add wget

# download shield volumes from aws s3
RUN wget https://dec23-mlops-accidents.s3.eu-west-3.amazonaws.com/shield_volumes.tar

# extract shield volumes
CMD tar -xvf shield_volumes.tar