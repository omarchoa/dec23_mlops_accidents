FROM ubuntu:20.04
COPY users_requirements.txt .
RUN apt-get update && apt-get install python3-pip -y && pip3 install -r users_requirements.txt
COPY users_api.py .
CMD ["uvicorn", "users_api:api", "--host", "0.0.0.0", "--port", "8002"]