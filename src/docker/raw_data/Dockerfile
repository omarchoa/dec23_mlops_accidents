FROM ubuntu:20.04
RUN apt-get update && apt-get install python3-pip -y && pip3 install uvicorn fastapi numpy pandas requests scikit-learn
COPY raw_data_api.py .
COPY containerdata.py .
EXPOSE 8000
CMD ["uvicorn", "raw_data_api:api", "--host", "0.0.0.0", "--port", "8000"]