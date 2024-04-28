# use python slim image
FROM python:slim

# copy streamlit folder
COPY streamlit \
    /home/shield/streamlit

# install dependencies
RUN apt-get update && \
    apt-get install python3-pip -y
RUN pip3 install -r /home/shield/streamlit/requirements.txt

# enable streamlit app to determine that it's running in a container
ENV CONTAINERIZED="yes"

# launch streamlit app
CMD streamlit run /home/shield/streamlit/app.py