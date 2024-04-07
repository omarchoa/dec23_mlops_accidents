# use python slim image
FROM python:slim

# define main variables
ARG ROOT_SOURCE="."
ENV ROOT_DESTINATION="home/shield"
ARG SCRIPTS="src"
ARG CONFIG_PACKAGE="${SCRIPTS}/config"

# define specific microservice variables
ENV MICROSERVICE_NAME="prediction"
ARG MICROSERVICE_SCRIPT="${SCRIPTS}/models/predict_model.py"
ENV MICROSERVICE_HOST="0.0.0.0"
ENV MICROSERVICE_PORT="8005"

# define general microservice variables
ENV MICROSERVICE_DIRECTORY="${SCRIPTS}/docker/${MICROSERVICE_NAME}"
ARG MICROSERVICE_REQUIREMENTS="${MICROSERVICE_DIRECTORY}/${MICROSERVICE_NAME}_requirements.txt"
ARG MICROSERVICE_API="${MICROSERVICE_DIRECTORY}/${MICROSERVICE_NAME}_api.py"

# install main dependencies
RUN apt-get update && \
    apt-get install python3-pip -y
COPY ${ROOT_SOURCE}/${MICROSERVICE_REQUIREMENTS} \
    ${ROOT_DESTINATION}/${MICROSERVICE_REQUIREMENTS}
RUN pip3 install -r ${ROOT_DESTINATION}/${MICROSERVICE_REQUIREMENTS}

# include additional dependencies under src folder
ENV PYTHONPATH="${ROOT_DESTINATION}/${SCRIPTS}"
ENV CONTAINERIZED="yes"
COPY ${ROOT_SOURCE}/${CONFIG_PACKAGE} \
    ${ROOT_DESTINATION}/${CONFIG_PACKAGE}

# copy microservice api file
COPY ${ROOT_SOURCE}/${MICROSERVICE_API} \
    ${ROOT_DESTINATION}/${MICROSERVICE_API}

# copy microservice script file
COPY ${ROOT_SOURCE}/${MICROSERVICE_SCRIPT} \
    ${ROOT_DESTINATION}/${MICROSERVICE_SCRIPT}

# launch microservice api server
CMD uvicorn \
    --app-dir ${ROOT_DESTINATION}/${MICROSERVICE_DIRECTORY} \
    ${MICROSERVICE_NAME}_api:api \
    --host ${MICROSERVICE_HOST} \
    --port ${MICROSERVICE_PORT}