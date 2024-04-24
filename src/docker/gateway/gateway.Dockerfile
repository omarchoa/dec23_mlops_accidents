FROM ubuntu:20.04
COPY gateway_requirements.txt .
RUN apt-get update && apt-get install python3-pip -y && apt-get install -y cron && pip3 install -r gateway_requirements.txt
COPY gateway_api.py .
COPY crontab_action.py .
COPY action_cron.txt /etc/cron.d/action_cron.txt
RUN crontab /etc/cron.d/action_cron.txt
CMD cron && uvicorn gateway_api:api --host 0.0.0.0 --port 8001