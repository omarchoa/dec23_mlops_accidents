FROM ubuntu:20.04
COPY data_requirements.txt .
RUN apt-get update && apt-get install python3-pip -y && pip3 install -r data_requirements.txt
COPY data_api.py .
COPY containerdata.py .
CMD ["uvicorn", "data_api:api", "--host", "0.0.0.0", "--port", "8003"]
