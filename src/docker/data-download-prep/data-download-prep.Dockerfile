FROM ubuntu:20.04

COPY data-download-prep_requirements.txt .

RUN apt-get update && \
    apt-get install python3-pip -y && \
    pip3 install -r data-download-prep_requirements.txt

COPY data-download-prep_api.py .

COPY containerdata.py .

CMD ["uvicorn", "data-download-prep_api:api", "--host", "0.0.0.0", "--port", "8003"]
