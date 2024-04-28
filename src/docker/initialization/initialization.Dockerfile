# use latest alpine image
FROM alpine:latest

# install dependencies
RUN apk add curl
RUN apk add jq

# copy microservice script
COPY initialize_app.sh .

# run microservice script
CMD [ "sh", "initialize_app.sh" ]