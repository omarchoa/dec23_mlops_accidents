FROM ubuntu:20.04
COPY requirements.txt .
RUN apt update && apt install python3-pip -y && pip3 install -r requirements.txt
COPY api.py .

# 8008 KEPT FOR DEBUG ONLY, TO BE REMOVED
EXPOSE 8008   

RUN python3 --version
CMD ["uvicorn", "api:api", "--host", "0.0.0.0", "--port", "8008"]