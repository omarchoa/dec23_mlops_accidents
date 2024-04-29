# use python slim image
FROM python:slim

# copy microservice directory to container
COPY . \
    /home/shield/frontend/

# install dependencies
RUN apt-get update && \
    apt-get install python3-pip -y
RUN pip3 install -r /home/shield/frontend/frontend_requirements.txt

# enable microservice to determine that it's running in a container
ENV CONTAINERIZED="yes"

# launch microservice
CMD streamlit run /home/shield/frontend/frontend_script.py