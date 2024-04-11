# imports
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import containerdata  ## custom library


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
    containerdata.Data(
        start_year=year_range.start_year,
        end_year=year_range.end_year,
        data_path="home/shield/data",
    )
    result = "Data updated."
    return JSONResponse(content=result)
