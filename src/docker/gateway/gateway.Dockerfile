FROM ubuntu:20.04
RUN apt-get update && apt-get install python3-pip -y && pip3 install fastapi requests uvicorn
COPY gateway_api.py .
CMD ["uvicorn", "gateway_api:api", "--host", "0.0.0.0", "--port", "8001"]