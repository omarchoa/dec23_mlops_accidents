# imports
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import time
import datetime
import containerdata  ## custom library
import random
import string
import json


# define input data model for endpoint /update
class YearRange(BaseModel):
    start_year: int
    end_year: int


# create fastapi instance
api = FastAPI(title="SHIELD Microservice API - Data")


# endpoint - status
@api.get(path="/status", tags=["STATUS"], name="check data microservice API status")
async def status():
    result = "The data microservice API is up."
    return JSONResponse(content=result)


# endpoint - update
@api.post(path="/update", tags=["PROCESS"], name="update data")
async def update(year_range: YearRange):
    ## download + clean + preprocess data within year range & save to data volume
    exec_time_start = time.time()
    containerdata.Data(
        start_year=year_range.start_year,
        end_year=year_range.end_year,
        data_path="home/shield/data",
    )
    exec_time_end = time.time()

    ## prepare log data for export
    log_dict = {
        "request_id": "".join(random.choices(string.digits, k=16)),
        "time_stamp": str(datetime.datetime.now()),
        ### "user_name": user,
        "response_status_code": 200,
        "start_year": year_range.start_year,
        "end_year": year_range.end_year,
        "execution_time": exec_time_end - exec_time_start,
    }
    log_json = json.dumps(obj=log_dict)

    ## export log data to log file
    log_path = "home/shield/logs/update_data.jsonl"
    with open(log_path, "a") as file:
        file.write(log_json + "\n")

    ## define result
    result = "Data updated."

    ## return result as json response
    return JSONResponse(content=result)
