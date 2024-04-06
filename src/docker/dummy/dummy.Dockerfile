# use latest alpine image
FROM alpine:latest

# install curl
RUN apk add curl

# keep container running
CMD tail -f /dev/null