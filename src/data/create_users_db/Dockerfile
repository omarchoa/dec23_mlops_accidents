FROM alpine:latest

ADD /src/data/create_users_db/create_users_db.py /home/shield/src/data/create_users_db/

WORKDIR /home/shield/

EXPOSE 8003

RUN apk update \
&& apk add python3

CMD ["/bin/sh", "-c", "mkdir -p src/features/api ; python3 src/data/create_users_db/create_users_db.py ; cp src/features/api/users_db_bis.json ../volume/"]

