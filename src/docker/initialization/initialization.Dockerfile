# use latest alpine image
FROM alpine:latest

# install dependencies
RUN apk add curl
RUN apk add jq

# copy microservice script
COPY initialization_script.sh .

# run microservice script
CMD [ "sh", "initialization_script.sh" ]