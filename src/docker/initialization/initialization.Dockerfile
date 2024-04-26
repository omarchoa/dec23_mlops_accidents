# use latest alpine image
FROM alpine:latest

# install curl
RUN apk add curl

# copy microservice script
COPY initialize_app.sh .

# run microservice script
CMD [ "sh", "initialize_app.sh" ]