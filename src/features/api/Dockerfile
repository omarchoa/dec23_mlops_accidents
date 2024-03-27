FROM ubuntu:22.04

ADD /src/features/api/api.py /home/shield/src/features/api/ 
ADD /src/data/datalib.py /home/shield/src/data/
ADD /src/features/api/requirements_api.txt /home/shield/src/features/api/

WORKDIR /home/shield/

EXPOSE 8000

RUN apt-get update \
&& apt-get install python3-pip -y\
&& pip3 install -r /home/shield/src/features/api/requirements_api.txt  

# Pour une raison que j'ignore, il faut mettre --host=0.0.0.0 
# sinon ça ne marche pas quand le conteneur tourne et qu'on essaie 
# d'accéder à l'api. Solution trouvée ici:
# https://stackoverflow.com/questions/1924434/what-is-the-curl-error-52-empty-reply-from-server
CMD uvicorn --app-dir src/features/api api:api --reload --host=0.0.0.0 
#--port=8000 après différents test, à ne pas mettre -> pourquoi? mystère...

