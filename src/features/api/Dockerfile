FROM ubuntu:22.04

ADD /src/features/api/api.py /home/shield/src/features/api/ 
ADD /src/data/datalib.py /home/shield/src/data/
ADD /src/features/api/requirements_api.txt /home/shield/src/features/api/

WORKDIR /home/shield/
VOLUME /home/volume/
EXPOSE 8000

RUN apt-get update \
&& apt-get install python3-pip -y\
&& pip3 install -r /home/shield/src/features/api/requirements_api.txt  

CMD ["/bin/bash", "-c", "\
# Copy users database from volume into container:
cp ../volume/users_db_bis.json src/features/api/ ; \
# Create directory inside container and import model save inside it from volume:
mkdir src/models/ ; \
cp ../volume/models/trained_model.joblib src/models/ ; \
# Create directory inside container and import preprocessed data inside it from volume:
mkdir -p data/preprocessed/ ; \
cp -r ../volume/data/preprocessed/ data/ ; \
# Create logs directory inside container:
mkdir logs/ ; \
# Run the api:
uvicorn --app-dir src/features/api api:api --reload --host=0.0.0.0\
# Copy api script into volume:
cp src/features/api/api.py ../volume/ ; \
# TODO: Copy files modified by the api into volume:
"]


# --host=0.0.0.0 needed instead of --host=127.0.0.1
# More info here:
# https://stackoverflow.com/questions/1924434/what-is-the-curl-error-52-empty-reply-from-server
# --port=8000 : not needed in the call of uvicorn.

