FROM ubuntu:20.04
COPY requirements.txt .
RUN apt update && apt install python3-pip -y && pip3 install -r requirements.txt
COPY api.py .

# 8002 KEPT FOR DEBUG ONLY, TO BE REMOVED
EXPOSE 8002

CMD ["uvicorn", "api:api", "--host", "0.0.0.0", "--port", "8002"]