FROM alpine:latest

ADD /src/data/create_users_db/create_users_db.py /home/shield/src/data/create_users_db/

WORKDIR /home/shield/

RUN apk update \
&& apk add python3

CMD ["/bin/sh", "-c", "mkdir -p src/features/api ; python3 src/data/create_users_db/create_users_db.py"]

