# imports
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from config import paths
import subprocess


# create fastapi instance
api = FastAPI(title="SHIELD Microservice API - Training")


# endpoint - status
@api.get(path="/status", tags=["STATUS"], name="check training microservice API status")
async def status():
    result = "The training microservice API is up."
    return JSONResponse(content=result)


# endpoint - train
@api.get(path="/train", tags=["PROCESS"], name="train model")
async def train():
    ## define shell command
    command = "python {script}".format(script=paths.SCRIPTS_MODELS_TRAIN)

    ## run shell command and save output to result
    result = subprocess.run(command, shell=True, capture_output=True, text=True)

    ## return formatted result as json response
    return JSONResponse(content=str(result.stdout).strip())
