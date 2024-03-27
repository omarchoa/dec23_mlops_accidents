FROM alpine:latest

ADD /src/data/create_users_db/create_users_db.py /home/shield/src/data/create_users_db/

WORKDIR /home/shield/

RUN apk update \
&& apk add python3

CMD ["/bin/sh", "-c", "mkdir -p src/features/api ; python3 src/data/create_users_db/create_users_db.py"]

# Installation depuis la racine:
# docker image build  -f ./src/data/create_users_db/Dockerfile -t shield_create_users_db_image .

# Lancement depuis la racine: 
# docker run --rm --mount type=volume,src=shield_users_volume,dst=/home/shield shield_create_users_db_image
# docker run --mount type=volume,src=shield_volume,dst=/home/shield shield_create_users_db_image
# docker run shield_create_users_db_image