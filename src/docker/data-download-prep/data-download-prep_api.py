# imports
import datetime
import json
import random
import string
import time

import containerdata
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel


# define input data model for endpoint /run
class YearRange(BaseModel):
    start_year: int
    end_year: int


# create fastapi instance
api = FastAPI(title="SHIELD Microservice API - Data-Download-Prep")


# endpoint - status
@api.get(
    path="/status",
    tags=["STATUS"],
    name="check data-download-prep microservice API status",
)
async def status():
    result = "The data-download-prep microservice API is up."
    return JSONResponse(content=result)


# endpoint - run
@api.post(path="/run", tags=["PROCESS"], name="download and prepare data")
async def run(year_range: YearRange):
    ## download and prepare data within year range and save to data-download-prep volume
    exec_time_start = time.time()
    containerdata.Data(
        start_year=year_range.start_year,
        end_year=year_range.end_year,
        data_path="home/shield/data-download-prep",
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
    log_path = "home/shield/logs/data-download-prep.jsonl"
    with open(log_path, "a") as file:
        file.write(log_json + "\n")

    ## define result
    result = "Data downloaded and prepared."

    ## return result as json response
    return JSONResponse(content=result)
