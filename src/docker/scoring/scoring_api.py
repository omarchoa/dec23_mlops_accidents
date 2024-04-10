# imports
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from config import paths
import subprocess


# create fastapi instance
api = FastAPI(
    title="SHIELD Microservice API - Scoring",
    openapi_tags=[
        {"name": "STATUS"},
        {"name": "PROCESSES"},
    ],
)


# define input data model
class PredLabel(BaseModel):
    request_id: int = 6012919476848551
    y_true: int = 1


# endpoint - status
@api.get(path="/status", tags=["STATUS"], name="check microservice status")
async def status():
    result = "The microservice API is up."
    return JSONResponse(result)


# endpoint - label prediction
@api.post(
    path="/label_prediction",
    tags=["PROCESSES"],
    name="execute microservice process 1",
)
async def label_prediction(input_data: PredLabel):
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
    name="execute microservice process 2",
)
async def update_f1_score():
    ## define shell command
    command = "python {script}".format(script=paths.SCRIPTS_SCORING_UPDATE_F1_SCORE)

    ## run shell command and save output to result
    result = subprocess.run(command, shell=True, capture_output=True, text=True)

    ## return formatted result as json response
    return JSONResponse(content=str(result.stdout).strip())