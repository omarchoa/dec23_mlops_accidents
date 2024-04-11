# imports
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from config import paths
import subprocess


# define input data model for endpoint /label_prediction
class InputDataLabelPred(BaseModel):
    request_id: int
    y_true: int


# create fastapi instance
api = FastAPI(title="SHIELD Microservice API - Scoring")


# endpoint - status
@api.get(path="/status", tags=["STATUS"], name="check scoring microservice API status")
async def status():
    result = "The scoring microservice API is up."
    return JSONResponse(content=result)


# endpoint - label prediction
@api.post(
    path="/label_prediction",
    tags=["PROCESSES"],
    name="label prediction",
)
async def label_prediction(input_data: InputDataLabelPred):
    ## save input data to json file
    input_data_json_object = input_data.model_dump_json()
    input_data_json_file = "input_data.json"
    with open(input_data_json_file, "w") as file:
        file.write(input_data_json_object)

    ## define shell command
    command = "python {script} {input}".format(
        script=paths.SCRIPTS_SCORING_LABEL_PREDICTION, input=input_data_json_file
    )

    ## run shell command and save output to result
    result = subprocess.run(command, shell=True, capture_output=True, text=True)

    ## return formatted result as json response
    return JSONResponse(content=str(result.stdout).strip())


# endpoint - update f1 score
@api.get(
    path="/update_f1_score",
    tags=["PROCESSES"],
    name="update f1 score",
)
async def update_f1_score():
    ## define shell command
    command = "python {script}".format(script=paths.SCRIPTS_SCORING_UPDATE_F1_SCORE)

    ## run shell command and save output to result
    result = subprocess.run(command, shell=True, capture_output=True, text=True)

    ## return formatted result as json response
    return JSONResponse(content=str(result.stdout).strip())
