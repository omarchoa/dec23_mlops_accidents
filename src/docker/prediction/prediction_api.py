# imports
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from config import paths
import subprocess


# define input data model for endpoint /predict_from_call
class InputDataPredCall(BaseModel):
    place: int
    catu: int
    sexe: int
    secu1: float
    year_acc: int
    victim_age: int
    catv: int
    obsm: int
    motor: int
    catr: int
    circ: int
    surf: int
    situ: int
    vma: int
    jour: int
    mois: int
    lum: int
    dep: int
    com: int
    agg_: int
    inter: int
    atm: int
    col: int
    lat: float
    long: float
    hour: int
    nb_victim: int
    nb_vehicules: int


# create fastapi instance
api = FastAPI(
    title="SHIELD Microservice API - Prediction",
    openapi_tags=[
        {"name": "STATUS"},
        {"name": "PROCESSES"},
    ],
)


# endpoint - status
@api.get(path="/status", tags=["STATUS"], name="check microservice status")
async def status():
    result = "The microservice API is up."
    return result


# endpoint - predict from test
@api.get(
    path="/predict_from_test",
    tags=["PROCESSES"],
    name="execute microservice process 1",
)
async def predict_from_test():
    ## define shell command
    command = "python {script} {input}".format(
        script=paths.SCRIPTS_MODELS_PREDICT, input=paths.SAMPLE_FEATURES
    )

    ## define environmental variables
    ### PYTHONPATH and CONTAINERIZED need to be redefined and passed explicitly to the subprocess as its env parameter resets the environmental variables inherited from the container
    env_dict = {
        "PYTHONPATH": "home/shield/src",
        "CONTAINERIZED": "yes",
        "ENDPOINT": "/predict_from_test",
    }

    ## run shell command and save output to result
    result = subprocess.run(
        command, shell=True, env=env_dict, capture_output=True, text=True
    )

    ## return formatted result as json response
    return JSONResponse(content=str(result.stdout).strip())


# endpoint - predict from call
@api.post(
    path="/predict_from_call",
    tags=["PROCESSES"],
    name="execute microservice process 2",
)
async def predict_from_call(input_data: InputDataPredCall):
    # save input data to json file
    input_data_json_object = input_data.model_dump_json()
    input_data_json_file = "input_data.json"
    with open(input_data_json_file, "w") as file:
        file.write(input_data_json_object)

    ## define shell command
    command = "python {script} {input}".format(
        script=paths.SCRIPTS_MODELS_PREDICT, input=input_data_json_file
    )

    ## define environmental variables
    ### PYTHONPATH and CONTAINERIZED need to be redefined and passed explicitly to the subprocess as its env parameter resets the environmental variables inherited from the container
    env_dict = {
        "PYTHONPATH": "home/shield/src",
        "CONTAINERIZED": "yes",
        "ENDPOINT": "/predict_from_call",
    }

    ## run shell command and save output to result
    result = subprocess.run(
        command, shell=True, env=env_dict, capture_output=True, text=True
    )

    ## return formatted result as json response
    return JSONResponse(content=str(result.stdout).strip())
